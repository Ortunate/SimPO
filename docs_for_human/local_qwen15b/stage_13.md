# Stage L13 Report: VRAM Policy Recalibration and API-Free Judge Template Prep

## 1. Current Stage
Stage L13 - VRAM policy recalibration and API-free AlpacaEval-style judge template preparation

Status: PASS

Date: 2026-05-05

Branch: `local-qwen15b-qlora`

## 2. Stage Goal
Apply the human update that 12GB VRAM does not need heavy warning treatment and that 14/15GB is the range requiring stronger caution.

Then prepare an API-free DeepSeek V4 Flash judge template path for the local fallback evaluation loop:

- no API call
- no `.env` read
- no secret presence check
- no model loading
- no training
- no download
- no dependency change
- no system configuration change

## 3. Execution / Findings
Read first:

- `AGENTS.md`
- `docs_for_agent/local_qwen15b/hardware_resource_policy.md`
- `docs_for_agent/local_qwen15b/api_eval_policy.md`
- `docs_for_agent/local_qwen15b/local_qwen15b_line.md`
- `docs_for_human/local_qwen15b/stage_12.md`

Key commands run:

```bash
sed -n '1,300p' AGENTS.md
sed -n '1,280p' docs_for_agent/local_qwen15b/hardware_resource_policy.md
sed -n '1,260p' docs_for_agent/local_qwen15b/api_eval_policy.md
sed -n '1,260p' docs_for_agent/local_qwen15b/local_qwen15b_line.md
sed -n '1,380p' docs_for_human/local_qwen15b/stage_12.md
git status --short
find . -maxdepth 4 -iname '*eval*' -o -iname '*judge*' | sort
find eval -maxdepth 4 -type f | sort
rg -n "alpaca|judge|template|DeepSeek|OpenAI|api|score|winner" eval docs_for_agent docs_for_human scripts -g '!stage_artifacts/**'
rg -n "12GB|14GB|15GB|16GB|VRAM|warning line|警戒" AGENTS.md docs_for_agent/local_qwen15b docs_for_human/local_qwen15b/stage_12.md stage_artifacts/local_qwen15b/stage12/l8_l11_comparison.md
.venv/bin/python stage_artifacts/local_qwen15b/stage13/dry_run_validate_judge_schema.py stage_artifacts/local_qwen15b/stage13/synthetic_eval_examples.jsonl
.venv/bin/python -m json.tool stage_artifacts/local_qwen15b/stage13/judge_output_schema.json
rg -n "12GB|14GB|15GB|16GB|VRAM|warning line|caution line|high-risk" AGENTS.md docs_for_agent/local_qwen15b/hardware_resource_policy.md stage_artifacts/local_qwen15b/stage13
```

Policy updates:

- `AGENTS.md`
  - Approval threshold changed from expected `>12GB GPU VRAM` to expected `>14GB GPU VRAM`.
  - Added tiered VRAM policy:
    - 12GB sampled VRAM is a normal observation point.
    - 14GB is the caution line.
    - 15GB or higher is high-risk local work.
    - 16GB remains the hard local device ceiling.
- `docs_for_agent/local_qwen15b/hardware_resource_policy.md`
  - Same tiered policy added.
  - Same approval threshold changed to expected `>14GB GPU VRAM`.

Evaluation-template preparation:

- Created a DeepSeek V4 Flash pairwise judge template draft.
- Created a strict JSON output schema.
- Created synthetic local examples.
- Created a dependency-free dry-run validator.
- Created an API approval checklist for later stages.

Dry-run validation:

```text
line 1: PASS: synthetic-001
line 2: PASS: synthetic-002
validated_examples=2
failures=0
```

JSON schema parse check passed through `python -m json.tool`.

## 4. Documentation Reorganization
No directory reorganization was performed in Stage L13.

Updated policy docs:

- `AGENTS.md`
- `docs_for_agent/local_qwen15b/hardware_resource_policy.md`

New Stage L13 artifacts:

- `docs_for_human/local_qwen15b/stage_13.md`
- `stage_artifacts/local_qwen15b/stage13/deepseek_judge_template.md`
- `stage_artifacts/local_qwen15b/stage13/judge_output_schema.json`
- `stage_artifacts/local_qwen15b/stage13/synthetic_eval_examples.jsonl`
- `stage_artifacts/local_qwen15b/stage13/dry_run_validate_judge_schema.py`
- `stage_artifacts/local_qwen15b/stage13/api_approval_checklist.md`

## 5. Reusable Assets
Reusable assets:

- Updated VRAM tiering for later local run planning.
- API-free pairwise judge prompt template.
- Strict judge JSON output schema.
- Synthetic dry-run examples.
- Local schema validator with no extra dependencies.
- API approval checklist for the later paid DeepSeek stage.

Existing repo eval assets noted:

- `eval/alpacaeval2/` contains prior generation configs/templates for other models.
- `eval/arenahard/` contains prior judge configs/templates for other model families.

The new Stage L13 assets are intentionally separate under `stage_artifacts/local_qwen15b/stage13/` to avoid mutating legacy benchmark configs.

## 6. Required Human Approvals for Future Stages
Still require explicit approval before:

- Any GPU training run.
- Loading the real Qwen2.5-1.5B-Instruct model.
- Any run expected to exceed 14GB VRAM.
- Any run sampled near or above 15GB VRAM continuing without a stop/rollback decision.
- Any command expected to exceed 10 minutes.
- Increasing `max_length`.
- Increasing batch size or gradient accumulation.
- Using a larger dataset subset.
- Any DeepSeek API call, including a single judge-template test.
- Any AlpacaEval-style paid judge run.
- Any new model/data download.
- Any dependency install or upgrade.
- Deleting outputs, logs, model/data/cache artifacts.

## 7. Risks
### High
- Any later API judge call may incur cost and must remain a separate approved stage.
- 15GB VRAM is close to the 16GB hard ceiling; runs near that range can fail from transient spikes even if external samples appear below the ceiling.

### Medium
- The Stage L13 judge template is only a local draft. Real API behavior may require small formatting adjustments after an approved single-request test.
- Pairwise judging can be position-biased; later stages should include A/B swap checks if cost allows.
- Current local training evidence remains smoke-level and must not be converted into benchmark claims.

### Low
- The dry-run validator checks schema shape only; it does not validate judge quality.
- Existing eval configs target other model families and should not be reused blindly for Qwen2.5-1.5B.

## 8. Recommendation
Recommended Stage L14:

Prepare a tiny offline evaluation input pack from existing local smoke artifacts or synthetic examples, still with no API call.

Stage L14 should:

- define the exact JSONL input format for later judge calls
- include response pair identifiers and provenance fields
- implement local formatting from JSONL to chat messages
- validate A/B and B/A swap construction locally
- stop before any DeepSeek API request

After Stage L14, a separately approved Stage L15 can do a single paid DeepSeek judge-template request.

## 9. Executive Summary
- Stage L13 PASS.
- VRAM policy was recalibrated: 12GB is normal observation, 14GB is caution, 15GB or higher is high-risk, 16GB remains the hard local ceiling.
- Approval threshold for expected GPU VRAM usage was updated from `>12GB` to `>14GB`.
- API-free DeepSeek judge template, JSON schema, synthetic examples, validator, and approval checklist were created.
- Dry-run validation passed with 2/2 synthetic examples.
- No training, model loading, download, dependency change, API call, `.env` read, secret operation, deletion, or system configuration change was performed.
