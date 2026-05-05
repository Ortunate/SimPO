#!/usr/bin/env python3
"""Pair Stage L16 static/dynamic generated responses for offline judging."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


STATIC_VARIANT = "static_64_16_20step"
DYNAMIC_VARIANT = "dynamic_64_16_20step"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--responses", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    by_prompt: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    with args.responses.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            by_prompt[row["prompt_id"]][row["variant"]] = row

    pairs: list[dict[str, Any]] = []
    failures: list[str] = []
    for prompt_id, variants in sorted(by_prompt.items()):
        static = variants.get(STATIC_VARIANT)
        dynamic = variants.get(DYNAMIC_VARIANT)
        if static is None or dynamic is None:
            failures.append(f"{prompt_id}: missing static or dynamic response")
            continue
        if static["instruction"] != dynamic["instruction"]:
            failures.append(f"{prompt_id}: instruction mismatch")
            continue
        pairs.append(
            {
                "pair_id": f"l16-{prompt_id}",
                "source": "stage16_tiny_generation",
                "instruction": static["instruction"],
                "candidate_a": {
                    "id": f"{prompt_id}-{STATIC_VARIANT}",
                    "label": STATIC_VARIANT,
                    "text": static["response"],
                },
                "candidate_b": {
                    "id": f"{prompt_id}-{DYNAMIC_VARIANT}",
                    "label": DYNAMIC_VARIANT,
                    "text": dynamic["response"],
                },
                "provenance": {
                    "stage": "L16",
                    "static_adapter": static["adapter_path"],
                    "dynamic_adapter": dynamic["adapter_path"],
                    "note": "Tiny local generation smoke outputs; not benchmark evidence.",
                },
            }
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        for pair in pairs:
            handle.write(json.dumps(pair, ensure_ascii=False, sort_keys=True) + "\n")

    print(f"prompt_groups={len(by_prompt)}")
    print(f"pairs={len(pairs)}")
    print(f"failures={len(failures)}")
    for failure in failures:
        print(f"FAIL: {failure}")
    print(f"output={args.output}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
