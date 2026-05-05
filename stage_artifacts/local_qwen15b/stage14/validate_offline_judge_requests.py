#!/usr/bin/env python3
"""Validate offline judge request JSONL shape and A/B swap coverage."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


REQUIRED_REQUEST_KEYS = {
    "request_id",
    "pair_id",
    "order",
    "source",
    "candidate_a_id",
    "candidate_b_id",
    "shown_response_a_id",
    "shown_response_b_id",
    "shown_response_a_label",
    "shown_response_b_label",
    "provenance",
    "messages",
    "expected_output_schema",
}


def validate_request(row: Any, line_no: int) -> list[str]:
    errors: list[str] = []
    if not isinstance(row, dict):
        return [f"line {line_no}: request must be an object"]
    missing = REQUIRED_REQUEST_KEYS - set(row)
    if missing:
        errors.append(f"line {line_no}: missing keys: {sorted(missing)}")
    if row.get("order") not in {"AB", "BA"}:
        errors.append(f"line {line_no}: order must be AB or BA")
    messages = row.get("messages")
    if not isinstance(messages, list) or len(messages) != 2:
        errors.append(f"line {line_no}: messages must contain system and user messages")
    else:
        expected_roles = ["system", "user"]
        for idx, expected_role in enumerate(expected_roles):
            message = messages[idx]
            if not isinstance(message, dict):
                errors.append(f"line {line_no}: messages[{idx}] must be an object")
                continue
            if message.get("role") != expected_role:
                errors.append(f"line {line_no}: messages[{idx}].role must be {expected_role}")
            content = message.get("content")
            if not isinstance(content, str) or not content.strip():
                errors.append(f"line {line_no}: messages[{idx}].content must be non-empty")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    args = parser.parse_args()

    errors: list[str] = []
    by_pair: dict[str, list[dict[str, Any]]] = defaultdict(list)
    total = 0
    with args.input.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            total += 1
            row = json.loads(line)
            errors.extend(validate_request(row, line_no))
            if isinstance(row, dict) and isinstance(row.get("pair_id"), str):
                by_pair[row["pair_id"]].append(row)

    for pair_id, rows in sorted(by_pair.items()):
        orders = {row.get("order") for row in rows}
        if orders != {"AB", "BA"}:
            errors.append(f"pair {pair_id}: expected AB and BA orders, got {sorted(orders)}")
            continue
        ab = next(row for row in rows if row.get("order") == "AB")
        ba = next(row for row in rows if row.get("order") == "BA")
        if ab.get("shown_response_a_id") != ba.get("shown_response_b_id"):
            errors.append(f"pair {pair_id}: AB shown A should match BA shown B")
        if ab.get("shown_response_b_id") != ba.get("shown_response_a_id"):
            errors.append(f"pair {pair_id}: AB shown B should match BA shown A")

    for error in errors:
        print(f"FAIL: {error}")
    print(f"judge_requests={total}")
    print(f"pairs={len(by_pair)}")
    print(f"failures={len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
