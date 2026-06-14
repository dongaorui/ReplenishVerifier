# ReplenishVerifier

`ReplenishVerifier` 是一个面向论文原型的 Python 研究代码框架，用于：

> LP-Structure-Grounded Process Supervision for LLM-based Replenishment Optimization Modeling  
> 面向库存补货优化的大语言模型结构验证增强过程监督方法

核心思想：现有 LLM-for-OR 方法通常只检查 solver code 是否可执行、是否可行、目标值是否正确；本项目进一步解析 PuLP 导出的 `.lp` 文件，检查库存补货优化模型中的领域结构是否完整，例如库存平衡、订货变量、缺货变量、容量约束、固定订货成本、binary 订货变量、Big-M 连接约束等。

## 1. 功能

当前最小闭环支持：

1. 生成 ReplenishmentOR 风格 benchmark。
2. 生成 reference PuLP/CBC 模型代码。
3. 求解 reference 模型并导出 `.lp`。
4. 解析 `.lp` 文件结构。
5. 根据 expected structures 执行补货语义结构验证。
6. 为 LLM 生成自然语言修复反馈。
7. 对 LLM candidate code 执行、验证、打分、Best-of-K 选择。
8. 统计实验指标。

## 2. 支持的补货问题类型

| problem_type | 说明 |
|---|---|
| `single_period_newsvendor` | 单品单周期，有订货量、剩余库存、缺货变量、持有成本、缺货成本 |
| `single_item_multi_period` | 单品多周期，有库存平衡、订货量、持有成本 |
| `single_item_multi_period_shortage` | 单品多周期，允许缺货，有缺货变量和缺货惩罚 |
| `multi_item_capacity` | 多品多周期，有库存平衡和容量约束 |
| `fixed_order_cost_big_m` | 多周期固定订货成本，有 binary 订货触发变量和 Big-M 约束 |

## 3. 安装

```bash
python -m pip install -r requirements.txt
```

推荐 Python 3.10+。

## 4. 生成 benchmark

```bash
python scripts/generate_benchmark.py \
  --output data/benchmark.jsonl \
  --lp-dir outputs/reference_lp \
  --n-per-type 20 \
  --seed 42
```

每条样本包含：

```json
{
  "id": "string",
  "difficulty": "easy|medium|hard|expert",
  "problem_type": "string",
  "natural_language": "string",
  "parameters": {},
  "expected_structures": {},
  "reference_code": "string",
  "reference_objective": 0.0,
  "reference_status": "Optimal",
  "reference_lp_path": "outputs/reference_lp/xxx.lp"
}
```

## 5. 验证 reference LP 结构

```bash
python scripts/run_structure_verification.py \
  --benchmark data/benchmark.jsonl \
  --out outputs/structure_check.jsonl
```

## 6. 候选选择

candidate JSONL 格式：

```json
{
  "problem_id": "sample_id",
  "candidate_id": "cand_0",
  "method": "direct",
  "generated_text": "modeling trace",
  "generated_code": "import pulp ... def build_model(): ..."
}
```

候选代码建议暴露：

```python
def build_model():
    ...
    return model
```

运行：

```bash
python scripts/run_candidate_selection.py \
  --benchmark data/benchmark.jsonl \
  --candidates examples/candidates.jsonl \
  --out outputs/selection.jsonl \
  --work-dir outputs/candidate_runs
```

## 7. 统计结果

```bash
python scripts/evaluate_results.py --results outputs/selection.jsonl
```

主要指标：

- executable rate
- feasible / optimal rate
- objective accuracy
- average structure completeness
- per-structure coverage
- selected candidate score

## 8. Run Experiments

本项目已实现 CCF-B 论文实验所需的主实验、消融实验和低资源分析。支持的方法包括：

- `Direct`：直接选择每个问题的第一个 candidate。
- `Best-of-K`：选择第一个可执行候选；若没有可执行候选，则选择第一个。
- `Solver-Filter`：只使用 executable、Optimal、objective accuracy 排序。
- `Structure-Only`：只使用 LP 结构完整性排序。
- `ReplenishVerifier-Full`：使用 executable + feasibility + objective + LP structure + semantic consistency 完整得分。
- `ReplenishVerifier-Repair`：选择 Full 最优候选，并为缺失结构生成 repair prompt。

候选文件为空时，脚本默认会自动生成 CPU 可跑的 demo candidates，便于验证实验流程：

```bash
python -m replenish.experiments.run_all_methods \
  --benchmark data/benchmark.jsonl \
  --candidates data/candidates/example_candidates.jsonl \
  --out_dir runs/exp_demo \
  --k_values 1,2,4 \
  --timeout 30
```

输出包括 JSONL、CSV、Markdown 三种格式：

```text
runs/exp_demo/candidate_evaluations.{jsonl,csv,md}
runs/exp_demo/main_results.{jsonl,csv,md}
runs/exp_demo/ablation_results.{jsonl,csv,md}
runs/exp_demo/low_resource_results.{jsonl,csv,md}
runs/exp_demo/difficulty_results.{jsonl,csv,md}
runs/exp_demo/benchmark_summary.{jsonl,csv,md}
runs/exp_demo/repair_prompts.{jsonl,csv,md}
```

生成论文表格：

```bash
python -m replenish.experiments.build_paper_tables \
  --exp_dir runs/exp_demo \
  --out_dir runs/paper_tables
```

会生成：

```text
runs/paper_tables/table1_benchmark.md
runs/paper_tables/table2_main.md
runs/paper_tables/table3_ablation.md
runs/paper_tables/table4_low_resource.md
runs/paper_tables/table5_difficulty.md
```

主要指标：

- Executable Rate
- Feasible/Optimal Rate
- Objective Accuracy
- Structure Completeness
- Inventory Balance Accuracy
- Constraint Coverage
- Average Runtime
- Average Repair Feedback Count

## 9. Real LLM Experiment

正式论文实验中，candidate selection 阶段不能使用 `reference_objective` 作为选择依据。当前实现中：

- `Solver-Filter` 只使用 candidate 自身的 executable、solver status 是否 Optimal、是否返回 objective；
- `ReplenishVerifier-Full` 只使用 executable、Optimal、LP structure completeness、semantic consistency；
- objective accuracy 只在选择完成后用于 reporting，不参与 formal selection score。

### 9.1 生成 50 条测试数据

```bash
python scripts/generate_benchmark.py \
  --output data/generated/test_50.jsonl \
  --lp-dir runs/lp/test_50 \
  --n-per-type 10 \
  --seed 42
```

### 9.2 用 Qwen3-8B 生成 K=4 candidates

先安装 LLM 推理依赖：

```bash
python -m pip install torch transformers accelerate
```

然后运行：

```bash
python -m replenish.llm.run_generation \
  --benchmark data/generated/test_50.jsonl \
  --out data/candidates/qwen3_8b_k4_50.jsonl \
  --model Qwen/Qwen3-8B \
  --k 4 \
  --max_new_tokens 2048 \
  --temperature 0.2 \
  --top_p 0.95 \
  --trust_remote_code
```

如果你已经把模型下载到本地，也可以把 `--model` 改成本地路径。

生成器会保存：

- `generated_text`：模型原始输出；
- `generated_code`：从 markdown python 代码块或 `import pulp` / `pulp.LpProblem` 附近提取出的 Python 代码；
- `error`：生成失败时记录错误，不中断整个流程。

### 9.3 跑所有方法

```bash
python -m replenish.experiments.run_all_methods \
  --benchmark data/generated/test_50.jsonl \
  --candidates data/candidates/qwen3_8b_k4_50.jsonl \
  --out_dir runs/qwen3_8b_k4_50 \
  --k_values 1,2,4 \
  --timeout 30
```

### 9.4 生成论文表格

```bash
python -m replenish.experiments.build_paper_tables \
  --exp_dir runs/qwen3_8b_k4_50 \
  --out_dir runs/paper_tables
```

### 9.5 检查 objective leakage

```bash
python -m replenish.experiments.audit_leakage \
  --exp_dir runs/qwen3_8b_k4_50
```

### 9.6 公平比较方式

- `Direct`：按 candidate 顺序选择第一个候选，不看 solver、不看结构、不看 reference objective。
- `Best-of-K`：选择第一个可执行候选，不看结构、不看 reference objective。
- `Solver-Filter`：使用 candidate 自身的执行状态和 solver status，不看 reference objective。
- `SIRL-like LP-Stats`：模拟 solver + generic LP artifact feedback，只使用 LP 是否导出、objective/constraint section 是否存在、变量/约束/binary/bounds 数量等通用统计，不使用补货语义。
- `OptArgus-like Audit`：模拟通用 hallucination / structural consistency auditing，只检查 objective、variables、constraints、empty model、可疑变量名、boundedness 等通用问题，不使用补货语义。
- `OptiRepair-like Repair-Prompt`：模拟通用 optimization repair prompt，基于执行错误和 generic audit issue 生成通用修复建议，不检查 inventory balance / Big-M 等补货结构。
- `ReplenishVerifier-Full`：使用 solver execution + replenishment-specific LP structure verification + semantic consistency，不看 reference objective。

强 baseline 的目的，是证明 ReplenishVerifier 的收益来自 replenishment-specific LP structure supervision，而不是普通 solver-in-the-loop、generic LP artifact feedback、generic hallucination auditing 或普通 repair prompt。

错误类型分析：

```bash
python -m replenishverifier.experiments.analyze_error_types \
  --exp_dir runs/qwen3_8b_k4_50
```

案例抽取：

```bash
python -m replenishverifier.experiments.extract_case_studies \
  --exp_dir runs/qwen3_8b_k4_50
```

生成包含强 baseline、错误类型和案例分析的论文表格：

```bash
python -m replenishverifier.experiments.build_paper_tables \
  --exp_dir runs/qwen3_8b_k4_50 \
  --out_dir runs/paper_tables_strong_baselines
```

`reference_objective` 仅用于最终报告 `objective_accuracy`，不用于正式候选选择。

## 10. 后续如何接入 LLM

你可以用任意 LLM 生成候选代码，保存成 candidate JSONL。推荐实验设置：

- Direct
- CoT
- Best-of-K
- Solver-filter
- Self-repair
- ReplenishVerifier selection
- ReplenishVerifier + DPO

DPO 数据构造方式：

1. 对同一问题生成 K 个候选。
2. 对每个候选执行 solver + LP structure verification。
3. 按综合分排序。
4. 构造 `chosen > rejected` 偏好对。
5. 使用 LoRA/DPO 微调 Qwen2.5-3B/7B 或 Qwen3-8B。

## 11. 安全说明

`solver/code_executor.py` 会执行候选 Python 代码。该原型默认用于本地可信研究代码。若接入外部 LLM 或不可信用户输入，应使用 Docker、firejail、nsjail 等沙箱。
