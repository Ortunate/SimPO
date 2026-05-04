# Experiment ID
local-dynamic-gamma-unit-checks-001

## Date
2026-05-04

## Owner
Codex

## Objective
Why this run exists:

Continue local-first Stage 4 preparation by validating dynamic gamma math and trainer contracts with CPU/dummy tensor checks before any server migration.

Decision this run should support:

Whether additional local-safe unit checks reduce migration risk enough to keep Stage 5 blocked until human cloud/server approval.

## Variant
Type:
- dynamic and baseline contract checks

Strategy:
- static
- sim_linear

Hypothesis:

The dynamic gamma helper methods should produce deterministic finite values, preserve static loss equivalence when gamma is scalar vs tensor, ignore masked prompt/pad positions during pooling, detach and remove the LM-head hook correctly, and log dynamic keys only on the dynamic path.

## Code State
Branch:

main

Commit:

1b3e8f3

Dirty working tree:
- yes

Key files changed:

- `stage_artifacts/stage4/local_dynamic_gamma_unit_checks.py`
- `stage_artifacts/stage4/dynamic_gamma_code_review.md`
- `docs_for_agent/experiment_logs/local-dynamic-gamma-unit-checks-001.md`
- `docs_for_human/stage_4.md`

Patch summary:

Added Stage 4 local-only dynamic gamma unit checks and focused code review artifacts. Core trainer/config source was not changed in this Stage 4 update.

## Environment
Machine:

Local WSL2 development node.

OS:

Previously detected WSL2 Linux environment.

WSL version:

WSL2 kernel previously detected.

Python:

`.venv` CPython 3.10.19

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

No new dependency was installed.

## Data
Dataset:

Dummy tensors embedded in `stage_artifacts/stage4/local_dynamic_gamma_unit_checks.py`

Split:

none

Sample size or ratio:

not applicable

Max sequence length:

tiny dummy tensors only

Preprocessing notes:

No external data access.

## Run Config
Base model:

No real model. One tiny dummy `nn.Module` is used only to test the LM-head pre-hook.

Precision:

fp32 CPU

Quantization:

none

LoRA / QLoRA:

none

Batch size:

not applicable

Gradient accumulation:

not applicable

Learning rate:

not applicable

Scheduler:

not applicable

Warmup:

not applicable

Epochs or max steps:

not applicable

Seed:

not required

Checkpoint policy:

none

Logging policy:

stdout and this experiment log

## Dynamic Gamma Settings
Enabled:
- directly tested through helper methods and metric contracts

Similarity source:

Dummy hidden-state tensors.

Hidden-state extraction point:

Temporary forward pre-hook on a dummy model output head.

Pooling / token selection:

`labels != label_pad_token_id`

Gamma strategy:

`sim_linear`

Gamma min:

tested with `0.0` and `0.1`

Gamma max:

tested with `0.5` and `0.4`

Clamp / threshold rule:

Clamp after similarity-based linear mapping.

Curriculum rule:

none

Logging fields:

`gamma_beta_ratio/mean`, `gamma_beta_ratio/min`, `gamma_beta_ratio/max`, `similarity/mean`, `similarity/min`, `similarity/max`

## Commands
Exact commands:

    .venv/bin/python -m py_compile stage_artifacts/stage4/local_dynamic_gamma_unit_checks.py
    .venv/bin/python stage_artifacts/stage4/local_dynamic_gamma_unit_checks.py

## Expected Healthy Behavior
Expected memory:

CPU/dummy only; negligible memory.

Expected loss behavior:

Static scalar gamma and equivalent per-sample gamma tensor produce identical losses/rewards.

Expected gamma behavior:

Gamma mapping and clamps match deterministic expected values.

Expected runtime:

Seconds.

## Actual Outcome
Run status:
- PASS

Summary:

All five unit checks passed.

Checks passed:

- `test_static_loss_matches_full_gamma_tensor`
- `test_response_pooling_ignores_masked_tokens`
- `test_dynamic_gamma_mapping_and_clamp`
- `test_lm_head_hook_detaches_and_removes`
- `test_metric_key_contract_static_and_dynamic`

## Metrics
Peak VRAM:

Not used.

Baseline peak VRAM, if applicable:

Not applicable.

Memory delta:

Not measured; CPU/dummy only.

Loss trend:

Not a training run.

Gradient norm trend:

Not a training run.

Gamma mean / min / max:

Deterministic helper checks passed.

Similarity mean / min / max:

Deterministic helper checks passed.

Throughput:

Not applicable.

Runtime:

Seconds.

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
- non-blocking Hugging Face cache warning printed during imports

## Artifacts
Log path:

`docs_for_agent/experiment_logs/local-dynamic-gamma-unit-checks-001.md`

Config path:

Not applicable.

Checkpoint path:

None.

TensorBoard / W&B path:

None.

Plot path:

None.

Other artifact paths:

- `stage_artifacts/stage4/local_dynamic_gamma_unit_checks.py`
- `stage_artifacts/stage4/dynamic_gamma_code_review.md`

## Interpretation
What this experiment suggests:

The dynamic gamma helper logic and logging contracts pass local-safe dummy validation, reducing migration risk without starting server/cloud work.

What it does not prove:

It does not prove real 8B/9B memory behavior, real dataset behavior, PEFT/FSDP/DeepSpeed compatibility, or benchmark impact.

## Next Action
Exact next step:

Continue local preparation or stop for human review. Do not start Stage 5 without explicit cloud/server approval.

Decision:
- continue local preparation
