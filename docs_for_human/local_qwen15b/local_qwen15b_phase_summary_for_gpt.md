# GPT-Facing Phase Summary: Local Qwen2.5-1.5B QLoRA Fallback Line

Date: 2026-05-05

## Purpose
This document summarizes the current `local-qwen15b-qlora` branch for a future GPT/ChatGPT review.

This branch is a local fallback proof-of-concept line for the SimPO dynamic-gamma project using:

- Qwen2.5-1.5B-Instruct
- QLoRA
- RTX 4090 Laptop under WSL
- static SimPO QLoRA vs dynamic-gamma SimPO QLoRA
- tiny local generation
- DeepSeek V4 Flash as a later/tiny judge path

Important boundary:

This branch does not prove Llama-3-8B, Gemma-2-9B, other 8B/9B, or full fine-tuning behavior.

## Current Status
Status: local fallback proof-of-concept loop complete at small scale.

Completed:

- documentation/policy setup
- environment readiness audit
- dependency setup and mirror source handling
- approved model/data acquisition
- static QLoRA tiny smoke
- dynamic-gamma QLoRA tiny smoke
- peak VRAM comparison
- gamma/similarity logging validation
- 64/16 small data-scale smoke
- judge template/schema/input preparation
- one approved DeepSeek judge-template request
- tiny static/dynamic local generation
- 4-request DeepSeek tiny AB/BA judge batch

## Repository Organization
Root entrypoint:

- `AGENTS.md`

Local-line agent docs:

- `docs_for_agent/local_qwen15b/`

Local-line human reports:

- `docs_for_human/local_qwen15b/stage_0.md` through `stage_18.md`

Local-line artifacts:

- `stage_artifacts/local_qwen15b/`

Archived previous local phase:

- `docs_for_agent/archive_previous_local_phase/`
- `docs_for_human/archive_previous_local_phase/`

Do not commit:

- model weights
- datasets
- checkpoints
- caches
- `.env`
- credentials/API keys
- generated large outputs

## Current Resource Policy
The local RTX 4090 Laptop is treated as a constrained 16GB VRAM node.

Current VRAM tiering:

- 12GB sampled VRAM: normal observation point
- 14GB sampled or expected VRAM: caution line and approval threshold
- 15GB sampled or expected VRAM: high-risk local work, needs stop/rollback plan
- 16GB VRAM: hard local ceiling

Approval is still required before:

- GPU training
- local model loading/generation
- expected >14GB VRAM
- >10 minute command
- new downloads
- dependency changes
- any additional DeepSeek API call
- deleting artifacts

## Key Implementation Changes
The real training entrypoint remains:

- `scripts/run_simpo.py`

Dynamic gamma config and loss path:

- `scripts/simpo_config.py`
- `scripts/simpo_trainer.py`

Key compatibility fixes made during this branch:

- guard Qwen tokenizer `bos_token` string stripping when `bos_token is None`
- guard BOS token id prepending when `bos_token_id is None`
- handle `model_init_kwargs["torch_dtype"]` when already a `torch.dtype`
- disable stale tokenization cache reuse for the smoke path
- add `log_train_samples` config to suppress prompt/chosen/rejected sample dumps

## Environment Snapshot
Known local stack:

- OS: Ubuntu under WSL2
- GPU: NVIDIA GeForce RTX 4090 Laptop GPU, 16376 MiB VRAM
- Python: `.venv/bin/python`, Python 3.10.19
- torch: 2.2.2 cu121
- transformers: 4.44.2
- datasets: 2.18.0
- accelerate: 0.29.2
- trl: 0.9.6
- peft: 0.7.1
- bitsandbytes: 0.41.2.post2
- deepspeed: not installed

HF cache variables used for local work:

- `HF_HOME=stage_artifacts/local_qwen15b/hf-cache`
- `HF_HUB_CACHE=stage_artifacts/local_qwen15b/hf-cache/hub`
- `HF_DATASETS_CACHE=stage_artifacts/local_qwen15b/hf-cache/datasets`
- `HF_ENDPOINT=https://hf-mirror.com`
- `HF_HUB_DISABLE_XET=1`

## Model and Data
Model:

- Source: `Qwen/Qwen2.5-1.5B-Instruct`
- Local path: `stage_artifacts/local_qwen15b/models/Qwen2.5-1.5B-Instruct/`
- Main weight file: `model.safetensors`, about 3.087GB
- Model type: `qwen2`
- Layers: 28
- Hidden size: 1536
- Attention heads: 12
- KV heads: 2
- Vocab size: 151936

Dataset:

- Main local dataset: `stage_artifacts/local_qwen15b/data/trl_ultrafeedback_binarized/`
- Tiny subset: `stage_artifacts/local_qwen15b/data/trl_ultrafeedback_binarized_tiny/`
- 64/16 subset: `stage_artifacts/local_qwen15b/data/trl_ultrafeedback_binarized_64_16/`

The primary H4 mirror path failed with HTTP 520; alternate `trl-lib/ultrafeedback_binarized` via `hf-mirror.com` with `HF_HUB_DISABLE_XET=1` succeeded.

## Training Smoke Results
All runs are smoke/proof-of-concept only.

| Stage | Variant | Data scale | Steps | Peak VRAM | Train loss | Eval loss | Reward acc | Gamma mean | Similarity mean |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| L8 | Static | 16/8 | 5 | 11620 MiB | 2.4892 | 1.0009 | n/a | n/a | n/a |
| L8 | Dynamic | 16/8 | 5 | 11693 MiB | 2.3154 | 0.8786 | n/a | 0.1309 | 0.9049 |
| L9 | Static | 16/8 | 20 | 11945 MiB | 1.6594 | 0.9879 | 0.625 | n/a | n/a |
| L9 | Dynamic | 16/8 | 20 | 11758 MiB | 1.4992 | 0.8711 | 0.500 | 0.1310 | 0.9045 |
| L10 | Static | 64/16 | 20 | 10571 MiB | 1.3097 | 1.0390 | 0.375 | n/a | n/a |
| L11 | Dynamic | 64/16 | 20 | 10556 MiB | 1.1609 | 0.9086 | 0.375 | 0.1297 | 0.9255 |

Interpretation:

- static path runs
- dynamic-gamma path runs
- dynamic metrics are emitted
- sampled VRAM stayed within local 16GB hard budget
- these are not quality results

## Generation and Judge Results
Stage L16 local generation:

- prompts: 2 synthetic prompts
- static responses: 2
- dynamic responses: 2
- total responses: 4
- peak sampled VRAM: 3965 MiB
- API calls: 0
- training steps: 0

Stage L17 DeepSeek judge batch:

- source: Stage L16 generated outputs
- requests: 4
- AB/BA swaps: yes
- HTTP 200: 4/4
- parse failures: 0
- total token usage: 2120
- pair count: 2
- consistent pairs: 2
- aggregate winners: both tie

Interpretation:

- judge request path works
- parser and AB/BA aggregation work
- tiny synthetic-prompt judge results are not benchmark evidence

## DeepSeek/API Handling
DeepSeek model used:

- `deepseek-v4-flash`

Endpoint host:

- `api.deepseek.com`

Secret handling:

- `.env` exists and is ignored
- key presence was checked only in approved API stages
- key value was never printed
- key value was never written to artifacts
- `.env` content was never printed
- `.env` was not modified

API calls made in this line were approved and small:

- minimal connectivity/template checks
- one single judge-template request
- one 4-request tiny judge batch

Full AlpacaEval-style evaluation was not run.

## Current Evidence Boundary
This branch supports the following statement:

The local Qwen2.5-1.5B-Instruct QLoRA fallback route can execute the project loop at proof-of-concept scale: static QLoRA, dynamic-gamma QLoRA, memory sampling, loss/gamma/similarity logging, tiny generation, and tiny DeepSeek judge-path validation.

This branch does not support:

- 8B/9B full fine-tuning claims
- benchmark claims
- model-quality claims
- production readiness claims
- broad SimPO/dynamic-gamma generalization claims

## Recommended Next Discussion
Before any further execution, decide which of these is desired:

1. stop and use this as the local fallback completion package
2. write a manuscript-facing limitations/methods appendix
3. design a larger but still bounded local evaluation plan with explicit prompt source, cost cap, and resource approvals

Do not proceed to more training, generation, or API calls without a new explicit stage scope.
