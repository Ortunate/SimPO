# Stage L5 Download Plan

Date: 2026-05-05

## Approved Scope
The human approved model and data downloads for this step.

This stage still does not approve:

- loading Qwen2.5-1.5B
- GPU training
- DeepSeek API calls
- full fine-tuning
- benchmark runs
- committing models, datasets, caches, checkpoints, credentials, or `.env`

## Model Download Plan
Model:

```text
Qwen/Qwen2.5-1.5B-Instruct
```

Source choice:

- primary: Hugging Face repository through domestic mirror endpoint `https://hf-mirror.com`
- fallback: stop and report if mirror download fails

Expected size:

- Hugging Face file listing reports repository size around 3.1 GB
- main weight file `model.safetensors` is around 3.09 GB

Target path:

```text
stage_artifacts/local_qwen15b/models/Qwen2.5-1.5B-Instruct/
```

Cache path:

```text
stage_artifacts/local_qwen15b/hf-cache/
```

Gitignore status:

- `stage_artifacts/local_qwen15b/models/` is ignored
- `stage_artifacts/local_qwen15b/hf-cache/` is ignored

Rollback / cleanup plan:

- remove only `stage_artifacts/local_qwen15b/models/Qwen2.5-1.5B-Instruct/`
- remove only model-related cache entries under `stage_artifacts/local_qwen15b/hf-cache/` if needed
- do not delete reports, `.env`, source files, checkpoints, or unrelated artifacts

## Data Download Plan
Dataset intent:

- obtain a tiny preference sample for local fallback smoke planning
- do not pull full UltraFeedback
- keep the local Stage L4 tiny fixture as the guaranteed no-network fallback

Preferred source:

- a small streamed/sample subset from an UltraFeedback-style preference dataset via the same Hugging Face mirror endpoint

Target path:

```text
stage_artifacts/local_qwen15b/data/ultrafeedback_tiny/
```

Gitignore status:

- `stage_artifacts/local_qwen15b/data/` is ignored

Rollback / cleanup plan:

- remove only `stage_artifacts/local_qwen15b/data/ultrafeedback_tiny/`
- keep `stage_artifacts/local_qwen15b/stage4/tiny_pref_dataset/` because it is a small source fixture

## Command-local Environment
Use command-local cache/mirror environment variables:

```bash
HF_ENDPOINT=https://hf-mirror.com
HF_HOME=stage_artifacts/local_qwen15b/hf-cache
HF_HUB_CACHE=stage_artifacts/local_qwen15b/hf-cache/hub
HF_DATASETS_CACHE=stage_artifacts/local_qwen15b/hf-cache/datasets
```

Do not write these to `.env` or shell profiles in this stage.
