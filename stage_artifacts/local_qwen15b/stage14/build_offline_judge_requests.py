#!/usr/bin/env python3
"""Build API-free pairwise judge request JSONL with A/B and B/A swaps."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SYSTEM_MESSAGE = (
    "You are an impartial evaluator. Compare two assistant responses to the same user instruction.\n\n"
    "Judge only the final answer quality. Do not favor response A or B by position. "
    "Consider correctness, completeness, helpfulness, instruction following, clarity, and safety. "
    "Ignore style differences that do not affect usefulness.\n\n"
    "Return only valid JSON matching the requested schema. Do not include chain-of-thought. "
    "Use a brief public rationale."
)


EXPECTED_OUTPUT_SCHEMA = {
    "winner": "A | B | tie",
    "score_a": "integer 1..10",
    "score_b": "integer 1..10",
    "confidence": "number 0.0..1.0",
    "rationale": "one or two concise public sentences",
}


REQUIRED_TOP_LEVEL = {"pair_id", "source", "instruction", "candidate_a", "candidate_b", "provenance"}
REQUIRED_CANDIDATE = {"id", "label", "text"}


def require_string(obj: dict[str, Any], key: str, context: str) -> str:
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{context}.{key} must be a non-empty string")
    return value


def validate_pair(row: Any, line_no: int) -> dict[str, Any]:
    if not isinstance(row, dict):
        raise ValueError(f"line {line_no}: row must be an object")
    missing = REQUIRED_TOP_LEVEL - set(row)
    if missing:
        raise ValueError(f"line {line_no}: missing top-level keys: {sorted(missing)}")

    require_string(row, "pair_id", f"line {line_no}")
    require_string(row, "source", f"line {line_no}")
    require_string(row, "instruction", f"line {line_no}")
    if not isinstance(row.get("provenance"), dict):
        raise ValueError(f"line {line_no}: provenance must be an object")

    for key in ("candidate_a", "candidate_b"):
        candidate = row.get(key)
        if not isinstance(candidate, dict):
            raise ValueError(f"line {line_no}: {key} must be an object")
        missing_candidate = REQUIRED_CANDIDATE - set(candidate)
        if missing_candidate:
            raise ValueError(f"line {line_no}: {key} missing keys: {sorted(missing_candidate)}")
        for field in REQUIRED_CANDIDATE:
            require_string(candidate, field, f"line {line_no}.{key}")

    return row


def user_prompt(instruction: str, response_a: str, response_b: str) -> str:
    return (
        "User instruction:\n"
        f"{instruction}\n\n"
        "Assistant response A:\n"
        f"{response_a}\n\n"
        "Assistant response B:\n"
        f"{response_b}\n\n"
        "Return JSON with:\n"
        '- winner: "A", "B", or "tie"\n'
        "- score_a: integer from 1 to 10\n"
        "- score_b: integer from 1 to 10\n"
        "- confidence: number from 0.0 to 1.0\n"
        "- rationale: one or two concise sentences, no private reasoning"
    )


def build_request(row: dict[str, Any], order: str) -> dict[str, Any]:
    original_a = row["candidate_a"]
    original_b = row["candidate_b"]
    if order == "AB":
        shown_a, shown_b = original_a, original_b
    elif order == "BA":
        shown_a, shown_b = original_b, original_a
    else:
        raise ValueError(f"unsupported order: {order}")

    pair_id = row["pair_id"]
    return {
        "request_id": f"{pair_id}-{order.lower()}",
        "pair_id": pair_id,
        "order": order,
        "source": row["source"],
        "candidate_a_id": original_a["id"],
        "candidate_b_id": original_b["id"],
        "shown_response_a_id": shown_a["id"],
        "shown_response_b_id": shown_b["id"],
        "shown_response_a_label": shown_a["label"],
        "shown_response_b_label": shown_b["label"],
        "provenance": row["provenance"],
        "messages": [
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": user_prompt(row["instruction"], shown_a["text"], shown_b["text"])},
        ],
        "expected_output_schema": EXPECTED_OUTPUT_SCHEMA,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    requests: list[dict[str, Any]] = []
    with args.input.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            row = validate_pair(json.loads(line), line_no)
            requests.append(build_request(row, "AB"))
            requests.append(build_request(row, "BA"))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        for request in requests:
            handle.write(json.dumps(request, ensure_ascii=False, sort_keys=True) + "\n")

    pair_count = len(requests) // 2
    print(f"input_pairs={pair_count}")
    print(f"judge_requests={len(requests)}")
    print(f"output={args.output}")
    print("api_calls=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
