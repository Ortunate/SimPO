# Experiment Log Template

## Experiment ID
Example: local-static-smoke-001

## Date
YYYY-MM-DD

## Owner
Codex / Human / Both

## Objective
Why this run exists:

Decision this run should support:

## Variant
Type:
- baseline / dynamic

Strategy:
- static / sim_linear / curriculum / combined

Hypothesis:

## Code State
Branch:

Commit:

Dirty working tree:
- yes / no

Key files changed:

Patch summary:

## Environment
Machine:

OS:

WSL version:

Python:

CUDA:

Driver:

GPU:

Detected VRAM:

PyTorch:

Transformers:

TRL:

Other relevant packages:

## Data
Dataset:

Split:

Sample size or ratio:

Max sequence length:

Preprocessing notes:

## Run Config
Base model:

Precision:

Quantization:

LoRA / QLoRA:

Batch size:

Gradient accumulation:

Learning rate:

Scheduler:

Warmup:

Epochs or max steps:

Seed:

Checkpoint policy:

Logging policy:

## Dynamic Gamma Settings
Enabled:
- yes / no

Similarity source:

Hidden-state extraction point:

Pooling / token selection:

Gamma strategy:

Gamma min:

Gamma max:

Clamp / threshold rule:

Curriculum rule:

Logging fields:

## Commands
Exact commands:

    <paste command here>
    <paste command here>

## Expected Healthy Behavior
Expected memory:

Expected loss behavior:

Expected gamma behavior:

Expected runtime:

## Actual Outcome
Run status:
- PASS / FAIL / INTERRUPTED / INCONCLUSIVE

Summary:

## Metrics
Peak VRAM:

Baseline peak VRAM, if applicable:

Memory delta:

Loss trend:

Gradient norm trend:

Gamma mean / min / max:

Similarity mean / min / max:

Throughput:

Runtime:

## Stability Check
OOM:
- yes / no

NaN / Inf:
- yes / no

Loss divergence:
- yes / no

Gradient explosion:
- yes / no

Abnormal logs:
- yes / no

## Artifacts
Log path:

Config path:

Checkpoint path:

TensorBoard / W&B path:

Plot path:

## Interpretation
What this experiment suggests:

What it does not prove:

## Next Action
Exact next step:

Decision:
- continue / repeat / narrow / rollback / promote to next stage
