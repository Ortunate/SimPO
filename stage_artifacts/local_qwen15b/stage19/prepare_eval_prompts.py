#!/usr/bin/env python3
"""Prepare a bounded local instruction prompt set from existing local data."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pyarrow.parquet as pq


def extract_user_instruction(row: dict[str, Any]) -> str | None:
    for field in ("chosen", "rejected"):
        messages = row.get(field)
        if not isinstance(messages, list):
            continue
        for message in messages:
            if not isinstance(message, dict):
                continue
            if message.get("role") == "user":
                content = message.get("content")
                if isinstance(content, str) and content.strip():
                    return content.strip()
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--limit", default=50, type=int)
    args = parser.parse_args()

    prompts: list[dict[str, Any]] = []
    seen: set[str] = set()
    if args.input.suffix == ".parquet":
        source_rows = enumerate(pq.read_table(args.input).to_pylist(), start=1)
    else:
        def jsonl_rows() -> Any:
            with args.input.open("r", encoding="utf-8") as handle:
                for line_no, line in enumerate(handle, start=1):
                    if line.strip():
                        yield line_no, json.loads(line)

        source_rows = jsonl_rows()

    for line_no, row in source_rows:
        if len(prompts) >= args.limit:
            break
        if isinstance(row, dict):
            instruction = extract_user_instruction(row)
        else:
            instruction = None
        if not instruction or instruction in seen:
            continue
        seen.add(instruction)
        prompts.append(
            {
                "prompt_id": f"uf-test-{len(prompts) + 1:03d}",
                "instruction": instruction,
                "source": "local_trl_ultrafeedback_binarized_test",
                "source_line": line_no,
            }
        )

    if len(prompts) != args.limit:
        raise RuntimeError(f"prepared {len(prompts)} prompts, expected {args.limit}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        for prompt in prompts:
            handle.write(json.dumps(prompt, ensure_ascii=False, sort_keys=True) + "\n")

    print(f"input={args.input}")
    print(f"output={args.output}")
    print(f"prompts={len(prompts)}")
    print("api_calls=0")
    print("downloads=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
