import json
import os
import subprocess
import sys
import time
from pathlib import Path


RUNNER_CODE = r'''
import importlib.util
import json
import pathlib
import sys
import traceback

from replenishverifier.solver.pulp_runner import solve_pulp_model

code_path = pathlib.Path(sys.argv[1])
lp_path = pathlib.Path(sys.argv[2])
time_limit = None if len(sys.argv) < 4 or sys.argv[3] == "" else float(sys.argv[3])

try:
    spec = importlib.util.spec_from_file_location("candidate_module", code_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    if hasattr(mod, "build_model"):
        model = mod.build_model()
    elif hasattr(mod, "model"):
        model = mod.model
    else:
        raise RuntimeError("Candidate code must define build_model() or global variable model.")

    if not hasattr(model, "writeLP"):
        raise RuntimeError("build_model() did not return a PuLP LpProblem-like object.")

    solve_result = solve_pulp_model(model, lp_path=lp_path, msg=False, time_limit=time_limit)
    print(json.dumps({
        "executable": True,
        "status": solve_result.get("status"),
        "objective": solve_result.get("objective"),
        "lp_path": solve_result.get("lp_path"),
        "solver_lp_export_time": float(solve_result.get("solver_lp_export_time") or 0.0),
        "lp_write_time": float(solve_result.get("lp_write_time") or solve_result.get("solver_lp_export_time") or 0.0),
        "solver_time": float(solve_result.get("solver_time") or 0.0),
        "error": None,
    }, ensure_ascii=False))
except Exception:
    print(json.dumps({
        "executable": False,
        "status": "Error",
        "objective": None,
        "lp_path": None,
        "solver_lp_export_time": 0.0,
        "lp_write_time": 0.0,
        "solver_time": 0.0,
        "error": traceback.format_exc(),
    }, ensure_ascii=False))
'''


def _execution_error(status, error, start, lp_path=None):
    return {
        "executable": False,
        "status": status,
        "objective": None,
        "lp_path": lp_path,
        "solver_lp_export_time": 0.0,
        "lp_write_time": 0.0,
        "solver_time": 0.0,
        "code_execution_time": float(time.perf_counter() - start),
        "error": error,
    }


def execute_generated_code(generated_code, run_dir, candidate_id="candidate", timeout=30):
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)

    code_path = (run_dir / f"{candidate_id}.py").resolve()
    runner_path = (run_dir / "_runner.py").resolve()
    lp_path = (run_dir / f"{candidate_id}.lp").resolve()

    code_path.write_text(generated_code, encoding="utf-8")
    runner_path.write_text(RUNNER_CODE, encoding="utf-8")

    start = time.perf_counter()
    try:
        env = os.environ.copy()
        project_root = Path(__file__).resolve().parents[2]
        existing_pythonpath = env.get("PYTHONPATH", "")
        env["PYTHONPATH"] = str(project_root) if not existing_pythonpath else str(project_root) + os.pathsep + existing_pythonpath
        proc = subprocess.run(
            [sys.executable, str(runner_path), str(code_path), str(lp_path), str(timeout)],
            cwd=str(run_dir),
            text=True,
            capture_output=True,
            timeout=timeout,
            env=env,
        )
    except subprocess.TimeoutExpired:
        return _execution_error("Timeout", f"Candidate execution timed out after {timeout} seconds.", start)

    stdout = proc.stdout.strip()
    if not stdout:
        return _execution_error("Error", proc.stderr or "No stdout from candidate execution.", start)

    try:
        result = json.loads(stdout.splitlines()[-1])
    except Exception:
        result = _execution_error("Error", f"Cannot parse executor output. stdout={stdout!r}, stderr={proc.stderr!r}", start)

    result["code_execution_time"] = float(time.perf_counter() - start)
    result["solver_lp_export_time"] = float(result.get("solver_lp_export_time") or 0.0)
    result["lp_write_time"] = float(result.get("lp_write_time") or result.get("solver_lp_export_time") or 0.0)
    result["solver_time"] = float(result.get("solver_time") or 0.0)

    if proc.stderr and result.get("error") is None:
        result["stderr"] = proc.stderr

    return result
