import json


SYSTEM_PROMPT = """You are an expert operations research modeler. Generate correct, executable PuLP code for inventory replenishment optimization problems."""


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


def build_prompt(sample):
    params = json.dumps(sample.get("parameters", {}), ensure_ascii=False, indent=2)
    expected = json.dumps(sample.get("expected_structures", {}), ensure_ascii=False, indent=2)
    return f'''Given the following inventory replenishment optimization problem, write one complete Python program using PuLP.

Problem ID: {sample.get('id')}
Problem type: {sample.get('problem_type')}
Difficulty: {sample.get('difficulty')}

Natural language problem:
{sample.get('natural_language')}

Parameters as JSON:
{params}

Expected high-level modeling structures as JSON:
{expected}

{CONSTRAINT_NAMING_REGULATION}
Hard requirements:
1. Use PuLP for modeling and solving.
2. Use these variable naming conventions whenever the structure is needed:
   - order variable: Q or Q_i_t
   - inventory variable: I or I_i_t
   - shortage/backlog variable: B or B_i_t
   - binary setup/order trigger variable: Y or Y_i_t
3. Use these constraint naming conventions whenever the structure is needed:
   - inventory_balance_t or inventory_balance_i_t
   - capacity_t
   - big_m_t
   - demand_satisfaction_t
   - shortage_balance_t
4. The code must contain:
   - import pulp
   - import os
   - prob = pulp.LpProblem(...)
   - prob.solve(pulp.PULP_CBC_CMD(msg=False))
   - print("STATUS:", pulp.LpStatus[prob.status])
   - print("OBJECTIVE:", pulp.value(prob.objective))
   - if environment variable OUTPUT_LP_PATH exists, run prob.writeLP(os.environ["OUTPUT_LP_PATH"])
5. Define a function build_model() that returns the PuLP LpProblem object named prob.
6. In the main block, call build_model(), optionally write the LP using OUTPUT_LP_PATH, solve, and print STATUS and OBJECTIVE.
7. Only output one complete Python code block. Do not output explanations or multiple code blocks.
'''


def build_chat_messages(sample):
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": build_prompt(sample)},
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
    feedback = repair_row.get("generic_repair_feedback") or repair_row.get("feedback") or repair_row.get("repair_prompt") or ""
    return f'''You are repairing Python PuLP code for an optimization problem using only generic execution and LP-artifact feedback.
Do not use replenishment-specific missing-structure labels unless they appear in the natural language problem itself.

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

Generic feedback:
{feedback}

{CONSTRAINT_NAMING_REGULATION}
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
