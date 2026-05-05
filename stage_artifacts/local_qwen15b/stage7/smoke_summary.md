# Stage L7 Smoke Summary

Date: 2026-05-05

## Successful Runs
| Variant | Status | Duration | Peak VRAM | Train loss | Eval loss |
|---|---:|---:|---:|---:|---:|
| Static QLoRA | PASS | 12.604 s | 11626 MiB | 2.4892 | 1.0009 |
| Dynamic gamma QLoRA | PASS | 10.912 s | 11695 MiB | 2.3154 | 0.8786 |

Dynamic minus static peak VRAM: 69 MiB.

## Dynamic Metrics
Eval gamma beta ratio:

- mean: 0.1309451162815094
- min: 0.1309451162815094
- max: 0.1309451162815094

Eval similarity:

- mean: 0.9048781991004944
- min: 0.9048781991004944
- max: 0.9048781991004944

## Artifacts
Successful static run:

- `stage_artifacts/local_qwen15b/stage7/static_success_candidate/summary.json`
- `stage_artifacts/local_qwen15b/stage7/static_success_candidate/gpu_samples.jsonl`
- ignored logs: `stdout.log`, `stderr.log`
- ignored output dir: `stage_artifacts/local_qwen15b/outputs/static_qlora_downloaded_tiny/`

Successful dynamic run:

- `stage_artifacts/local_qwen15b/stage7/dynamic_success_candidate/summary.json`
- `stage_artifacts/local_qwen15b/stage7/dynamic_success_candidate/gpu_samples.jsonl`
- ignored logs: `stdout.log`, `stderr.log`
- ignored output dir: `stage_artifacts/local_qwen15b/outputs/dynamic_qlora_downloaded_tiny/`

## Compatibility Fixes Made
- `scripts/run_simpo.py`: skip BOS string stripping when `tokenizer.bos_token is None`.
- `scripts/simpo_trainer.py`: accept already-resolved `torch.dtype` in `model_init_kwargs["torch_dtype"]`.
- `scripts/simpo_trainer.py`: skip BOS token prepend when `tokenizer.bos_token_id is None`.
- `scripts/simpo_trainer.py`: force tokenization map to ignore stale cache with `load_from_cache_file=False`.
- `stage_artifacts/local_qwen15b/stage7_run_smoke.py`: run wrapper with local HF cache env, `PYTHONPATH`, stdout/stderr capture, and `nvidia-smi` sampling.

## Resource Note
Both successful runs exceeded the 8GB warning threshold but stayed below the 16GB local VRAM budget.

No DeepSeek API call, dataset/model download, dependency install, full fine-tuning, 8B/9B run, or system configuration change was performed.

