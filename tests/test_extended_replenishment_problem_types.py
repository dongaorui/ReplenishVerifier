import random
from pathlib import Path

from replenishverifier.benchmark.generator import generate_benchmark
from replenishverifier.benchmark.schemas import ALL_PROBLEM_TYPES, DIFFICULTY_BY_TYPE, EXTENDED_PROBLEM_TYPES
from replenishverifier.benchmark.templates import (
    build_model,
    modeling_steps,
    natural_language_variants,
    replenishment_entities,
    sample_params,
    semantic_frame,
    validate_replenishment_instance,
)
from replenishverifier.data.structure_schema import get_structure_schema
from replenishverifier.solver.pulp_runner import solve_pulp_model


EXTENDED_TYPES = list(EXTENDED_PROBLEM_TYPES)


def test_extended_problem_types_are_registered_with_schema_and_difficulty():
    for problem_type in EXTENDED_TYPES:
        assert problem_type in ALL_PROBLEM_TYPES
        assert problem_type in DIFFICULTY_BY_TYPE
        schema = get_structure_schema(problem_type)
        assert "inventory_balance" in schema["required"]
        assert "order_variable" in schema["required"]
        assert "objective_minimize" in schema["required"]

    assert "lead_time" in get_structure_schema("single_item_multi_period_lead_time")["required"]
    assert "service_level_constraint" in get_structure_schema("single_item_multi_period_service_level")["required"]
    assert "moq_constraint" in get_structure_schema("single_item_multi_period_moq_batch")["required"]
    assert "batch_integer_variable" in get_structure_schema("single_item_multi_period_moq_batch")["required"]


def test_extended_templates_sample_params_metadata_and_language():
    for problem_type in EXTENDED_TYPES:
        params = sample_params(problem_type, random.Random(17))
        frame = semantic_frame(problem_type, params)
        entities = replenishment_entities(problem_type, params)
        steps = modeling_steps(problem_type, params)
        variants = natural_language_variants(problem_type, params)

        assert frame["decision_variables"]
        assert frame["objective_terms"]
        assert frame["constraints"]
        assert set(frame["required_structures"]) <= set(frame["replenishment_structures"])
        assert entities["periods"]
        assert len(variants) >= 4
        assert len({variant["template_id"] for variant in variants}) == len(variants)
        assert steps

    lead = semantic_frame("single_item_multi_period_lead_time", sample_params("single_item_multi_period_lead_time", random.Random(1)))
    assert any("Q_{t-L}" in item or "lead" in item.lower() for item in lead["constraints"])
    service = semantic_frame("single_item_multi_period_service_level", sample_params("single_item_multi_period_service_level", random.Random(2)))
    assert any("service" in item.lower() or "fill" in item.lower() for item in service["constraints"])
    moq = semantic_frame("single_item_multi_period_moq_batch", sample_params("single_item_multi_period_moq_batch", random.Random(3)))
    assert any("batch" in item.lower() for item in moq["constraints"])


def test_extended_reference_models_solve_and_have_expected_structure_names(tmp_path):
    for problem_type in EXTENDED_TYPES:
        params = sample_params(problem_type, random.Random(23))
        model = build_model(problem_type, params)
        result = solve_pulp_model(model, lp_path=tmp_path / f"{problem_type}.lp", msg=False)
        lp_text = Path(result["lp_path"]).read_text(encoding="utf-8")

        assert result["status"] == "Optimal"
        assert result["objective"] is not None
        assert "inventory_balance" in lp_text
        if problem_type == "single_item_multi_period_lead_time":
            assert "lead_time" in lp_text or "arrival" in lp_text
        if problem_type == "single_item_multi_period_service_level":
            assert "service_level" in lp_text or "fill_rate" in lp_text
        if problem_type == "single_item_multi_period_moq_batch":
            assert "moq" in lp_text
            assert "Generals" in lp_text or "Binaries" in lp_text


def test_generate_extended_benchmark_rows_and_validation(tmp_path):
    rows = generate_benchmark(
        tmp_path / "extended.jsonl",
        tmp_path / "lp",
        n_per_type=1,
        seed=31,
        problem_types=EXTENDED_TYPES,
    )

    assert len(rows) == 3
    assert {row["problem_type"] for row in rows} == set(EXTENDED_TYPES)
    for row in rows:
        assert validate_replenishment_instance(row, include_labels=True) is True
        assert Path(row["reference_lp_path"]).exists()
        assert row["reference_status"] == "Optimal"
        assert row["expected_structures"]
        assert row["semantic_frame"]
        assert row["replenishment_entities"]


def test_generate_20_per_extended_type_creates_60_rows_without_labels(tmp_path):
    rows = generate_benchmark(
        tmp_path / "extended_unlabeled.jsonl",
        tmp_path / "lp",
        n_per_type=20,
        seed=42,
        problem_types=EXTENDED_TYPES,
        include_labels=False,
        include_parameters=True,
    )

    assert len(rows) == 60
    counts = {problem_type: 0 for problem_type in EXTENDED_TYPES}
    for row in rows:
        counts[row["problem_type"]] += 1
        assert "reference_objective" not in row
        assert "reference_code" not in row
        assert "parameters" in row
    assert counts == {problem_type: 20 for problem_type in EXTENDED_TYPES}
