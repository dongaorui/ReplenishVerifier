from pathlib import Path

from replenishverifier.utils.io import read_jsonl, write_jsonl


VALID_CODE = """import pulp


def build_model():
    prob = pulp.LpProblem('x', pulp.LpMinimize)
    x = pulp.LpVariable('x', lowBound=0)
    prob += x, 'total_cost'
    prob += x >= 1, 'constraint_0'
    return prob
"""


REPAIRED_CODE = """import pulp


def build_model():
    prob = pulp.LpProblem('repaired', pulp.LpMinimize)
    x = pulp.LpVariable('x_repaired', lowBound=0)
    prob += x, 'total_cost'
    prob += x >= 2, 'constraint_repaired'
    return prob
"""


def _candidate(cid, *, executable=True, status="Optimal", code=VALID_CODE, extra=None):
    row = {
        "problem_id": "p0",
        "candidate_id": cid,
        "candidate_index": int(cid.replace("c", "")),
        "k": 2,
        "generated_text": code,
        "generated_code": code,
        "prompt_type": "type_aware_hidden_verifier",
        "execution": {"executable": executable, "status": status, "objective": 1.0 if executable else None},
        "code_output_format_valid": executable,
        "static_validation_errors": [] if executable else ["syntax_error"],
        "structure_verification": {"missing": [], "structure_score": 1.0},
        "objective_term_coverage": 1.0,
        "objective_term_lp_coefficient_coverage": 1.0,
        "lp_stats": {"lp_exported": executable, "objective_present": executable, "constraints_count": 1 if executable else 0, "variables_count": 1 if executable else 0},
    }
    if extra:
        row.update(extra)
    return row


def _benchmark_path(tmp_path):
    path = tmp_path / "benchmark.jsonl"
    write_jsonl(path, [{"id": "p0", "problem_type": "multi_item_capacity", "natural_language": "x", "parameters": {}}])
    return path


def test_policy_has_no_reference_leakage_in_prompts_and_outputs(tmp_path):
    from replenishverifier.llm.nonreference_repair_policy import run_nonreference_repair_policy

    candidates_path = tmp_path / "candidates.jsonl"
    out_path = tmp_path / "out.jsonl"
    write_jsonl(candidates_path, [
        _candidate("c0", executable=False, status="Error", code="def broken(: pass", extra={
            "reference_objective": 1.0,
            "relative_error": 0.0,
            "oracle_note": "do not copy",
        })
    ])

    captured = {}

    def fake_engine(**kwargs):
        prompts = read_jsonl(kwargs["repair_prompts_path"])
        captured["prompts"] = prompts
        rows = [{
            "problem_id": "p0",
            "candidate_id": "generic_repair_c0",
            "source_candidate_id": "c0",
            "generated_text": REPAIRED_CODE,
            "generated_code": REPAIRED_CODE,
            "repair_type": "generic",
            "prompt": "non-reference prompt",
            "error": None,
        }]
        write_jsonl(kwargs["out_path"], rows)
        return rows

    rows = run_nonreference_repair_policy(
        benchmark_path=_benchmark_path(tmp_path),
        candidates_path=candidates_path,
        out_path=out_path,
        model_name_or_path="fake-model",
        repair_engine=fake_engine,
    )

    forbidden = {"reference_objective", "relative_error", "oracle", "objective_correct", "reference_lp", "reference_answer"}
    prompt_text = "\n".join(row.get("repair_prompt", "") + row.get("feedback", "") for row in captured["prompts"])
    output_text = "\n".join(str(row) for row in rows)
    for token in forbidden:
        assert token not in prompt_text
        assert token not in output_text
    assert rows[0]["uses_reference_objective_for_repair"] is False


def test_clean_candidates_are_untouched_and_output_length_is_preserved(tmp_path):
    from replenishverifier.llm.nonreference_repair_policy import run_nonreference_repair_policy

    clean = _candidate("c0")
    failed = _candidate("c1", executable=False, status="Error", code="def broken(: pass")
    candidates_path = tmp_path / "candidates.jsonl"
    out_path = tmp_path / "out.jsonl"
    write_jsonl(candidates_path, [clean, failed])

    def fake_engine(**kwargs):
        write_jsonl(kwargs["out_path"], [{
            "problem_id": "p0",
            "candidate_id": "generic_repair_c1",
            "source_candidate_id": "c1",
            "generated_text": REPAIRED_CODE,
            "generated_code": REPAIRED_CODE,
            "repair_type": "generic",
            "error": None,
        }])
        return read_jsonl(kwargs["out_path"])

    rows = run_nonreference_repair_policy(
        benchmark_path=_benchmark_path(tmp_path),
        candidates_path=candidates_path,
        out_path=out_path,
        model_name_or_path="fake-model",
        repair_engine=fake_engine,
    )

    assert len(rows) == 2
    assert rows[0] == clean
    assert rows[1]["candidate_id"] == "c1"
    assert rows[1]["source_repair_candidate_id"] == "generic_repair_c1"
    assert rows[1]["generated_code"] == REPAIRED_CODE
    assert rows[1]["non_reference_policy_repaired"] is True
    assert read_jsonl(out_path) == rows


def test_failed_candidates_are_repaired_and_id_alignment_is_preserved(tmp_path):
    from replenishverifier.llm.nonreference_repair_policy import run_nonreference_repair_policy

    failed = _candidate("c0", executable=True, status="Infeasible", code=VALID_CODE)
    candidates_path = tmp_path / "candidates.jsonl"
    out_path = tmp_path / "out.jsonl"
    write_jsonl(candidates_path, [failed])

    def fake_engine(**kwargs):
        write_jsonl(kwargs["out_path"], [{
            "problem_id": "p0",
            "candidate_id": "generic_repair_c0",
            "source_candidate_id": "c0",
            "generated_text": REPAIRED_CODE,
            "generated_code": REPAIRED_CODE,
            "repair_type": "generic",
            "error": None,
        }])
        return read_jsonl(kwargs["out_path"])

    rows = run_nonreference_repair_policy(
        benchmark_path=_benchmark_path(tmp_path),
        candidates_path=candidates_path,
        out_path=out_path,
        model_name_or_path="fake-model",
        repair_engine=fake_engine,
    )

    assert rows[0]["problem_id"] == failed["problem_id"]
    assert rows[0]["candidate_id"] == failed["candidate_id"]
    assert rows[0]["candidate_index"] == failed["candidate_index"]
    assert rows[0]["k"] == failed["k"]
    assert rows[0]["generated_code"] == REPAIRED_CODE
    assert rows[0]["requires_re_evaluation"] is True


def test_policy_is_deterministic_with_mocked_repair_engine(tmp_path):
    from replenishverifier.llm.nonreference_repair_policy import run_nonreference_repair_policy

    candidates_path = tmp_path / "candidates.jsonl"
    write_jsonl(candidates_path, [
        _candidate("c0", executable=False, status="Error", code="broken"),
        _candidate("c1"),
    ])

    def fake_engine(**kwargs):
        write_jsonl(kwargs["out_path"], [{
            "problem_id": "p0",
            "candidate_id": "generic_repair_c0",
            "source_candidate_id": "c0",
            "generated_text": REPAIRED_CODE,
            "generated_code": REPAIRED_CODE,
            "repair_type": "generic",
            "error": None,
        }])
        return read_jsonl(kwargs["out_path"])

    out_a = tmp_path / "out_a.jsonl"
    out_b = tmp_path / "out_b.jsonl"
    rows_a = run_nonreference_repair_policy(_benchmark_path(tmp_path), candidates_path, out_a, "fake-model", repair_engine=fake_engine)
    rows_b = run_nonreference_repair_policy(_benchmark_path(tmp_path), candidates_path, out_b, "fake-model", repair_engine=fake_engine)

    assert rows_a == rows_b
