# Stage L15 Report: Single DeepSeek Judge Request and Generation Plan

## 1. Current Stage
Stage L15 - approved single DeepSeek judge-template request plus static/dynamic answer generation planning

Status: PASS

Date: 2026-05-05

Branch: `local-qwen15b-qlora`

## 2. Stage Goal
Execute both approved next actions under project protocol:

1. Run exactly one DeepSeek V4 Flash judge-template API request using one synthetic Stage L14 request.
2. Prepare static/dynamic answer generation config without running generation, loading models, or using GPU.

This stage must not run batch evaluation, full AlpacaEval-style evaluation, model generation, training, downloads, dependency changes, deletion, or system configuration changes.

## 3. Execution / Findings
Read first:

- `AGENTS.md`
- `docs_for_agent/local_qwen15b/api_eval_policy.md`
- `docs_for_agent/local_qwen15b/hardware_resource_policy.md`
- `docs_for_agent/local_qwen15b/local_qwen15b_line.md`
- `docs_for_agent/local_qwen15b/mirror_download_policy.md`
- `docs_for_human/local_qwen15b/stage_14.md`
- `stage_artifacts/local_qwen15b/stage13/api_approval_checklist.md`

Key commands run:

```bash
sed -n '1,240p' AGENTS.md
sed -n '1,220p' docs_for_agent/local_qwen15b/api_eval_policy.md
sed -n '1,180p' docs_for_agent/local_qwen15b/hardware_resource_policy.md
sed -n '1,220p' docs_for_agent/local_qwen15b/local_qwen15b_line.md
sed -n '1,260p' docs_for_agent/local_qwen15b/mirror_download_policy.md
sed -n '1,360p' docs_for_human/local_qwen15b/stage_14.md
sed -n '1,220p' stage_artifacts/local_qwen15b/stage13/api_approval_checklist.md
git status --short
.venv/bin/python stage_artifacts/local_qwen15b/stage15/validate_answer_generation_plan.py
.venv/bin/python -m py_compile stage_artifacts/local_qwen15b/stage15/single_deepseek_judge_request.py stage_artifacts/local_qwen15b/stage15/validate_answer_generation_plan.py
.venv/bin/python -c "<inspect first Stage L14 offline judge request id/order/message count>"
git check-ignore -v .env stage_artifacts/local_qwen15b/outputs/stage10_static_64_16_20step/adapter_model.safetensors stage_artifacts/local_qwen15b/outputs/stage11_dynamic_64_16_20step/adapter_model.safetensors
.venv/bin/python stage_artifacts/local_qwen15b/stage15/single_deepseek_judge_request.py --request-jsonl stage_artifacts/local_qwen15b/stage14/tiny_offline_judge_requests.jsonl --out-dir stage_artifacts/local_qwen15b/stage15/single_api_request --max-tokens 256
cat stage_artifacts/local_qwen15b/stage15/single_api_request/single_request_metadata.json
cat stage_artifacts/local_qwen15b/stage15/single_api_request/single_request_result.json
find stage_artifacts/local_qwen15b/stage15 -maxdepth 3 -type f | sort
du -sh stage_artifacts/local_qwen15b/stage15
```

Generation plan validation:

```text
plan_path=/home/ubuntu0/Code_place/Github_repoes/SimPO/stage_artifacts/local_qwen15b/stage15/answer_generation_plan.json
adapter_count=2
failures=0
```

First offline judge request selected:

```text
request_id synthetic-pair-001-ab
order AB
messages 2
```

Gitignore checks:

- `.env` is ignored.
- Stage L10 static adapter output is ignored through `outputs/`.
- Stage L11 dynamic adapter output is ignored through `outputs/`.

Single DeepSeek API result:

```text
env_file_exists: yes
deepseek_key_present: yes
api_calls: 1
status_code: 200
parse_failures: 0
```

Metadata:

- Request id: `synthetic-pair-001-ab`
- Pair id: `synthetic-pair-001`
- Order: `AB`
- Endpoint host: `api.deepseek.com`
- Model: `deepseek-v4-flash`
- Response model: `deepseek-v4-flash`
- Status code: 200
- Duration: 1.676 s
- Max tokens: 256
- API calls: 1
- Prompt tokens: 214
- Completion tokens: 83
- Total tokens: 297

Parsed judge JSON:

```json
{
  "winner": "A",
  "score_a": 8,
  "score_b": 2,
  "confidence": 0.95,
  "rationale": "Response A provides two concrete, practical pre-launch checks (gitignore and resource monitoring) that help avoid common issues, while response B suggests starting immediately without any checks, which is not practical for a smoke run."
}
```

Secret handling:

- `.env` existence was checked.
- DeepSeek key presence was checked.
- No key value was printed.
- No key value was written to artifacts.
- `.env` content was not printed.
- `.env` was not modified.

## 4. Documentation Reorganization
No directory reorganization was performed in Stage L15.

New Stage L15 artifacts:

- `docs_for_human/local_qwen15b/stage_15.md`
- `stage_artifacts/local_qwen15b/stage15/single_deepseek_judge_request.py`
- `stage_artifacts/local_qwen15b/stage15/answer_generation_plan.json`
- `stage_artifacts/local_qwen15b/stage15/validate_answer_generation_plan.py`
- `stage_artifacts/local_qwen15b/stage15/single_api_request/single_request_metadata.json`
- `stage_artifacts/local_qwen15b/stage15/single_api_request/single_request_result.json`
- `stage_artifacts/local_qwen15b/stage15/stage15_summary.md`

Generated Python `__pycache__` files also exist under Stage L15 from local syntax compilation. They are generated artifacts and should not be committed.

## 5. Reusable Assets
Reusable assets:

- Single-request DeepSeek judge script with non-secret logging.
- Validated response parsing for the pairwise judge JSON schema.
- Non-secret metadata and parsed judge output for one synthetic request.
- Static/dynamic answer generation plan for later model-output preparation.
- Adapter path validation for Stage L10 static and Stage L11 dynamic adapters.

## 6. Required Human Approvals for Future Stages
Still require explicit approval before:

- Any additional DeepSeek API call.
- Any batch or AlpacaEval-style paid evaluation.
- Any `.env` or secret presence check for another API stage.
- Any model loading or local generation run.
- Any GPU training run.
- Any run expected to exceed 14GB VRAM.
- Any command expected to exceed 10 minutes.
- Any new model/data download.
- Any dependency install or upgrade.
- Deleting outputs, logs, model/data/cache artifacts, or generated stage artifacts.

## 7. Risks
### High
- This was a paid/cost-incurring API request, though limited to exactly one request and 297 total tokens.
- The API request used a synthetic formatting fixture. It must not be treated as static/dynamic model evaluation evidence.

### Medium
- Real model answer generation is still not executed. The generation plan only validates paths and future output contracts.
- DeepSeek judge behavior on real model outputs may differ from this synthetic test.
- Future batch evaluation needs aggregation logic for AB/BA swap consistency and position-bias handling.

### Low
- Python `__pycache__` files were generated during syntax compilation and should remain untracked/ignored.

## 8. Recommendation
Recommended Stage L16:

Prepare and optionally run a tiny local generation smoke only after explicit approval for model loading/generation.

Narrow recommended path:

- use 1-2 synthetic prompts
- load base Qwen2.5-1.5B plus one adapter at a time
- generate static and dynamic responses with deterministic settings
- write response JSONL under `stage_artifacts/local_qwen15b/stage16/`
- do not call DeepSeek API in the same stage

If avoiding GPU/model loading, the alternate Stage L16 is to prepare the generation script only and stop before execution.

## 9. Executive Summary
- Stage L15 PASS.
- Exactly one DeepSeek V4 Flash judge-template API request was executed.
- HTTP status: 200.
- Parsed judge JSON passed validation with winner `A`, scores `8` vs `2`, confidence `0.95`.
- Usage was 297 total tokens.
- `.env` and DeepSeek key presence were checked without printing or writing secret values.
- Static/dynamic answer generation planning was prepared and validated with 2 adapter paths and 0 failures.
- No batch evaluation, AlpacaEval-style run, model loading, generation, training, download, dependency change, deletion, or system configuration change was performed.
