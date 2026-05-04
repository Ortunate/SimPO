# Experiment ID
local-tiny-gpu-memory-001

## Date
2026-05-04

## Owner
Codex

## Objective
Why this run exists:

Recover the Stage 3 memory-validation gap by running a bounded tiny GPU memory comparison between static SimPO and dynamic gamma.

Decision this run should support:

Whether the dynamic `sim_linear` path introduces an obvious CUDA memory overhead in a tiny local smoke test, and whether CUDA visibility is usable outside the execution sandbox.

## Variant
Type:
- baseline and dynamic

Strategy:
- static
- sim_linear

Hypothesis:

Both variants should complete 3 tiny GPU steps with finite loss/gradient metrics. Dynamic gamma should log finite gamma and similarity metrics, and peak reserved CUDA memory should stay below the 1GB guard.

## Code State
Branch:

main

Commit:

1b3e8f3

Dirty working tree:
- yes

Key files changed:

- `scripts/simpo_config.py`
- `scripts/simpo_trainer.py`
- `stage_artifacts/stage3/local_tiny_gpu_memory_compare.py`
- `docs_for_agent/experiment_logs/local-tiny-gpu-memory-001.md`

Patch summary:

Stage 2 dynamic gamma implementation remains unchanged. This Stage 3 recovery added a tiny GPU memory comparison artifact script only.

## Environment
Machine:

Local WSL2 development node.

OS:

Linux `5.15.167.4-microsoft-standard-WSL2`, Ubuntu userspace.

WSL version:

WSL2 kernel detected.

Python:

`.venv` CPython 3.10.19

CUDA:

PyTorch build CUDA 12.1. `nvidia-smi` reports CUDA Version 13.2 from driver capability.

Driver:

595.79

GPU:

NVIDIA GeForce RTX 4090 Laptop GPU

Detected VRAM:

16375.5 MiB visible to PyTorch; `nvidia-smi` reported 16376 MiB.

PyTorch:

2.2.2+cu121

Transformers:

4.44.2

TRL:

0.9.6

Other relevant packages:

`datasets==2.18.0`, `peft==0.7.1`

## Data
Dataset:

Synthetic local preference data embedded in `stage_artifacts/stage3/local_tiny_gpu_memory_compare.py`.

Split:

train only

Sample size or ratio:

3 preference pairs

Max sequence length:

64

Preprocessing notes:

Uses a local WordLevel tokenizer and a random tiny GPT-2 model. No external dataset or model download is used.

## Run Config
Base model:

Random tiny GPT-2

Precision:

fp32

Quantization:

none

LoRA / QLoRA:

none

Batch size:

1

Gradient accumulation:

1

Learning rate:

1e-5

Scheduler:

Default Trainer scheduler

Warmup:

0

Epochs or max steps:

3 steps per variant

Seed:

42

Checkpoint policy:

`save_strategy="no"`

Logging policy:

stdout plus JSON summaries under `stage_artifacts/stage3/`

## Dynamic Gamma Settings
Enabled:
- yes for dynamic variant
- no for static variant

Similarity source:

LM-head input hidden states captured from the existing forward pass.

Hidden-state extraction point:

Temporary forward pre-hook on `model.get_output_embeddings()`.

Pooling / token selection:

Mean-pool response tokens where labels are not `label_pad_token_id`.

Gamma strategy:

`sim_linear`

Gamma min:

0.0

Gamma max:

0.5

Clamp / threshold rule:

Clamp effective gamma/beta ratio to `[0.0, 0.5]`.

Curriculum rule:

none

Logging fields:

`gamma_beta_ratio/mean`, `gamma_beta_ratio/min`, `gamma_beta_ratio/max`, `similarity/mean`, `similarity/min`, `similarity/max`

## Commands
Exact commands:

    .venv/bin/python -c 'import torch, ctypes; print("torch", torch.__version__); print("torch_cuda_build", torch.version.cuda); print("cuda_available", torch.cuda.is_available()); print("device_count", torch.cuda.device_count()); lib=ctypes.CDLL("libcuda.so.1"); print("cuInit", lib.cuInit(0))'
    .venv/bin/python -m py_compile stage_artifacts/stage3/local_tiny_gpu_memory_compare.py
    HF_HOME=stage_artifacts/stage3/hf-cache WANDB_DISABLED=true .venv/bin/python stage_artifacts/stage3/local_tiny_gpu_memory_compare.py

Note:

The CUDA visibility check and GPU smoke were run outside the execution sandbox with CLI approval because the sandbox did not expose the CUDA device. They did not modify the environment.

## Expected Healthy Behavior
Expected memory:

Peak reserved CUDA memory below 1GB per variant.

Expected loss behavior:

Finite loss for both variants, no obvious divergence.

Expected gamma behavior:

Dynamic gamma finite and clamped within `[0.0, 0.5]`; static control should not log dynamic gamma/similarity metrics.

Expected runtime:

Seconds.

## Actual Outcome
Run status:
- PASS

Summary:

Static and dynamic variants both completed 3 tiny GPU steps. Peak reserved CUDA memory was 22.0 MB for both variants. Dynamic gamma metrics were finite and inside configured bounds.

## Metrics
Peak VRAM:

- static max reserved CUDA memory: `22.0` MB
- dynamic max reserved CUDA memory: `22.0` MB

Baseline peak VRAM, if applicable:

`22.0` MB

Memory delta:

Dynamic minus static max reserved CUDA memory: `0.0` MB

Loss trend:

- static loss values: `[1.4129, 1.2753, 1.2603]`
- dynamic loss values: `[1.0948, 0.969, 0.9704]`

Gradient norm trend:

- static max grad norm: `12.718899726867676`
- dynamic max grad norm: `11.186634063720703`

Gamma mean / min / max:

- dynamic gamma mean values: `[0.27681225538253784, 0.27203166484832764, 0.2836344242095947]`
- dynamic gamma min: `0.27203166484832764`
- dynamic gamma max: `0.2836344242095947`

Similarity mean / min / max:

- similarity mean values: `[0.7855019569396973, 0.8237468004226685, 0.7309247255325317]`
- similarity min: `0.7309247255325317`
- similarity max: `0.8237468004226685`

Throughput:

- static: `5.046` steps/s from Trainer summary
- dynamic: `7.29` steps/s from Trainer summary

Runtime:

- static variant measured runtime: `0.6667491660000451` seconds
- dynamic variant measured runtime: `0.4821848390001833` seconds

## Stability Check
OOM:
- no

NaN / Inf:
- no

Loss divergence:
- no

Gradient explosion:
- no

Abnormal logs:
- no blocking abnormal logs. A non-blocking Transformers tokenizer cleanup deprecation warning was printed.

## Artifacts
Log path:

`docs_for_agent/experiment_logs/local-tiny-gpu-memory-001.md`

Config path:

Embedded in `stage_artifacts/stage3/local_tiny_gpu_memory_compare.py`

Checkpoint path:

None. Checkpoint saving disabled.

TensorBoard / W&B path:

None. W&B disabled.

Plot path:

None.

Other artifact paths:

- `stage_artifacts/stage3/local_tiny_gpu_memory_compare.py`
- `stage_artifacts/stage3/local-tiny-gpu-memory-001-static.json`
- `stage_artifacts/stage3/local-tiny-gpu-memory-001-dynamic.json`
- `stage_artifacts/stage3/local-tiny-gpu-memory-001-summary.json`

## Interpretation
What this experiment suggests:

At tiny scale, dynamic gamma does not add measurable CUDA peak reserved memory over static SimPO in this setup and remains numerically stable.

What it does not prove:

It does not prove 8B/9B memory overhead, real UltraFeedback behavior, PEFT/FSDP/DeepSpeed compatibility, or benchmark impact.

## Next Action
Exact next step:

Promote Stage 3 to PASS for local tiny validation, then proceed to Stage 4 local-only cloud readiness preparation. Do not start cloud usage, full training, benchmark runs, large downloads, or 8B/9B training without explicit human approval.

Decision:
- continue
