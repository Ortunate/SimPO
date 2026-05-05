# Stage L11 Report: Dynamic 64/16 Data-Scale Smoke

## 1. Current Stage
Stage L11 - dynamic-gamma QLoRA 64/16 data-scale smoke

Status: PASS

Date: 2026-05-05

Branch: `local-qwen15b-qlora`

## 2. Stage Goal
Run the narrowest next stage after Stage L10:

- Use the same local 64/16 subset as Stage L10.
- Keep `max_steps: 20`.
- Keep `max_length: 512`.
- Keep batch size 1.
- Enable dynamic gamma with the existing `sim_linear` path.
- Compare against Stage L10 static QLoRA on the same data scale.

This stage does not download models/data, does not install dependencies, does not call DeepSeek API, does not modify system configuration, and does not run full fine-tuning.

## 3. Execution / Findings
Read first:

- `AGENTS.md`
- `docs_for_agent/local_qwen15b/local_qwen15b_line.md`
- `docs_for_agent/local_qwen15b/hardware_resource_policy.md`
- `docs_for_agent/local_qwen15b/mirror_download_policy.md`
- `docs_for_agent/local_qwen15b/api_eval_policy.md`
- `docs_for_human/local_qwen15b/stage_10.md`

Key commands run:

```bash
sed -n '1,280p' AGENTS.md
sed -n '1,260p' docs_for_agent/local_qwen15b/local_qwen15b_line.md
sed -n '1,260p' docs_for_agent/local_qwen15b/hardware_resource_policy.md
sed -n '1,260p' docs_for_agent/local_qwen15b/mirror_download_policy.md
sed -n '1,240p' docs_for_agent/local_qwen15b/api_eval_policy.md
sed -n '1,320p' docs_for_human/local_qwen15b/stage_10.md
git status --short
sed -n '1,260p' stage_artifacts/local_qwen15b/stage10/qwen25_1p5b_static_qlora_64_16_20step.yaml
sed -n '1,280p' stage_artifacts/local_qwen15b/stage9/qwen25_1p5b_dynamic_qlora_20step.yaml
find stage_artifacts/local_qwen15b/stage10 -maxdepth 3 -type f | sort
find stage_artifacts/local_qwen15b/data/trl_ultrafeedback_binarized_64_16 -maxdepth 2 -type f | sort
.venv/bin/python -c "<parse Stage L11 YAML with H4ArgumentParser>"
git check-ignore -v stage_artifacts/local_qwen15b/outputs/stage11_dynamic_64_16_20step stage_artifacts/local_qwen15b/data/trl_ultrafeedback_binarized_64_16/train.jsonl stage_artifacts/local_qwen15b/stage11/qwen25_1p5b_dynamic_qlora_64_16_20step.yaml
du -sh stage_artifacts/local_qwen15b/data/trl_ultrafeedback_binarized_64_16 stage_artifacts/local_qwen15b/models/Qwen2.5-1.5B-Instruct
nvidia-smi --query-gpu=name,memory.total,memory.used --format=csv,noheader,nounits
timeout 10m .venv/bin/python stage_artifacts/local_qwen15b/stage7_run_smoke.py --label dynamic --config stage_artifacts/local_qwen15b/stage11/qwen25_1p5b_dynamic_qlora_64_16_20step.yaml --out-dir stage_artifacts/local_qwen15b/stage11/dynamic_64_16_20step
cat stage_artifacts/local_qwen15b/stage11/dynamic_64_16_20step/summary.json
cat stage_artifacts/local_qwen15b/outputs/stage11_dynamic_64_16_20step/train_results.json
cat stage_artifacts/local_qwen15b/outputs/stage11_dynamic_64_16_20step/eval_results.json
rg -n "'loss'|train_loss|eval_loss|grad_norm|rewards/|logps/|dynamic_gamma|gamma|similarity" stage_artifacts/local_qwen15b/stage11/dynamic_64_16_20step/*.log
rg -n "Traceback|CUDA out|out of memory|RuntimeError|ValueError|TypeError|NaN|nan" stage_artifacts/local_qwen15b/stage11/dynamic_64_16_20step/*.log
rg -n "Prompt sample|Chosen sample|Rejected sample" stage_artifacts/local_qwen15b/stage11/dynamic_64_16_20step/stdout.log
du -sh stage_artifacts/local_qwen15b/outputs/stage11_dynamic_64_16_20step stage_artifacts/local_qwen15b/stage11/dynamic_64_16_20step
stat -c '%n %s' stage_artifacts/local_qwen15b/outputs/stage11_dynamic_64_16_20step/adapter_model.safetensors
cat stage_artifacts/local_qwen15b/outputs/stage10_static_64_16_20step/train_results.json
cat stage_artifacts/local_qwen15b/outputs/stage10_static_64_16_20step/eval_results.json
cat stage_artifacts/local_qwen15b/stage10/static_64_16_20step/summary.json
git check-ignore -v stage_artifacts/local_qwen15b/outputs/stage11_dynamic_64_16_20step/adapter_model.safetensors stage_artifacts/local_qwen15b/stage11/dynamic_64_16_20step/stdout.log stage_artifacts/local_qwen15b/stage11/dynamic_64_16_20step/summary.json
```

Config added:

- `stage_artifacts/local_qwen15b/stage11/qwen25_1p5b_dynamic_qlora_64_16_20step.yaml`

Run result:

| Variant | Status | Peak VRAM sample | Train loss | Eval loss | Eval reward acc | Eval gamma mean | Eval similarity mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| Dynamic QLoRA 64/16 | PASS | 10556 MiB | 1.1609 | 0.9086 | 0.375 | 0.1297 | 0.9255 |

Static comparison from Stage L10:

| Variant | Peak VRAM sample | Train loss | Eval loss | Eval reward acc |
|---|---:|---:|---:|---:|
| Static QLoRA 64/16 | 10571 MiB | 1.3097 | 1.0390 | 0.375 |

Dynamic-gamma observations:

- `dynamic_gamma_enabled=True` was present in the training log.
- Train-step gamma and similarity metrics were emitted.
- Final eval gamma mean/min/max were all `0.1296570897102356`.
- Final eval similarity mean/min/max were all `0.9254865646362305`.

Stability checks:

- Return code: 0.
- Duration: 26.820 seconds.
- GPU sample count: 25.
- Peak sampled VRAM: 10556 MiB, below the current 12GB warning line.
- No Traceback/OOM/RuntimeError/TypeError found.
- `NaN|nan` search only matched `logging_nan_inf_filter=True`; no numeric NaN failure was found.
- No prompt/chosen/rejected sample dumps found.
- Adapter file size: 73,911,112 bytes.
- Output directory size: about 82M.

## 4. Documentation Reorganization
No directory reorganization was performed in Stage L11.

New Stage L11 artifacts:

- `docs_for_human/local_qwen15b/stage_11.md`
- `stage_artifacts/local_qwen15b/stage11/dynamic_64_16_summary.md`
- `stage_artifacts/local_qwen15b/stage11/qwen25_1p5b_dynamic_qlora_64_16_20step.yaml`
- `stage_artifacts/local_qwen15b/stage11/dynamic_64_16_20step/summary.json`
- `stage_artifacts/local_qwen15b/stage11/dynamic_64_16_20step/gpu_samples.jsonl`

Ignored generated artifacts:

- `stage_artifacts/local_qwen15b/outputs/stage11_dynamic_64_16_20step/`
- Stage L11 `.log` files under the run directory.

## 5. Reusable Assets
Reusable assets:

- Stage L11 dynamic 64/16 config.
- Stage L11 dynamic loss/eval/gamma/similarity logs.
- Stage L11 sampled VRAM trace.
- Stage L10 vs L11 same-scale comparison.
- Existing local Qwen2.5-1.5B QLoRA smoke runner.

## 6. Required Human Approvals for Future Stages
Still require explicit approval before:

- Any run expected to exceed 12GB VRAM.
- Any command expected to exceed 10 minutes.
- Increasing `max_length`.
- Increasing batch size or gradient accumulation.
- Using a larger dataset subset.
- Running a longer training run.
- Any DeepSeek API call or AlpacaEval-style judge.
- Any new model/data download.
- Any dependency install or upgrade.
- Deleting outputs, logs, model/data/cache artifacts.

## 7. Risks
### High
- This is still a tiny smoke run. It is useful for route validation, but it is not training-quality evidence and must not be used for benchmark claims or 8B/9B full fine-tuning claims.
- Future longer or larger runs may cross the 12GB warning line even though this run did not.

### Medium
- The 64/16 subset is first-row derived from local parquet files, not a curated representative split.
- The dynamic result has lower tiny-run train/eval loss than static, but the sample size and step count are too small for quality conclusions.
- Peak VRAM is sampled externally, so short spikes between samples may be missed.

### Low
- `evaluation_strategy` deprecation warning remains non-blocking.
- `logging_nan_inf_filter=True` creates a false-positive `nan` text hit during broad log searches.

## 8. Recommendation
Next recommended Stage L12:

- Create a consolidated local fallback comparison table covering L8, L9, L10, and L11.
- Decide whether the next execution stage should be a slightly longer same-configuration run or evaluation-template preparation.
- Do not expand data size, sequence length, or batch size until the comparison table confirms the current memory and logging evidence is coherent.

If proceeding directly to another run, the narrowest useful run is a same-shape static/dynamic pair with more steps but no larger data/length/batch.

## 9. Executive Summary
- Stage L11 PASS.
- Dynamic-gamma QLoRA on the same 64/16 subset completed successfully.
- Peak VRAM sample: 10556 MiB, below the 12GB warning line.
- Train loss: 1.1609; eval loss: 0.9086; eval reward accuracy: 0.375.
- Eval gamma mean: 0.1297; eval similarity mean: 0.9255.
- Static Stage L10 comparison peak was 10571 MiB, so sampled VRAM was effectively unchanged at this scale.
- No download, dependency install, DeepSeek API call, full fine-tuning, 8B/9B training, system config change, deletion, or secret exposure occurred.
