import time
from pathlib import Path

import pulp


def _solver_available(solver):
    try:
        return bool(solver.available())
    except Exception:
        return False


def _build_solver(msg=False, time_limit=None):
    solver_kwargs = {"msg": msg, "timeLimit": time_limit}

    for solver_cls in (getattr(pulp, "COIN_CMD", None), getattr(pulp, "PULP_CBC_CMD", None)):
        if solver_cls is None:
            continue
        try:
            solver = solver_cls(**solver_kwargs)
        except Exception:
            continue
        if _solver_available(solver):
            return solver

    raise pulp.PulpSolverError("No available CBC solver found via COIN_CMD or PULP_CBC_CMD.")


def _export_lp(model, lp_path):
    lp_path = Path(lp_path)
    lp_path.parent.mkdir(parents=True, exist_ok=True)
    export_start = time.perf_counter()
    try:
        model.writeLP(str(lp_path))
    except Exception as exc:
        raise RuntimeError(f"LP export failed: writeLP raised {exc}") from exc
    solver_lp_export_time = time.perf_counter() - export_start

    if not lp_path.is_file():
        raise RuntimeError(f"LP export failed: writeLP did not create file at {lp_path}")
    try:
        if lp_path.stat().st_size <= 0:
            raise RuntimeError(f"LP export failed: writeLP created empty file at {lp_path}")
    except OSError as exc:
        raise RuntimeError(f"LP export failed: cannot stat LP file at {lp_path}: {exc}") from exc
    return lp_path, solver_lp_export_time


def solve_pulp_model(model, lp_path=None, msg=False, time_limit=None):
    solver_lp_export_time = 0.0
    lp_exported = False
    lp_export_error = None
    if lp_path is not None:
        lp_path, solver_lp_export_time = _export_lp(model, lp_path)
        lp_exported = True

    solver = _build_solver(msg=msg, time_limit=time_limit)
    solve_start = time.perf_counter()
    status_code = model.solve(solver)
    solver_time = time.perf_counter() - solve_start
    status = pulp.LpStatus.get(status_code, str(status_code))

    try:
        obj = pulp.value(model.objective)
    except Exception:
        obj = None

    return {
        "status": status,
        "objective": None if obj is None else float(obj),
        "lp_path": None if lp_path is None else str(lp_path),
        "lp_exported": bool(lp_exported),
        "lp_export_error": lp_export_error,
        "solver_lp_export_time": float(solver_lp_export_time),
        "lp_write_time": float(solver_lp_export_time),
        "solver_time": float(solver_time),
    }
