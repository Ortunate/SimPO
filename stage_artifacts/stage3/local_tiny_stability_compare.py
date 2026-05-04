import argparse
import json
import math
import os
import resource
import subprocess
import sys
import time
from pathlib import Path

from datasets import Dataset
from tokenizers import Tokenizer
from tokenizers.models import WordLevel
from tokenizers.pre_tokenizers import Whitespace
from transformers import GPT2Config, GPT2LMHeadModel, PreTrainedTokenizerFast, set_seed


REPO_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = REPO_ROOT / "stage_artifacts" / "stage3"
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from simpo_config import SimPOConfig
from simpo_trainer import SimPOTrainer


def build_tokenizer() -> PreTrainedTokenizerFast:
    tokens = [
        "[UNK]",
        "<pad>",
        "<bos>",
        "<eos>",
        "User",
        ":",
        "Assistant",
        "Say",
        "hello",
        ".",
        "Hello",
        "there",
        "Goodbye",
        "Give",
        "a",
        "color",
        "Blue",
        "Stone",
        "Name",
        "fruit",
        "Apple",
        "Chair",
        "Pick",
        "number",
        "Seven",
        "Cloud",
        "Briefly",
        "answer",
        "yes",
        "Yes",
        "No",
        "List",
        "animal",
        "Cat",
        "Table",
    ]
    vocab = {token: idx for idx, token in enumerate(tokens)}
    tokenizer = Tokenizer(WordLevel(vocab=vocab, unk_token="[UNK]"))
    tokenizer.pre_tokenizer = Whitespace()
    return PreTrainedTokenizerFast(
        tokenizer_object=tokenizer,
        unk_token="[UNK]",
        pad_token="<pad>",
        bos_token="<bos>",
        eos_token="<eos>",
    )


def build_dataset() -> Dataset:
    return Dataset.from_list(
        [
            {
                "prompt": "User: Say hello. Assistant: ",
                "chosen": "Hello there.",
                "rejected": "Goodbye.",
            },
            {
                "prompt": "User: Give a color. Assistant: ",
                "chosen": "Blue.",
                "rejected": "Stone.",
            },
            {
                "prompt": "User: Name a fruit. Assistant: ",
                "chosen": "Apple.",
                "rejected": "Chair.",
            },
            {
                "prompt": "User: Pick a number. Assistant: ",
                "chosen": "Seven.",
                "rejected": "Cloud.",
            },
            {
                "prompt": "User: Briefly answer yes. Assistant: ",
                "chosen": "Yes.",
                "rejected": "No.",
            },
            {
                "prompt": "User: List animal. Assistant: ",
                "chosen": "Cat.",
                "rejected": "Table.",
            },
        ]
    )


def build_model(tokenizer: PreTrainedTokenizerFast) -> GPT2LMHeadModel:
    config = GPT2Config(
        vocab_size=len(tokenizer),
        n_positions=64,
        n_ctx=64,
        n_embd=32,
        n_layer=2,
        n_head=4,
        bos_token_id=tokenizer.bos_token_id,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.pad_token_id,
    )
    return GPT2LMHeadModel(config)


def finite_values(values: list[float]) -> bool:
    return all(math.isfinite(float(value)) for value in values)


def run_variant(variant: str) -> dict:
    dynamic_gamma_enabled = variant == "dynamic"
    set_seed(42)
    tokenizer = build_tokenizer()
    output_dir = ARTIFACT_DIR / f"local-tiny-stability-001-{variant}-output"
    args = SimPOConfig(
        output_dir=str(output_dir),
        beta=2.0,
        gamma_beta_ratio=0.5,
        dynamic_gamma_enabled=dynamic_gamma_enabled,
        dynamic_gamma_strategy="sim_linear",
        dynamic_gamma_similarity_scale=0.5,
        dynamic_gamma_min=0.0,
        dynamic_gamma_max=0.5,
        loss_type="sigmoid",
        max_length=64,
        max_prompt_length=48,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=1,
        max_steps=6,
        learning_rate=1e-5,
        logging_steps=1,
        logging_strategy="steps",
        save_strategy="no",
        do_eval=False,
        report_to=[],
        remove_unused_columns=False,
        disable_tqdm=True,
        seed=42,
        dataloader_num_workers=0,
        fp16=False,
        bf16=False,
        use_cpu=True,
    )
    trainer = SimPOTrainer(
        model=build_model(tokenizer),
        args=args,
        train_dataset=build_dataset(),
        eval_dataset=None,
        tokenizer=tokenizer,
    )
    started = time.perf_counter()
    train_result = trainer.train()
    runtime_s = time.perf_counter() - started
    step_logs = [entry for entry in trainer.state.log_history if "loss" in entry]
    if len(step_logs) != args.max_steps:
        raise RuntimeError(f"{variant} logged {len(step_logs)} loss steps, expected {args.max_steps}")

    losses = [float(entry["loss"]) for entry in step_logs]
    grad_norms = [float(entry["grad_norm"]) for entry in step_logs if "grad_norm" in entry]
    if not finite_values(losses + grad_norms + [train_result.metrics["train_loss"]]):
        raise RuntimeError(f"{variant} produced non-finite loss or grad metrics")
    if max(losses) > 50.0:
        raise RuntimeError(f"{variant} loss exceeded stability guard: {max(losses)}")

    result = {
        "variant": variant,
        "dynamic_gamma_enabled": dynamic_gamma_enabled,
        "status": "PASS",
        "global_step": trainer.state.global_step,
        "train_loss": float(train_result.metrics["train_loss"]),
        "loss_first": losses[0],
        "loss_last": losses[-1],
        "loss_min": min(losses),
        "loss_max": max(losses),
        "loss_values": losses,
        "grad_norm_values": grad_norms,
        "grad_norm_max": max(grad_norms) if grad_norms else None,
        "runtime_s": runtime_s,
        "max_rss_mb": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0,
        "last_step": step_logs[-1],
    }

    if dynamic_gamma_enabled:
        gamma_means = [float(entry["gamma_beta_ratio/mean"]) for entry in step_logs]
        gamma_mins = [float(entry["gamma_beta_ratio/min"]) for entry in step_logs]
        gamma_maxs = [float(entry["gamma_beta_ratio/max"]) for entry in step_logs]
        similarity_means = [float(entry["similarity/mean"]) for entry in step_logs]
        similarity_mins = [float(entry["similarity/min"]) for entry in step_logs]
        similarity_maxs = [float(entry["similarity/max"]) for entry in step_logs]
        dynamic_values = (
            gamma_means
            + gamma_mins
            + gamma_maxs
            + similarity_means
            + similarity_mins
            + similarity_maxs
        )
        if not finite_values(dynamic_values):
            raise RuntimeError(f"{variant} produced non-finite dynamic metrics")
        if min(gamma_mins) < 0.0 or max(gamma_maxs) > 0.5:
            raise RuntimeError(f"{variant} gamma escaped clamp bounds")
        if min(similarity_mins) < -1.0001 or max(similarity_maxs) > 1.0001:
            raise RuntimeError(f"{variant} similarity escaped cosine bounds")
        result.update(
            {
                "gamma_mean_values": gamma_means,
                "gamma_min": min(gamma_mins),
                "gamma_max": max(gamma_maxs),
                "similarity_mean_values": similarity_means,
                "similarity_min": min(similarity_mins),
                "similarity_max": max(similarity_maxs),
            }
        )
    else:
        dynamic_keys = [
            key
            for entry in step_logs
            for key in entry
            if key.startswith("gamma_beta_ratio/") or key.startswith("similarity/")
        ]
        if dynamic_keys:
            raise RuntimeError(f"{variant} unexpectedly logged dynamic keys: {dynamic_keys}")

    variant_path = ARTIFACT_DIR / f"local-tiny-stability-001-{variant}.json"
    variant_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def run_driver() -> None:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.setdefault("HF_HOME", str(ARTIFACT_DIR / "hf-cache"))
    env.setdefault("TRANSFORMERS_CACHE", str(ARTIFACT_DIR / "hf-cache" / "transformers"))
    env.setdefault("WANDB_DISABLED", "true")

    results = {}
    for variant in ("static", "dynamic"):
        command = [sys.executable, __file__, "--variant", variant]
        completed = subprocess.run(
            command,
            cwd=str(REPO_ROOT),
            check=True,
            env=env,
            capture_output=True,
            text=True,
        )
        print(completed.stdout, end="")
        if completed.stderr:
            print(completed.stderr, file=sys.stderr, end="")
        result_path = ARTIFACT_DIR / f"local-tiny-stability-001-{variant}.json"
        results[variant] = json.loads(result_path.read_text())

    static = results["static"]
    dynamic = results["dynamic"]
    memory_delta_mb = dynamic["max_rss_mb"] - static["max_rss_mb"]
    summary = {
        "status": "PASS",
        "experiment_id": "local-tiny-stability-001",
        "scope": "cpu_tiny_synthetic",
        "static": static,
        "dynamic": dynamic,
        "memory_delta_mb_dynamic_minus_static": memory_delta_mb,
        "notes": [
            "Each variant ran in a separate Python subprocess for isolated max RSS.",
            "No GPU, model download, dataset download, or 8B/9B model was used.",
            "CPU RSS is not a substitute for real GPU VRAM measurement.",
        ],
    }
    summary_path = ARTIFACT_DIR / "local-tiny-stability-001-summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print("LOCAL_TINY_STABILITY_SUMMARY " + json.dumps(summary, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant", choices=("static", "dynamic"))
    args = parser.parse_args()
    if args.variant:
        ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
        result = run_variant(args.variant)
        print("VARIANT_SUMMARY " + json.dumps(result, sort_keys=True))
    else:
        run_driver()


if __name__ == "__main__":
    main()
