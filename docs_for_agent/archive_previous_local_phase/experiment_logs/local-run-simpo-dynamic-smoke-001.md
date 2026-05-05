# Experiment ID
local-run-simpo-dynamic-smoke-001

## Date
2026-05-04

## Owner
Codex

## Objective
Why this run exists:

Validate the repository entrypoint `scripts/run_simpo.py` with dynamic gamma enabled using only local tiny CPU artifacts.

Decision this run should support:

Whether Stage 2 dynamic gamma prototype can be considered runnable through the real training entrypoint on tiny data.

## Variant
Type:
- dynamic

Strategy:
- sim_linear

Hypothesis:

The real entrypoint should load local tiny data/model, apply chat templating, instantiate `SimPOTrainer`, run dynamic gamma for two CPU steps, log gamma/similarity metrics, and save outputs.

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
- `stage_artifacts/stage2/local-run-simpo-dynamic-smoke.yaml`
- `docs_for_agent/experiment_logs/local-run-simpo-dynamic-smoke-001.md`

Patch summary:

Dynamic gamma enabled in a tiny local entrypoint config; no full-scale training code path was changed beyond Stage 2 prototype.

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

`stage_artifacts/stage1/local_pref_dataset`

Split:

train/test

Sample size or ratio:

4 train pairs, 2 test pairs

Max sequence length:

64

Preprocessing notes:

Local dataset script and explicit chat template from `stage_artifacts/stage2/local-run-simpo-dynamic-smoke.yaml`.

## Run Config
Base model:

`stage_artifacts/stage1/local_tiny_gpt2`

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

linear

Warmup:

0

Epochs or max steps:

2 max steps

Seed:

42

Checkpoint policy:

`save_strategy="no"` during training; final model saved by `run_simpo.py`.

Logging policy:

`logging_steps=1`

## Dynamic Gamma Settings
Enabled:
- yes

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

    PYTHONPATH=. HF_HOME=stage_artifacts/stage2/hf-cache WANDB_DISABLED=true .venv/bin/python scripts/run_simpo.py stage_artifacts/stage2/local-run-simpo-dynamic-smoke.yaml

## Expected Healthy Behavior
Expected memory:

CPU tiny run; no GPU use.

Expected loss behavior:

Finite loss.

Expected gamma behavior:

Gamma metrics finite and clamped to `[0.0, 0.5]`.

Expected runtime:

Seconds.

## Actual Outcome
Run status:
- PASS

Summary:

The real entrypoint completed 2 CPU training steps with dynamic gamma enabled and saved output artifacts.

## Metrics
Peak VRAM:

Not applicable; CPU run.

Baseline peak VRAM, if applicable:

Not applicable.

Memory delta:

Not measured.

Loss trend:

Step losses: 1.0116, 1.0179. Reported `train_loss`: 1.0147329568862915.

Gradient norm trend:

Step grad norms: 3.0673575401306152, 4.925373554229736.

Gamma mean / min / max:

Step 1: 0.25390729308128357 / 0.25390729308128357 / 0.25390729308128357.

Step 2: 0.2633712887763977 / 0.2633712887763977 / 0.2633712887763977.

Similarity mean / min / max:

Step 1: 0.9687416553497314 / 0.9687416553497314 / 0.9687416553497314.

Step 2: 0.8930298089981079 / 0.8930298089981079 / 0.8930298089981079.

Throughput:

7.728 samples/s, 7.728 steps/s.

Runtime:

0.2588 seconds reported by Trainer.

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

`stage_artifacts/stage2/local-run-simpo-dynamic-smoke-output/trainer_state.json`

Config path:

`stage_artifacts/stage2/local-run-simpo-dynamic-smoke.yaml`

Checkpoint path:

`stage_artifacts/stage2/local-run-simpo-dynamic-smoke-output/`

TensorBoard / W&B path:

none

Plot path:

none

## Interpretation
What this experiment suggests:

The Stage 2 dynamic gamma prototype runs through the real SimPO entrypoint on tiny local CPU data and logs the expected gamma/similarity metrics.

What it does not prove:

It does not prove real-model memory overhead, training stability on UltraFeedback, or distributed training compatibility.

## Next Action
Exact next step:

Proceed to Stage 3 only for local stability validation planning and tiny/small validation under the approval policy.

Decision:
- promote to next stage
