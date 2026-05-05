# Experiment ID
local-run-simpo-smoke-001

## Date
2026-04-30

## Owner
Codex

## Objective
Why this run exists:

Validate the real training entrypoint `scripts/run_simpo.py` on a tiny local baseline config without external model or dataset downloads.

Decision this run should support:

Whether Stage 1 has a working baseline smoke path through the repository entrypoint before dynamic gamma work begins.

## Variant
Type:
- baseline

Strategy:
- static

Hypothesis:

With a local tiny causal LM, local preference dataset script, and static `gamma_beta_ratio`, `scripts/run_simpo.py` should load data, apply chat templates, instantiate `SimPOTrainer`, run two train steps, save metrics, and finish without NaN/OOM.

## Code State
Branch:

main

Commit:

1b3e8f3

Dirty working tree:
- yes

Key files changed:

- `stage_artifacts/stage1/prepare_run_simpo_smoke_assets.py`
- `stage_artifacts/stage1/local_pref_dataset/local_pref_dataset.py`
- `stage_artifacts/stage1/local-run-simpo-smoke.yaml`
- `stage_artifacts/stage1/local_tiny_gpt2/`
- `stage_artifacts/stage1/local-run-simpo-smoke-output/`
- `docs_for_agent/experiment_logs/local-run-simpo-smoke-001.md`

Patch summary:

Added local Stage 1 artifacts only. No repository training source file was changed.

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

`datasets==2.18.0`, `accelerate==0.29.2`, `peft==0.7.1`, `huggingface-hub==0.23.2`, `wandb==0.13.11`

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

Local dataset script yields OpenAI-format `prompt`, `chosen`, and `rejected` message lists. `scripts/run_simpo.py` applies an explicit local chat template from the smoke YAML.

## Run Config
Base model:

`stage_artifacts/stage1/local_tiny_gpt2`, random tiny GPT-2 checkpoint

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

`logging_steps=1`; metrics saved by Trainer.

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

    HF_HOME=stage_artifacts/stage1/hf-cache .venv/bin/python stage_artifacts/stage1/prepare_run_simpo_smoke_assets.py
    HF_HOME=stage_artifacts/stage1/hf-cache .venv/bin/python -c "from alignment.data import get_datasets; ds=get_datasets({'stage_artifacts/stage1/local_pref_dataset':1.0}, splits=['train','test'], columns_to_keep=['prompt','chosen','rejected']); print(ds); print(ds['train'][0])"
    HF_HOME=stage_artifacts/stage1/hf-cache WANDB_DISABLED=true .venv/bin/python scripts/run_simpo.py stage_artifacts/stage1/local-run-simpo-smoke.yaml
    PYTHONPATH=. HF_HOME=stage_artifacts/stage1/hf-cache WANDB_DISABLED=true .venv/bin/python scripts/run_simpo.py stage_artifacts/stage1/local-run-simpo-smoke.yaml

## Expected Healthy Behavior
Expected memory:

Tiny GPU memory use; no OOM.

Expected loss behavior:

Finite loss for two steps.

Expected gamma behavior:

Static `gamma_beta_ratio=0.5`.

Expected runtime:

Seconds.

## Actual Outcome
Run status:
- PASS

Summary:

Initial direct invocation failed because `alignment` was not importable without `PYTHONPATH=.`. After adding `PYTHONPATH=.`, a second attempt failed because the local tiny tokenizer lacked `default_chat_template`; adding an explicit `chat_template` to the local smoke YAML fixed it. The final `scripts/run_simpo.py` run completed 2 training steps and saved metrics/model artifacts.

## Metrics
Peak VRAM:

Not instrumented for this entrypoint run. `nvidia-smi` after the run showed 4112 MiB used globally, but that includes system/WSL baseline and is not a run peak.

Baseline peak VRAM, if applicable:

Use `local-static-smoke-001` for PyTorch tiny peak: 17.78 MiB allocated, 22.0 MiB reserved.

Memory delta:

Not meaningful for tiny random model.

Loss trend:

Step losses: 1.3513, 1.3447. Reported `train_loss`: 1.3480247855186462.

Gradient norm trend:

Step grad norms: 3.572326898574829, 5.702247142791748.

Gamma mean / min / max:

Static `gamma_beta_ratio=0.5`; no distribution.

Similarity mean / min / max:

Not applicable.

Throughput:

4.677 samples/s, 4.677 steps/s.

Runtime:

0.4276 seconds reported by Trainer.

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

Trainer logs in `stage_artifacts/stage1/local-run-simpo-smoke-output/trainer_state.json`.

Config path:

`stage_artifacts/stage1/local-run-simpo-smoke.yaml`

Checkpoint path:

`stage_artifacts/stage1/local-run-simpo-smoke-output/`

TensorBoard / W&B path:

none

Plot path:

none

## Interpretation
What this experiment suggests:

The repository's real SimPO entrypoint can execute locally with a tiny static baseline config, local data, and local model. The trainer/loss path, chat formatting, tokenization, metrics logging, and final save path are operational.

What it does not prove:

It does not prove real Llama/Gemma training fits local VRAM, that gated model/dataset access is configured, or that full benchmark quality is reproduced.

## Next Action
Exact next step:

Proceed to Phase 2 dynamic gamma prototype, keeping the tiny entrypoint smoke as the first regression check after implementation.

Decision:
- promote to next stage
