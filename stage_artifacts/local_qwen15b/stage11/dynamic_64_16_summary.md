# Stage L11 Dynamic 64/16 Summary

Date: 2026-05-05

## Scope
Controlled data-scale dynamic-gamma smoke only.

- Uses the same 64/16 local subset as Stage L10.
- Uses the same `max_steps: 20`, `max_length: 512`, and batch size 1 setup as Stage L10.
- Dynamic gamma is enabled with `sim_linear`.
- No downloads, dependency installs, DeepSeek API calls, full fine-tuning, 8B/9B runs, or system configuration changes were performed.

## Config
- Config: `stage_artifacts/local_qwen15b/stage11/qwen25_1p5b_dynamic_qlora_64_16_20step.yaml`
- Variant: dynamic-gamma QLoRA
- `dynamic_gamma_enabled: true`
- `dynamic_gamma_strategy: sim_linear`
- `dynamic_gamma_min: 0.0`
- `dynamic_gamma_max: 0.25`
- `dynamic_gamma_similarity_scale: 0.5`

## Result
| Variant | Status | Duration | Peak VRAM sample | Train loss | Eval loss | Eval reward acc | Eval gamma mean | Eval similarity mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Dynamic QLoRA 64/16 | PASS | 26.820 s | 10556 MiB | 1.1609 | 0.9086 | 0.375 | 0.1297 | 0.9255 |

The sampled peak stayed below the updated 12GB warning line.

## Static Comparison
| Variant | Peak VRAM sample | Train loss | Eval loss | Eval reward acc |
|---|---:|---:|---:|---:|
| Static QLoRA 64/16, Stage L10 | 10571 MiB | 1.3097 | 1.0390 | 0.375 |
| Dynamic QLoRA 64/16, Stage L11 | 10556 MiB | 1.1609 | 0.9086 | 0.375 |

In this tiny smoke, dynamic-gamma used effectively the same sampled VRAM as static and emitted gamma/similarity metrics as expected.

## Stability Check
- Run completed with return code 0.
- No Traceback/OOM/RuntimeError/TypeError was found.
- `NaN|nan` search only matched the configured `logging_nan_inf_filter=True` line.
- No prompt/chosen/rejected sample dumps were found.
- Output directory is ignored by git through `outputs/`.
- Adapter file size: 73,911,112 bytes.

## Boundary
This is a local fallback smoke and data-scale check only. It does not prove 8B/9B full fine-tuning behavior and does not support benchmark claims.
