# Stage L2 Dependency Approval Plan

Date: 2026-05-05

## Purpose
Define the minimal dependency action needed before local Qwen2.5-1.5B QLoRA can run.

This is a plan only. No dependency was installed or upgraded in Stage L2.

## Current Environment
Python:

- `.venv/bin/python`
- Python 3.10.19

Installed packages:

- torch 2.2.2+cu121
- transformers 4.44.2
- datasets 2.18.0
- accelerate 0.29.2
- trl 0.9.6
- peft 0.7.1

Missing packages:

- bitsandbytes
- deepspeed

## Minimal Proposed Dependency Action
Install `bitsandbytes` into the repository `.venv`.

Rationale:

- QLoRA requires 4-bit quantization support.
- Repository code already uses `BitsAndBytesConfig` when `load_in_4bit: true`.
- `bitsandbytes` is absent, so any real QLoRA run would fail before training.

## Version Decision
Use one of these only after human approval:

- Conservative repo-aligned option: `bitsandbytes==0.41.2.post2`, because `environment.yml` already pins it.
- Revised option: a newer version selected after an approved compatibility check against the existing `torch==2.2.2+cu121` environment.

Do not change torch, CUDA, transformers, accelerate, TRL, PEFT, WSL, driver, or system packages as part of the minimal first attempt unless separately approved.

## Validation After Approved Install
Run lightweight checks only:

```bash
.venv/bin/python -c "import bitsandbytes as bnb; print('bitsandbytes import: ok'); print(getattr(bnb, '__version__', '<unknown>'))"
.venv/bin/python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else '<none>')"
```

If the CUDA check needs sandbox-external execution, request approval for that exact lightweight diagnostic.

## Stop Conditions
Stop and report before proceeding if:

- `bitsandbytes` import fails
- CUDA is unavailable outside the sandbox
- installation attempts to upgrade torch/CUDA/transformers/accelerate/TRL/PEFT unexpectedly
- network access or package source is uncertain
- installation requires system-level packages

## Explicit Non-Actions
This plan does not approve:

- model downloads
- dataset downloads
- Qwen2.5-1.5B loading
- GPU training
- DeepSeek API calls
- benchmark runs
- full fine-tuning
