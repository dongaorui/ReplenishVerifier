import json
import os
import subprocess
import sys
from pathlib import Path


RUNNER_CODE = r'''
import importlib.util
import json
import pathlib
import sys
import traceback

import pulp

code_path = pathlib.Path(sys.argv[1])
lp_path = pathlib.Path(sys.argv[2])

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

    lp_path.parent.mkdir(parents=True, exist_ok=True)
    model.writeLP(str(lp_path))

    status_code = model.solve(pulp.PULP_CBC_CMD(msg=False))
    status = pulp.LpStatus.get(status_code, str(status_code))
    obj = pulp.value(model.objective)
    print(json.dumps({
        "executable": True,
        "status": status,
        "objective": None if obj is None else float(obj),
        "lp_path": str(lp_path),
        "error": None,
    }, ensure_ascii=False))
except Exception:
    print(json.dumps({
        "executable": False,
        "status": "Error",
        "objective": None,
        "lp_path": None,
        "error": traceback.format_exc(),
    }, ensure_ascii=False))
'''


def execute_generated_code(generated_code, run_dir, candidate_id="candidate", timeout=30):
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)

    code_path = (run_dir / f"{candidate_id}.py").resolve()
    runner_path = (run_dir / "_runner.py").resolve()
    lp_path = (run_dir / f"{candidate_id}.lp").resolve()

    code_path.write_text(generated_code, encoding="utf-8")
    runner_path.write_text(RUNNER_CODE, encoding="utf-8")

    try:
        env = os.environ.copy()
        project_root = Path(__file__).resolve().parents[2]
        existing_pythonpath = env.get("PYTHONPATH", "")
        env["PYTHONPATH"] = str(project_root) if not existing_pythonpath else str(project_root) + os.pathsep + existing_pythonpath
        proc = subprocess.run(
            [sys.executable, str(runner_path), str(code_path), str(lp_path)],
            cwd=str(run_dir),
            text=True,
            capture_output=True,
            timeout=timeout,
            env=env,
        )
    except subprocess.TimeoutExpired:
        return {
            "executable": False,
            "status": "Timeout",
            "objective": None,
            "lp_path": None,
            "error": f"Candidate execution timed out after {timeout} seconds.",
        }

    stdout = proc.stdout.strip()
    if not stdout:
        return {
            "executable": False,
            "status": "Error",
            "objective": None,
            "lp_path": None,
            "error": proc.stderr or "No stdout from candidate execution.",
        }

    try:
        result = json.loads(stdout.splitlines()[-1])
    except Exception:
        result = {
            "executable": False,
            "status": "Error",
            "objective": None,
            "lp_path": None,
            "error": f"Cannot parse executor output. stdout={stdout!r}, stderr={proc.stderr!r}",
        }

    if proc.stderr and result.get("error") is None:
        result["stderr"] = proc.stderr

    return result
