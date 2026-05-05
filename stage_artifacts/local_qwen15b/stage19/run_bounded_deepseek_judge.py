#!/usr/bin/env python3
"""Run an approved bounded DeepSeek judge batch and aggregate results."""

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
STATIC_LABEL = "static_64_16_20step"
DYNAMIC_LABEL = "dynamic_64_16_20step"


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
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
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
    if isinstance(parsed_judge, dict):
        winner = parsed_judge.get("winner")
        if winner == "A":
            shown_winner_label = request_record.get("shown_response_a_label")
        elif winner == "B":
            shown_winner_label = request_record.get("shown_response_b_label")
        elif winner == "tie":
            shown_winner_label = "tie"

    return {
        "request_id": request_record.get("request_id"),
        "pair_id": request_record.get("pair_id"),
        "order": request_record.get("order"),
        "candidate_a_id": request_record.get("candidate_a_id"),
        "candidate_b_id": request_record.get("candidate_b_id"),
        "shown_response_a_label": request_record.get("shown_response_a_label"),
        "shown_response_b_label": request_record.get("shown_response_b_label"),
        "shown_winner_label": shown_winner_label,
        "original_winner_label": shown_winner_label,
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


def label_to_metric(winner: str | None) -> str:
    if winner == STATIC_LABEL:
        return "static"
    if winner == DYNAMIC_LABEL:
        return "dynamic"
    if winner == "tie":
        return "tie"
    return "invalid"


def aggregate(results: list[dict[str, Any]]) -> dict[str, Any]:
    by_pair: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for result in results:
        pair_id = result.get("pair_id")
        if isinstance(pair_id, str):
            by_pair[pair_id].append(result)

    pair_summaries: list[dict[str, Any]] = []
    winner_counts: dict[str, int] = defaultdict(int)
    consistent_pairs = 0
    parse_failures = 0
    http_failures = 0
    for pair_id, rows in sorted(by_pair.items()):
        winners = [row.get("original_winner_label") for row in rows]
        normalized = [label_to_metric(winner) for winner in winners if winner]
        unique_winners = sorted(set(normalized))
        row_parse_failures = sum(1 for row in rows if row.get("parse_errors"))
        row_http_failures = sum(
            1
            for row in rows
            if not (isinstance(row.get("status_code"), int) and 200 <= row["status_code"] < 300)
        )
        parse_failures += row_parse_failures
        http_failures += row_http_failures
        consistent = (
            len(rows) == 2
            and row_parse_failures == 0
            and row_http_failures == 0
            and len(unique_winners) == 1
        )
        aggregate_winner = unique_winners[0] if consistent else "inconsistent"
        if consistent:
            consistent_pairs += 1
            winner_counts[aggregate_winner] += 1
        pair_summaries.append(
            {
                "pair_id": pair_id,
                "orders": sorted(row.get("order") for row in rows),
                "winners": winners,
                "normalized_winners": normalized,
                "consistent": consistent,
                "aggregate_winner": aggregate_winner,
                "parse_failures": row_parse_failures,
                "http_failures": row_http_failures,
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

    judged_pairs = len(by_pair)
    comparable_pairs = consistent_pairs
    dynamic_wins = winner_counts.get("dynamic", 0)
    static_wins = winner_counts.get("static", 0)
    ties = winner_counts.get("tie", 0)
    non_tie = dynamic_wins + static_wins
    return {
        "request_count": len(results),
        "pair_count": judged_pairs,
        "consistent_pairs": consistent_pairs,
        "inconsistent_pairs": judged_pairs - consistent_pairs,
        "ab_ba_consistency_rate": round(consistent_pairs / judged_pairs, 4) if judged_pairs else None,
        "winner_counts": {
            "static": static_wins,
            "dynamic": dynamic_wins,
            "tie": ties,
            "inconsistent": judged_pairs - consistent_pairs,
        },
        "dynamic_win_rate_all_consistent": round(dynamic_wins / comparable_pairs, 4) if comparable_pairs else None,
        "dynamic_win_rate_non_tie": round(dynamic_wins / non_tie, 4) if non_tie else None,
        "parse_failures": parse_failures,
        "http_failures": http_failures,
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
    parser.add_argument("--max-requests", default=110, type=int)
    parser.add_argument("--max-retries", default=10, type=int)
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
    retry_candidates = [
        (index, row)
        for index, row in enumerate(results)
        if row.get("parse_errors")
        or not (isinstance(row.get("status_code"), int) and 200 <= row["status_code"] < 300)
    ]
    retry_budget = min(args.max_retries, args.max_requests - len(results))
    retry_count = 0
    for index, _failed_result in retry_candidates[:retry_budget]:
        retry_result = request_judge(
            key=key,
            endpoint=endpoint,
            model=model,
            request_record=request_records[index],
            max_tokens=args.max_tokens,
        )
        retry_result["retry_of_request_id"] = request_records[index].get("request_id")
        retry_result["retry_attempt"] = 1
        results[index] = retry_result
        retry_count += 1

    aggregate_result = aggregate(results)
    metadata = {
        "stage": "L19",
        "api_calls": len(request_records) + retry_count,
        "primary_requests": len(request_records),
        "retry_budget": retry_budget,
        "retry_candidates": len(retry_candidates),
        "retry_count": retry_count,
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
    print(f"api_calls: {metadata['api_calls']}")
    print(f"all_status_2xx: {'yes' if metadata['all_status_2xx'] else 'no'}")
    print(f"parse_failures: {metadata['parse_failures']}")
    print(f"pair_count: {aggregate_result['pair_count']}")
    print(f"consistent_pairs: {aggregate_result['consistent_pairs']}")
    print(f"static_wins: {aggregate_result['winner_counts']['static']}")
    print(f"dynamic_wins: {aggregate_result['winner_counts']['dynamic']}")
    print(f"ties: {aggregate_result['winner_counts']['tie']}")
    print(f"result_path: {results_path}")
    return 0 if metadata["all_status_2xx"] and metadata["parse_failures"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
