#!/usr/bin/env python3
"""Run an approved tiny DeepSeek judge batch and aggregate AB/BA consistency."""

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Any


DEFAULT_ENDPOINT = "https://api.deepseek.com/chat/completions"
DEFAULT_MODEL = "deepseek-v4-flash"


def load_dotenv(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip("'").strip('"')
            if key:
                values[key] = value
    return values


def get_config(env_path: Path) -> tuple[str, str, str, dict[str, bool]]:
    dotenv = load_dotenv(env_path)

    def pick(*names: str) -> str | None:
        for name in names:
            value = os.environ.get(name) or dotenv.get(name)
            if value:
                return value
        return None

    key = pick("DEEPSEEK_API_KEY", "DEEPSEEK_KEY")
    endpoint = pick("DEEPSEEK_API_URL", "DEEPSEEK_API_BASE", "DEEPSEEK_BASE_URL") or DEFAULT_ENDPOINT
    model = pick("DEEPSEEK_MODEL", "DEEPSEEK_JUDGE_MODEL") or DEFAULT_MODEL
    presence = {
        "env_file_exists": env_path.exists(),
        "deepseek_key_present": bool(key),
        "endpoint_present": bool(endpoint),
        "model_present": bool(model),
    }
    if not key:
        raise RuntimeError("DeepSeek API key presence check failed")
    return key, endpoint, model, presence


def extract_json_object(text: str) -> dict[str, Any]:
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = [line for line in stripped.splitlines() if not line.strip().startswith("```")]
        stripped = "\n".join(lines).strip()
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        start = stripped.find("{")
        end = stripped.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise
        return json.loads(stripped[start : end + 1])


def validate_judge_output(obj: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(obj, dict):
        return ["judge output is not an object"]
    allowed = {"winner", "score_a", "score_b", "confidence", "rationale"}
    missing = allowed - set(obj)
    extra = set(obj) - allowed
    if missing:
        errors.append(f"missing keys: {sorted(missing)}")
    if extra:
        errors.append(f"extra keys: {sorted(extra)}")
    if obj.get("winner") not in {"A", "B", "tie"}:
        errors.append("winner must be A, B, or tie")
    for key in ("score_a", "score_b"):
        value = obj.get(key)
        if not isinstance(value, int) or not 1 <= value <= 10:
            errors.append(f"{key} must be an integer from 1 to 10")
    confidence = obj.get("confidence")
    if not isinstance(confidence, (int, float)) or not 0.0 <= float(confidence) <= 1.0:
        errors.append("confidence must be a number from 0.0 to 1.0")
    rationale = obj.get("rationale")
    if not isinstance(rationale, str) or not rationale.strip():
        errors.append("rationale must be a non-empty string")
    return errors


def request_judge(
    *,
    key: str,
    endpoint: str,
    model: str,
    request_record: dict[str, Any],
    max_tokens: int,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": model,
        "messages": request_record["messages"],
        "temperature": 0,
        "max_tokens": max_tokens,
        "thinking": {"type": "disabled"},
    }
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        endpoint,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )

    started = time.time()
    status_code = None
    response_json: dict[str, Any] | None = None
    error_text = None
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            status_code = response.status
            response_json = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        status_code = exc.code
        error_text = exc.read().decode("utf-8", errors="replace")
    except Exception as exc:  # noqa: BLE001
        error_text = f"{type(exc).__name__}: {exc}"
    ended = time.time()

    judge_text = None
    parsed_judge = None
    parse_errors: list[str] = []
    usage = None
    response_model = None
    if response_json is not None:
        usage = response_json.get("usage")
        response_model = response_json.get("model")
        choices = response_json.get("choices") or []
        if choices:
            judge_text = (choices[0].get("message") or {}).get("content")
    if isinstance(judge_text, str):
        try:
            parsed_judge = extract_json_object(judge_text)
            parse_errors = validate_judge_output(parsed_judge)
        except Exception as exc:  # noqa: BLE001
            parse_errors = [f"{type(exc).__name__}: {exc}"]

    shown_winner_label = None
    original_winner_label = None
    if isinstance(parsed_judge, dict):
        winner = parsed_judge.get("winner")
        if winner == "A":
            shown_winner_label = request_record.get("shown_response_a_label")
        elif winner == "B":
            shown_winner_label = request_record.get("shown_response_b_label")
        elif winner == "tie":
            shown_winner_label = "tie"
        original_winner_label = shown_winner_label

    return {
        "request_id": request_record.get("request_id"),
        "pair_id": request_record.get("pair_id"),
        "order": request_record.get("order"),
        "candidate_a_id": request_record.get("candidate_a_id"),
        "candidate_b_id": request_record.get("candidate_b_id"),
        "shown_response_a_label": request_record.get("shown_response_a_label"),
        "shown_response_b_label": request_record.get("shown_response_b_label"),
        "shown_winner_label": shown_winner_label,
        "original_winner_label": original_winner_label,
        "status_code": status_code,
        "duration_s": round(ended - started, 3),
        "response_model": response_model,
        "usage": usage,
        "judge_text": judge_text,
        "parsed_judge": parsed_judge,
        "parse_errors": parse_errors,
        "http_error_body": error_text if status_code and status_code >= 400 else None,
        "transport_error": error_text if status_code is None else None,
    }


def aggregate(results: list[dict[str, Any]]) -> dict[str, Any]:
    by_pair: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for result in results:
        pair_id = result.get("pair_id")
        if isinstance(pair_id, str):
            by_pair[pair_id].append(result)

    pair_summaries: list[dict[str, Any]] = []
    winner_counts: dict[str, int] = defaultdict(int)
    consistent_pairs = 0
    for pair_id, rows in sorted(by_pair.items()):
        winners = [row.get("original_winner_label") for row in rows]
        non_null_winners = [winner for winner in winners if winner]
        unique_winners = sorted(set(non_null_winners))
        consistent = len(unique_winners) == 1 and len(rows) == 2
        if consistent:
            consistent_pairs += 1
            winner_counts[unique_winners[0]] += 1
        pair_summaries.append(
            {
                "pair_id": pair_id,
                "orders": sorted(row.get("order") for row in rows),
                "winners": winners,
                "consistent": consistent,
                "aggregate_winner": unique_winners[0] if consistent else "inconsistent",
            }
        )

    total_tokens = 0
    prompt_tokens = 0
    completion_tokens = 0
    for result in results:
        usage = result.get("usage") or {}
        total_tokens += int(usage.get("total_tokens") or 0)
        prompt_tokens += int(usage.get("prompt_tokens") or 0)
        completion_tokens += int(usage.get("completion_tokens") or 0)

    return {
        "request_count": len(results),
        "pair_count": len(by_pair),
        "consistent_pairs": consistent_pairs,
        "inconsistent_pairs": len(by_pair) - consistent_pairs,
        "winner_counts": dict(sorted(winner_counts.items())),
        "pair_summaries": pair_summaries,
        "usage": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request-jsonl", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--env-file", default=Path(".env"), type=Path)
    parser.add_argument("--max-tokens", default=256, type=int)
    parser.add_argument("--max-requests", default=4, type=int)
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    key, endpoint, model, presence = get_config(args.env_file)

    request_records: list[dict[str, Any]] = []
    with args.request_jsonl.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                request_records.append(json.loads(line))
    if len(request_records) > args.max_requests:
        raise RuntimeError(f"refusing to run {len(request_records)} requests; max is {args.max_requests}")

    results: list[dict[str, Any]] = []
    for request_record in request_records:
        results.append(
            request_judge(
                key=key,
                endpoint=endpoint,
                model=model,
                request_record=request_record,
                max_tokens=args.max_tokens,
            )
        )

    aggregate_result = aggregate(results)
    metadata = {
        "api_calls": len(results),
        "request_jsonl": str(args.request_jsonl),
        "endpoint_host": endpoint.split("/")[2] if "://" in endpoint else endpoint,
        "model": model,
        "max_tokens": args.max_tokens,
        "presence": presence,
        "all_status_2xx": all(
            isinstance(row.get("status_code"), int) and 200 <= row["status_code"] < 300 for row in results
        ),
        "parse_failures": sum(1 for row in results if row.get("parse_errors")),
        "aggregate": aggregate_result,
    }

    results_path = args.out_dir / "judge_results.jsonl"
    with results_path.open("w", encoding="utf-8") as handle:
        for result in results:
            handle.write(json.dumps(result, ensure_ascii=False, sort_keys=True) + "\n")

    (args.out_dir / "aggregate.json").write_text(
        json.dumps(aggregate_result, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (args.out_dir / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    print(f"env_file_exists: {'yes' if presence['env_file_exists'] else 'no'}")
    print(f"deepseek_key_present: {'yes' if presence['deepseek_key_present'] else 'no'}")
    print(f"api_calls: {len(results)}")
    print(f"all_status_2xx: {'yes' if metadata['all_status_2xx'] else 'no'}")
    print(f"parse_failures: {metadata['parse_failures']}")
    print(f"pair_count: {aggregate_result['pair_count']}")
    print(f"consistent_pairs: {aggregate_result['consistent_pairs']}")
    print(f"result_path: {results_path}")
    return 0 if metadata["all_status_2xx"] and metadata["parse_failures"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
