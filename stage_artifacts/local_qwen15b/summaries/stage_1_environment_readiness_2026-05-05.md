# Stage L1 Environment Readiness Summary

Date: 2026-05-05

Branch: `local-qwen15b-qlora`

Status: audit PASS; execution readiness PARTIAL

## Key Findings
- OS: Ubuntu 24.04.2 LTS on WSL2 kernel `5.15.167.4-microsoft-standard-WSL2`.
- System Python: `/usr/bin/python3`, version 3.12.3, no target training packages installed.
- Repo venv Python: `.venv/bin/python`, version 3.10.19.
- `VIRTUAL_ENV` is unset in the current shell.
- GPU visible to `nvidia-smi`: NVIDIA GeForce RTX 4090 Laptop GPU, 16376 MiB total VRAM, driver 595.79.
- `.venv` PyTorch: 2.2.2+cu121, but `torch.cuda.is_available()` is `False`.
- CUDA warning from PyTorch: `Can't initialize NVML`.
- `/dev/dxg` was absent during this check.
- `bitsandbytes` is not installed.
- `deepspeed` is not installed.
- `.env` exists and is ignored.
- `DEEPSEEK_API_KEY` is present in `.env`; no value was printed.
- No mirror variables were configured in process env or `.env`.
- No Hugging Face or ModelScope cache directory was found.

## Installed Packages in `.venv`
- torch: 2.2.2
- transformers: 4.44.2
- datasets: 2.18.0
- accelerate: 0.29.2
- trl: 0.9.6
- peft: 0.7.1
- bitsandbytes: not installed
- deepspeed: not installed

## Recommendation
Stage L2 should be a recovery/readiness planning stage:

1. Diagnose CUDA visibility mismatch between `nvidia-smi` and PyTorch.
2. Plan `bitsandbytes` installation compatibility without installing until approved.
3. Draft Qwen2.5-1.5B QLoRA static config placeholders without downloading or loading model/data.

No model, dataset, API call, GPU-heavy command, training run, dependency install, or system configuration change was performed.
