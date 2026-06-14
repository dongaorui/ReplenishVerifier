import random
from pathlib import Path

from tqdm import tqdm

from replenishverifier.benchmark.schemas import DIFFICULTY_BY_TYPE, PROBLEM_TYPES
from replenishverifier.benchmark.templates import (
    build_model,
    expected_for,
    natural_language,
    reference_code,
    sample_params,
)
from replenishverifier.solver.pulp_runner import solve_pulp_model
from replenishverifier.utils.io import write_jsonl


def generate_benchmark(output, lp_dir, n_per_type=20, seed=42, problem_types=None):
    rng = random.Random(seed)
    output = Path(output)
    lp_dir = Path(lp_dir)
    problem_types = problem_types or PROBLEM_TYPES

    rows = []
    for problem_type in problem_types:
        for idx in tqdm(range(n_per_type), desc=f"generate:{problem_type}"):
            sample_id = f"{problem_type}_{idx:04d}"
            params = sample_params(problem_type, rng)
            model = build_model(problem_type, params)
            lp_path = lp_dir / f"{sample_id}.lp"
            solve_result = solve_pulp_model(model, lp_path=lp_path, msg=False)

            row = {
                "id": sample_id,
                "difficulty": DIFFICULTY_BY_TYPE[problem_type],
                "problem_type": problem_type,
                "natural_language": natural_language(problem_type, params),
                "parameters": params,
                "expected_structures": expected_for(problem_type),
                "reference_code": reference_code(problem_type, params),
                "reference_objective": solve_result["objective"],
                "reference_status": solve_result["status"],
                "reference_lp_path": str(lp_path),
            }
            rows.append(row)

    write_jsonl(output, rows)
    return rows
