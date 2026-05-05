# Stage L9 Controlled 20-Step Summary

Date: 2026-05-05

## Scope
Controlled 20-step smoke only. The run kept the Stage L8 local constraints:

- `max_steps: 20`
- `max_length: 512`
- `max_prompt_length: 384`
- `per_device_train_batch_size: 1`
- `per_device_eval_batch_size: 1`
- tiny local preference dataset
- QLoRA 4-bit
- no DeepSeek API
- no downloads
- no dependency or system changes

## Configs
- Static: `stage_artifacts/local_qwen15b/stage9/qwen25_1p5b_static_qlora_20step.yaml`
- Dynamic: `stage_artifacts/local_qwen15b/stage9/qwen25_1p5b_dynamic_qlora_20step.yaml`

## Results
| Variant | Status | Duration | Peak VRAM sample | Train loss | Eval loss | Eval reward acc |
|---|---:|---:|---:|---:|---:|---:|
| Static QLoRA | PASS | 25.546 s | 11945 MiB | 1.6594 | 0.9879 | 0.625 |
| Dynamic gamma QLoRA | PASS | 23.463 s | 11758 MiB | 1.4992 | 0.8711 | 0.5 |

`nvidia-smi` samples are approximate wall-clock samples, not exact allocator peaks.

## Dynamic Metrics
Final eval gamma beta ratio:

- mean: 0.13096913695335388
- min: 0.13096913695335388
- max: 0.13096913695335388

Final eval similarity:

- mean: 0.9044938683509827
- min: 0.9044938683509827
- max: 0.9044938683509827

## Stage L8 vs L9
| Variant | L8 Peak | L9 Peak | L8 train loss | L9 train loss | L8 eval loss | L9 eval loss |
|---|---:|---:|---:|---:|---:|---:|
| Static | 11620 MiB | 11945 MiB | 2.4892 | 1.6594 | 1.0009 | 0.9879 |
| Dynamic | 11693 MiB | 11758 MiB | 2.3154 | 1.4992 | 0.8786 | 0.8711 |

## Stability Check
- Both runs completed with return code 0.
- No Traceback/OOM error was found in Stage L9 logs.
- Grep for prompt/chosen/rejected sample dumps returned no matches.
- Output directories are ignored by git through `outputs/`.
- Each adapter file size: 73,911,112 bytes.

## Boundary
This remains a local fallback smoke and stability check. It does not prove 8B/9B full fine-tuning behavior and does not support benchmark claims.

