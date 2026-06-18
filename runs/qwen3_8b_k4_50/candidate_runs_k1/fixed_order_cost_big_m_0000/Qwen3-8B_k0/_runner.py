
import importlib.util
import json
import pathlib
import sys
import time
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
    export_start = time.perf_counter()
    model.writeLP(str(lp_path))
    solver_lp_export_time = time.perf_counter() - export_start

    solve_start = time.perf_counter()
    status_code = model.solve(pulp.PULP_CBC_CMD(msg=False))
    solver_time = time.perf_counter() - solve_start
    status = pulp.LpStatus.get(status_code, str(status_code))
    obj = pulp.value(model.objective)
    print(json.dumps({
        "executable": True,
        "status": status,
        "objective": None if obj is None else float(obj),
        "lp_path": str(lp_path),
        "solver_lp_export_time": float(solver_lp_export_time),
        "solver_time": float(solver_time),
        "error": None,
    }, ensure_ascii=False))
except Exception:
    print(json.dumps({
        "executable": False,
        "status": "Error",
        "objective": None,
        "lp_path": None,
        "solver_lp_export_time": None,
        "solver_time": None,
        "error": traceback.format_exc(),
    }, ensure_ascii=False))
