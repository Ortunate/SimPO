# Experiment ID
local-static-smoke-001

## Date
2026-04-30

## Owner
Codex

## Objective
Why this run exists:

Validate that the repository's static SimPO trainer/loss path can execute a minimal local training step after environment setup.

Decision this run should support:

Whether Phase 1 can proceed from dependency setup into dynamic-gamma implementation planning, while still requiring a more realistic baseline smoke later.

## Variant
Type:
- baseline

Strategy:
- static

Hypothesis:

The existing `SimPOTrainer` can tokenize chosen/rejected samples, run the concatenated forward path, compute static `gamma_beta_ratio` loss, and complete two tiny training steps without NaN/OOM.

## Code State
Branch:

main

Commit:

1b3e8f3

Dirty working tree:
- yes

Key files changed:

- `stage_artifacts/stage1/local_static_smoke.py`
- `docs_for_agent/experiment_logs/local-static-smoke-001.md`

Patch summary:

Added a Stage 1 local smoke artifact script and this experiment log. No training pipeline code was changed.

## Environment
Machine:

WSL2 local node

OS:

Ubuntu 24.04.2 LTS on `5.15.167.4-microsoft-standard-WSL2`

WSL version:

WSL2 detected from kernel string.

Python:

`.venv` CPython 3.10.19

CUDA:

PyTorch CUDA 12.1

Driver:

595.79

GPU:

NVIDIA GeForce RTX 4090 Laptop GPU

Detected VRAM:

16376 MiB

PyTorch:

2.2.2+cu121

Transformers:

4.44.2

TRL:

0.9.6

Other relevant packages:

`datasets==2.18.0`, `accelerate==0.29.2`, `peft==0.7.1`, `wandb==0.13.11`, `rich==11.2.0`, `setuptools==68.2.2`

## Data
Dataset:

Synthetic local preference data embedded in `stage_artifacts/stage1/local_static_smoke.py`

Split:

train only

Sample size or ratio:

2 preference pairs

Max sequence length:

64

Preprocessing notes:

Uses a tiny local WordLevel tokenizer with explicit BOS/EOS/PAD tokens. Does not download datasets or models.

## Run Config
Base model:

Random tiny `GPT2LMHeadModel`

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

default Trainer scheduler

Warmup:

default 0

Epochs or max steps:

2 max steps

Seed:

42

Checkpoint policy:

`save_strategy="no"`

Logging policy:

`logging_steps=1`, stdout only

## Dynamic Gamma Settings
Enabled:
- no

Similarity source:

none

Hidden-state extraction point:

none

Pooling / token selection:

none

Gamma strategy:

static

Gamma min:

not applicable

Gamma max:

not applicable

Clamp / threshold rule:

not applicable

Curriculum rule:

not applicable

Logging fields:

Existing SimPO metrics: loss, grad norm, rewards, margins, logps, logits.

## Commands
Exact commands:

    UV_CACHE_DIR=/tmp/uv-cache UV_PYTHON_INSTALL_DIR=/tmp/uv-python uv venv --python 3.10 --seed .venv
    uv --cache-dir /tmp/uv-cache pip install --python .venv/bin/python --no-progress torch==2.2.2 transformers==4.44.2 datasets==2.18.0 accelerate==0.29.2 trl==0.9.6 peft==0.7.1 wandb==0.13.11 pyyaml==6.0.1 sentencepiece==0.2.0 protobuf==3.20.1
    uv --cache-dir /tmp/uv-cache pip install --python .venv/bin/python --no-progress rich==11.2.0 setuptools==68.2.2
    HF_HOME=stage_artifacts/stage1/hf-cache WANDB_DISABLED=true .venv/bin/python stage_artifacts/stage1/local_static_smoke.py

## Expected Healthy Behavior
Expected memory:

Tiny GPU memory use; no OOM.

Expected loss behavior:

Finite loss for both steps.

Expected gamma behavior:

Static `gamma_beta_ratio=0.5`.

Expected runtime:

Seconds.

## Actual Outcome
Run status:
- PASS

Summary:

The tiny static baseline smoke completed 2 training steps on the RTX 4090 Laptop GPU. Loss, grad norm, rewards, logps, and logits were finite.

## Metrics
Peak VRAM:

PyTorch peak allocated 17.78 MiB; peak reserved 22.0 MiB.

Baseline peak VRAM, if applicable:

This run is the first tiny baseline smoke.

Memory delta:

Not comparable to realistic model scale.

Loss trend:

Step losses: 1.5129, 1.3701. Reported `train_loss`: 1.4414799213409424.

Gradient norm trend:

Step grad norms: 12.91686725616455, 11.616397857666016.

Gamma mean / min / max:

Static `gamma_beta_ratio=0.5`; no distribution.

Similarity mean / min / max:

Not applicable.

Throughput:

4.902 samples/s, 4.902 steps/s.

Runtime:

0.408 seconds reported by Trainer.

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
- no

## Artifacts
Log path:

No raw stdout log file; summary captured in this experiment log.

Config path:

`stage_artifacts/stage1/local_static_smoke.py`

Checkpoint path:

none

TensorBoard / W&B path:

none

Plot path:

none

## Interpretation
What this experiment suggests:

The local Python environment and the repository's current static SimPO trainer/loss path can execute a minimal GPU training step.

What it does not prove:

It does not prove that original 7B/8B/9B configs fit on 16GB VRAM, that real UltraFeedback data loads correctly, or that cloud-scale baseline quality is reproduced.

## Next Action
Exact next step:

Run a more realistic local baseline smoke with a tiny public or local causal LM and local preference data through `scripts/run_simpo.py`, or add the minimal local-dataset support needed to exercise that entrypoint without downloading gated models.

Decision:
- continue
