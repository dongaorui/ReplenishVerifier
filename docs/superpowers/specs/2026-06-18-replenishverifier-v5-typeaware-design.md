# ReplenishVerifier v5 TypeAware Design

## Scope

Implement a v5 mechanism that gives future candidate pools more problem-type-aware modeling guidance and gives formal selection a stronger no-reference replenishment-structure signal. This change must modify code directly in `/home/dongaorui/projects/lunwen`, must not create or use a git worktree, must not run large LLM generation, and must not improve reported results by using reference objectives or oracle metrics.

This spec implements the static-feedback version of v5 repair support. It does not perform a second LLM repair call. Repair success must not be claimed until repaired candidates are generated and re-evaluated through the standard pipeline.

## Goals

1. Add `type_aware_hidden_verifier` generation prompts.
2. Add problem-type-aware static validation and repair feedback fields.
3. Add a no-reference `ReplenishVerifier-TypeAware` formal selector.
4. Surface objective-term coverage and hard-gate components in selection diagnostics.
5. Strengthen leakage guards and tests so TypeAware selection cannot use reference objective, objective correctness, reference LP, or oracle gaps.

## Non-goals

- Do not run Qwen3-8B or any other real LLM generation in this implementation step.
- Do not fabricate experiments or modify evaluation metrics to make ReplenishVerifier look better.
- Do not implement a true closed-loop LLM repair/resampling call in v5 static-feedback mode.
- Do not remove or break legacy methods or output fields.

## Prompt design

Add `type_aware_hidden_verifier` to `PROMPT_TYPES` in `replenishverifier/llm/prompt_builder.py` and to the `run_generation.py --prompt_type` choices.

The prompt remains hidden-verifier style: it does not expose raw `expected_structures` JSON, reference objectives, reference LPs, or reference answers. It injects a natural-language checklist derived from `problem_type`:

- `single_period_newsvendor`: order quantity, overage/underage or demand-scenario representation, objective terms for ordering/purchase plus overage/holding and underage/shortage where applicable.
- `single_item_multi_period`: period-indexed order and inventory variables, inventory balance across periods, ordering and holding cost objective terms.
- `single_item_multi_period_shortage`: period-indexed order, inventory, and shortage/unmet-demand variables; inventory/shortage balance; shortage penalty objective term.
- `multi_item_capacity`: item-period order/inventory variables, item-wise inventory balances, per-period capacity/resource constraints, ordering and holding objective terms.
- `fixed_order_cost_big_m`: period-indexed order/inventory variables, binary order/setup variables, Big-M linking constraints, fixed-order cost objective term, inventory balance.

Default generation should move to `type_aware_hidden_verifier` for v5 while preserving `hidden_verifier`, `plain`, and `structured` for compatibility.

## Static validation design

Extend `replenishverifier/pipeline/quality_signals.py` with problem-type-aware validation. The existing `compute_static_validation()` result remains backward-compatible and gains additional fields:

- `type_aware_static_validation`: nested dict with problem type, checklist items, passed items, missing items, score, repair feedback, and evidence booleans.
- `type_aware_static_validation_score`: numeric score in `[0, 1]`.
- `type_aware_static_validation_errors`: list of machine-readable missing-item IDs.
- Compatibility booleans or error IDs for missing inventory balance, capacity constraints, shortage variables/cost terms, fixed-order binary variables, Big-M linking, fixed-order cost terms, and objective terms.

Validation uses generated code text and AST/pattern heuristics only. It does not use reference objective, objective correctness, objective gap, reference LP, or reference answer. It may use `problem_type` because this is benchmark metadata already used by the verifier schema and prompt routing.

## Selection design

Add `ReplenishVerifier-TypeAware` to `METHODS`, ablation/low-resource method lists, and leakage audit formal methods.

The selector uses this no-reference raw score before the existing executable + optimal hard selection gate:

```text
score =
  1000 * executable
+ 500  * solver_optimal
+ 100  * structure_completeness
+ 80   * constraint_coverage
+ 80   * objective_term_coverage
+ 50   * hard_gate_score
+ 30   * consensus_score
- 5    * repair_feedback_count
- 0.1  * runtime_sec
```

Components:

- `executable`: candidate execution flag.
- `solver_optimal`: solver status normalized to Optimal.
- `structure_completeness`: LP structure score.
- `constraint_coverage`: required replenishment structure coverage from LP verification.
- `objective_term_coverage`: heuristic objective term coverage from generated code / LP signals.
- `hard_gate_score`: fraction of problem-type hard gates passed.
- `consensus_score`: candidate-objective consensus within the same problem.
- `repair_feedback_count`: number of type-aware static validation errors plus missing required structures.
- `runtime_sec`: candidate evaluation runtime.

The selected row should include `selection_components`, `hard_gate_failures`, `hard_gate_score`, `constraint_coverage`, `objective_term_coverage`, `repair_feedback_count`, and `uses_reference_objective_for_selection=False`.

## Hard-gate design

TypeAware hard gates are represented as explainable components, not oracle filters. They are based on problem type and candidate-observable evidence:

- All multi-period replenishment types: inventory balance evidence.
- `multi_item_capacity`: capacity constraint evidence.
- `single_item_multi_period_shortage`: shortage variable evidence and shortage cost/objective evidence.
- `fixed_order_cost_big_m`: binary order/setup evidence, Big-M linking evidence, and fixed-order cost/objective evidence.

A failed gate lowers the TypeAware score through `hard_gate_score` and appears in `hard_gate_failures`. The global executable + optimal hard selection gate still controls whether a candidate receives non-zero formal selection score by default.

## Repair prompt design

Do not implement real second-call repair in this step. Instead, structure-aware repair prompt rows should include static validation and TypeAware missing-item feedback so a later `run_repair_generation.py` call can use it.

Repair prompts should contain:

1. problem ID / statement / parameters via existing repair prompt builders;
2. original code;
3. static validation errors;
4. TypeAware missing checklist items;
5. explicit instruction to fix missing capacity, shortage, Big-M, fixed-order, inventory-balance, or objective-term items when present;
6. instruction that final output must be raw Python code.

Rows should clearly indicate this is prompt/feedback generation only, not evaluated repair success.

## Leakage guard design

Update leakage audit/tests so `ReplenishVerifier-TypeAware` is a formal method and must satisfy:

- `uses_reference_objective_for_selection is False`.
- selection policy states no reference objective.
- objective-correctness and oracle fields, if present, are post-hoc diagnostics only.
- TypeAware selection components do not include `reference_objective`, `objective_correct`, `relative_error`, `reference_lp`, or reference answer fields.

## Testing design

Add or update tests for:

- prompt type acceptance and content for `type_aware_hidden_verifier`;
- no raw expected-structures JSON in TypeAware hidden prompt;
- static validation missing capacity / shortage / fixed-order Big-M / fixed cost / inventory balance items;
- TypeAware score components and tie-breaking can select a non-k0 candidate in constructed no-reference cases;
- `run_all_methods` includes `ReplenishVerifier-TypeAware` without breaking old output fields;
- leakage audit includes TypeAware and rejects forbidden selection components or policy wording.

Verification command:

```bash
PYTHONNOUSERSITE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q
```

After tests, run a lightweight existing-candidate debug evaluation only if suitable local candidate files are present. Do not run real LLM generation.
