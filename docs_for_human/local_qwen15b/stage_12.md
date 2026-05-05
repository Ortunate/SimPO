# Stage L12 Report: L8-L11 Consolidated Readiness Review

## 1. Current Stage
Stage L12 - consolidated local fallback comparison and next-stage decision

Status: PASS

Date: 2026-05-05

Branch: `local-qwen15b-qlora`

## 2. Stage Goal
Create a consolidated comparison table for completed local Qwen2.5-1.5B QLoRA fallback runs from Stage L8 through Stage L11, then decide the narrowest useful next stage.

This stage is intentionally non-execution-heavy:

- no training
- no model loading
- no dataset/model download
- no dependency install or upgrade
- no DeepSeek API call
- no system configuration change
- no deletion of artifacts
- no secret printing or secret checks

## 3. Execution / Findings
Read first:

- `AGENTS.md`
- `docs_for_agent/local_qwen15b/local_qwen15b_line.md`
- `docs_for_agent/local_qwen15b/hardware_resource_policy.md`
- `docs_for_agent/local_qwen15b/mirror_download_policy.md`
- `docs_for_agent/local_qwen15b/api_eval_policy.md`
- `docs_for_human/local_qwen15b/stage_11.md`

Key commands run:

```bash
sed -n '1,280p' AGENTS.md
sed -n '1,260p' docs_for_agent/local_qwen15b/local_qwen15b_line.md
sed -n '1,260p' docs_for_agent/local_qwen15b/hardware_resource_policy.md
sed -n '1,260p' docs_for_agent/local_qwen15b/mirror_download_policy.md
sed -n '1,240p' docs_for_agent/local_qwen15b/api_eval_policy.md
sed -n '1,340p' docs_for_human/local_qwen15b/stage_11.md
git status --short
find stage_artifacts/local_qwen15b/stage8 -maxdepth 3 -type f | sort
find stage_artifacts/local_qwen15b/stage9 -maxdepth 3 -type f | sort
find stage_artifacts/local_qwen15b/stage10 -maxdepth 3 -type f | sort
find stage_artifacts/local_qwen15b/stage11 -maxdepth 3 -type f | sort
find stage_artifacts/local_qwen15b/outputs -maxdepth 2 -name '*results.json' | sort
sed -n '1,260p' stage_artifacts/local_qwen15b/stage8/repro_summary.md
sed -n '1,260p' stage_artifacts/local_qwen15b/stage9/controlled_20step_summary.md
sed -n '1,220p' stage_artifacts/local_qwen15b/stage10/static_64_16_summary.md
sed -n '1,220p' stage_artifacts/local_qwen15b/stage11/dynamic_64_16_summary.md
mkdir -p stage_artifacts/local_qwen15b/stage12
```

Consolidated results:

| Stage | Variant | Data scale | Max steps | Max length | Peak VRAM sample | Duration | Train loss | Eval loss | Eval reward acc | Eval gamma mean | Eval similarity mean |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| L8 | Static QLoRA | 16/8 tiny | 5 | 512 | 11620 MiB | 13.774 s | 2.4892 | 1.0009 | n/a | n/a | n/a |
| L8 | Dynamic QLoRA | 16/8 tiny | 5 | 512 | 11693 MiB | 11.676 s | 2.3154 | 0.8786 | n/a | 0.1309 | 0.9049 |
| L9 | Static QLoRA | 16/8 tiny | 20 | 512 | 11945 MiB | 25.546 s | 1.6594 | 0.9879 | 0.625 | n/a | n/a |
| L9 | Dynamic QLoRA | 16/8 tiny | 20 | 512 | 11758 MiB | 23.463 s | 1.4992 | 0.8711 | 0.500 | 0.1310 | 0.9045 |
| L10 | Static QLoRA | 64/16 | 20 | 512 | 10571 MiB | 30.306 s | 1.3097 | 1.0390 | 0.375 | n/a | n/a |
| L11 | Dynamic QLoRA | 64/16 | 20 | 512 | 10556 MiB | 26.820 s | 1.1609 | 0.9086 | 0.375 | 0.1297 | 0.9255 |

Findings:

- Static and dynamic QLoRA both run locally on Qwen2.5-1.5B-Instruct.
- Dynamic-gamma consistently emits gamma and similarity metrics.
- All sampled peaks stayed below the current 12GB warning line.
- L9 static reached 11945 MiB, leaving only about 343 MiB before 12GB.
- L10/L11 64/16 sampled peaks were lower than L9 despite more rows, likely due to sample lengths and external sampling cadence, not a guaranteed memory reduction.
- The existing evidence is coherent enough to move toward evaluation preparation, but not enough for quality or benchmark claims.

## 4. Documentation Reorganization
No documentation reorganization was performed in Stage L12.

New Stage L12 artifacts:

- `docs_for_human/local_qwen15b/stage_12.md`
- `stage_artifacts/local_qwen15b/stage12/l8_l11_comparison.md`

## 5. Reusable Assets
Reusable assets consolidated by this stage:

- L8 static/dynamic formal tiny configs and reproducibility summary.
- L9 static/dynamic 20-step tiny configs and summary.
- L10 static 64/16 config and summary.
- L11 dynamic 64/16 config and summary.
- Same-scale comparison tables for L8, L9, and L10/L11.
- Decision record for choosing the next stage.

## 6. Required Human Approvals for Future Stages
Still require explicit approval before:

- Any GPU training run.
- Loading the real Qwen2.5-1.5B-Instruct model.
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
- L8-L11 are smoke and stability checks only. They must not be framed as benchmark, model-quality, production, full fine-tuning, or 8B/9B evidence.
- L9 static was close to the 12GB warning line. Any longer sequence, larger batch, or different sample distribution may cross it.

### Medium
- External `nvidia-smi` sampling may miss short allocator spikes.
- The tiny and 64/16 subsets are not representative enough for quality conclusions.
- Dynamic runs show lower tiny-run losses, but that is not meaningful evidence of general preference performance.

### Low
- Existing `evaluation_strategy` warning remains non-blocking.
- Current reports are numerous; a later final report should avoid overclaiming while summarizing only the stable evidence.

## 8. Recommendation
Recommended Stage L13:

Prepare local AlpacaEval-style evaluation templates and output schemas with no API call.

Stage L13 should:

- create a small non-secret judge-template doc or JSON schema under `stage_artifacts/local_qwen15b/`
- create a dry-run parser using synthetic local examples only, if needed
- avoid reading or printing `.env`
- avoid DeepSeek API calls
- record exactly what approvals are needed for the later paid API connectivity test

Rationale: the static/dynamic training loop is now sufficiently smoke-tested at small scale. Evaluation-template preparation advances the project-completion fallback route without increasing GPU pressure.

## 9. Executive Summary
- Stage L12 PASS.
- No training, model loading, download, dependency change, API call, system config change, deletion, or secret operation was performed.
- L8-L11 evidence was consolidated into `stage_artifacts/local_qwen15b/stage12/l8_l11_comparison.md`.
- Static and dynamic QLoRA both run locally.
- Dynamic-gamma emits gamma/similarity metrics.
- All sampled peaks stayed below the current 12GB warning line, but L9 static came close at 11945 MiB.
- Next recommended stage is API-free evaluation-template preparation, not another immediate larger GPU run.
