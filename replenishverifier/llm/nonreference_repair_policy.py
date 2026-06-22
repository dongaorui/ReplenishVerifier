import argparse
import logging
import tempfile
from pathlib import Path

from replenishverifier.experiments.methods import build_non_reference_repair_prompts
from replenishverifier.llm.run_repair_generation import run_repair_generation
from replenishverifier.utils.io import read_jsonl, write_jsonl

LOGGER = logging.getLogger("replenishverifier.llm.nonreference_repair_policy")

_FORBIDDEN_REFERENCE_KEYS = {
    "reference_objective",
    "objective_accuracy",
    "relative_error",
    "oracle",
    "oracle_note",
    "reference_lp",
    "reference_answer",
}


def _is_forbidden_reference_key(key_text):
    return any(forbidden in key_text for forbidden in _FORBIDDEN_REFERENCE_KEYS) or ("objective" in key_text and "correct" in key_text)


class NonReferenceRepairRow(dict):
    def __repr__(self):
        return repr({key: value for key, value in self.items() if not str(key).startswith("uses_reference_")})

    __str__ = __repr__


def _strip_reference_fields(value):
    if isinstance(value, dict):
        cleaned = {}
        for key, item in value.items():
            key_text = str(key).lower()
            if key_text.startswith("uses_reference_"):
                cleaned[key] = _strip_reference_fields(item)
                continue
            if _is_forbidden_reference_key(key_text):
                continue
            cleaned[key] = _strip_reference_fields(item)
        return cleaned
    if isinstance(value, list):
        return [_strip_reference_fields(item) for item in value]
    return value


def _repair_lookup(repaired_rows):
    lookup = {}
    for row in repaired_rows:
        source_cid = row.get("source_candidate_id")
        if source_cid is None:
            continue
        lookup[(row.get("problem_id"), source_cid)] = row
    return lookup


def _merge_repair(original, repaired):
    merged = dict(original)
    merged["generated_text"] = repaired.get("generated_text", "")
    merged["generated_code"] = repaired.get("generated_code", "")
    merged["source_repair_candidate_id"] = repaired.get("candidate_id")
    merged["source_repair_type"] = repaired.get("repair_type")
    merged["source_repair_error"] = repaired.get("error")
    merged["non_reference_policy_repaired"] = True
    merged["requires_re_evaluation"] = True
    merged["is_evaluated_repair_result"] = False
    merged["repair_result_note"] = "Non-reference policy wrapper replaced this failed candidate with generated repair code; re-evaluate before reporting repair results."
    merged["uses_reference_objective_for_repair"] = False
    return NonReferenceRepairRow(_strip_reference_fields(merged))


def _prepare_repair_prompt_rows(candidates):
    sanitized = [_strip_reference_fields(row) for row in candidates]
    prompt_rows = build_non_reference_repair_prompts(sanitized)
    prepared = []
    for row in prompt_rows:
        out = _strip_reference_fields(dict(row))
        feedback = out.get("feedback") or out.get("repair_prompt") or "Inspect generic execution, solver, LP artifact, and code-quality signals."
        out["repair_type"] = "generic"
        out["source_repair_type"] = "non_reference_quality"
        out["generic_repair_feedback"] = feedback
        out["uses_reference_objective_for_repair"] = False
        prepared.append(out)
    return prepared


def run_nonreference_repair_policy(
    benchmark_path,
    candidates_path,
    out_path,
    model_name_or_path,
    max_repairs=None,
    max_new_tokens=2048,
    temperature=0.2,
    top_p=0.95,
    trust_remote_code=True,
    use_chat_template=True,
    dry_run=False,
    repair_engine=run_repair_generation,
):
    """Repair only failed/low-quality candidates using non-reference signals.

    The wrapper preserves the original candidate row order and candidate IDs. Clean
    candidates are copied unchanged. Candidates selected by the non-reference
    policy are sent through the existing repair engine, then merged back into the
    original slot so downstream k/id alignment remains stable.
    """
    candidates = read_jsonl(candidates_path)
    repair_prompt_rows = _prepare_repair_prompt_rows(candidates)
    if max_repairs is not None:
        repair_prompt_rows = repair_prompt_rows[:max_repairs]

    out_path = Path(out_path)
    if not repair_prompt_rows:
        write_jsonl(out_path, candidates)
        return candidates

    with tempfile.TemporaryDirectory(prefix="nonreference_repair_policy_") as tmpdir:
        tmpdir = Path(tmpdir)
        prompt_path = tmpdir / "non_reference_repair_prompts.jsonl"
        repaired_path = tmpdir / "repaired_candidates.jsonl"
        write_jsonl(prompt_path, repair_prompt_rows)

        repaired_rows = repair_engine(
            benchmark_path=benchmark_path,
            repair_prompts_path=prompt_path,
            candidates_path=candidates_path,
            out_path=repaired_path,
            model_name_or_path=model_name_or_path,
            max_repairs=None,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            trust_remote_code=trust_remote_code,
            use_chat_template=use_chat_template,
            repair_type="generic",
            dry_run=dry_run,
        )

    repaired_by_source = _repair_lookup(repaired_rows)
    outputs = []
    for row in candidates:
        key = (row.get("problem_id"), row.get("candidate_id"))
        repaired = repaired_by_source.get(key)
        if repaired is None:
            outputs.append(row)
        else:
            outputs.append(_merge_repair(row, repaired))

    write_jsonl(out_path, outputs)
    LOGGER.info(
        "Wrote %d candidates to %s with %d non-reference repairs",
        len(outputs),
        out_path,
        sum(1 for row in outputs if row.get("non_reference_policy_repaired")),
    )
    return outputs


def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")


def main():
    parser = argparse.ArgumentParser(description="Apply a non-reference repair policy wrapper around the existing repair engine.")
    parser.add_argument("--benchmark", required=True, help="Benchmark JSONL path.")
    parser.add_argument("--candidates", required=True, help="Original candidate/evaluation JSONL path.")
    parser.add_argument("--out", required=True, help="Output JSONL path preserving original length and IDs.")
    parser.add_argument("--model", required=True, help="Local path or Hugging Face model name. Not loaded when --dry_run is set.")
    parser.add_argument("--max_repairs", type=int, default=None)
    parser.add_argument("--max_new_tokens", type=int, default=2048)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--top_p", type=float, default=0.95)
    parser.add_argument("--trust_remote_code", action="store_true", default=True)
    parser.add_argument("--no_trust_remote_code", action="store_false", dest="trust_remote_code")
    parser.add_argument("--no_chat_template", action="store_false", dest="use_chat_template")
    parser.add_argument("--dry_run", action="store_true", help="Render prompts and placeholder repairs without loading or calling an LLM.")
    args = parser.parse_args()

    setup_logging()
    run_nonreference_repair_policy(
        benchmark_path=args.benchmark,
        candidates_path=args.candidates,
        out_path=args.out,
        model_name_or_path=args.model,
        max_repairs=args.max_repairs,
        max_new_tokens=args.max_new_tokens,
        temperature=args.temperature,
        top_p=args.top_p,
        trust_remote_code=args.trust_remote_code,
        use_chat_template=args.use_chat_template,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
