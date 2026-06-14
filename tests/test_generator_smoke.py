from pathlib import Path

from replenishverifier.benchmark.generator import generate_benchmark
from replenishverifier.utils.io import read_jsonl


def test_generate_benchmark_smoke(tmp_path):
    out = tmp_path / "benchmark.jsonl"
    lp_dir = tmp_path / "lp"
    rows = generate_benchmark(out, lp_dir, n_per_type=1, seed=1)
    assert len(rows) == 5
    loaded = read_jsonl(out)
    assert len(loaded) == 5
    for row in loaded:
        assert Path(row["reference_lp_path"]).exists()
        assert row["reference_status"] == "Optimal"
