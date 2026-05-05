#!/usr/bin/env python3
"""Validate the Stage L15 answer generation plan without loading models."""

from __future__ import annotations

import json
from pathlib import Path


def main() -> int:
    path = Path(__file__).with_name("answer_generation_plan.json")
    plan = json.loads(path.read_text(encoding="utf-8"))
    failures: list[str] = []
    if plan.get("run_generation") is not False:
        failures.append("run_generation must be false")
    if plan.get("resource_boundaries", {}).get("no_gpu_action_in_stage_l15") is not True:
        failures.append("no_gpu_action_in_stage_l15 must be true")
    adapters = plan.get("adapters", {})
    for name, adapter in adapters.items():
        adapter_path = Path(adapter.get("path", ""))
        if not adapter_path.exists():
            failures.append(f"adapter path missing for {name}: {adapter_path}")
        if not (adapter_path / "adapter_model.safetensors").exists():
            failures.append(f"adapter_model.safetensors missing for {name}")
    print(f"plan_path={path}")
    print(f"adapter_count={len(adapters)}")
    print(f"failures={len(failures)}")
    for failure in failures:
        print(f"FAIL: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
