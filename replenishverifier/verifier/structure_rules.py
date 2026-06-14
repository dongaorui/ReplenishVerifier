from dataclasses import asdict, dataclass


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


@dataclass
class StructureCheckResult:
    expected: dict
    detected: dict
    passed: dict
    missing: list
    extra_detected: list
    structure_score: float
    messages: list

    def to_dict(self):
        return asdict(self)


def _has_prefix(names, prefix):
    return any(name == prefix or name.startswith(prefix + "_") or name.startswith(prefix + "(") for name in names)


def _objective_has_var(parsed, prefix):
    return any(
        variable in parsed.objective
        for variable in parsed.variable_names
        if variable == prefix or variable.startswith(prefix + "_") or variable.startswith(prefix + "(")
    )


def detect_structures(parsed):
    variables = parsed.variable_names
    binaries = parsed.binary_variables
    constraint_names = parsed.constraint_names
    constraint_text = " ".join(parsed.constraints.values())
    constraint_name_text = " ".join(constraint_names).lower()

    detected = {
        "order_variable": _has_prefix(variables, "Q"),
        "inventory_variable": _has_prefix(variables, "I"),
        "shortage_variable": _has_prefix(variables, "B"),
        "binary_order_variable": _has_prefix(binaries, "Y"),
        "capacity_constraint": "capacity" in constraint_name_text,
        "big_m_constraint": "big_m" in constraint_name_text or (
            _has_prefix(variables, "Q") and _has_prefix(variables, "Y") and "<=" in constraint_text
        ),
        "inventory_balance": "inventory_balance" in constraint_name_text or (
            _has_prefix(variables, "I") and _has_prefix(variables, "Q") and "=" in constraint_text
        ),
        "lead_time": "lead_time" in constraint_name_text or "leadtime" in constraint_name_text,
        "holding_cost": _objective_has_var(parsed, "I"),
        "shortage_cost": _objective_has_var(parsed, "B"),
        "fixed_order_cost": _objective_has_var(parsed, "Y"),
    }

    return detected


def check_structures(parsed, expected):
    detected = detect_structures(parsed)
    passed = {}
    missing = []
    messages = []

    expected_true = [key for key, value in expected.items() if value]
    for key, needed in expected.items():
        if needed:
            ok = bool(detected.get(key, False))
            passed[key] = ok
            if not ok:
                missing.append(key)
                messages.append(f"Missing {STRUCTURE_DESCRIPTIONS.get(key, key)}.")
        else:
            passed[key] = True

    extra_detected = [key for key, value in detected.items() if value and not expected.get(key, False)]

    if expected_true:
        structure_score = sum(1 for key in expected_true if detected.get(key, False)) / len(expected_true)
    else:
        structure_score = 1.0

    return StructureCheckResult(
        expected=dict(expected),
        detected=detected,
        passed=passed,
        missing=missing,
        extra_detected=extra_detected,
        structure_score=float(structure_score),
        messages=messages,
    )
