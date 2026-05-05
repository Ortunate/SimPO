# Stage L10 Static 64/16 Summary

Date: 2026-05-05

## Scope
Controlled data-scale static smoke only.

- VRAM warning line updated to 12GB.
- 16GB VRAM remains the hard local budget.
- Dataset subset was derived from already downloaded local parquet files.
- No downloads, dependency installs, DeepSeek API calls, full fine-tuning, 8B/9B runs, or system configuration changes were performed.

## Dataset
- Path: `stage_artifacts/local_qwen15b/data/trl_ultrafeedback_binarized_64_16`
- Train rows: 64
- Test rows: 16
- Disk usage: about 356K
- Git status: ignored through `stage_artifacts/local_qwen15b/data/`

## Config
- Config: `stage_artifacts/local_qwen15b/stage10/qwen25_1p5b_static_qlora_64_16_20step.yaml`
- Variant: static QLoRA
- `max_steps: 20`
- `max_length: 512`
- `max_prompt_length: 384`
- batch size: 1
- dynamic gamma: disabled

## Result
| Variant | Status | Duration | Peak VRAM sample | Train loss | Eval loss | Eval reward acc |
|---|---:|---:|---:|---:|---:|---:|
| Static QLoRA 64/16 | PASS | 30.306 s | 10571 MiB | 1.3097 | 1.0390 | 0.375 |

The sampled peak stayed below the updated 12GB warning line.

## Stability Check
- Run completed with return code 0.
- No Traceback/OOM/RuntimeError/TypeError was found.
- No prompt/chosen/rejected sample dumps were found.
- Output directory is ignored by git through `outputs/`.
- Adapter file size: 73,911,112 bytes.

## Boundary
This is a local fallback smoke and data-scale check only. It does not prove 8B/9B full fine-tuning behavior and does not support benchmark claims.

