import json
import os
import sys
from pathlib import Path

import torch
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
        "Answer",
        "briefly",
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
    fast = PreTrainedTokenizerFast(
        tokenizer_object=tokenizer,
        unk_token="[UNK]",
        pad_token="<pad>",
        bos_token="<bos>",
        eos_token="<eos>",
    )
    return fast


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


def main() -> None:
    os.environ.setdefault("WANDB_DISABLED", "true")

    tokenizer = build_tokenizer()
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
    model = GPT2LMHeadModel(config)

    dataset = build_dataset()
    output_dir = REPO_ROOT / "stage_artifacts" / "stage1" / "local-static-smoke-001-output"
    args = SimPOConfig(
        output_dir=str(output_dir),
        beta=2.0,
        gamma_beta_ratio=0.5,
        loss_type="sigmoid",
        max_length=64,
        max_prompt_length=48,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=1,
        max_steps=2,
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
    )

    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()

    trainer = SimPOTrainer(
        model=model,
        args=args,
        train_dataset=dataset,
        eval_dataset=None,
        tokenizer=tokenizer,
    )

    train_result = trainer.train()
    metrics = train_result.metrics

    summary = {
        "status": "PASS",
        "cuda_available": torch.cuda.is_available(),
        "device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu",
        "torch_cuda": torch.version.cuda,
        "train_loss": metrics.get("train_loss"),
        "global_step": trainer.state.global_step,
        "peak_memory_allocated_mb": (
            round(torch.cuda.max_memory_allocated() / 1024 / 1024, 2) if torch.cuda.is_available() else None
        ),
        "peak_memory_reserved_mb": (
            round(torch.cuda.max_memory_reserved() / 1024 / 1024, 2) if torch.cuda.is_available() else None
        ),
        "metrics": metrics,
    }
    print("SMOKE_SUMMARY " + json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
