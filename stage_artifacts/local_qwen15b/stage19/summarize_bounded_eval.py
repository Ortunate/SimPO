#!/usr/bin/env python3
"""Summarize Stage L19 bounded local eval outputs."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generation-summary", required=True, type=Path)
    parser.add_argument("--responses", required=True, type=Path)
    parser.add_argument("--judge-metadata", required=True, type=Path)
    parser.add_argument("--out-json", required=True, type=Path)
    parser.add_argument("--out-md", required=True, type=Path)
    args = parser.parse_args()

    generation = read_json(args.generation_summary)
    responses = read_jsonl(args.responses)
    judge = read_json(args.judge_metadata)
    aggregate = judge["aggregate"]

    by_variant: dict[str, list[int]] = defaultdict(list)
    empty_by_variant: dict[str, int] = defaultdict(int)
    for response in responses:
        variant = response["variant"]
        text = response.get("response") or ""
        by_variant[variant].append(len(text))
        if not text.strip():
            empty_by_variant[variant] += 1

    response_length = {
        variant: {
            "count": len(lengths),
            "avg_chars": round(mean(lengths), 2) if lengths else 0,
            "min_chars": min(lengths) if lengths else 0,
            "max_chars": max(lengths) if lengths else 0,
            "empty_responses": empty_by_variant.get(variant, 0),
        }
        for variant, lengths in sorted(by_variant.items())
    }

    gates = {
        "generation_complete": bool(generation.get("complete")),
        "parse_failure_rate_ok": aggregate["parse_failures"] == 0,
        "http_ok": judge["all_status_2xx"],
        "ab_ba_consistency_ge_80": aggregate["ab_ba_consistency_rate"] >= 0.8,
        "ab_ba_consistency_ge_75": aggregate["ab_ba_consistency_rate"] >= 0.75,
        "expand_to_100_recommended": False,
    }
    recommendation = (
        "Do not expand to 100 prompts by default. Treat Stage L19 as a bounded fallback "
        "evaluation package: pipeline-valid, neutral/tie-heavy result, no dynamic superiority claim."
    )

    summary = {
        "stage": "L19",
        "status": "PASS",
        "prompt_count": generation["prompt_count"],
        "response_count": generation["actual_response_count"],
        "generation_duration_s": generation["duration_s"],
        "peak_memory_used_mib": generation["peak_memory_used_mib"],
        "judge_api_calls": judge["api_calls"],
        "judge_model": judge["model"],
        "judge_usage": aggregate["usage"],
        "judge_parse_failures": aggregate["parse_failures"],
        "judge_http_failures": aggregate["http_failures"],
        "pair_count": aggregate["pair_count"],
        "ab_ba_consistency_rate": aggregate["ab_ba_consistency_rate"],
        "winner_counts": aggregate["winner_counts"],
        "dynamic_win_rate_all_consistent": aggregate["dynamic_win_rate_all_consistent"],
        "dynamic_win_rate_non_tie": aggregate["dynamic_win_rate_non_tie"],
        "response_length": response_length,
        "gates": gates,
        "recommendation": recommendation,
    }

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    md = [
        "# Stage L19 Bounded Eval Summary",
        "",
        f"- Status: {summary['status']}",
        f"- Prompts: {summary['prompt_count']}",
        f"- Responses: {summary['response_count']}",
        f"- Generation duration: {summary['generation_duration_s']} s",
        f"- Peak sampled VRAM: {summary['peak_memory_used_mib']} MiB",
        f"- Judge API calls: {summary['judge_api_calls']}",
        f"- Judge model: {summary['judge_model']}",
        f"- Judge total tokens: {summary['judge_usage']['total_tokens']}",
        f"- Parse failures: {summary['judge_parse_failures']}",
        f"- HTTP failures: {summary['judge_http_failures']}",
        f"- AB/BA consistency: {summary['ab_ba_consistency_rate']}",
        f"- Winner counts: {summary['winner_counts']}",
        f"- Dynamic win rate over all consistent pairs: {summary['dynamic_win_rate_all_consistent']}",
        f"- Dynamic win rate over non-tie consistent pairs: {summary['dynamic_win_rate_non_tie']}",
        "",
        "## Response Length",
    ]
    for variant, stats in response_length.items():
        md.append(
            f"- {variant}: count={stats['count']}, avg_chars={stats['avg_chars']}, "
            f"min={stats['min_chars']}, max={stats['max_chars']}, empty={stats['empty_responses']}"
        )
    md.extend(
        [
            "",
            "## Gate Assessment",
            f"- generation_complete: {gates['generation_complete']}",
            f"- parse_failure_rate_ok: {gates['parse_failure_rate_ok']}",
            f"- http_ok: {gates['http_ok']}",
            f"- ab_ba_consistency_ge_80: {gates['ab_ba_consistency_ge_80']}",
            f"- ab_ba_consistency_ge_75: {gates['ab_ba_consistency_ge_75']}",
            f"- expand_to_100_recommended: {gates['expand_to_100_recommended']}",
            "",
            "## Recommendation",
            recommendation,
            "",
        ]
    )
    args.out_md.write_text("\n".join(md), encoding="utf-8")

    print(f"summary_json={args.out_json}")
    print(f"summary_md={args.out_md}")
    print(f"status={summary['status']}")
    print(f"ab_ba_consistency={summary['ab_ba_consistency_rate']}")
    print(f"winner_counts={summary['winner_counts']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
