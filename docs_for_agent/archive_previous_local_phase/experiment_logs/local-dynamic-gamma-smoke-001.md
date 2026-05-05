# Experiment ID
local-dynamic-gamma-smoke-001

## Date
2026-05-04

## Owner
Codex

## Objective
Why this run exists:

Validate the Stage 2 dynamic gamma trainer path on CPU using a tiny local model and synthetic preference data.

Decision this run should support:

Whether the dynamic gamma prototype can run at all before trying the repository entrypoint smoke.

## Variant
Type:
- dynamic

Strategy:
- sim_linear

Hypothesis:

The dynamic path should run one tiny static-control step and one tiny dynamic step. Static metrics should not include gamma/similarity fields; dynamic metrics should include finite `gamma_beta_ratio/*` and `similarity/*` fields inside configured bounds.

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
- `stage_artifacts/stage2/local_dynamic_gamma_smoke.py`
- `docs_for_agent/experiment_logs/local-dynamic-gamma-smoke-001.md`

Patch summary:

Added default-disabled dynamic gamma config and trainer path; added CPU tiny smoke script.

## Environment
Machine:

WSL2 local node

OS:

Ubuntu 24.04.2 LTS on WSL2, based on prior Stage 0/1 detection.

WSL version:

WSL2 detected from kernel string in prior stage.

Python:

`.venv` CPython 3.10.19, repaired to use `.uv-python/cpython-3.10.19-linux-x86_64-gnu`.

CUDA:

Not used for this run.

Driver:

Not used for this run.

GPU:

Not used for this run.

Detected VRAM:

Not used for this run.

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

Synthetic local preference data embedded in `stage_artifacts/stage2/local_dynamic_gamma_smoke.py`

Split:

train only

Sample size or ratio:

2 preference pairs

Max sequence length:

64

Preprocessing notes:

Uses a tiny local WordLevel tokenizer and random tiny GPT-2 model.

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

default Trainer scheduler

Warmup:

0

Epochs or max steps:

1 step per variant

Seed:

42

Checkpoint policy:

`save_strategy="no"`

Logging policy:

stdout and summary JSON

## Dynamic Gamma Settings
Enabled:
- yes for dynamic variant; no for static control

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

    UV_CACHE_DIR=/tmp/uv-cache UV_PYTHON_INSTALL_DIR=/home/ubuntu0/Code_place/Github_repoes/SimPO/.uv-python uv python install 3.10
    ln -sfn /home/ubuntu0/Code_place/Github_repoes/SimPO/.uv-python/cpython-3.10.19-linux-x86_64-gnu/bin/python3.10 .venv/bin/python
    HF_HOME=stage_artifacts/stage2/hf-cache WANDB_DISABLED=true .venv/bin/python stage_artifacts/stage2/local_dynamic_gamma_smoke.py

## Expected Healthy Behavior
Expected memory:

CPU tiny run; no GPU use.

Expected loss behavior:

Finite loss.

Expected gamma behavior:

Dynamic run logs finite gamma in `[0.0, 0.5]`; static control logs no dynamic gamma fields.

Expected runtime:

Seconds.

## Actual Outcome
Run status:
- PASS

Summary:

The CPU tiny smoke passed for both static-control and dynamic variants. Dynamic metrics were finite and within clamp bounds.

## Metrics
Peak VRAM:

Not applicable; CPU run.

Baseline peak VRAM, if applicable:

Not applicable.

Memory delta:

Not measured.

Loss trend:

Static control `train_loss`: 1.2368441820144653. Dynamic `train_loss`: 1.0641738176345825.

Gradient norm trend:

Static: 10.647841453552246. Dynamic: 10.643580436706543.

Gamma mean / min / max:

Dynamic: 0.2812894284725189 / 0.2812894284725189 / 0.2812894284725189.

Similarity mean / min / max:

Dynamic: 0.7496845722198486 / 0.7496845722198486 / 0.7496845722198486.

Throughput:

Static: 12.313 steps/s. Dynamic: 86.853 steps/s. These tiny CPU timings are not meaningful for performance comparison.

Runtime:

Static: 0.0812s. Dynamic: 0.0115s.

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

`stage_artifacts/stage2/local-dynamic-gamma-smoke-001-summary.json`

Config path:

`stage_artifacts/stage2/local_dynamic_gamma_smoke.py`

Checkpoint path:

none

TensorBoard / W&B path:

none

Plot path:

none

## Interpretation
What this experiment suggests:

The dynamic gamma trainer path can run on tiny CPU data, logs expected metrics, and keeps the static path free of dynamic metrics when disabled.

What it does not prove:

It does not prove memory overhead on real models, stability on real preference data, or compatibility with distributed wrappers.

## Next Action
Exact next step:

Run the tiny `scripts/run_simpo.py` entrypoint smoke with dynamic gamma enabled.

Decision:
- continue
