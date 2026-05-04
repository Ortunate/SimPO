# Stage 1: Environment and Baseline Smoke Path

Backfill date: 2026-05-04

Source: current Codex conversation only.

## Stage Status

PASS

## Key Actions Performed

- Advanced from Stage 0 because Stage 0 passed.
- Created a repository-local Python environment:
  - `.venv`
  - CPython 3.10.19
- Installed minimal smoke dependencies into `.venv`:
  - `torch==2.2.2`
  - `transformers==4.44.2`
  - `datasets==2.18.0`
  - `accelerate==0.29.2`
  - `trl==0.9.6`
  - `peft==0.7.1`
  - `wandb==0.13.11`
  - plus small compatibility dependencies.
- Resolved dependency compatibility issues:
  - Added `rich==11.2.0`.
  - Downgraded `setuptools` to `68.2.2` for `pkg_resources` compatibility.
  - Adjusted `huggingface-hub` to `0.23.2`, which satisfied `transformers==4.44.2` while preserving the repository's old private import path.
- Verified package imports and `pip check`.
- Verified PyTorch CUDA visibility under approved execution context.
- Ran a trainer-level tiny static baseline smoke:
  - `local-static-smoke-001`
- Ran a real-entrypoint tiny static baseline smoke:
  - `local-run-simpo-smoke-001`
  - used `scripts/run_simpo.py`
  - used a local tiny GPT-2 model
  - used a local tiny preference dataset
  - ran 2 training steps.
- Created experiment logs for both runs.

## Evidence and Artifacts

Experiment logs:

- `docs_for_agent/experiment_logs/local-static-smoke-001.md`
- `docs_for_agent/experiment_logs/local-run-simpo-smoke-001.md`

Stage artifacts:

- `stage_artifacts/stage1/local_static_smoke.py`
- `stage_artifacts/stage1/prepare_run_simpo_smoke_assets.py`
- `stage_artifacts/stage1/local_pref_dataset/local_pref_dataset.py`
- `stage_artifacts/stage1/local-run-simpo-smoke.yaml`
- `stage_artifacts/stage1/local_tiny_gpt2/`
- `stage_artifacts/stage1/local-run-simpo-smoke-output/`

Trainer-level smoke evidence:

- Run ID: `local-static-smoke-001`
- Status: PASS
- Model: random tiny GPT-2
- Data: 2 synthetic preference pairs
- Steps: 2
- `train_loss`: 1.4414799213409424
- Step losses: 1.5129, 1.3701
- Peak PyTorch allocated memory: 17.78 MiB
- Peak PyTorch reserved memory: 22.0 MiB

Entrypoint smoke evidence:

- Run ID: `local-run-simpo-smoke-001`
- Status: PASS
- Entrypoint: `scripts/run_simpo.py`
- Local train data: 4 preference pairs
- Local test data: 2 preference pairs
- Steps: 2
- Output metrics file: `stage_artifacts/stage1/local-run-simpo-smoke-output/train_results.json`
- `train_loss`: 1.3480247855186462
- Step losses: 1.3513, 1.3447
- Step grad norms: 3.572326898574829, 5.702247142791748
- Output model and trainer artifacts were saved under `stage_artifacts/stage1/local-run-simpo-smoke-output/`.

Important recovery observations:

- Direct `python scripts/run_simpo.py ...` failed because `alignment` was not importable without `PYTHONPATH=.`.
- Re-running with `PYTHONPATH=.` fixed the import path issue.
- The local tiny tokenizer needed an explicit `chat_template` in the smoke YAML.
- `save_to_disk` style local datasets did not exercise `get_datasets()` correctly, so a local Hugging Face dataset script was used as a smoke artifact.

## Hardware / Resource Findings

- GPU:
  - NVIDIA GeForce RTX 4090 Laptop GPU
  - 16376 MiB VRAM
  - Driver 595.79
  - PyTorch CUDA 12.1
- PyTorch CUDA visibility:
  - Default non-approved context could not initialize CUDA/NVML.
  - Approved execution context reported CUDA available with one GPU.
- Memory:
  - Trainer-level tiny smoke recorded 17.78 MiB peak allocated and 22.0 MiB peak reserved by PyTorch.
  - Entrypoint run did not instrument exact peak VRAM.
  - Post-run `nvidia-smi` showed about 4112 MiB globally used, but this included system/WSL baseline and was not a run peak.
- Disk/resource impact:
  - `.venv` size was about 5.2 GiB after dependency installation.
  - `stage_artifacts/stage1` size was about 508 KiB after smoke artifacts and output.
  - `/tmp/uv-cache` size was about 56 MiB after cache use.
- Note under current updated rules:
  - The dependency installation and large PyTorch/CUDA downloads performed in Stage 1 would now require explicit human approval under the new human approval gate.
  - No such further action should be repeated without approval.

## Current Risks

### High

- Stage 1 tiny runs do not prove real Llama-3-8B or Gemma-2-9B local feasibility.
- Real UltraFeedback data and gated model access were not validated.
- Any real 8B/9B smoke or dependency upgrade now requires explicit human approval.

### Medium

- `scripts/run_simpo.py` local direct execution requires `PYTHONPATH=.` unless launched in a context that already includes the repository root.
- Entrypoint smoke did not record exact peak VRAM.
- The installed local `.venv` is useful but large and should not be modified further without considering the updated approval rule.
- `huggingface-hub==0.23.2` is a compatibility compromise based on observed repository/runtime behavior.

### Low

- Tiny synthetic data/model only validate code path, not model quality or benchmark behavior.
- Raw stdout for the trainer-level smoke was not persisted as a separate log file; summarized metrics were persisted in the experiment log.

## Missing / Unknown

- Exact raw stdout log path for `local-static-smoke-001`: not recorded.
- Exact peak VRAM for `local-run-simpo-smoke-001`: not recorded.
- Hugging Face authentication state for gated Llama/Gemma models: unknown.
- Real UltraFeedback download/access status: unknown.
- Full host Windows RAM outside WSL: unknown.

## Recommendation

The project state is safe to proceed only after this human-facing backfill is complete.

Recommended next stage remains Stage 2: Dynamic gamma prototype.

Stage 2 should:

- avoid resource-heavy actions unless approved;
- start with source-level implementation and tiny dummy smoke only;
- keep the feature fully disable-able;
- use Stage 1 tiny entrypoint smoke as the first regression test;
- add or define lightweight peak memory instrumentation before comparing static vs dynamic paths.

Do not recommend cloud migration after Stage 1.

## Executive Summary

- Stage 1 passed as a minimal environment and baseline smoke stage.
- A local Python 3.10 `.venv` was created and verified.
- Core SimPO dependencies import successfully after compatibility fixes.
- PyTorch can see the RTX 4090 Laptop GPU only under approved execution context.
- A trainer-level static baseline smoke passed.
- A real `scripts/run_simpo.py` static baseline smoke also passed with a local tiny model and local tiny dataset.
- Losses and gradient norms were finite; no OOM, NaN, or divergence was observed in tiny runs.
- These results validate the local code path only, not real 8B/9B feasibility or final research performance.
