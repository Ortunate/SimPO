# Stage L18 Report: Local Fallback Final Evidence Consolidation

## 1. Current Stage
Stage L18 - local fallback final evidence consolidation and GPT-facing summary

Status: PASS

Date: 2026-05-05

Branch: `local-qwen15b-qlora`

## 2. Stage Goal
Consolidate all completed local Qwen2.5-1.5B QLoRA fallback stages through Stage L17.

The user also requested an additional GPT-facing staged summary under:

- `docs_for_human/local_qwen15b/`

This stage is documentation-only:

- no training
- no model loading
- no generation
- no DeepSeek API call
- no download
- no dependency install or upgrade
- no system configuration change
- no artifact deletion
- no `.env` or secret read/print

## 3. Execution / Findings
Read first:

- `AGENTS.md`
- `docs_for_agent/local_qwen15b/local_qwen15b_line.md`
- `docs_for_agent/local_qwen15b/hardware_resource_policy.md`
- `docs_for_agent/local_qwen15b/api_eval_policy.md`
- `docs_for_agent/local_qwen15b/mirror_download_policy.md`
- `docs_for_human/local_qwen15b/stage_17.md`

Key commands run:

```bash
sed -n '1,240p' AGENTS.md
sed -n '1,220p' docs_for_agent/local_qwen15b/local_qwen15b_line.md
sed -n '1,180p' docs_for_agent/local_qwen15b/hardware_resource_policy.md
sed -n '1,220p' docs_for_agent/local_qwen15b/api_eval_policy.md
sed -n '1,260p' docs_for_agent/local_qwen15b/mirror_download_policy.md
sed -n '1,460p' docs_for_human/local_qwen15b/stage_17.md
find docs_for_human/local_qwen15b -maxdepth 1 -type f | sort
git status --short
sed -n '1,180p' docs_for_human/local_qwen15b/stage_0.md
sed -n '1,220p' docs_for_human/local_qwen15b/stage_1.md
sed -n '1,220p' docs_for_human/local_qwen15b/stage_5.md
sed -n '1,220p' docs_for_human/local_qwen15b/stage_6.md
sed -n '1,220p' docs_for_human/local_qwen15b/stage_7.md
sed -n '1,220p' stage_artifacts/local_qwen15b/stage12/l8_l11_comparison.md
cat stage_artifacts/local_qwen15b/stage16/tiny_generation/summary.json
cat stage_artifacts/local_qwen15b/stage17/tiny_judge_batch/aggregate.json
mkdir -p stage_artifacts/local_qwen15b/stage18
```

Stage coverage:

- L0 established the branch documentation and archive structure.
- L1 audited environment/API readiness and recorded minimal approved DeepSeek connectivity context.
- L2-L4 prepared and validated local/static data and config readiness.
- L5 downloaded the local model and approved dataset through mirror/alternate flow.
- L6 audited static code readiness and run gates.
- L7 first ran static and dynamic QLoRA tiny smoke on real Qwen2.5-1.5B.
- L8-L11 produced formal reproducible static/dynamic smoke comparisons.
- L12 consolidated L8-L11 training smoke evidence.
- L13-L14 prepared API-free judge templates, schemas, and AB/BA request formatting.
- L15 validated one approved DeepSeek judge-template request.
- L16 generated tiny static/dynamic responses locally.
- L17 ran a 4-request approved DeepSeek tiny judge batch over the L16 outputs.

Core proof-of-concept result:

- static QLoRA route runs locally
- dynamic-gamma QLoRA route runs locally
- gamma/similarity metrics are emitted
- peak VRAM is sampled and stays within the local 16GB hard budget in completed runs
- tiny generation works for static and dynamic adapters
- DeepSeek judge request path works
- AB/BA tiny judge aggregation works

## 4. Documentation Reorganization
No directory reorganization was performed in Stage L18.

New Stage L18 artifacts:

- `docs_for_human/local_qwen15b/stage_18.md`
- `docs_for_human/local_qwen15b/local_qwen15b_phase_summary_for_gpt.md`
- `stage_artifacts/local_qwen15b/stage18/local_fallback_evidence_summary.md`

## 5. Reusable Assets
Reusable assets now available:

- local-line policy docs under `docs_for_agent/local_qwen15b/`
- human reports `stage_0.md` through `stage_18.md`
- model/data/cache artifacts under ignored `stage_artifacts/local_qwen15b/`
- static and dynamic QLoRA smoke configs and outputs
- Stage L7 smoke runner
- L8-L12 comparison artifacts
- DeepSeek judge template/schema/formatter scripts
- tiny local generation script and outputs
- tiny DeepSeek judge batch runner and aggregation output

## 6. Required Human Approvals for Future Stages
Still require explicit approval before:

- any additional DeepSeek API call
- any larger or benchmark-style paid evaluation
- any local model loading or generation run
- any GPU training run
- any command expected to exceed 10 minutes
- any run expected to exceed 14GB VRAM
- any new model/data download
- any dependency install or upgrade
- deleting outputs, logs, model/data/cache artifacts, or generated stage artifacts
- any claim that exceeds local Qwen2.5-1.5B QLoRA fallback proof-of-concept evidence

## 7. Risks
### High
- Completed runs are proof-of-concept smoke runs, not benchmark or model-quality evidence.
- The branch must not claim to prove 8B/9B full fine-tuning behavior.
- Any future larger paid judge evaluation needs explicit cost and scope approval.

### Medium
- External `nvidia-smi` sampling may miss short memory spikes.
- Tiny synthetic prompts and small preference subsets are not representative.
- Dynamic runs often had lower tiny-run loss than static, but this is not meaningful quality evidence.
- The generated answers from smoke adapters are weak and only validate the pipeline.

### Low
- Some stage reports retain earlier 12GB warning wording before the L13 policy update; current policy is 12GB observation, 14GB caution, 15GB high-risk, 16GB hard ceiling.
- `__pycache__` files exist under stage artifacts from syntax checks and should remain untracked/ignored.

## 8. Recommendation
Recommended next step:

Stop execution and review the full local fallback package.

If one more documentation step is needed, prepare a manuscript-facing limitations and methods appendix from this evidence. Do not run additional training, generation, or API calls unless a new explicit stage scope is requested.

## 9. Executive Summary
- Stage L18 PASS.
- All completed local fallback stages through L17 were consolidated.
- Extra GPT-facing summary was written to `docs_for_human/local_qwen15b/local_qwen15b_phase_summary_for_gpt.md`.
- The local proof-of-concept loop is complete at small scale: static QLoRA, dynamic-gamma QLoRA, memory sampling, gamma/similarity logging, tiny generation, and tiny DeepSeek judge path.
- No training, model loading, generation, API call, download, dependency change, deletion, system configuration change, or secret operation was performed in Stage L18.
