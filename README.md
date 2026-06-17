# ReplenishVerifier

> **ReplenishVerifier: Constraint-Level LP-Structure Verification for LLM-Based Supply Chain Replenishment Optimization Modeling**  
> **ReplenishVerifier：面向大语言模型供应链补货优化自动建模的约束级 LP 结构验证方法**

ReplenishVerifier is a research prototype for auditing LLM-generated optimization models in **supply chain replenishment**. It targets a concrete failure mode: generated PuLP/Python code can be executable, return solver status `Optimal`, and even agree with other candidates on objective values, while still omitting required replenishment structures such as inventory balance, capacity constraints, shortage/backlog variables, fixed ordering cost, binary setup/order triggers, or Big-M linking constraints.

The core thesis is:

> Correct optimization modeling requires constraint-level semantic structure, not only executable solver code or objective-value consensus. ReplenishVerifier verifies these structures from the LP artifact induced by generated code and uses the evidence for no-reference candidate selection, feedback, repair prompting, and future preference-data construction.

Formal candidate selection **must not use `reference_objective`**. Reference objectives are evaluation-only and may be used only after selection for metrics such as objective accuracy and relative error.

---

## What the current code implements

The repository currently supports the following pipeline:

1. Generate replenishment benchmark rows with natural-language prompts, sampled parameters, reference PuLP models, and replenishment-specific semantic metadata.
2. Execute LLM-generated PuLP candidates and export their induced `.lp` artifacts.
3. Parse LP artifact sections: objective, constraints, variable names, binary declarations, and bounds.
4. Check problem-type-aware required / optional replenishment structures.
5. Emit rule-level structure certificates with evidence, missing reasons, and repair hints.
6. Select candidates using no-reference policies.
7. Build generic or replenishment-specific repair prompts.
8. Build verifier-guided preference pairs for future training data.

The project is **not** a general LLM-for-OR agent, not a complete mathematical-equivalence checker, not a faithful reproduction of SIRL / OR-R1 / OptArgus / OptiRepair, and not an already completed DPO/RL training system.

All `*-like` methods are **lightweight signal-isolation baselines**. They are included to isolate whether generic execution, LP statistics, objective consensus, audit, or repair-prompt signals explain the gains; they are not faithful reproductions of the original systems.

---

## Repository layout

```text
replenishverifier/
  benchmark/            # schemas, templates, generator, semantic benchmark fields
  data/                 # problem-type-aware replenishment structure schema
  solver/               # PuLP runner and generated-code executor
  verifier/             # LP parser, LP graph evidence, structure rules, feedback
  pipeline/             # scoring utilities
  experiments/          # method selection, baselines, evaluation, tables, audits
  llm/                  # prompt building, code extraction, generation, repair generation

scripts/                # lightweight CLI entry points
papers/                 # Chinese and English paper drafts
docs/                   # experiment plans, risk audits, revision roadmap
runs/                   # smoke/demo and future real experiment outputs
data/generated/         # generated benchmark splits
data/candidates/        # candidate JSONL files
```

---

## Benchmark schema and generated fields

Supported problem types:

| problem_type | Required replenishment semantics |
|---|---|
| `single_period_newsvendor` | demand satisfaction, order quantity, ending inventory, shortage variable, ordering / holding / shortage costs |
| `single_item_multi_period` | period-indexed orders and inventory, inventory balance, ordering and holding costs |
| `single_item_multi_period_shortage` | inventory balance with shortage/backlog variables and shortage penalty |
| `multi_item_capacity` | item and period sets, item volume, shared storage capacity, per-period capacity constraints |
| `fixed_order_cost_big_m` | binary order trigger, fixed ordering cost, and Big-M linking constraint |

Generated benchmark rows now include replenishment-specific fields:

- `semantic_frame`: domain-specific frame with sets, parameters, decision variables, objective terms, constraints, solver type, replenishment structures, required structures, and optional structures.
- `replenishment_entities`: extracted replenishment entities such as demand, initial inventory, periods, items, order quantity, inventory level, shortage/backlog, costs, storage capacity, item volume, Big-M, and lead time when present.
- `replenishment_modeling_steps`: deterministic LP-structure-grounded steps for labeled benchmark rows. Unlabeled prompt rows omit this field by default to avoid leaking the modeling process.

The generator validates each row with lightweight rules and raises `ValueError` on malformed rows. It does not call an LLM during validation.

---

## Problem-type-aware structure schema

`replenishverifier/data/structure_schema.py` defines `EXPECTED_STRUCTURES_BY_TYPE`. Each problem type has:

- `required`: structures included in the main structure score;
- `optional`: structures reported in certificates but excluded from the main score denominator;
- `forbidden`: explicit metadata reserved for future diagnostics.

Current structure keys include inventory balance, order variables, inventory variables, shortage variables, capacity constraints, binary order variables, Big-M constraints, lead time, order cost, holding cost, shortage cost, fixed order cost, demand satisfaction, nonnegative bounds, and objective minimization.

If a benchmark instance has truthy `expected_structures`, those keys override the default required set for that instance. Otherwise the problem-type schema is used as fallback.

---

## Method and selection policies

Core ReplenishVerifier scoring uses candidate-observable signals only:

```text
0.25 executable
+ 0.25 optimal solver status
+ 0.35 required replenishment structure score
+ 0.15 semantic consistency
```

The hard selection gate gives non-zero formal selection score only to executable + `Optimal` candidates by default. Structure certificates are still retained for failed candidates for diagnosis and repair.

Implemented methods include:

- `Direct`
- `Best-of-K`
- `Solver-Filter`
- `OR-R1-like Voting` — lightweight executable / valid-code / objective-consensus baseline; no replenishment structures; no reference objective.
- `SIRL-like LP-Stats` — lightweight generic LP-artifact statistics baseline; no replenishment structures.
- `OptArgus-like Audit` — lightweight generic optimization-model audit baseline; no inventory-specific checks.
- `OptiRepair-like Repair-Prompt` — lightweight generic repair-readiness / feedback baseline; no replenishment-specific feedback.
- `Structure-Only`
- `Structure-Grounded Consistency` — ReplenishVerifier-style selector using execution, solver status, LP artifact structure coverage, required replenishment structures, and candidate objective consensus; no reference objective.
- `ReplenishVerifier-Full`
- `ReplenishVerifier-Repair` — should be reported as actual repair only after real repaired candidates are generated and re-evaluated.

`--use_objective_consensus` is optional and uses only candidate-objective clustering within the same problem. It never uses `reference_objective` and should be treated as an appendix ablation unless explicitly made part of the final method.

---

## Pre-experiment protocol safeguards

Candidate generation supports `--prompt_type hidden_verifier|plain|structured`.

- `hidden_verifier` is the recommended main-experiment setting. It hides `expected_structures`, keeps the PuLP solve/export contract, and asks for clear variable/constraint names without exposing required replenishment structure labels.
- `plain` hides `expected_structures` and gives the natural-language problem plus JSON parameters. Parameters are provided so generated PuLP code can build an executable instance model.
- `structured` exposes expected structures and is only for guided generation or appendix ablations. It must not be used as the default main-experiment prompt.

Generation rows should save raw generations, `prompt_type`, seed, decoding parameters, and model path/version/hash where available. Seeds improve reproducibility, but exact determinism is not guaranteed across GPU sampling, Transformers backends, CUDA kernels, hardware, or model versions.

`run_all_methods` writes both structure-aware `repair_prompts.*` and generic `generic_repair_prompts.*`. Generic repair uses execution/solver/audit feedback only and intentionally avoids replenishment-specific missing-structure labels. Structure-aware repair may use missing required structures, rule certificates, and replenishment repair hints.

Runtime overhead is a required future reporting metric. Use `python -m replenishverifier.experiments.analyze_runtime_overhead --exp_dir <exp_dir>` after an evaluation run to summarize total candidate evaluation time, LP parse time, and structure-check time. Missing timing fields are reported as `NA`; no runtime numbers should be invented before real experiments.

Variable-renaming robustness uses `rename_variables_for_robustness.py` as a lightweight text-level perturbation. It is not AST-safe renaming and should be manually spot-checked before formal experiments.

Preference pairs exported by `build_preference_data.py` are future DPO/PRM/LoRA-style learning signals. They do not imply that any SFT, DPO, PRM, RL, LoRA, or TGRPO training has been completed. Formal selection and preference construction do not use `reference_objective`; reference objectives are evaluation-only.

---

## Installation and tests

Python 3.10+ is expected.

```bash
python -m pip install -r requirements.txt
python -m pytest
```

If running local LLM generation or repair generation, install the required model stack separately, e.g. `torch`, `transformers`, and `accelerate`. Real LLM generation is intentionally not required for the unit tests.

---

## Benchmark generation

Labeled benchmark split:

```bash
python scripts/generate_benchmark.py \
  --output data/generated/test_50.jsonl \
  --lp-dir runs/lp/test_50 \
  --n-per-type 10 \
  --seed 42
```

Unlabeled prompt-only rows:

```bash
python scripts/generate_benchmark.py \
  --output data/generated/prompts_50.jsonl \
  --n-per-type 10 \
  --seed 42 \
  --unlabeled
```

Unlabeled rows omit `reference_code`, `reference_objective`, and `expected_structures`. They also omit `replenishment_modeling_steps` by default. Use `--include-modeling-steps` only for explicit process-supervision data export.

The parameter RNG and language-template RNG are separated; language template selection does not affect sampled parameters or reference objectives.

---

## Real LLM experiment workflow

Do **not** use smoke/demo runs as main paper evidence. Main claims require real LLM candidates.

Example generation command, to be run only when real experiments are intended:

```bash
python -m replenishverifier.llm.run_generation \
  --benchmark data/generated/test_50.jsonl \
  --out data/candidates/qwen3_8b_k4_50.jsonl \
  --model Qwen/Qwen3-8B \
  --k 4 \
  --max_new_tokens 2048 \
  --temperature 0.2 \
  --top_p 0.95 \
  --prompt_type hidden_verifier \
  --seed 42 \
  --trust_remote_code
```

Evaluation workflow after real candidates exist:

```bash
python -m replenishverifier.experiments.run_all_methods \
  --benchmark data/generated/test_50.jsonl \
  --candidates data/candidates/qwen3_8b_k4_50.jsonl \
  --out_dir runs/qwen3_8b_k4_50 \
  --k_values 1,2,4 \
  --timeout 30

python -m replenishverifier.experiments.analyze_error_types --exp_dir runs/qwen3_8b_k4_50
python -m replenishverifier.experiments.extract_case_studies --exp_dir runs/qwen3_8b_k4_50
python -m replenishverifier.experiments.build_paper_tables \
  --exp_dir runs/qwen3_8b_k4_50 \
  --out_dir runs/paper_tables_qwen3_8b_k4_50
python -m replenishverifier.experiments.audit_leakage \
  --exp_dir runs/qwen3_8b_k4_50 \
  --write_report
```

The leakage audit must pass before results are used in the paper.

---

## Repair and preference data

Repair prompts are generated from missing required structures. Actual repair claims require a second LLM generation pass and re-evaluation:

```bash
python -m replenishverifier.llm.run_repair_generation \
  --benchmark data/generated/test_50.jsonl \
  --repair_prompts runs/qwen3_8b_k4_50/repair_prompts.jsonl \
  --candidates data/candidates/qwen3_8b_k4_50.jsonl \
  --out data/candidates/qwen3_8b_k4_50_repaired.jsonl \
  --model Qwen/Qwen3-8B \
  --max_new_tokens 2048 \
  --temperature 0.2 \
  --top_p 0.95 \
  --trust_remote_code
```

If this step is not run and evaluated, write only “repair prompt generation,” not “repair result.”

Verifier-guided preference pairs can be built for future DPO / PRM / reranker experiments:

```bash
python -m replenishverifier.experiments.build_preference_data \
  --exp_dir runs/qwen3_8b_k4_50 \
  --out runs/qwen3_8b_k4_50/preference_pairs.jsonl \
  --min_score_gap 0.10 \
  --max_pairs_per_problem 3
```

Preference data is future training data; it is not evidence that DPO, PRM, or RL training has already been completed.

---

## Synthetic smoke tests

Synthetic/demo smoke tests are allowed only for checking that the pipeline runs end to end. They must not be reported as main empirical results.

Existing smoke outputs under `runs/smoke_*` and `runs/paper_tables_*` are sanity-check artifacts. Any main-table value in a paper draft must remain:

```text
[TO FILL AFTER REAL LLM EXPERIMENT]
```

until real LLM experiments are completed and audited.

---

## Known limitations

- The LP parser depends on PuLP LP format.
- Structure verification is heuristic and is not full mathematical-equivalence verification.
- The verifier may miss coefficient errors, index errors, boundary-condition errors, or invalid Big-M magnitudes.
- The benchmark currently covers only a small set of replenishment model families.
- Selection weights are hand-designed and should later be learned or calibrated.
- Repair effectiveness requires real repaired LLM candidates and re-evaluation.
- Preference pairs do not imply completed DPO / PRM / RL training.
- All `*-like` baselines are lightweight signal-isolation baselines, not faithful reproductions.
- Executing external generated code is risky; untrusted candidates should be run in a sandbox.

---

## Documentation for submission preparation

- `docs/ccfa_revision_roadmap.md` — roadmap for moving from current prototype to a stronger submission.
- `docs/submit_readiness_checklist.md` — code, documentation, real LLM experiment, paper, and CCF-A risk checklist.
- `docs/real_llm_experiment_checklist.md` — real experiment protocol.
- `docs/paper_experiment_revision_plan.md` — paper table and baseline design plan.
- `docs/code_and_claim_risk_audit.md` — code/claim consistency and leakage-risk audit.
