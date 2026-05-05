# Stage L8 Reproducibility Summary

Date: 2026-05-05

## Formal Configs
- Static: `stage_artifacts/local_qwen15b/stage8/qwen25_1p5b_static_qlora_tiny_smoke.yaml`
- Dynamic: `stage_artifacts/local_qwen15b/stage8/qwen25_1p5b_dynamic_qlora_tiny_smoke.yaml`

Shared limits:

- model: `stage_artifacts/local_qwen15b/models/Qwen2.5-1.5B-Instruct`
- dataset: `stage_artifacts/local_qwen15b/data/trl_ultrafeedback_binarized_tiny`
- `max_steps: 5`
- `per_device_train_batch_size: 1`
- `per_device_eval_batch_size: 1`
- `max_length: 512`
- `max_prompt_length: 384`
- `load_in_4bit: true`
- `log_train_samples: false`
- `remove_unused_columns: false`

## Stage L8 Successful Runs
| Variant | Status | Duration | Peak VRAM | Train loss | Eval loss |
|---|---:|---:|---:|---:|---:|
| Static QLoRA | PASS | 13.774 s | 11620 MiB | 2.4892 | 1.0009 |
| Dynamic gamma QLoRA | PASS | 11.676 s | 11693 MiB | 2.3154 | 0.8786 |

Dynamic minus static peak VRAM: 73 MiB.

## Stage L7 vs L8 Repro Check
| Variant | L7 Peak VRAM | L8 Peak VRAM | Delta |
|---|---:|---:|---:|
| Static QLoRA | 11626 MiB | 11620 MiB | -6 MiB |
| Dynamic gamma QLoRA | 11695 MiB | 11693 MiB | -2 MiB |

Loss metrics matched the L7 successful run values for both variants.

## Dynamic Metrics
Eval gamma beta ratio:

- mean: 0.1309451162815094
- min: 0.1309451162815094
- max: 0.1309451162815094

Eval similarity:

- mean: 0.9048781991004944
- min: 0.9048781991004944
- max: 0.9048781991004944

## Log Hygiene
`log_train_samples: false` suppressed the previous prompt/chosen/rejected sample dumps. A grep check for `Prompt sample`, `Chosen sample`, and `Rejected sample` in Stage L8 stdout logs returned no matches.

## Output Footprint
- Static output dir: about 82M.
- Dynamic output dir: about 82M.
- Each adapter file: 73,911,112 bytes.
- Output dirs are ignored by git through the `outputs/` rule.

## Boundary
This is a local fallback smoke and reproducibility check only. It does not prove 8B/9B full fine-tuning behavior and does not support benchmark claims.

No DeepSeek API call, dataset/model download, dependency install, full fine-tuning, 8B/9B run, or system configuration change was performed.

