# Stage L0 Report: Local Qwen2.5-1.5B QLoRA Fallback Line Setup

## 1. Current Stage
Name: Stage L0 - Documentation reorganization and local fallback line setup

Status: PASS

Date: 2026-05-05

Branch: `local-qwen15b-qlora`

## 2. Stage Goal
Establish this branch as the local Qwen2.5-1.5B-Instruct QLoRA fallback route.

Non-goals:

- no model download
- no dataset download
- no training
- no real Qwen2.5-1.5B model loading
- no GPU-heavy command
- no DeepSeek API call
- no dependency installation or upgrade
- no WSL/CUDA/driver/global environment modification

## 3. Execution / Findings
Commands run:

- `git branch --show-current`
- `git status --short --branch`
- `find docs_for_agent docs_for_human stage_artifacts -maxdepth 3 -type f`
- `sed` reads of `AGENTS.md`, archived project brief, templates, and hardware notes
- `rg` search for SimPO, gamma, margin, and dynamic gamma implementation
- `sed` reads of `scripts/run_simpo.py`, `scripts/simpo_config.py`, `scripts/simpo_trainer.py`, and `stage_artifacts/stage4/dynamic_gamma_code_review.md`
- `mkdir -p` for new local-line directories
- `git mv` for previous-phase documentation archival

Key findings:

- Current branch is `local-qwen15b-qlora`.
- Initial working tree was clean.
- The real SimPO training entrypoint is `scripts/run_simpo.py`.
- SimPO configuration is in `scripts/simpo_config.py`.
- SimPO loss and dynamic gamma logic are in `scripts/simpo_trainer.py`.
- Existing dynamic gamma can be disabled by config and currently defaults to disabled.
- Existing dynamic metrics include gamma beta ratio summaries and similarity summaries.

No model/data/API/GPU-heavy action was run.

## 4. Documentation Reorganization
Performed reorganization:

- moved previous agent docs into `docs_for_agent/archive_previous_local_phase/`
- moved previous experiment logs into `docs_for_agent/archive_previous_local_phase/experiment_logs/`
- moved previous human reports into `docs_for_human/archive_previous_local_phase/`
- created `docs_for_agent/local_qwen15b/`
- created `docs_for_human/local_qwen15b/`
- created `stage_artifacts/local_qwen15b/`
- updated root `AGENTS.md` as the branch entrypoint for the local Qwen2.5-1.5B QLoRA fallback line

New local-line docs:

- `docs_for_agent/local_qwen15b/local_qwen15b_line.md`
- `docs_for_agent/local_qwen15b/hardware_resource_policy.md`
- `docs_for_agent/local_qwen15b/mirror_download_policy.md`
- `docs_for_agent/local_qwen15b/api_eval_policy.md`
- `docs_for_agent/local_qwen15b/stage_report_template.md`
- `docs_for_agent/local_qwen15b/experiment_log_template.md`

`AGENTS.md` now states:

- this branch is the local Qwen2.5-1.5B-Instruct QLoRA fallback line
- reports go under `docs_for_human/local_qwen15b/`
- local-line artifacts go under `stage_artifacts/local_qwen15b/`
- approval is required before GPU training, real Qwen model loading, dataset download, large file download, long runs, high-memory commands, system changes, API calls, and destructive artifact deletion
- files >= 0.3GB require mirror/alternate-source planning and approval
- DeepSeek key management is out of scope; only presence checks are allowed before future approved API calls

## 5. Reusable Assets
Reusable code path:

- `scripts/run_simpo.py`: existing SimPO entrypoint
- `scripts/simpo_config.py`: dynamic gamma arguments already present
- `scripts/simpo_trainer.py`: static SimPO loss, optional per-sample dynamic gamma, hidden-state similarity, and logging

Reusable prior artifacts:

- archived experiment logs under `docs_for_agent/archive_previous_local_phase/experiment_logs/`
- prior code review at `stage_artifacts/stage4/dynamic_gamma_code_review.md`
- prior tiny validation scripts under `stage_artifacts/stage2/`, `stage_artifacts/stage3/`, and `stage_artifacts/stage4/`

These are references only for the new local Qwen1.5B route. They do not prove Qwen2.5-1.5B QLoRA behavior until this branch runs approved validation.

## 6. Local Qwen1.5B Route Stage Plan
Stage L1: environment and static readiness audit without large installs or downloads.

Stage L2: smallest static path validation on dummy/tiny assets where possible.

Stage L3: smallest dynamic gamma validation with gamma/similarity logging.

Stage L4: approved Qwen2.5-1.5B QLoRA static vs dynamic smoke and memory comparison.

Stage L5: approved DeepSeek judge-template and tiny API connectivity/evaluation checks.

Stage L6: final local fallback report with limitations and next actions.

## 7. Resource Usage
Model loaded: no

Dataset downloaded: no

GPU-heavy action run: no

API call run: no

Dependency install/upgrade: no

WSL/CUDA/driver/global config modified: no

Expected VRAM used by this stage: none beyond normal shell/editor usage

## 8. Risks
### High
- Qwen2.5-1.5B QLoRA memory behavior remains unvalidated on this local WSL node.
- Real data and real model downloads are future approval gates and may be blocked by source/mirror availability.

### Medium
- Existing dynamic gamma uses an LM-head pre-hook; compatibility with Qwen2.5-1.5B plus QLoRA/PEFT still needs validation.
- Prior tiny validation artifacts came from an earlier local phase and are references, not evidence for this branch.

### Low
- Documentation paths changed; future agents must read the new `docs_for_agent/local_qwen15b/` docs rather than old root templates.

## 9. Recommendation
Recommended decision: Proceed to Stage L1 only.

Stage L1 should audit the environment and prepare static QLoRA readiness without downloads, model loading, GPU training, API calls, or dependency upgrades unless separately approved.

## 10. Executive Summary
- Stage L0 passed.
- Branch confirmed: `local-qwen15b-qlora`.
- Previous local infrastructure docs and reports were archived, not deleted.
- New local Qwen2.5-1.5B QLoRA fallback documentation was created.
- Root `AGENTS.md` now points to the new local-line docs and approval policies.
- Existing SimPO dynamic gamma code appears reusable as the starting point.
- No model, dataset, API, training, GPU-heavy command, dependency upgrade, or system configuration change was performed.
- Next recommended stage is L1: local environment and static readiness audit.
