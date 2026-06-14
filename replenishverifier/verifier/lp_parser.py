import re
from dataclasses import asdict, dataclass
from pathlib import Path


SECTION_NAMES = ["Minimize", "Maximize", "Subject To", "Bounds", "Generals", "Binaries", "End"]


@dataclass
class ParsedLP:
    path: str
    sense: str
    objective: str
    constraints: dict
    constraint_names: list
    variable_names: list
    binary_variables: list
    bounds: list
    raw_text: str

    def to_dict(self):
        return asdict(self)


def _get_section(text, section_name, next_names):
    pattern = rf"(?ims)^\s*{re.escape(section_name)}\s*$"
    match = re.search(pattern, text)
    if not match:
        return ""
    start = match.end()
    end = len(text)
    for next_name in next_names:
        next_match = re.search(rf"(?ims)^\s*{re.escape(next_name)}\s*$", text[start:])
        if next_match:
            end = start + next_match.start()
            break
    return text[start:end].strip()


def _parse_constraints(subject_text):
    constraints = {}
    current_name = None
    current_lines = []

    for raw in subject_text.splitlines():
        line = raw.strip()
        if not line:
            continue

        if ":" in line:
            if current_name is not None:
                constraints[current_name] = " ".join(current_lines).strip()
            name, expr = line.split(":", 1)
            current_name = name.strip()
            current_lines = [expr.strip()]
        elif current_name is not None:
            current_lines.append(line)

    if current_name is not None:
        constraints[current_name] = " ".join(current_lines).strip()

    return constraints


def _extract_names_from_expr(expr):
    tokens = re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\b", expr)
    blacklist = {
        "Minimize", "Maximize", "Subject", "To", "Bounds", "Generals", "Binaries", "End",
        "OBJ", "obj", "total_cost", "free", "inf", "infinity",
    }
    names = []
    for token in tokens:
        if token in blacklist:
            continue
        if re.fullmatch(r"[eE]", token):
            continue
        names.append(token)
    return names


def parse_lp_text(text, path="<memory>"):
    sense = "minimize" if re.search(r"(?im)^\s*Minimize\s*$", text) else "maximize"
    objective = _get_section(text, "Minimize", ["Subject To", "Bounds", "Generals", "Binaries", "End"])
    if not objective:
        objective = _get_section(text, "Maximize", ["Subject To", "Bounds", "Generals", "Binaries", "End"])

    subject = _get_section(text, "Subject To", ["Bounds", "Generals", "Binaries", "End"])
    bounds_text = _get_section(text, "Bounds", ["Generals", "Binaries", "End"])
    binaries_text = _get_section(text, "Binaries", ["End"])

    constraints = _parse_constraints(subject)
    bounds = [line.strip() for line in bounds_text.splitlines() if line.strip()]

    binary_variables = []
    for line in binaries_text.splitlines():
        line = line.strip()
        if line:
            binary_variables.extend(_extract_names_from_expr(line))

    variable_set = set()
    for name in _extract_names_from_expr(objective):
        variable_set.add(name)
    for expr in constraints.values():
        for name in _extract_names_from_expr(expr):
            variable_set.add(name)
    for line in bounds:
        for name in _extract_names_from_expr(line):
            variable_set.add(name)
    for name in binary_variables:
        variable_set.add(name)

    for constraint_name in constraints:
        variable_set.discard(constraint_name)

    return ParsedLP(
        path=str(path),
        sense=sense,
        objective=objective,
        constraints=constraints,
        constraint_names=sorted(constraints.keys()),
        variable_names=sorted(variable_set),
        binary_variables=sorted(set(binary_variables)),
        bounds=bounds,
        raw_text=text,
    )


def parse_lp_file(path):
    path = Path(path)
    text = path.read_text(encoding="utf-8", errors="ignore")
    return parse_lp_text(text, path=str(path))
