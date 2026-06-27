import re

from replenishverifier.verifier.lp_parser import expression_variables, normalize_symbol_name


DEEP_ERROR_WEIGHTS = {
    "newsvendor_python_max_on_lp_variable": 1.0,
    "shortage_variable_without_shortage_cost": 1.0,
    "capacity_not_shared_aggregation": 1.0,
    "lead_time_uses_current_order": 1.0,
    "missing_lead_time_lagged_order": 1.0,
    "missing_service_level_constraint": 1.0,
    "moq_forces_order_every_period": 1.0,
    "batch_multiplier_not_integer": 1.0,
    "missing_batch_linking_constraint": 0.5,
    "big_m_link_wrong_direction": 1.0,
    "binary_not_linked_to_order": 1.0,
}


def _constraint_relation(expr):
    if "<=" in expr:
        return "le"
    if ">=" in expr:
        return "ge"
    if "=" in expr:
        return "eq"
    return "unknown"


def _vars(parsed, expr):
    if parsed is None:
        return []
    return expression_variables(expr or "", parsed.variable_names)


def _has_role(name, role_terms):
    normalized = normalize_symbol_name(name)
    return any(term in normalized for term in role_terms)


def _order_vars(parsed, expr):
    return [name for name in _vars(parsed, expr) if _has_role(name, ["q", "order", "replenish", "purchase"])]


def _inventory_vars(parsed, expr):
    return [name for name in _vars(parsed, expr) if _has_role(name, ["i", "inventory", "stock", "inv"])]


def _shortage_vars(parsed, expr):
    return [name for name in _vars(parsed, expr) if _has_role(name, ["b", "shortage", "backlog", "unmet"])]


def _binary_vars(parsed, expr):
    binary_set = set((parsed.binary_variables if parsed is not None else []) or [])
    return [name for name in _vars(parsed, expr) if name in binary_set or _has_role(name, ["y", "setup", "trigger", "binary", "open_order"])]


def _numeric_suffix(name):
    numbers = re.findall(r"\d+", str(name or ""))
    return int(numbers[-1]) if numbers else None


def _objective_contains_any(parsed, names):
    objective = (parsed.objective if parsed is not None else "") or ""
    return any(re.search(rf"(?<![A-Za-z0-9_]){re.escape(name)}(?![A-Za-z0-9_])", objective) for name in names)


def _detect_newsvendor_python_max(code):
    code = code or ""
    return bool(re.search(r"\bmax\s*\([^\n)]*(?:LpVariable|\bQ\b|Q\[|I\[|B\[|inventory|shortage)", code, flags=re.IGNORECASE | re.DOTALL))


def _detect_shortage_cost_missing(problem_type, parsed):
    if problem_type not in {"single_item_multi_period_shortage", "single_item_multi_period_service_level", "single_period_newsvendor"}:
        return False
    shortage_names = []
    if parsed is not None:
        for expr in parsed.constraints.values():
            shortage_names.extend(_shortage_vars(parsed, expr))
        shortage_names.extend(name for name in parsed.variable_names if _has_role(name, ["b", "shortage", "backlog", "unmet"]))
    shortage_names = sorted(set(shortage_names))
    return bool(shortage_names) and not _objective_contains_any(parsed, shortage_names)


def _detect_capacity_not_shared(problem_type, parsed):
    if problem_type != "multi_item_capacity" or parsed is None:
        return False, True
    candidates = []
    for cname, expr in parsed.constraints.items():
        normalized = normalize_symbol_name(cname + " " + expr)
        if not any(term in normalized for term in ["capacity", "cap", "storage", "resource", "warehouse", "limit"]):
            continue
        if _constraint_relation(expr) != "le":
            continue
        vars_in_expr = _vars(parsed, expr)
        order_or_inventory = [name for name in vars_in_expr if _has_role(name, ["q", "order", "i", "inventory", "stock", "inv"])]
        candidates.append((cname, order_or_inventory))
    if not candidates:
        return True, False
    shared = any(len(set(vars_)) >= 2 for _, vars_ in candidates)
    return not shared, shared


def _detect_lead_time_errors(problem_type, parsed, parameters):
    if problem_type != "single_item_multi_period_lead_time" or parsed is None:
        return []
    lead_time = int((parameters or {}).get("lead_time") or 1)
    has_lagged = False
    uses_current = False
    for cname, expr in parsed.constraints.items():
        normalized = normalize_symbol_name(cname + " " + expr)
        if not any(term in normalized for term in ["balance", "inventory", "lead", "arrival"]):
            continue
        inv_suffixes = [_numeric_suffix(name) for name in _inventory_vars(parsed, expr)]
        order_suffixes = [_numeric_suffix(name) for name in _order_vars(parsed, expr)]
        inv_suffixes = [value for value in inv_suffixes if value is not None]
        order_suffixes = [value for value in order_suffixes if value is not None]
        if not inv_suffixes or not order_suffixes:
            continue
        period = max(inv_suffixes)
        if period >= lead_time and period in order_suffixes:
            uses_current = True
        if period >= lead_time and (period - lead_time) in order_suffixes:
            has_lagged = True
    errors = []
    if uses_current:
        errors.append("lead_time_uses_current_order")
    if not has_lagged:
        errors.append("missing_lead_time_lagged_order")
    return errors


def _detect_missing_service_level(problem_type, parsed):
    if problem_type != "single_item_multi_period_service_level" or parsed is None:
        return False
    for cname, expr in parsed.constraints.items():
        normalized = normalize_symbol_name(cname + " " + expr)
        if any(term in normalized for term in ["service", "fill", "rate", "shortage_limit", "unmet_limit"]):
            return False
        shortage_names = _shortage_vars(parsed, expr)
        if shortage_names and _constraint_relation(expr) == "le" and not _inventory_vars(parsed, expr):
            return False
    return True


def _detect_moq_batch_errors(problem_type, parsed):
    if problem_type != "single_item_multi_period_moq_batch" or parsed is None:
        return []
    errors = []
    has_batch_link = False
    for cname, expr in parsed.constraints.items():
        normalized = normalize_symbol_name(cname + " " + expr)
        order_names = _order_vars(parsed, expr)
        binary_names = _binary_vars(parsed, expr)
        batch_names = [name for name in _vars(parsed, expr) if _has_role(name, ["z", "batch", "lot", "multiple"])]
        if "moq" in normalized and _constraint_relation(expr) == "ge" and order_names and not binary_names:
            errors.append("moq_forces_order_every_period")
        if order_names and batch_names and _constraint_relation(expr) == "eq":
            has_batch_link = True
    if not has_batch_link:
        errors.append("missing_batch_linking_constraint")
    integer_names = set(parsed.binary_variables or [])
    raw = parsed.raw_text or ""
    generals_match = re.search(r"(?ims)^\s*Generals\s*(.*?)(?:^\s*Binaries\s*|^\s*End\s*$)", raw)
    if generals_match:
        integer_names.update(re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\b", generals_match.group(1)))
    batch_like = [name for name in parsed.variable_names if _has_role(name, ["z", "batch", "lot", "multiple"])]
    if batch_like and not any(name in integer_names for name in batch_like):
        errors.append("batch_multiplier_not_integer")
    return sorted(set(errors))


def _detect_big_m_errors(problem_type, parsed):
    if problem_type not in {"fixed_order_cost_big_m", "single_item_multi_period_moq_batch"} or parsed is None:
        return []
    errors = []
    linked = False
    wrong_direction = False
    for _, expr in parsed.constraints.items():
        order_names = _order_vars(parsed, expr)
        binary_names = _binary_vars(parsed, expr)
        if not order_names or not binary_names:
            continue
        linked = True
        relation = _constraint_relation(expr)
        if relation == "ge" and re.search(r"\bQ\w*\s*-", expr):
            wrong_direction = True
    if problem_type == "fixed_order_cost_big_m" and not linked:
        errors.append("binary_not_linked_to_order")
    if wrong_direction:
        errors.append("big_m_link_wrong_direction")
    return errors


def compute_semantic_structure_validation(problem_type, parsed=None, generated_code="", parameters=None):
    errors = []
    capacity_bad, capacity_shared = _detect_capacity_not_shared(problem_type, parsed)
    if _detect_shortage_cost_missing(problem_type, parsed):
        errors.append("shortage_variable_without_shortage_cost")
    if capacity_bad:
        errors.append("capacity_not_shared_aggregation")
    errors.extend(_detect_lead_time_errors(problem_type, parsed, parameters))
    if _detect_missing_service_level(problem_type, parsed):
        errors.append("missing_service_level_constraint")
    errors.extend(_detect_moq_batch_errors(problem_type, parsed))
    errors.extend(_detect_big_m_errors(problem_type, parsed))
    errors = sorted(set(errors))
    total_weight = max(sum(DEEP_ERROR_WEIGHTS.get(error, 1.0) for error in errors), 0.0)
    score = max(0.0, 1.0 - min(total_weight, 4.0) / 4.0)
    return {
        "validator": "semantic_structure_validation",
        "problem_type": problem_type,
        "score": float(score),
        "errors": errors,
        "error_count": len(errors),
        "capacity_shared_aggregation": bool(capacity_shared),
        "posthoc_only": False,
    }


def compute_deep_type_aware_validation(problem_type, generated_code="", parsed=None, parameters=None):
    semantic = compute_semantic_structure_validation(problem_type, parsed=parsed, generated_code=generated_code, parameters=parameters)
    errors = list(semantic["errors"])
    if problem_type == "single_period_newsvendor" and _detect_newsvendor_python_max(generated_code):
        errors.append("newsvendor_python_max_on_lp_variable")
    errors = sorted(set(errors))
    hard = {
        "newsvendor_python_max_on_lp_variable",
        "shortage_variable_without_shortage_cost",
        "capacity_not_shared_aggregation",
        "lead_time_uses_current_order",
        "missing_service_level_constraint",
        "moq_forces_order_every_period",
        "batch_multiplier_not_integer",
        "big_m_link_wrong_direction",
        "binary_not_linked_to_order",
    }
    hard_failures = [error for error in errors if error in hard]
    total_weight = max(sum(DEEP_ERROR_WEIGHTS.get(error, 1.0) for error in errors), 0.0)
    score = max(0.0, 1.0 - min(total_weight, 4.0) / 4.0)
    hard_gate_score = 1.0 if not hard_failures else max(0.0, 1.0 - min(len(hard_failures), 4) / 4.0)
    return {
        "validator": "deep_type_aware_validation",
        "problem_type": problem_type,
        "score": float(score),
        "hard_gate_score": float(hard_gate_score),
        "errors": errors,
        "hard_gate_failures": hard_failures,
        "error_count": len(errors),
        "semantic_structure_score": semantic["score"],
        "posthoc_only": False,
    }
