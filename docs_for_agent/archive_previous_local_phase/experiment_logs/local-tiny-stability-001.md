# Experiment ID
local-tiny-stability-001

## Date
2026-05-04

## Owner
Codex

## Objective
Why this run exists:

Run a local-safe Stage 3 stability comparison between the static SimPO path and the default-disabled dynamic gamma path.

Decision this run should support:

Whether the `sim_linear` dynamic gamma prototype survives a short CPU-only tiny validation without NaN/Inf, loss blow-up, missing logs, or obvious memory regression at the process RSS level.

## Variant
Type:
- baseline and dynamic

Strategy:
- static
- sim_linear

Hypothesis:

Static and dynamic variants should both complete 6 tiny training steps. Dynamic logs should include finite `gamma_beta_ratio/*` and `similarity/*` fields within configured bounds.

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
- `stage_artifacts/stage3/local_tiny_stability_compare.py`
- `docs_for_agent/experiment_logs/local-tiny-stability-001.md`

Patch summary:

Stage 2 dynamic gamma prototype remains in trainer/config. Stage 3 added a local artifact script that runs static and dynamic tiny variants in separate Python subprocesses with a fixed seed before model construction.

## Environment
Machine:

Local WSL2 development node.

OS:

Linux `5.15.167.4-microsoft-standard-WSL2`, Ubuntu userspace from prior stage context.

WSL version:

WSL2 kernel detected.

Python:

`.venv` CPython 3.10.19

CUDA:

Not used for this run. `torch.cuda.is_available()` returned `False` in the normal sandboxed Python context.

Driver:

NVIDIA driver 595.79 from `nvidia-smi`.

GPU:

NVIDIA GeForce RTX 4090 Laptop GPU.

Detected VRAM:

16376 MiB total, 3197 MiB used at query time.

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

Synthetic local preference data embedded in `stage_artifacts/stage3/local_tiny_stability_compare.py`.

Split:

train only

Sample size or ratio:

6 preference pairs

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

6 steps per variant

Seed:

42, set before model construction in each subprocess

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

    .venv/bin/python -m py_compile stage_artifacts/stage3/local_tiny_stability_compare.py
    free -h
    uname -a
    nvidia-smi --query-gpu=name,memory.total,memory.used,driver_version --format=csv,noheader
    HF_HOME=stage_artifacts/stage3/hf-cache TRANSFORMERS_CACHE=stage_artifacts/stage3/hf-cache/transformers WANDB_DISABLED=true .venv/bin/python stage_artifacts/stage3/local_tiny_stability_compare.py

## Expected Healthy Behavior
Expected memory:

CPU tiny process RSS around hundreds of MB; no GPU use.

Expected loss behavior:

Finite loss for both variants, no guard-triggering loss blow-up.

Expected gamma behavior:

Dynamic gamma finite and clamped within `[0.0, 0.5]`. Static control should not log dynamic gamma/similarity metrics.

Expected runtime:

Seconds.

## Actual Outcome
Run status:
- PASS

Summary:

Static and dynamic variants both completed 6 CPU-only steps. No NaN/Inf, loss guard violation, missing dynamic metrics, or clamp violation was detected.

## Metrics
Peak VRAM:

Not used. GPU query showed 3197 MiB already used outside this run, but the run itself was CPU-only.

Baseline peak VRAM, if applicable:

Not applicable.

Memory delta:

Process max RSS dynamic minus static: `-0.51171875` MB. This is CPU RSS only and does not prove real GPU VRAM overhead.

Loss trend:

- static loss values: `[1.4275, 1.499, 1.2816, 1.3645, 1.2182, 1.3824]`
- dynamic loss values: `[1.1289, 1.1842, 0.9814, 1.045, 0.9331, 1.0469]`

Gradient norm trend:

- static max grad norm: `11.861966133117676`
- dynamic max grad norm: `10.559185028076172`

Gamma mean / min / max:

- dynamic gamma mean values: `[0.2925293445587158, 0.2863449454307556, 0.2776424288749695, 0.27108025550842285, 0.28287655115127563, 0.2605389952659607]`
- dynamic gamma min: `0.2605389952659607`
- dynamic gamma max: `0.2925293445587158`

Similarity mean / min / max:

- similarity mean values: `[0.659765362739563, 0.7092403769493103, 0.7788605093955994, 0.8313578367233276, 0.7369875907897949, 0.9156879186630249]`
- similarity min: `0.659765362739563`
- similarity max: `0.9156879186630249`

Throughput:

- static: `53.012` steps/s from Trainer summary
- dynamic: `117.489` steps/s from Trainer summary

Runtime:

- static variant measured runtime: `0.18678673199974583` seconds
- dynamic variant measured runtime: `0.12312405100010437` seconds

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
- no blocking abnormal logs. Non-blocking Transformers deprecation warnings were printed for `TRANSFORMERS_CACHE` and tokenizer cleanup defaults.

## Artifacts
Log path:

`docs_for_agent/experiment_logs/local-tiny-stability-001.md`

Config path:

Embedded in `stage_artifacts/stage3/local_tiny_stability_compare.py`

Checkpoint path:

None. Checkpoint saving disabled.

TensorBoard / W&B path:

None. W&B disabled.

Plot path:

None.

Other artifact paths:

- `stage_artifacts/stage3/local_tiny_stability_compare.py`
- `stage_artifacts/stage3/local-tiny-stability-001-static.json`
- `stage_artifacts/stage3/local-tiny-stability-001-dynamic.json`
- `stage_artifacts/stage3/local-tiny-stability-001-summary.json`

## Interpretation
What this experiment suggests:

The Stage 2 dynamic gamma implementation can run for more than a one-step smoke on CPU tiny synthetic data, logs expected dynamic metrics, respects configured gamma clamps, and does not show immediate numerical instability.

What it does not prove:

It does not prove GPU VRAM overhead, compatibility with 8B/9B models, compatibility with PEFT/FSDP/DeepSpeed wrappers, real UltraFeedback behavior, or benchmark impact.

## Next Action
Exact next step:

Continue Stage 3 rather than advancing to Stage 4. The narrow next validation should be either a local-safe entrypoint-level tiny static/dynamic comparison or an explicitly approved tiny GPU memory check if CUDA visibility is repaired/available.

Decision:
- narrow
