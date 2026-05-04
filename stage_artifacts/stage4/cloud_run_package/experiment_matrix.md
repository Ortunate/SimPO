# Stage 4 Experiment Matrix

## Primary Matrix

| Run ID | Type | Model | Dataset | Gamma Mode | Key Gamma Settings | Purpose | Promotion Criteria |
|---|---|---|---|---|---|---|---|
| `stage4-gemma-2-9b-it-simpo-static` | baseline | `google/gemma-2-9b-it` | `princeton-nlp/gemma2-ultrafeedback-armorm` | static | `beta=10`, `gamma_beta_ratio=0.5` | Reproduce the closest repository baseline for comparison | Completes without OOM/NaN; logs train/eval metrics; checkpoint saved |
| `stage4-gemma-2-9b-it-simpo-dynamic-sim-linear` | dynamic | `google/gemma-2-9b-it` | `princeton-nlp/gemma2-ultrafeedback-armorm` | `sim_linear` | base `gamma_beta_ratio=0.5`, `scale=0.5`, clamp `[0.0, 0.5]` | Test the adaptive gamma hypothesis with minimum experiment count | Completes without OOM/NaN; gamma/similarity logs sane; memory not materially worse than baseline |

## Deferred Matrix

| Candidate | Reason Deferred |
|---|---|
| Llama-3-8B-Instruct static/dynamic | Requires gated model access and `flash_attention_2` readiness; run only if Gemma path passes or project direction changes |
| Curriculum gamma | Not implemented yet; would expand scope beyond the validated `sim_linear` prototype |
| Combined similarity + curriculum | Not implemented yet; defer until `sim_linear` has real-run evidence |
| Large ablation grid | Conflicts with the project priority to minimize experiment count |

## Required Comparison Fields

Record these fields for both primary runs:

- git commit and dirty diff summary
- exact config path and copied config snapshot
- accelerate config path
- environment package versions
- model and dataset revisions if pinned
- total samples and effective global batch size
- train loss and eval loss
- grad norm trend
- rewards/margins trend
- peak GPU memory per process if available
- wall-clock runtime
- checkpoint path
- W&B or offline log path
- final model output path

Dynamic-only fields:

- `gamma_beta_ratio/mean`
- `gamma_beta_ratio/min`
- `gamma_beta_ratio/max`
- `similarity/mean`
- `similarity/min`
- `similarity/max`

## Stop Conditions

Stop and review if any of these occur:

- OOM or repeated CUDA allocator failures
- NaN/Inf in loss, reward, gamma, similarity, or grad norm
- severe loss divergence relative to static baseline
- dynamic run materially exceeds baseline memory without a clear explanation
- hidden-state hook fails under the cloud/distributed wrapper
- dataset formatting mismatch or unexpected prompt/chosen/rejected schema
