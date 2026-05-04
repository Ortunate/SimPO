import json
import math
import os
import sys
from pathlib import Path

from datasets import Dataset
from tokenizers import Tokenizer
from tokenizers.models import WordLevel
from tokenizers.pre_tokenizers import Whitespace
from transformers import GPT2Config, GPT2LMHeadModel, PreTrainedTokenizerFast


REPO_ROOT = Path(__file__).resolve().parents[2]
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


def run_smoke(name: str, dynamic_gamma_enabled: bool) -> dict:
    tokenizer = build_tokenizer()
    output_dir = REPO_ROOT / "stage_artifacts" / "stage2" / f"{name}-output"
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
        max_steps=1,
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
    train_result = trainer.train()
    step_logs = [entry for entry in trainer.state.log_history if "loss" in entry]
    last_step = step_logs[-1]
    required_values = [last_step["loss"], train_result.metrics["train_loss"]]
    if dynamic_gamma_enabled:
        required_values.extend(
            [
                last_step["gamma_beta_ratio/mean"],
                last_step["gamma_beta_ratio/min"],
                last_step["gamma_beta_ratio/max"],
                last_step["similarity/mean"],
                last_step["similarity/min"],
                last_step["similarity/max"],
            ]
        )
    if not all(math.isfinite(float(value)) for value in required_values):
        raise RuntimeError(f"{name} produced a non-finite metric: {last_step}")
    if dynamic_gamma_enabled and not (0.0 <= last_step["gamma_beta_ratio/min"] <= last_step["gamma_beta_ratio/max"] <= 0.5):
        raise RuntimeError(f"{name} dynamic gamma metrics are out of clamp bounds: {last_step}")
    if not dynamic_gamma_enabled and any(key.startswith("gamma_beta_ratio/") for key in last_step):
        raise RuntimeError(f"{name} static path unexpectedly logged dynamic gamma metrics: {last_step}")
    return {
        "dynamic_gamma_enabled": dynamic_gamma_enabled,
        "train_loss": train_result.metrics["train_loss"],
        "global_step": trainer.state.global_step,
        "last_step": last_step,
    }


def main() -> None:
    artifact_dir = REPO_ROOT / "stage_artifacts" / "stage2"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("HF_HOME", str(artifact_dir / "hf-cache"))
    os.environ.setdefault("WANDB_DISABLED", "true")

    summary = {
        "status": "PASS",
        "static": run_smoke("local-dynamic-gamma-smoke-001-static", dynamic_gamma_enabled=False),
        "dynamic": run_smoke("local-dynamic-gamma-smoke-001-dynamic", dynamic_gamma_enabled=True),
    }
    summary_path = artifact_dir / "local-dynamic-gamma-smoke-001-summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print("DYNAMIC_GAMMA_SMOKE_SUMMARY " + json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
