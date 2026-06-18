# ReplenishVerifier v5 TypeAware Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Do not use git worktrees or agent worktrees for this plan; execute directly in `/home/dongaorui/projects/lunwen`.

**Goal:** Add v5 problem-type-aware generation prompts, static validation feedback, and a no-reference `ReplenishVerifier-TypeAware` selector.

**Architecture:** The implementation extends existing modules instead of adding a new pipeline. Prompt routing stays in `replenishverifier/llm/prompt_builder.py`; static candidate-observable signals stay in `replenishverifier/pipeline/quality_signals.py`; formal selection stays in `replenishverifier/experiments/methods.py`; experiment orchestration stays in `replenishverifier/experiments/run_all_methods.py`; leakage checks stay in `replenishverifier/experiments/audit_leakage.py`.

**Tech Stack:** Python 3.10+, pytest, PuLP, existing ReplenishVerifier modules.

## Global Constraints

- Modify code directly in `/home/dongaorui/projects/lunwen` only.
- Do not create a git worktree.
- Do not use agent worktrees.
- Do not modify files in `/tmp`, `.worktrees`, `../lunwen-*`, or any temporary project copy.
- Run `git status` before implementation and after implementation.
- Run `git diff --name-only` after implementation.
- Do not run Qwen3-8B or any other large model generation.
- Do not fabricate experiment results.
- Formal selection must not use `reference_objective`, `objective_correct`, reference LP, reference answer, objective gap, or relative error.
- `objective_term_coverage`, hard-gate signals, structure scores, static validation, solver status, runtime, and objective consensus may be used only when derived from candidate code / LP / candidate evaluations.
- Repair support in this plan is static feedback and prompt generation only; do not claim repair success.
- Do not commit unless the user explicitly asks; this overrides any generic plan template advice to commit.

---

## File Structure

- Modify `replenishverifier/llm/prompt_builder.py`
  - Adds `type_aware_hidden_verifier` and problem-type checklist text.
  - Keeps old prompt types compatible.

- Modify `replenishverifier/llm/run_generation.py`
  - Adds new prompt type to CLI choices.
  - Makes v5 prompt type the default for generation.
  - Keeps generation retry/static validation behavior unchanged except for new fields produced by `compute_static_validation()`.

- Modify `replenishverifier/pipeline/quality_signals.py`
  - Adds candidate-code-only type-aware static validation.
  - Returns backward-compatible old fields plus new `type_aware_static_validation*` fields.

- Modify `replenishverifier/experiments/methods.py`
  - Adds `ReplenishVerifier-TypeAware` to method lists.
  - Adds TypeAware selection component functions.
  - Adds TypeAware repair feedback to structure-aware repair prompts.

- Modify `replenishverifier/experiments/run_all_methods.py`
  - Adds TypeAware to ablation and low-resource lists.
  - Keeps old output files and fields.

- Modify `replenishverifier/experiments/audit_leakage.py`
  - Adds TypeAware to formal method audit.
  - Rejects forbidden reference-derived keys in TypeAware selection components.

- Modify tests:
  - `tests/test_prompt_modes.py`
  - `tests/test_static_validation.py`
  - `tests/test_selection_gating.py`
  - `tests/test_leakage_audit.py`
  - optionally `tests/test_strong_baselines.py` if method-list expectations require it.

---

### Task 1: Add TypeAware hidden generation prompt

**Files:**
- Modify: `replenishverifier/llm/prompt_builder.py`
- Modify: `replenishverifier/llm/run_generation.py`
- Test: `tests/test_prompt_modes.py`

**Interfaces:**
- Consumes: `build_prompt(sample: dict, prompt_type: str) -> str`; `build_chat_messages(sample, prompt_type)`; `render_prompt(tokenizer, sample, use_chat_template=True, prompt_type=...)`.
- Produces: prompt type string `type_aware_hidden_verifier`; helper `type_aware_generation_checklist(problem_type: str | None) -> str`.

- [ ] **Step 1: Write failing prompt tests**

Add these imports / tests to `tests/test_prompt_modes.py`:

```python
from replenishverifier.llm.prompt_builder import build_chat_messages, build_prompt, type_aware_generation_checklist
from replenishverifier.llm.run_generation import render_prompt
```

Append tests:

```python
def test_type_aware_hidden_verifier_prompt_includes_fixed_order_checklist_without_expected_json():
    prompt = build_prompt(_sample(), prompt_type="type_aware_hidden_verifier")

    assert "Problem-type modeling checklist" in prompt
    assert "binary order" in prompt.lower() or "binary setup" in prompt.lower()
    assert "big-m" in prompt.lower() or "big m" in prompt.lower()
    assert "fixed order cost" in prompt.lower() or "setup cost" in prompt.lower()
    assert "Expected high-level modeling structures as JSON" not in prompt
    assert '"inventory_balance"' not in prompt
    assert '"big_m_constraint"' not in prompt
    assert '"fixed_order_cost"' not in prompt
    assert "build_model()" in prompt
    assert "The first line of your answer must be exactly: import pulp" in prompt


def test_type_aware_checklist_mentions_capacity_for_multi_item_capacity():
    checklist = type_aware_generation_checklist("multi_item_capacity")

    assert "capacity" in checklist.lower()
    assert "item" in checklist.lower()
    assert "period" in checklist.lower()
    assert "inventory balance" in checklist.lower()


def test_render_prompt_accepts_type_aware_hidden_verifier_with_chat_template():
    rendered = render_prompt(DummyTokenizer(), _sample(), use_chat_template=True, prompt_type="type_aware_hidden_verifier")

    assert "Problem-type modeling checklist" in rendered
    assert "Expected high-level modeling structures as JSON" not in rendered
    assert "build_model()" in rendered
```

- [ ] **Step 2: Run prompt tests and verify they fail**

Run:

```bash
PYTHONNOUSERSITE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests/test_prompt_modes.py -q
```

Expected before implementation: failure because `type_aware_generation_checklist` does not exist and prompt type is unknown.

- [ ] **Step 3: Implement prompt helper and prompt type**

In `replenishverifier/llm/prompt_builder.py`, change:

```python
PROMPT_TYPES = {"structured", "plain", "hidden_verifier"}
```

to:

```python
PROMPT_TYPES = {"structured", "plain", "hidden_verifier", "type_aware_hidden_verifier"}
```

Add after `_parameters_block()`:

```python
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
```

In `build_prompt()`, add before the final `return` for `hidden_verifier`:

```python
    if prompt_type == "type_aware_hidden_verifier":
        return f'''Given the following optimization problem, write one complete Python program using PuLP.

{_plain_problem_header(sample)}
{params}
{type_aware_generation_checklist(sample.get('problem_type'))}
{GENERIC_CONSTRAINT_NAMING_GUIDANCE}
{PULP_INTERFACE_REQUIREMENTS}'''
```

In `replenishverifier/llm/run_generation.py`, change CLI default and choices:

```python
parser.add_argument("--prompt_type", choices=["hidden_verifier", "plain", "structured", "type_aware_hidden_verifier"], default="type_aware_hidden_verifier")
```

Change `run_generation(... prompt_type="hidden_verifier", ...)` default to:

```python
prompt_type="type_aware_hidden_verifier",
```

- [ ] **Step 4: Run prompt tests and verify pass**

Run:

```bash
PYTHONNOUSERSITE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests/test_prompt_modes.py -q
```

Expected: all prompt tests pass.

---

### Task 2: Add problem-type-aware static validation signals

**Files:**
- Modify: `replenishverifier/pipeline/quality_signals.py`
- Test: `tests/test_static_validation.py`

**Interfaces:**
- Consumes: `compute_static_validation(generated_code: str, problem_type: str | None = None) -> dict`.
- Produces: nested `type_aware_static_validation` and top-level `type_aware_static_validation_score`, `type_aware_static_validation_errors`.

- [ ] **Step 1: Write failing static validation tests**

Append to `tests/test_static_validation.py`:

```python
def test_type_aware_static_validation_flags_missing_capacity_for_capacity_problem():
    code = '''import pulp


def build_model():
    prob = pulp.LpProblem("cap", pulp.LpMinimize)
    order = pulp.LpVariable.dicts("order", ((i, t) for i in range(2) for t in range(2)), lowBound=0)
    inventory = pulp.LpVariable.dicts("inventory", ((i, t) for i in range(2) for t in range(2)), lowBound=0)
    prob += order[(0, 0)] + inventory[(0, 0)], "total_cost"
    prob += inventory[(0, 0)] == order[(0, 0)] - 3, "inventory_balance_0_0"
    return prob
'''

    result = compute_static_validation(code, problem_type="multi_item_capacity")

    assert "missing_capacity_constraint" in result["type_aware_static_validation_errors"]
    assert result["type_aware_static_validation"]["hard_gate_failures"] == ["missing_capacity_constraint"]
    assert result["type_aware_static_validation_score"] < 1.0


def test_type_aware_static_validation_flags_missing_shortage_cost():
    code = '''import pulp


def build_model():
    prob = pulp.LpProblem("shortage", pulp.LpMinimize)
    order = pulp.LpVariable.dicts("order", range(2), lowBound=0)
    inventory = pulp.LpVariable.dicts("inventory", range(2), lowBound=0)
    shortage = pulp.LpVariable.dicts("shortage", range(2), lowBound=0)
    prob += order[0] + inventory[0], "total_cost"
    prob += inventory[0] + shortage[0] == order[0] - 4, "inventory_shortage_balance_0"
    return prob
'''

    result = compute_static_validation(code, problem_type="single_item_multi_period_shortage")

    assert "missing_shortage_cost_term" in result["type_aware_static_validation_errors"]
    assert "missing_shortage_variable" not in result["type_aware_static_validation_errors"]


def test_type_aware_static_validation_flags_fixed_order_big_m_failures():
    code = '''import pulp


def build_model():
    prob = pulp.LpProblem("fixed", pulp.LpMinimize)
    order = pulp.LpVariable.dicts("order", range(2), lowBound=0)
    inventory = pulp.LpVariable.dicts("inventory", range(2), lowBound=0)
    prob += order[0] + inventory[0], "total_cost"
    prob += inventory[0] == order[0] - 4, "inventory_balance_0"
    return prob
'''

    result = compute_static_validation(code, problem_type="fixed_order_cost_big_m")

    errors = result["type_aware_static_validation_errors"]
    assert "missing_fixed_order_binary" in errors
    assert "missing_big_m_linking" in errors
    assert "missing_fixed_order_cost_term" in errors
    assert result["type_aware_static_validation"]["hard_gate_score"] < 1.0
```

- [ ] **Step 2: Run static validation tests and verify they fail**

Run:

```bash
PYTHONNOUSERSITE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests/test_static_validation.py -q
```

Expected before implementation: failures because `type_aware_static_validation*` fields do not exist.

- [ ] **Step 3: Implement type-aware validation helpers**

In `replenishverifier/pipeline/quality_signals.py`, add below `PATTERNS`:

```python
OBJECTIVE_CONTEXT_PATTERNS = {
    "order_cost": re.compile(r"order_cost|ordering_cost|unit_order_cost|purchase_cost|procurement|order\s*\[|Q\s*\[", re.IGNORECASE),
    "holding_cost": re.compile(r"holding_cost|hold_cost|inventory_cost|holding|inventory\s*\[|I\s*\[", re.IGNORECASE),
    "shortage_cost": re.compile(r"shortage_cost|shortage_penalty|backlog_cost|unmet_penalty|shortage\s*\[|backlog\s*\[|unmet\s*\[", re.IGNORECASE),
    "fixed_order_cost": re.compile(r"fixed_order_cost|setup_cost|fixed_cost|ordering_fixed|setup\s*\[|order_binary\s*\[", re.IGNORECASE),
}
```

Add helper functions before `compute_static_validation()`:

```python
def _code_has(pattern_key, code):
    return bool(PATTERNS[pattern_key].search(code or ""))


def _objective_has(term_key, code):
    return bool(OBJECTIVE_CONTEXT_PATTERNS[term_key].search(code or ""))


def _type_aware_checks(problem_type, code, result):
    checks = []

    def add(item_id, passed, feedback):
        checks.append({"id": item_id, "passed": bool(passed), "feedback": feedback})

    has_inventory = result.get("has_inventory_balance_pattern")
    has_capacity = result.get("has_capacity_pattern")
    has_shortage = result.get("has_shortage_pattern")
    has_binary = result.get("has_binary_order_pattern")
    has_big_m = result.get("has_big_m_pattern")
    has_fixed_cost = result.get("has_fixed_order_cost_pattern") or _objective_has("fixed_order_cost", code)
    has_shortage_cost = _objective_has("shortage_cost", code)
    has_order_cost = _objective_has("order_cost", code)
    has_holding_cost = _objective_has("holding_cost", code)

    if problem_type in {"single_item_multi_period", "single_item_multi_period_shortage", "multi_item_capacity", "fixed_order_cost_big_m"}:
        add("inventory_balance", has_inventory, "Add explicit inventory balance constraints linking inventory, orders, and demand across periods.")
    if problem_type == "multi_item_capacity":
        add("capacity_constraint", has_capacity, "Add per-period capacity/resource constraints across items.")
    if problem_type == "single_item_multi_period_shortage":
        add("shortage_variable", has_shortage, "Add shortage/backlog/unmet-demand variables.")
        add("shortage_cost_term", has_shortage_cost, "Include shortage penalty terms in the objective.")
    if problem_type == "fixed_order_cost_big_m":
        add("fixed_order_binary", has_binary, "Add binary order/setup variables.")
        add("big_m_linking", has_big_m, "Add Big-M linking constraints tying order quantities to binary setup/order variables.")
        add("fixed_order_cost_term", has_fixed_cost, "Include fixed order/setup cost terms in the objective.")
    if problem_type in {"single_item_multi_period", "single_item_multi_period_shortage", "multi_item_capacity", "fixed_order_cost_big_m"}:
        add("order_cost_term", has_order_cost, "Include ordering or purchase cost terms in the objective.")
        add("holding_cost_term", has_holding_cost, "Include holding or inventory cost terms in the objective.")

    missing = [f"missing_{item['id']}" for item in checks if not item["passed"]]
    passed = [item["id"] for item in checks if item["passed"]]
    feedback = [item["feedback"] for item in checks if not item["passed"]]
    score = float(len(passed) / max(len(checks), 1))
    hard_gate_failures = [item for item in missing if item in {
        "missing_inventory_balance",
        "missing_capacity_constraint",
        "missing_shortage_variable",
        "missing_shortage_cost_term",
        "missing_fixed_order_binary",
        "missing_big_m_linking",
        "missing_fixed_order_cost_term",
    }]
    hard_gate_score = float((len(checks) - len(hard_gate_failures)) / max(len(checks), 1)) if checks else 1.0
    return {
        "problem_type": problem_type,
        "checklist": checks,
        "passed_items": passed,
        "missing_items": missing,
        "repair_feedback": feedback,
        "score": score,
        "hard_gate_failures": hard_gate_failures,
        "hard_gate_score": hard_gate_score,
        "evidence": {
            "inventory_balance": bool(has_inventory),
            "capacity_constraint": bool(has_capacity),
            "shortage_variable": bool(has_shortage),
            "shortage_cost_term": bool(has_shortage_cost),
            "fixed_order_binary": bool(has_binary),
            "big_m_linking": bool(has_big_m),
            "fixed_order_cost_term": bool(has_fixed_cost),
            "order_cost_term": bool(has_order_cost),
            "holding_cost_term": bool(has_holding_cost),
        },
    }
```

At the end of `compute_static_validation()` before `return result`, add:

```python
    type_aware = _type_aware_checks(problem_type, code, result)
    result["type_aware_static_validation"] = type_aware
    result["type_aware_static_validation_score"] = float(type_aware["score"])
    result["type_aware_static_validation_errors"] = list(type_aware["missing_items"])
```

For early returns in empty-code and syntax-error branches, compute with the current `result` before returning:

```python
        type_aware = _type_aware_checks(problem_type, code, result)
        result["type_aware_static_validation"] = type_aware
        result["type_aware_static_validation_score"] = float(type_aware["score"])
        result["type_aware_static_validation_errors"] = list(type_aware["missing_items"])
        return result
```

- [ ] **Step 4: Run static validation tests and verify pass**

Run:

```bash
PYTHONNOUSERSITE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests/test_static_validation.py -q
```

Expected: all static validation tests pass.

---

### Task 3: Add TypeAware formal selection score

**Files:**
- Modify: `replenishverifier/experiments/methods.py`
- Test: `tests/test_selection_gating.py`

**Interfaces:**
- Consumes: evaluated candidate row fields `execution`, `structure_verification`, `structure_score`, `objective_term_coverage`, `objective_consensus_score`, `runtime_sec`, `type_aware_static_validation`, `type_aware_static_validation_errors`.
- Produces: method `ReplenishVerifier-TypeAware`; helper `type_aware_selection_components(row: dict) -> dict`; helper `type_aware_selection_score(row: dict) -> float`.

- [ ] **Step 1: Write failing selection tests**

Append to `tests/test_selection_gating.py`:

```python
def test_type_aware_selection_prefers_non_k0_with_better_objective_terms_and_gates():
    rows = [
        _row("c0", structure_score=1.0, missing=[], consensus=0.2, feedback="needs repair"),
        _row("c1", structure_score=0.9, missing=[], consensus=0.1, feedback=""),
    ]
    rows[0]["objective_term_coverage"] = 0.0
    rows[0]["runtime_sec"] = 1.0
    rows[0]["type_aware_static_validation"] = {
        "score": 0.5,
        "hard_gate_score": 0.5,
        "hard_gate_failures": ["missing_capacity_constraint"],
        "missing_items": ["missing_capacity_constraint", "missing_order_cost_term"],
        "repair_feedback": ["Add capacity constraints.", "Add order cost terms."],
    }
    rows[0]["type_aware_static_validation_errors"] = ["missing_capacity_constraint", "missing_order_cost_term"]
    rows[1]["objective_term_coverage"] = 1.0
    rows[1]["runtime_sec"] = 1.0
    rows[1]["type_aware_static_validation"] = {
        "score": 1.0,
        "hard_gate_score": 1.0,
        "hard_gate_failures": [],
        "missing_items": [],
        "repair_feedback": [],
    }
    rows[1]["type_aware_static_validation_errors"] = []

    selected = select_for_method("ReplenishVerifier-TypeAware", {"p0": rows}, _benchmark())

    assert selected[0]["candidate_id"] == "c1"
    assert selected[0]["method_name"] == "ReplenishVerifier-TypeAware"
    assert selected[0]["uses_reference_objective_for_selection"] is False
    assert selected[0]["selection_components"]["objective_term_coverage"] == 1.0
    assert selected[0]["hard_gate_failures"] == []


def test_type_aware_selection_components_do_not_include_reference_or_oracle_fields():
    rows = [_row("c0", structure_score=1.0, missing=[])]
    rows[0]["objective_term_coverage"] = 1.0
    rows[0]["reference_objective"] = 123.0
    rows[0]["objective_correct"] = 0.0
    rows[0]["relative_error"] = 0.9
    rows[0]["type_aware_static_validation"] = {"hard_gate_score": 1.0, "hard_gate_failures": [], "missing_items": []}
    rows[0]["type_aware_static_validation_errors"] = []

    selected = select_for_method("ReplenishVerifier-TypeAware", {"p0": rows}, _benchmark())
    component_keys = set(selected[0]["selection_components"].keys())

    assert "reference_objective" not in component_keys
    assert "objective_correct" not in component_keys
    assert "relative_error" not in component_keys
    assert "reference_lp" not in component_keys
```

- [ ] **Step 2: Run selection tests and verify they fail**

Run:

```bash
PYTHONNOUSERSITE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests/test_selection_gating.py -q
```

Expected before implementation: unknown method or missing selection components.

- [ ] **Step 3: Implement TypeAware components and method routing**

In `replenishverifier/experiments/methods.py`, add `"ReplenishVerifier-TypeAware"` to `METHODS` before `"ReplenishVerifier-Full"`.

Add it to `STRUCTURE_AWARE_METHODS`.

Add helpers after `_repair_feedback_count()`:

```python
def _type_aware_validation(row):
    return row.get("type_aware_static_validation") or ((row.get("static_validation") or {}).get("type_aware_static_validation")) or {}


def _type_aware_errors(row):
    direct = row.get("type_aware_static_validation_errors")
    if direct is not None:
        return list(direct or [])
    nested = row.get("static_validation") or {}
    return list(nested.get("type_aware_static_validation_errors") or [])


def _objective_term_coverage(row):
    value = row.get("objective_term_coverage")
    if value is None:
        value = (row.get("objective_term_verification") or {}).get("objective_term_coverage")
    return float(value or 0.0)


def _type_aware_hard_gate_score(row):
    validation = _type_aware_validation(row)
    return float(validation.get("hard_gate_score", 1.0) if validation else 1.0)


def _type_aware_hard_gate_failures(row):
    validation = _type_aware_validation(row)
    return list(validation.get("hard_gate_failures") or [])


def _type_aware_repair_feedback_count(row):
    missing = set(_type_aware_errors(row))
    missing.update(_critical_missing_structures(row))
    return len(missing)


def type_aware_selection_components(row):
    execution = row.get("execution") or {}
    status = str(execution.get("status") or "")
    executable = 1.0 if execution.get("executable") else 0.0
    solver_optimal = 1.0 if status == "Optimal" else 0.0
    structure_completeness = float(row.get("structure_score", ((row.get("structure_verification") or {}).get("structure_score", 0.0))) or 0.0)
    constraint_coverage = _constraint_coverage(row)
    objective_term_coverage = _objective_term_coverage(row)
    hard_gate_score = _type_aware_hard_gate_score(row)
    consensus_score = float(row.get("objective_consensus_score", 0.0) or 0.0)
    repair_feedback_count = float(_type_aware_repair_feedback_count(row))
    runtime_sec = float(row.get("runtime_sec", row.get("total_candidate_evaluation_time", 0.0)) or 0.0)
    return {
        "executable": executable,
        "solver_optimal": solver_optimal,
        "structure_completeness": structure_completeness,
        "constraint_coverage": constraint_coverage,
        "objective_term_coverage": objective_term_coverage,
        "hard_gate_score": hard_gate_score,
        "consensus_score": consensus_score,
        "repair_feedback_count": repair_feedback_count,
        "runtime_sec": runtime_sec,
    }


def type_aware_selection_score(row):
    c = type_aware_selection_components(row)
    return float(
        1000.0 * c["executable"]
        + 500.0 * c["solver_optimal"]
        + 100.0 * c["structure_completeness"]
        + 80.0 * c["constraint_coverage"]
        + 80.0 * c["objective_term_coverage"]
        + 50.0 * c["hard_gate_score"]
        + 30.0 * c["consensus_score"]
        - 5.0 * c["repair_feedback_count"]
        - 0.1 * c["runtime_sec"]
    )
```

In `_method_raw_score()`, add before `ReplenishVerifier-Full` branch:

```python
    if method_name == "ReplenishVerifier-TypeAware":
        return type_aware_selection_score(row)
```

In `_selection_tie_break_key()`, add objective and TypeAware signal before static validation:

```python
        _objective_term_coverage(row),
        _type_aware_hard_gate_score(row),
        -_type_aware_repair_feedback_count(row),
```

In `_annotate_selected_score()`, after `hard_selection_gate`, add:

```python
    if method_name == "ReplenishVerifier-TypeAware":
        best["selection_components"] = type_aware_selection_components(best)
        best["hard_gate_failures"] = _type_aware_hard_gate_failures(best)
        best["hard_gate_score"] = best["selection_components"]["hard_gate_score"]
        best["constraint_coverage"] = best["selection_components"]["constraint_coverage"]
        best["objective_term_coverage"] = best["selection_components"]["objective_term_coverage"]
        best["repair_feedback_count"] = best["selection_components"]["repair_feedback_count"]
```

In `select_for_method()` policy section, add:

```python
        elif method_name == "ReplenishVerifier-TypeAware":
            best["selection_policy"] = "Hard Selection Gate over executable + optimal candidates, ranked by TypeAware no-reference score using structure completeness, constraint coverage, objective-term coverage, type-aware hard gates, candidate objective consensus, repair feedback count, and runtime; no reference objective"
```

- [ ] **Step 4: Run selection tests and verify pass**

Run:

```bash
PYTHONNOUSERSITE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests/test_selection_gating.py -q
```

Expected: all selection tests pass.

---

### Task 4: Wire TypeAware into experiment outputs and repair prompts

**Files:**
- Modify: `replenishverifier/experiments/run_all_methods.py`
- Modify: `replenishverifier/experiments/methods.py`
- Test: `tests/test_strong_baselines.py` or existing method-output tests if assertions exist there.

**Interfaces:**
- Consumes: `METHODS`, `select_for_method()`, `build_structure_aware_repair_prompts()`.
- Produces: `ReplenishVerifier-TypeAware` rows in `main_results`, `ablation_results`, and `low_resource_results`; TypeAware static feedback in repair prompt rows.

- [ ] **Step 1: Inspect method-list tests**

Read `tests/test_strong_baselines.py` and locate any hard-coded method lists. If there are no method-list assertions, add a focused test near existing baseline tests.

- [ ] **Step 2: Add test for method registration**

Add to `tests/test_strong_baselines.py` or `tests/test_selection_gating.py`:

```python
from replenishverifier.experiments.methods import METHODS


def test_type_aware_method_is_registered_for_main_experiments():
    assert "ReplenishVerifier-TypeAware" in METHODS
```

- [ ] **Step 3: Add TypeAware to run_all_methods lists**

In `replenishverifier/experiments/run_all_methods.py`, add `"ReplenishVerifier-TypeAware"` to the ablation method list near `"ReplenishVerifier-Full"`.

In the low-resource method loop, add `"ReplenishVerifier-TypeAware"` near `"ReplenishVerifier-Full"`.

No changes are needed to `main_results` loop if `METHODS` already includes TypeAware.

- [ ] **Step 4: Add TypeAware feedback to structure-aware repair prompt rows**

In `replenishverifier/experiments/methods.py`, inside `build_structure_aware_repair_prompts()` after static validation errors are appended, add:

```python
        type_aware = _type_aware_validation(row)
        type_aware_missing = list(type_aware.get("missing_items") or _type_aware_errors(row))
        type_aware_feedback = list(type_aware.get("repair_feedback") or [])
        if type_aware_missing:
            repair_prompt += "\nType-aware static validation missing items:\n" + "\n".join(f"- {item}" for item in type_aware_missing) + "\n"
        if type_aware_feedback:
            repair_prompt += "\nType-aware repair requirements:\n" + "\n".join(f"- {item}" for item in type_aware_feedback) + "\n"
        if type_aware_missing or type_aware_feedback:
            repair_prompt += "\nReturn only raw Python source code with no Markdown fences or explanations.\n"
```

In `_base_repair_prompt_row()`, add fields:

```python
        "type_aware_static_validation": _type_aware_validation(row),
        "type_aware_static_validation_errors": _type_aware_errors(row),
        "repair_generation_executed": False,
        "is_evaluated_repair_result": False,
```

- [ ] **Step 5: Run focused registration/repair tests**

Run:

```bash
PYTHONNOUSERSITE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests/test_selection_gating.py tests/test_repair_prompt_fairness.py tests/test_strong_baselines.py -q
```

Expected: pass.

---

### Task 5: Strengthen leakage audit for TypeAware

**Files:**
- Modify: `replenishverifier/experiments/audit_leakage.py`
- Test: `tests/test_leakage_audit.py`

**Interfaces:**
- Consumes: output rows from `main_results.jsonl`, including `selection_components` for TypeAware.
- Produces: leakage failures when TypeAware components contain forbidden reference/oracle keys.

- [ ] **Step 1: Write failing leakage audit test**

Append to `tests/test_leakage_audit.py`:

```python
def test_type_aware_selection_components_reject_reference_fields():
    issues = _audit_rows([
        _formal_row(
            method_name="ReplenishVerifier-TypeAware",
            selection_policy="TypeAware score over candidate signals; no reference objective",
            selection_components={
                "executable": 1.0,
                "objective_term_coverage": 1.0,
                "reference_objective": 42.0,
            },
        )
    ], "main_results", require_selected=True)

    assert any("selection_components" in issue and "reference_objective" in issue for issue in issues)


def test_type_aware_allows_candidate_observable_components():
    issues = _audit_rows([
        _formal_row(
            method_name="ReplenishVerifier-TypeAware",
            selection_policy="TypeAware score over candidate static validation, LP structure, objective-term coverage, and consensus; no reference objective",
            selection_components={
                "executable": 1.0,
                "solver_optimal": 1.0,
                "structure_completeness": 1.0,
                "constraint_coverage": 1.0,
                "objective_term_coverage": 1.0,
                "hard_gate_score": 1.0,
                "consensus_score": 0.5,
                "repair_feedback_count": 0.0,
                "runtime_sec": 0.2,
            },
        )
    ], "main_results", require_selected=True)

    assert issues == []
```

- [ ] **Step 2: Run leakage tests and verify they fail**

Run:

```bash
PYTHONNOUSERSITE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests/test_leakage_audit.py -q
```

Expected before implementation: first new test fails because component keys are not inspected.

- [ ] **Step 3: Implement audit guard**

In `replenishverifier/experiments/audit_leakage.py`, add `"ReplenishVerifier-TypeAware"` to `FORMAL_METHODS`.

Add near constants:

```python
FORBIDDEN_SELECTION_COMPONENT_KEYS = {
    "reference_objective",
    "objective_correct",
    "objective_accuracy",
    "objective_score",
    "relative_error",
    "reference_lp",
    "reference_answer",
    "objective_gap",
    "oracle",
    "objective_correct_posthoc",
}
```

In `_audit_rows()`, inside `if method in FORMAL_METHODS:` after policy phrase checks, add:

```python
            components = row.get("selection_components") or {}
            if isinstance(components, dict):
                bad_keys = sorted(set(components) & FORBIDDEN_SELECTION_COMPONENT_KEYS)
                if bad_keys:
                    issues.append(f"{source_name} row {idx} method={method} selection_components contain forbidden reference/oracle keys: {bad_keys}")
```

- [ ] **Step 4: Run leakage tests and verify pass**

Run:

```bash
PYTHONNOUSERSITE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests/test_leakage_audit.py -q
```

Expected: pass.

---

### Task 6: Full verification and lightweight existing-candidate debug run

**Files:**
- Modify if needed: `progress.md`
- No code files should be modified in this task unless tests reveal a real issue.

**Interfaces:**
- Consumes: completed Tasks 1-5.
- Produces: verified test output, `git status`, `git diff --name-only`, and optional debug run output containing `ReplenishVerifier-TypeAware`.

- [ ] **Step 1: Run full pytest with requested environment**

Run:

```bash
PYTHONNOUSERSITE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q
```

Expected: all tests pass. Existing PuLP/Torch warnings may appear; record exact pass/fail summary.

- [ ] **Step 2: Run diff check**

Run:

```bash
git diff --check
```

Expected: no whitespace errors. If Git safe-directory issues occur from the Windows/WSL boundary, report them honestly and do not change global Git config unless the user asks.

- [ ] **Step 3: Run lightweight existing-candidate debug evaluation if candidate files exist**

First inspect candidate files with file tools or a safe listing. If `data/candidates/demo_candidates.jsonl` and `data/generated/test.jsonl` exist, run:

```bash
PYTHONNOUSERSITE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m replenishverifier.experiments.run_all_methods \
  --benchmark data/generated/test.jsonl \
  --candidates data/candidates/demo_candidates.jsonl \
  --out_dir runs/debug_v5_typeaware_existing_candidates \
  --k_values 1,2,4 \
  --timeout 30
```

Expected: command completes and `runs/debug_v5_typeaware_existing_candidates/main_results.jsonl` contains `ReplenishVerifier-TypeAware`. Do not claim improvement; this is only a smoke/debug run on existing candidates.

If those files are absent, skip this step and state which input file was missing.

- [ ] **Step 4: Inspect TypeAware candidate index diagnostics if debug run completed**

If debug run completed, run a small read-only Python summary:

```bash
PYTHONNOUSERSITE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python - <<'PY'
import json
from collections import Counter
path = 'runs/debug_v5_typeaware_existing_candidates/main_results.jsonl'
rows = [json.loads(line) for line in open(path, encoding='utf-8')]
for method in ['Direct', 'Best-of-K', 'Solver-Filter', 'ReplenishVerifier-TypeAware', 'ReplenishVerifier-Full']:
    counts = Counter()
    for row in rows:
        if row.get('method_name') == method:
            cid = str(row.get('candidate_id', ''))
            if '_k' in cid:
                counts['k' + cid.rsplit('_k', 1)[1].split('_', 1)[0]] += 1
            else:
                counts[cid] += 1
    print(method, dict(counts))
PY
```

Expected: summary prints method candidate distribution. Report whether TypeAware selected any non-k0 if candidate IDs encode k indices. If IDs do not encode k, report that this diagnostic is not applicable.

- [ ] **Step 5: Run final status commands required by user**

Run:

```bash
git status --short --branch
```

Then run:

```bash
git diff --name-only
```

Expected: output lists the files modified by this task and any pre-existing unrelated worktree deletion noise. Do not reset or delete pre-existing changes.

- [ ] **Step 6: Update planning files**

Append a concise session entry to `progress.md` describing:

- v5 TypeAware prompt and selection changes;
- static-feedback-only repair scope;
- tests/debug run results;
- no worktree created;
- no real LLM generation run;
- no reference objective or objective correctness used for selection.

- [ ] **Step 7: Final response checklist**

Final response must answer the user's requested 16 items:

1. current directory is `/home/dongaorui/projects/lunwen` or explain path caveat;
2. no worktree created;
3. modified files;
4. new prompt types;
5. TypeAware checklist by problem type;
6. static validation enhancements;
7. whether `ReplenishVerifier-TypeAware` was added;
8. TypeAware score formula;
9. hard gate rules;
10. whether objective-term coverage enters selection;
11. guarantee no reference objective/objective_correct in selection;
12. new tests;
13. pytest result;
14. whether debug run contains TypeAware;
15. whether TypeAware selected non-k0 in diagnostics, or why not applicable;
16. next commands for true v5 generation experiment.

## Self-Review

- Spec coverage: Tasks 1-5 cover prompt, static validation, selection, experiment output/repair prompts, and leakage guard. Task 6 covers verification, debug run, final status, and user-facing summary.
- Placeholder scan: The plan contains no TBD/TODO/fill-later placeholders. Each implementation task has explicit tests, code snippets, commands, and expected outcomes.
- Type consistency: `type_aware_generation_checklist`, `type_aware_static_validation`, `type_aware_static_validation_errors`, `type_aware_selection_components`, and `type_aware_selection_score` are named consistently across tasks.
