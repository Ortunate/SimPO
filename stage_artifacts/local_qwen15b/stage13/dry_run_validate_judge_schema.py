#!/usr/bin/env python3
"""Validate synthetic judge output shape without API calls or extra dependencies."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ALLOWED_KEYS = {"winner", "score_a", "score_b", "confidence", "rationale"}


def validate_output(obj: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(obj, dict):
        return ["output is not an object"]

    keys = set(obj)
    missing = ALLOWED_KEYS - keys
    extra = keys - ALLOWED_KEYS
    if missing:
        errors.append(f"missing keys: {sorted(missing)}")
    if extra:
        errors.append(f"extra keys: {sorted(extra)}")

    winner = obj.get("winner")
    if winner not in {"A", "B", "tie"}:
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


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("synthetic_eval_examples.jsonl")
    failures = 0
    total = 0
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            total += 1
            row = json.loads(line)
            errors = validate_output(row.get("expected_judge_shape"))
            if errors:
                failures += 1
                print(f"line {line_no}: FAIL: {'; '.join(errors)}")
            else:
                print(f"line {line_no}: PASS: {row.get('id', '<missing-id>')}")

    print(f"validated_examples={total}")
    print(f"failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
