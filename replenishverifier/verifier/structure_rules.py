from dataclasses import asdict, dataclass

from replenishverifier.benchmark.schemas import STRUCTURE_KEYS
from replenishverifier.data.structure_schema import split_expected_structures
from replenishverifier.verifier.lp_graph import LPStructureGraph


STRUCTURE_DESCRIPTIONS = {
    "inventory_balance": "inventory balance constraints",
    "order_variable": "order quantity variable Q",
    "inventory_variable": "inventory variable I",
    "shortage_variable": "shortage/backorder variable B",
    "capacity_constraint": "capacity constraint",
    "binary_order_variable": "binary order trigger variable Y",
    "big_m_constraint": "Big-M linking constraint Q <= M * Y",
    "lead_time": "lead-time structure",
    "holding_cost": "holding cost term",
    "shortage_cost": "shortage cost term",
    "fixed_order_cost": "fixed ordering cost term",
}


REPAIR_HINTS = {
    "inventory_balance": "Add inventory-flow constraints such as I[t] = I[t-1] + Q[t] - demand[t]; with backlogs, use net inventory I[t] - B[t].",
    "order_variable": "Add nonnegative order quantity variables, e.g. Q[t] or Q[i,t].",
    "inventory_variable": "Add nonnegative inventory state variables, e.g. I[t] or I[i,t].",
    "shortage_variable": "Add shortage/backlog variables, e.g. B[t] or B[i,t], when shortages are allowed or penalized.",
    "capacity_constraint": "Add capacity constraints, e.g. sum_i volume[i] * I[i,t] <= capacity.",
    "binary_order_variable": "Add binary setup/order-trigger variables, e.g. Y[t] in {0,1}.",
    "big_m_constraint": "Add linking constraints such as Q[t] <= M * Y[t].",
    "lead_time": "Represent delayed arrivals in the inventory balance, e.g. Q[t-L].",
    "holding_cost": "Include holding_cost * I[t] terms in the objective.",
    "shortage_cost": "Include shortage_cost * B[t] terms in the objective.",
    "fixed_order_cost": "Include fixed_order_cost * Y[t] terms in the objective.",
}


@dataclass
class RuleCertificate:
    rule_name: str
    required: bool
    passed: bool
    score: float
    evidence: list
    missing_reason: str
    repair_hint: str
    optional: bool = False

    def to_dict(self):
        return asdict(self)


@dataclass
class StructureCheckResult:
    expected: dict
    detected: dict
    passed: dict
    missing: list
    extra_detected: list
    structure_score: float
    messages: list
    certificates: list
    optional_detected: dict
    weak_evidence: dict
    required_structures: list
    optional_structures: list

    def to_dict(self):
        return asdict(self)


ROLE_ALIASES = {
    "order": ["Q", "order", "order_qty", "order_quantity", "purchase", "replenish", "replenishment"],
    "inventory": ["I", "inventory", "stock", "onhand", "on_hand", "ending_inventory", "inv"],
    "shortage": ["B", "shortage", "backlog", "backorder", "unmet", "lost_sales"],
    "binary_order": ["Y", "setup", "order_flag", "order_indicator", "is_order", "open_order", "binary_order"],
}


def _normalize(name):
    return str(name).lower().replace("-", "_")


def _has_prefix(names, prefix):
    return any(name == prefix or name.startswith(prefix + "_") or name.startswith(prefix + "(") for name in names)


def _has_role(names, role):
    aliases = ROLE_ALIASES[role]
    for name in names:
        normalized = _normalize(name)
        for alias in aliases:
            alias_norm = _normalize(alias)
            if name == alias or name.startswith(alias + "_") or name.startswith(alias + "("):
                return True
            if normalized == alias_norm or normalized.startswith(alias_norm + "_") or alias_norm in normalized:
                return True
    return False


def _objective_has_var(parsed, prefix):
    return any(
        variable in parsed.objective
        for variable in parsed.variable_names
        if variable == prefix or variable.startswith(prefix + "_") or variable.startswith(prefix + "(")
    )


def _objective_has_role(parsed, role):
    return any(variable in parsed.objective for variable in parsed.variable_names if _has_role([variable], role))


def _matching_vars(names, role=None, prefix=None):
    out = []
    for name in names:
        if prefix and (name == prefix or name.startswith(prefix + "_") or name.startswith(prefix + "(")):
            out.append(name)
        elif role and _has_role([name], role):
            out.append(name)
    return out


def _constraint_evidence(parsed, terms, limit=5):
    evidence = []
    for cname, expr in parsed.constraints.items():
        haystack = f"{cname} {expr}".lower()
        if any(term in haystack for term in terms):
            evidence.append({"constraint": cname, "expr": expr})
    return evidence[:limit]


def _objective_evidence(parsed, variables, limit=8):
    return [{"variable": v, "objective_excerpt": parsed.objective[:300]} for v in variables if v in parsed.objective][:limit]


def detect_structures(parsed):
    variables = parsed.variable_names
    binaries = parsed.binary_variables
    constraint_names = parsed.constraint_names
    constraint_text = " ".join(parsed.constraints.values())
    constraint_name_text = " ".join(constraint_names).lower()
    graph = LPStructureGraph(parsed)
    weak = graph.weak_evidence()

    has_order = _has_prefix(variables, "Q") or _has_role(variables, "order")
    has_inventory = _has_prefix(variables, "I") or _has_role(variables, "inventory")
    has_shortage = _has_prefix(variables, "B") or _has_role(variables, "shortage")
    has_binary_order = _has_prefix(binaries, "Y") or _has_role(binaries, "binary_order")
    balance_name = "inventory_balance" in constraint_name_text or "balance" in constraint_name_text or "flow" in constraint_name_text
    capacity_name = "capacity" in constraint_name_text or "cap_" in constraint_name_text or "resource" in constraint_name_text
    big_m_name = "big_m" in constraint_name_text or "bigm" in constraint_name_text or "link" in constraint_name_text or "setup" in constraint_name_text

    detected = {
        "order_variable": has_order,
        "inventory_variable": has_inventory,
        "shortage_variable": has_shortage,
        "binary_order_variable": has_binary_order,
        "capacity_constraint": capacity_name,
        "big_m_constraint": big_m_name or (
            has_order and has_binary_order and "<=" in constraint_text
        ) or weak["big_m_like_constraints"]["found"],
        "inventory_balance": balance_name or (
            has_inventory and has_order and "=" in constraint_text
        ) or weak["inventory_recurrence_candidates"]["found"],
        "lead_time": "lead_time" in constraint_name_text or "leadtime" in constraint_name_text or "arrival" in constraint_name_text,
        "holding_cost": _objective_has_var(parsed, "I") or _objective_has_role(parsed, "inventory"),
        "shortage_cost": _objective_has_var(parsed, "B") or _objective_has_role(parsed, "shortage"),
        "fixed_order_cost": _objective_has_var(parsed, "Y") or _objective_has_role(parsed, "binary_order") or weak["fixed_cost_binary_terms"]["found"],
    }

    return detected


def _certificate_evidence(rule_name, parsed, detected, weak_evidence):
    if rule_name == "order_variable":
        vars_ = _matching_vars(parsed.variable_names, role="order", prefix="Q")
        return [{"variables": vars_[:10]}] if vars_ else []
    if rule_name == "inventory_variable":
        vars_ = _matching_vars(parsed.variable_names, role="inventory", prefix="I")
        return [{"variables": vars_[:10]}] if vars_ else []
    if rule_name == "shortage_variable":
        vars_ = _matching_vars(parsed.variable_names, role="shortage", prefix="B")
        return [{"variables": vars_[:10]}] if vars_ else []
    if rule_name == "binary_order_variable":
        vars_ = _matching_vars(parsed.binary_variables, role="binary_order", prefix="Y")
        return [{"binary_variables": vars_[:10]}] if vars_ else []
    if rule_name == "capacity_constraint":
        return _constraint_evidence(parsed, ["capacity", "cap_", "resource"])
    if rule_name == "lead_time":
        return _constraint_evidence(parsed, ["lead_time", "leadtime", "arrival"])
    if rule_name == "inventory_balance":
        ev = _constraint_evidence(parsed, ["inventory_balance", "balance", "flow", "inventory"])
        weak = weak_evidence.get("inventory_recurrence_candidates", {})
        if weak.get("found"):
            ev.append({"weak_detector": weak.get("detector"), "confidence": weak.get("confidence"), "evidence": weak.get("evidence")})
        return ev[:6]
    if rule_name == "big_m_constraint":
        ev = _constraint_evidence(parsed, ["big_m", "bigm", "link", "setup"])
        weak = weak_evidence.get("big_m_like_constraints", {})
        if weak.get("found"):
            ev.append({"weak_detector": weak.get("detector"), "confidence": weak.get("confidence"), "evidence": weak.get("evidence")})
        return ev[:6]
    if rule_name == "holding_cost":
        vars_ = _matching_vars(parsed.variable_names, role="inventory", prefix="I")
        return _objective_evidence(parsed, vars_)
    if rule_name == "shortage_cost":
        vars_ = _matching_vars(parsed.variable_names, role="shortage", prefix="B")
        return _objective_evidence(parsed, vars_)
    if rule_name == "fixed_order_cost":
        vars_ = _matching_vars(parsed.binary_variables, role="binary_order", prefix="Y")
        ev = _objective_evidence(parsed, vars_)
        weak = weak_evidence.get("fixed_cost_binary_terms", {})
        if weak.get("found"):
            ev.append({"weak_detector": weak.get("detector"), "confidence": weak.get("confidence"), "evidence": weak.get("evidence")})
        return ev[:8]
    return []


def build_structure_certificate(parsed, expected, detected, required_structures, optional_structures, weak_evidence):
    certificates = []
    required_set = set(required_structures)
    optional_set = set(optional_structures)
    for rule_name in STRUCTURE_KEYS:
        required = rule_name in required_set
        optional = rule_name in optional_set and not required
        passed = bool(detected.get(rule_name, False)) if (required or optional) else True
        evidence = _certificate_evidence(rule_name, parsed, detected, weak_evidence) if detected.get(rule_name, False) else []
        missing_reason = "" if passed else f"Required structure not detected: {STRUCTURE_DESCRIPTIONS.get(rule_name, rule_name)}."
        repair_hint = "" if passed else REPAIR_HINTS.get(rule_name, f"Add missing structure: {rule_name}.")
        certificates.append(RuleCertificate(
            rule_name=rule_name,
            required=required,
            optional=optional,
            passed=passed,
            score=1.0 if passed else 0.0,
            evidence=evidence,
            missing_reason=missing_reason,
            repair_hint=repair_hint,
        ).to_dict())
    return certificates


def check_structures(parsed, expected, problem_type=None):
    detected = detect_structures(parsed)
    graph = LPStructureGraph(parsed)
    weak_evidence = graph.weak_evidence()
    required_structures, optional_structures = split_expected_structures(expected, problem_type=problem_type)
    passed = {}
    missing = []
    messages = []

    for key in STRUCTURE_KEYS:
        if key in required_structures:
            ok = bool(detected.get(key, False))
            passed[key] = ok
            if not ok:
                missing.append(key)
                messages.append(f"Missing {STRUCTURE_DESCRIPTIONS.get(key, key)}.")
        else:
            passed[key] = True

    extra_detected = [key for key, value in detected.items() if value and key not in required_structures and key not in optional_structures]
    optional_detected = {key: bool(detected.get(key, False)) for key in optional_structures}

    if required_structures:
        structure_score = sum(1 for key in required_structures if detected.get(key, False)) / len(required_structures)
    else:
        structure_score = 1.0

    certificates = build_structure_certificate(
        parsed=parsed,
        expected=expected,
        detected=detected,
        required_structures=required_structures,
        optional_structures=optional_structures,
        weak_evidence=weak_evidence,
    )

    return StructureCheckResult(
        expected=dict(expected),
        detected=detected,
        passed=passed,
        missing=missing,
        extra_detected=extra_detected,
        structure_score=float(structure_score),
        messages=messages,
        certificates=certificates,
        optional_detected=optional_detected,
        weak_evidence=weak_evidence,
        required_structures=list(required_structures),
        optional_structures=list(optional_structures),
    )
