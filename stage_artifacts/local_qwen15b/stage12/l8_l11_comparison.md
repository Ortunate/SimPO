# Stage L12 L8-L11 Local Fallback Comparison

Date: 2026-05-05

## Scope
This artifact consolidates completed local Qwen2.5-1.5B-Instruct QLoRA fallback smoke runs from Stage L8 through Stage L11.

No training, model loading, downloads, dependency changes, API calls, system configuration changes, deletion, or secret checks were performed while creating this artifact.

## Consolidated Results
| Stage | Variant | Data scale | Max steps | Max length | Peak VRAM sample | Duration | Train loss | Eval loss | Eval reward acc | Eval gamma mean | Eval similarity mean |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| L8 | Static QLoRA | 16/8 tiny | 5 | 512 | 11620 MiB | 13.774 s | 2.4892 | 1.0009 | n/a | n/a | n/a |
| L8 | Dynamic QLoRA | 16/8 tiny | 5 | 512 | 11693 MiB | 11.676 s | 2.3154 | 0.8786 | n/a | 0.1309 | 0.9049 |
| L9 | Static QLoRA | 16/8 tiny | 20 | 512 | 11945 MiB | 25.546 s | 1.6594 | 0.9879 | 0.625 | n/a | n/a |
| L9 | Dynamic QLoRA | 16/8 tiny | 20 | 512 | 11758 MiB | 23.463 s | 1.4992 | 0.8711 | 0.500 | 0.1310 | 0.9045 |
| L10 | Static QLoRA | 64/16 | 20 | 512 | 10571 MiB | 30.306 s | 1.3097 | 1.0390 | 0.375 | n/a | n/a |
| L11 | Dynamic QLoRA | 64/16 | 20 | 512 | 10556 MiB | 26.820 s | 1.1609 | 0.9086 | 0.375 | 0.1297 | 0.9255 |

## Same-Scale Comparisons
### L8 5-Step Tiny
| Metric | Static | Dynamic | Dynamic minus static |
|---|---:|---:|---:|
| Peak VRAM sample | 11620 MiB | 11693 MiB | +73 MiB |
| Train loss | 2.4892 | 2.3154 | -0.1738 |
| Eval loss | 1.0009 | 0.8786 | -0.1223 |

### L9 20-Step Tiny
| Metric | Static | Dynamic | Dynamic minus static |
|---|---:|---:|---:|
| Peak VRAM sample | 11945 MiB | 11758 MiB | -187 MiB |
| Train loss | 1.6594 | 1.4992 | -0.1602 |
| Eval loss | 0.9879 | 0.8711 | -0.1168 |
| Eval reward acc | 0.625 | 0.500 | -0.125 |

### L10/L11 20-Step 64/16
| Metric | Static | Dynamic | Dynamic minus static |
|---|---:|---:|---:|
| Peak VRAM sample | 10571 MiB | 10556 MiB | -15 MiB |
| Train loss | 1.3097 | 1.1609 | -0.1488 |
| Eval loss | 1.0390 | 0.9086 | -0.1304 |
| Eval reward acc | 0.375 | 0.375 | 0.000 |

## Resource Read
- All L8-L11 sampled peaks stayed below the current 12GB warning line.
- The highest sampled peak was L9 static at 11945 MiB, only 343 MiB below 12GB.
- The 64/16 pair stayed around 10.56GB sampled VRAM, but this may reflect sample lengths and wall-clock sampling.
- External `nvidia-smi` sampling is useful for comparison, but not an exact allocator maximum.

## Logging Read
- Dynamic runs emitted gamma metrics.
- Dynamic runs emitted similarity metrics.
- `log_train_samples: false` suppressed prompt/chosen/rejected sample dumps in the formal configs.
- No successful L8-L11 report recorded Traceback or OOM.

## Interpretation Boundary
These are local fallback smoke results only.

They support:

- Qwen2.5-1.5B-Instruct QLoRA can run locally in this branch.
- Static and dynamic-gamma paths both execute.
- Dynamic-gamma logging is present.
- Sampled VRAM is currently under the 12GB warning line for these small runs.

They do not support:

- benchmark claims
- model quality claims
- full fine-tuning claims
- 8B/9B behavior claims
- production readiness claims

## Next-Step Decision
The next execution stage should be one of two narrow paths:

1. Same-shape longer run: static and dynamic on 64/16, `max_length: 512`, batch size 1, more steps, with timeout and 12GB warning-line monitoring.
2. Evaluation-template preparation: create DeepSeek judge prompt/schema and dry-run parsing with no API call.

Given the project-completion fallback goal, the recommended next stage is evaluation-template preparation first. It reduces API-stage risk without increasing GPU pressure or producing another tiny training artifact with limited interpretive value.
