#!/usr/bin/env python3
"""Generate bounded local eval responses with static and dynamic adapters."""

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
        values = [int(line.strip()) for line in output.splitlines() if line.strip()]
        return max(values) if values else None
    except Exception:
        return None


def read_prompts(path: Path, limit: int) -> list[dict[str, str]]:
    prompts: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            if len(prompts) >= limit:
                break
            if not line.strip():
                continue
            row = json.loads(line)
            prompt_id = row.get("prompt_id")
            instruction = row.get("instruction")
            if not isinstance(prompt_id, str) or not prompt_id.strip():
                raise ValueError(f"line {line_no}: prompt_id must be a non-empty string")
            if not isinstance(instruction, str) or not instruction.strip():
                raise ValueError(f"line {line_no}: instruction must be a non-empty string")
            prompts.append({"prompt_id": prompt_id, "instruction": instruction})
    if len(prompts) != limit:
        raise RuntimeError(f"loaded {len(prompts)} prompts, expected {limit}")
    return prompts


def load_done(path: Path) -> set[tuple[str, str]]:
    done: set[tuple[str, str]] = set()
    if not path.exists():
        return done
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            prompt_id = row.get("prompt_id")
            variant = row.get("variant")
            if isinstance(prompt_id, str) and isinstance(variant, str):
                done.add((prompt_id, variant))
    return done


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


def generate_variant(
    *,
    variant: str,
    source_stage: str,
    model_path: Path,
    adapter_path: Path,
    prompts: list[dict[str, str]],
    response_path: Path,
    memory_samples: list[dict[str, Any]],
    max_new_tokens: int,
    done: set[tuple[str, str]],
) -> dict[str, Any]:
    started = time.time()
    peak_sample = gpu_memory_mib()
    generated_count = 0
    skipped_count = 0
    tokenizer = None
    model = None
    after_load = None
    try:
        pending = [prompt for prompt in prompts if (prompt["prompt_id"], variant) not in done]
        skipped_count = len(prompts) - len(pending)
        if not pending:
            return {
                "variant": variant,
                "adapter_path": str(adapter_path),
                "records_generated": 0,
                "records_skipped": skipped_count,
                "duration_s": round(time.time() - started, 3),
                "memory_after_load_mib": None,
                "peak_memory_used_mib": peak_sample,
            }
        tokenizer, model = load_model(model_path, adapter_path)
        after_load = gpu_memory_mib()
        if after_load is not None:
            peak_sample = max(peak_sample or 0, after_load)

        with response_path.open("a", encoding="utf-8") as handle:
            for prompt in pending:
                formatted = format_prompt(tokenizer, prompt["instruction"])
                inputs = tokenizer(formatted, return_tensors="pt").to(model.device)
                before_generate = gpu_memory_mib()
                with torch.inference_mode():
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
                record = {
                    "prompt_id": prompt["prompt_id"],
                    "instruction": prompt["instruction"],
                    "variant": variant,
                    "base_model": str(model_path),
                    "adapter_path": str(adapter_path),
                    "response": response,
                    "response_char_len": len(response),
                    "generation_config": {
                        "max_new_tokens": max_new_tokens,
                        "do_sample": False,
                        "temperature": 0.0,
                        "top_p": 1.0,
                        "batch_size": 1,
                    },
                    "provenance": {
                        "stage": "L19",
                        "variant_source_stage": source_stage,
                        "prompt_source": "local_trl_ultrafeedback_binarized_64_16_test",
                    },
                }
                handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
                handle.flush()
                generated_count += 1
                memory_samples.append(
                    {
                        "variant": variant,
                        "prompt_id": prompt["prompt_id"],
                        "before_generate_mib": before_generate,
                        "after_generate_mib": after_generate,
                    }
                )
    finally:
        del model
        del tokenizer
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    return {
        "variant": variant,
        "adapter_path": str(adapter_path),
        "records_generated": generated_count,
        "records_skipped": skipped_count,
        "duration_s": round(time.time() - started, 3),
        "memory_after_load_mib": after_load,
        "peak_memory_used_mib": peak_sample,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", required=True, type=Path)
    parser.add_argument("--prompts", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--prompt-count", default=50, type=int)
    parser.add_argument("--max-new-tokens", default=256, type=int)
    args = parser.parse_args()

    started = time.time()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    response_path = args.out_dir / "responses.jsonl"
    prompts = read_prompts(args.prompts, args.prompt_count)
    done = load_done(response_path)
    memory_samples: list[dict[str, Any]] = []
    run_summaries: list[dict[str, Any]] = []

    for variant, spec in VARIANTS.items():
        summary = generate_variant(
            variant=variant,
            source_stage=spec["source_stage"],
            model_path=args.model_path,
            adapter_path=Path(spec["adapter_path"]),
            prompts=prompts,
            response_path=response_path,
            memory_samples=memory_samples,
            max_new_tokens=args.max_new_tokens,
            done=done,
        )
        run_summaries.append(summary)
        done = load_done(response_path)

    expected_records = args.prompt_count * len(VARIANTS)
    actual_records = sum(1 for line in response_path.open("r", encoding="utf-8") if line.strip())
    summary = {
        "stage": "L19",
        "api_calls": 0,
        "training_steps": 0,
        "model_path": str(args.model_path),
        "prompt_path": str(args.prompts),
        "prompt_count": args.prompt_count,
        "expected_response_count": expected_records,
        "actual_response_count": actual_records,
        "complete": actual_records == expected_records,
        "max_new_tokens": args.max_new_tokens,
        "variants": run_summaries,
        "peak_memory_used_mib": max(
            [item["peak_memory_used_mib"] for item in run_summaries if item["peak_memory_used_mib"] is not None],
            default=None,
        ),
        "duration_s": round(time.time() - started, 3),
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
    return 0 if summary["complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
