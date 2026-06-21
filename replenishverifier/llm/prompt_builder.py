import json


SYSTEM_PROMPT = """You are an expert operations research modeler. Generate correct, executable PuLP code for inventory replenishment optimization problems."""

PROMPT_TYPES = {"structured", "plain", "hidden_verifier", "type_aware_hidden_verifier"}


CONSTRAINT_NAMING_REGULATION = """CRITICAL REGULATION:
You MUST explicitly provide string names for ALL constraints in PuLP.
For example:
    prob += I[t] == I[t-1] + Q[t] - demand[t], f"inventory_balance_{t}"
    prob += Q[t] <= M * Y[t], f"big_m_{t}"
    prob += pulp.lpSum(volume[i] * I[i,t] for i in items) <= capacity[t], f"capacity_{t}"
Do NOT write anonymous constraints such as:
    prob += I[t] == I[t-1] + Q[t] - demand[t]
Anonymous PuLP constraints are exported as _C1/_C2 and are unsafe for structure verification.
Use descriptive names such as inventory_balance_*, capacity_*, big_m_*, demand_satisfaction_*, shortage_balance_*, and lead_time_*.
"""


GENERIC_CONSTRAINT_NAMING_GUIDANCE = """Modeling clarity guidance:
- Give decision variables meaningful names that reflect their optimization role.
- You should explicitly name every PuLP constraint with a short descriptive string.
- Do NOT rely on anonymous PuLP constraints such as _C1/_C2.
- Do not include explanations outside the requested Python code block.
"""


GENERIC_REPAIR_NAMING_GUIDANCE = """Generic modeling clarity guidance:
- Use meaningful decision-variable names, but do not rely on task-specific verifier labels.
- Explicitly name every PuLP constraint with a short descriptive string.
- Do NOT write anonymous constraints such as prob += expression without a name.
"""


PULP_INTERFACE_REQUIREMENTS = """Hard output and runner-interface requirements:
1. Output only plain Python source code. Do not output Markdown fences, explanations, natural-language reasoning, or multiple alternatives.
2. Do not output <think>, </think>, chain-of-thought, analysis, or any hidden reasoning text.
3. The first line of your answer must be exactly: import pulp
4. The generated file must be importable as a Python module.
5. Define build_model() with no arguments. build_model() must return a pulp.LpProblem object.
6. A global model = pulp.LpProblem(...) object is acceptable only as a secondary runner-compatible interface; build_model() is preferred.
7. Use PuLP for modeling and include import pulp.
8. Build a complete objective and all required constraints inside build_model().
9. If you include a main block, it may call build_model(), write OUTPUT_LP_PATH when present, solve with pulp.PULP_CBC_CMD(msg=False), and print STATUS and OBJECTIVE.
10. Do not output Markdown. Do not wrap the answer in ```python or ``` fences.

Required format template:
import pulp

def build_model():
    prob = pulp.LpProblem("replenishment_model", pulp.LpMinimize)

    # Define decision variables here

    # Define objective here
    prob += ...

    # Define constraints here

    return prob

Replace the template placeholders with complete executable PuLP code for the given problem.
"""


CANDIDATE_QUALITY_SELF_CHECK = """Candidate-quality self-check before final answer:
- Silently verify that your model includes every decision variable family implied by the problem statement and JSON parameters.
- Silently verify that the objective contains all cost and penalty terms described by the problem.
- Silently verify that each period/item balance, capacity, setup/linking, shortage, and nonnegativity requirement implied by the problem is modeled when applicable.
- Silently verify that every PuLP constraint has an explicit descriptive name.
- Do not reveal this checklist or any reasoning; output only the final Python source code.
"""


_CANDIDATE_DIVERSITY_STYLES = [
    "Use clear tuple-indexed PuLP dictionaries for multi-index variables when the problem has item or period dimensions.",
    "Use nested loops with explicit per-period or per-item constraint names; keep algebra simple and readable.",
    "Write the objective as a single pulp.lpSum expression after defining all decision variables.",
    "Define objective-term helper lists before adding the objective, then add named constraints in a separate section.",
    "Use concise variable names but descriptive constraint names that expose the mathematical role.",
    "Use descriptive variable names and compact comprehension-based constraints where this stays readable.",
    "Emphasize boundary conditions such as initial inventory and first-period balance before writing later-period constraints.",
    "Emphasize linking/setup/capacity constraints before returning the model, while preserving the same mathematical problem.",
]


def candidate_diversity_instruction(candidate_index=None, k=None):
    if candidate_index is None or k is None:
        return ""
    try:
        idx = int(candidate_index)
        total = int(k)
    except (TypeError, ValueError):
        return ""
    if total <= 1:
        return ""
    style = _CANDIDATE_DIVERSITY_STYLES[idx % len(_CANDIDATE_DIVERSITY_STYLES)]
    return f"""Candidate diversity instruction:
You are generating candidate {idx + 1} of {total}. Construct the model independently, using this style preference while keeping the same mathematical model and runner interface:
- {style}
Do not simplify, omit, or change the mathematical requirements just to be different.
"""




def _validate_prompt_type(prompt_type):
    if prompt_type not in PROMPT_TYPES:
        raise ValueError(f"prompt_type must be one of {sorted(PROMPT_TYPES)}, got {prompt_type!r}")


def _structured_problem_header(sample):
    return f"""Problem ID: {sample.get('id')}
Problem type: {sample.get('problem_type')}
Difficulty: {sample.get('difficulty')}

Natural language problem:
{sample.get('natural_language')}
"""


def _plain_problem_header(sample):
    return f"""Problem ID: {sample.get('id')}

Natural language problem:
{sample.get('natural_language')}
"""


def _parameters_block(sample):
    params = json.dumps(sample.get("parameters", {}), ensure_ascii=False, indent=2)
    return f"""Parameters as JSON:
{params}
"""


def type_aware_generation_checklist(problem_type):
    """Natural-language modeling checklist for hidden type-aware generation.

    This intentionally does not expose expected_structures JSON, reference
    objectives, reference LPs, or reference answers.
    """
    checklists = {
        "single_period_newsvendor": [
            "Define an order quantity decision variable and represent demand-dependent leftover or unmet-demand effects when needed.",
            "Include objective terms for ordering or purchasing cost and overage/holding and underage/shortage penalties when they are present in the data.",
            "Use explicit variable and constraint names that reflect order, inventory, overage, underage, or shortage roles.",
        ],
        "single_item_multi_period": [
            "Define period-indexed order and inventory decision variables.",
            "Add inventory balance constraints linking inventory across periods with orders and demand.",
            "Include ordering and holding cost terms in the objective.",
        ],
        "single_item_multi_period_shortage": [
            "Define period-indexed order, inventory, and shortage or unmet-demand decision variables.",
            "Add balance constraints that connect inventory, order quantity, demand, and shortage across periods.",
            "Include shortage penalty terms in the objective along with ordering and holding costs.",
        ],
        "multi_item_capacity": [
            "Define item-period order and inventory decision variables.",
            "Add item-wise inventory balance constraints for every item and period.",
            "Add per-period capacity or resource constraints that limit total replenishment or inventory usage across items.",
            "Include item-wise ordering and holding cost terms in the objective.",
        ],
        "fixed_order_cost_big_m": [
            "Define period-indexed order and inventory decision variables.",
            "Define binary order/setup variables that indicate whether an order is placed in each period.",
            "Add Big-M linking constraints so positive order quantities require the binary order/setup variable to be active.",
            "Include fixed order or setup cost terms in the objective along with variable ordering and holding costs.",
            "Add inventory balance constraints linking inventory across periods with orders and demand.",
        ],
    }
    items = checklists.get(problem_type) or [
        "Define clear PuLP decision variables for the optimization decisions.",
        "Include a complete objective and all constraints implied by the natural-language problem.",
        "Use explicit names for constraints and variables so the exported LP is interpretable.",
    ]
    body = "\n".join(f"- {item}" for item in items)
    return f"Problem-type modeling checklist:\n{body}\n"



def build_prompt(sample, prompt_type="hidden_verifier", candidate_index=None, k=None):
    _validate_prompt_type(prompt_type)
    params = _parameters_block(sample)
    diversity = candidate_diversity_instruction(candidate_index=candidate_index, k=k)

    if prompt_type == "structured":
        expected = json.dumps(sample.get("expected_structures", {}), ensure_ascii=False, indent=2)
        return f'''Given the following inventory replenishment optimization problem, write one complete Python program using PuLP.

{_structured_problem_header(sample)}
{params}
Expected high-level modeling structures as JSON:
{expected}

{CONSTRAINT_NAMING_REGULATION}
{CANDIDATE_QUALITY_SELF_CHECK}
{diversity}
{PULP_INTERFACE_REQUIREMENTS}'''

    if prompt_type == "plain":
        return f'''Given the following optimization problem, write one complete Python program using PuLP.

{_plain_problem_header(sample)}
{params}
{CANDIDATE_QUALITY_SELF_CHECK}
{diversity}
{PULP_INTERFACE_REQUIREMENTS}'''

    if prompt_type == "type_aware_hidden_verifier":
        return f'''Given the following optimization problem, write one complete Python program using PuLP.

{_plain_problem_header(sample)}
{params}
{type_aware_generation_checklist(sample.get('problem_type'))}
{GENERIC_CONSTRAINT_NAMING_GUIDANCE}
{CANDIDATE_QUALITY_SELF_CHECK}
{diversity}
{PULP_INTERFACE_REQUIREMENTS}'''

    return f'''Given the following optimization problem, write one complete Python program using PuLP.

{_plain_problem_header(sample)}
{params}
{GENERIC_CONSTRAINT_NAMING_GUIDANCE}
{CANDIDATE_QUALITY_SELF_CHECK}
{diversity}
{PULP_INTERFACE_REQUIREMENTS}'''


def build_chat_messages(sample, prompt_type="hidden_verifier", candidate_index=None, k=None):
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": build_prompt(sample, prompt_type=prompt_type, candidate_index=candidate_index, k=k)},
    ]


def build_repair_prompt(sample, repair_row, original_code=""):
    params = json.dumps(sample.get("parameters", {}), ensure_ascii=False, indent=2)
    return f'''You are repairing Python PuLP code for an inventory replenishment optimization problem.

Problem ID: {sample.get('id')}
Problem type: {sample.get('problem_type')}
Difficulty: {sample.get('difficulty')}

Natural language problem:
{sample.get('natural_language')}

Parameters as JSON:
{params}

Original candidate code:
```python
{original_code or repair_row.get('generated_code', '')}
```

Verifier feedback:
{repair_row.get('feedback') or repair_row.get('repair_prompt') or ''}

{CONSTRAINT_NAMING_REGULATION}
Hard requirements:
1. Return one complete corrected Python program using PuLP.
2. Preserve the required solve/export interface: build_model(), optional OUTPUT_LP_PATH writeLP, solver call, STATUS and OBJECTIVE prints.
3. Fix only the modeling and execution issues indicated by the feedback and problem statement.
4. Output only one Python code block.
'''


def build_generic_repair_prompt(sample, repair_row, original_code=""):
    params = json.dumps(sample.get("parameters", {}), ensure_ascii=False, indent=2)
    feedback = repair_row.get("generic_repair_feedback") or "- Inspect generic execution, objective, variable, constraint, and solver issues."
    return f'''You are repairing Python PuLP code for an optimization problem using only generic execution, solver, and LP-artifact feedback.
Do not use task-specific verifier labels or missing-structure names.

Problem ID: {sample.get('id')}
Problem category: optimization instance
Difficulty: {sample.get('difficulty')}

Natural language problem:
{sample.get('natural_language')}

Parameters as JSON:
{params}

Original candidate code:
```python
{original_code or repair_row.get('generated_code', '') or repair_row.get('original_candidate_code', '')}
```

Generic feedback:
{feedback}

{GENERIC_REPAIR_NAMING_GUIDANCE}
Hard requirements:
1. Return one complete corrected Python program using PuLP.
2. Preserve build_model(), optional OUTPUT_LP_PATH writeLP, solver call, STATUS and OBJECTIVE prints.
3. Focus on generic modeling/code validity: objective, variables, constraints, bounds, solver execution, and meaningful names.
4. Output only one Python code block.
'''


def build_repair_chat_messages(sample, repair_row, original_code="", repair_type="structure_aware"):
    prompt = build_generic_repair_prompt(sample, repair_row, original_code=original_code) if repair_type == "generic" else build_repair_prompt(sample, repair_row, original_code=original_code)
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]
