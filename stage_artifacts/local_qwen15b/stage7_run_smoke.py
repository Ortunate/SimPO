#!/usr/bin/env python3
"""Run one approved local Qwen2.5-1.5B QLoRA smoke and sample VRAM."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def query_gpu() -> dict[str, object] | None:
    cmd = [
        "nvidia-smi",
        "--query-gpu=timestamp,name,memory.used,memory.total,utilization.gpu",
        "--format=csv,noheader,nounits",
    ]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=5)
    except Exception as exc:  # noqa: BLE001 - report sampler failures without killing training
        return {"error": str(exc)}

    line = result.stdout.strip().splitlines()[0] if result.stdout.strip() else ""
    parts = [part.strip() for part in line.split(",")]
    if len(parts) < 5:
        return {"raw": line}
    return {
        "timestamp": parts[0],
        "name": parts[1],
        "memory_used_mib": int(parts[2]),
        "memory_total_mib": int(parts[3]),
        "utilization_gpu_percent": int(parts[4]),
    }


def sampler(stop: threading.Event, out_path: Path, interval_s: float) -> None:
    with out_path.open("w", encoding="utf-8") as handle:
        while not stop.is_set():
            sample = query_gpu()
            if sample is not None:
                sample["monotonic_s"] = time.monotonic()
                handle.write(json.dumps(sample, ensure_ascii=False) + "\n")
                handle.flush()
            stop.wait(interval_s)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", required=True, choices=["static", "dynamic"])
    parser.add_argument("--config", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--sample-interval", type=float, default=1.0)
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    stdout_path = out_dir / "stdout.log"
    stderr_path = out_dir / "stderr.log"
    samples_path = out_dir / "gpu_samples.jsonl"
    summary_path = out_dir / "summary.json"

    env = os.environ.copy()
    env.update(
        {
            "HF_HOME": str(ROOT / "stage_artifacts/local_qwen15b/hf-cache"),
            "HF_HUB_CACHE": str(ROOT / "stage_artifacts/local_qwen15b/hf-cache/hub"),
            "HF_DATASETS_CACHE": str(ROOT / "stage_artifacts/local_qwen15b/hf-cache/datasets"),
            "HF_ENDPOINT": "https://hf-mirror.com",
            "HF_HUB_DISABLE_XET": "1",
            "TOKENIZERS_PARALLELISM": "false",
        }
    )
    existing_pythonpath = env.get("PYTHONPATH")
    env["PYTHONPATH"] = str(ROOT) if not existing_pythonpath else f"{ROOT}:{existing_pythonpath}"

    cmd = [
        str(ROOT / ".venv/bin/python"),
        str(ROOT / "scripts/run_simpo.py"),
        str(ROOT / args.config),
    ]

    start_wall = time.strftime("%Y-%m-%d %H:%M:%S %z")
    start = time.monotonic()
    stop = threading.Event()
    thread = threading.Thread(target=sampler, args=(stop, samples_path, args.sample_interval), daemon=True)
    thread.start()

    with stdout_path.open("w", encoding="utf-8") as stdout, stderr_path.open("w", encoding="utf-8") as stderr:
        proc = subprocess.Popen(cmd, cwd=ROOT, env=env, stdout=stdout, stderr=stderr, text=True)
        returncode = proc.wait()

    stop.set()
    thread.join(timeout=5)
    end_wall = time.strftime("%Y-%m-%d %H:%M:%S %z")
    duration_s = time.monotonic() - start

    peak_mib = None
    sample_count = 0
    if samples_path.exists():
        for line in samples_path.read_text(encoding="utf-8").splitlines():
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue
            if "memory_used_mib" in item:
                sample_count += 1
                peak_mib = max(peak_mib or 0, int(item["memory_used_mib"]))

    summary = {
        "label": args.label,
        "config": args.config,
        "command": cmd,
        "returncode": returncode,
        "start_wall": start_wall,
        "end_wall": end_wall,
        "duration_s": round(duration_s, 3),
        "gpu_sample_count": sample_count,
        "peak_memory_used_mib": peak_mib,
        "stdout": str(stdout_path),
        "stderr": str(stderr_path),
        "gpu_samples": str(samples_path),
    }
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return returncode


if __name__ == "__main__":
    sys.exit(main())
