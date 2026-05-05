#!/usr/bin/env python3
"""Generate tiny local responses with static and dynamic adapters."""

from __future__ import annotations

import argparse
import gc
import json
import subprocess
import time
from pathlib import Path
from typing import Any

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig


VARIANTS = {
    "static_64_16_20step": {
        "adapter_path": "stage_artifacts/local_qwen15b/outputs/stage10_static_64_16_20step",
        "source_stage": "L10",
    },
    "dynamic_64_16_20step": {
        "adapter_path": "stage_artifacts/local_qwen15b/outputs/stage11_dynamic_64_16_20step",
        "source_stage": "L11",
    },
}


def gpu_memory_mib() -> int | None:
    try:
        output = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
            text=True,
            timeout=5,
        )
        return max(int(line.strip()) for line in output.splitlines() if line.strip())
    except Exception:
        return None


def read_prompts(path: Path) -> list[dict[str, str]]:
    prompts: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            row = json.loads(line)
            for key in ("prompt_id", "instruction"):
                value = row.get(key)
                if not isinstance(value, str) or not value.strip():
                    raise ValueError(f"line {line_no}: {key} must be a non-empty string")
            prompts.append({"prompt_id": row["prompt_id"], "instruction": row["instruction"]})
    return prompts


def format_prompt(tokenizer: Any, instruction: str) -> str:
    messages = [{"role": "user", "content": instruction}]
    return tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)


def load_model(model_path: Path, adapter_path: Path) -> tuple[Any, Any]:
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
    )
    tokenizer = AutoTokenizer.from_pretrained(
        model_path,
        trust_remote_code=False,
        local_files_only=True,
    )
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    base_model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        quantization_config=quantization_config,
        trust_remote_code=False,
        local_files_only=True,
    )
    model = PeftModel.from_pretrained(base_model, adapter_path, local_files_only=True)
    model.eval()
    return tokenizer, model


def generate_for_variant(
    *,
    variant: str,
    model_path: Path,
    adapter_path: Path,
    prompts: list[dict[str, str]],
    max_new_tokens: int,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    started = time.time()
    samples: list[dict[str, Any]] = []
    peak_sample = gpu_memory_mib()
    tokenizer, model = load_model(model_path, adapter_path)
    after_load = gpu_memory_mib()
    if after_load is not None:
        peak_sample = max(peak_sample or 0, after_load)

    records: list[dict[str, Any]] = []
    for prompt in prompts:
        formatted = format_prompt(tokenizer, prompt["instruction"])
        inputs = tokenizer(formatted, return_tensors="pt").to(model.device)
        before_generate = gpu_memory_mib()
        generated = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            temperature=None,
            top_p=None,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )
        after_generate = gpu_memory_mib()
        for value in (before_generate, after_generate):
            if value is not None:
                peak_sample = max(peak_sample or 0, value)
        new_tokens = generated[0, inputs["input_ids"].shape[-1] :]
        response = tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
        records.append(
            {
                "prompt_id": prompt["prompt_id"],
                "instruction": prompt["instruction"],
                "variant": variant,
                "base_model": str(model_path),
                "adapter_path": str(adapter_path),
                "response": response,
                "generation_config": {
                    "max_new_tokens": max_new_tokens,
                    "do_sample": False,
                    "temperature": 0.0,
                    "top_p": 1.0,
                    "batch_size": 1,
                },
                "provenance": {
                    "stage": "L16",
                    "source": "synthetic_generation_prompts",
                },
            }
        )
        samples.append(
            {
                "variant": variant,
                "prompt_id": prompt["prompt_id"],
                "before_generate_mib": before_generate,
                "after_generate_mib": after_generate,
            }
        )

    del model
    del tokenizer
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    ended = time.time()
    summary = {
        "variant": variant,
        "adapter_path": str(adapter_path),
        "records": len(records),
        "duration_s": round(ended - started, 3),
        "memory_after_load_mib": after_load,
        "peak_memory_used_mib": peak_sample,
    }
    return records, {"summary": summary, "samples": samples}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", required=True, type=Path)
    parser.add_argument("--prompts", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--max-new-tokens", default=128, type=int)
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    prompts = read_prompts(args.prompts)
    all_records: list[dict[str, Any]] = []
    run_summaries: list[dict[str, Any]] = []
    memory_samples: list[dict[str, Any]] = []

    for variant, spec in VARIANTS.items():
        records, evidence = generate_for_variant(
            variant=variant,
            model_path=args.model_path,
            adapter_path=Path(spec["adapter_path"]),
            prompts=prompts,
            max_new_tokens=args.max_new_tokens,
        )
        all_records.extend(records)
        run_summaries.append(evidence["summary"])
        memory_samples.extend(evidence["samples"])

    response_path = args.out_dir / "tiny_generation_responses.jsonl"
    with response_path.open("w", encoding="utf-8") as handle:
        for record in all_records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

    summary = {
        "stage": "L16",
        "api_calls": 0,
        "training_steps": 0,
        "model_path": str(args.model_path),
        "prompt_count": len(prompts),
        "response_count": len(all_records),
        "max_new_tokens": args.max_new_tokens,
        "variants": run_summaries,
        "peak_memory_used_mib": max(
            [item["peak_memory_used_mib"] for item in run_summaries if item["peak_memory_used_mib"] is not None],
            default=None,
        ),
        "response_path": str(response_path),
    }
    (args.out_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (args.out_dir / "gpu_samples.json").write_text(
        json.dumps(memory_samples, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
