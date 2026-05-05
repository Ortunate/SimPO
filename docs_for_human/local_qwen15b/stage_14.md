# Stage L14 Report: Offline Evaluation Input Pack and Swap Validation

## 1. Current Stage
Stage L14 - offline evaluation input pack and A/B swap validation

Status: PASS

Date: 2026-05-05

Branch: `local-qwen15b-qlora`

## 2. Stage Goal
Prepare a tiny offline evaluation input pack for later DeepSeek V4 Flash pairwise judging.

This stage defines and validates local formatting only:

- exact JSONL input format
- response pair identifiers
- provenance fields
- local conversion to chat messages
- A/B and B/A swap construction

This stage does not call DeepSeek API, does not read `.env`, does not check secrets, does not load a model, does not train, does not download data, and does not change dependencies or system configuration.

## 3. Execution / Findings
Read first:

- `AGENTS.md`
- `docs_for_agent/local_qwen15b/local_qwen15b_line.md`
- `docs_for_agent/local_qwen15b/hardware_resource_policy.md`
- `docs_for_agent/local_qwen15b/api_eval_policy.md`
- `docs_for_agent/local_qwen15b/mirror_download_policy.md`
- `docs_for_human/local_qwen15b/stage_13.md`
- Stage L13 artifacts under `stage_artifacts/local_qwen15b/stage13/`

Key commands run:

```bash
sed -n '1,240p' AGENTS.md
sed -n '1,220p' docs_for_agent/local_qwen15b/local_qwen15b_line.md
sed -n '1,180p' docs_for_agent/local_qwen15b/hardware_resource_policy.md
sed -n '1,220p' docs_for_agent/local_qwen15b/api_eval_policy.md
sed -n '1,260p' docs_for_agent/local_qwen15b/mirror_download_policy.md
sed -n '1,380p' docs_for_human/local_qwen15b/stage_13.md
find stage_artifacts/local_qwen15b/stage13 -maxdepth 2 -type f | sort
git status --short
.venv/bin/python stage_artifacts/local_qwen15b/stage14/build_offline_judge_requests.py --input stage_artifacts/local_qwen15b/stage14/tiny_offline_eval_pairs.jsonl --output stage_artifacts/local_qwen15b/stage14/tiny_offline_judge_requests.jsonl
.venv/bin/python -m json.tool stage_artifacts/local_qwen15b/stage14/tiny_offline_eval_pairs.jsonl
.venv/bin/python stage_artifacts/local_qwen15b/stage14/validate_offline_judge_requests.py --input stage_artifacts/local_qwen15b/stage14/tiny_offline_judge_requests.jsonl
.venv/bin/python -c "<line-by-line JSONL parse for tiny_offline_eval_pairs.jsonl>"
.venv/bin/python -c "<line-by-line JSONL parse for tiny_offline_judge_requests.jsonl>"
sed -n '1,220p' stage_artifacts/local_qwen15b/stage14/eval_input_format.md
sed -n '1,4p' stage_artifacts/local_qwen15b/stage14/tiny_offline_judge_requests.jsonl
```

Note: `python -m json.tool` returned `Extra data` on the JSONL input because JSONL is multiple JSON documents, not one JSON document. This was not a data failure. The subsequent line-by-line JSONL checks passed.

Artifacts created:

- `stage_artifacts/local_qwen15b/stage14/eval_input_format.md`
- `stage_artifacts/local_qwen15b/stage14/tiny_offline_eval_pairs.jsonl`
- `stage_artifacts/local_qwen15b/stage14/build_offline_judge_requests.py`
- `stage_artifacts/local_qwen15b/stage14/validate_offline_judge_requests.py`
- `stage_artifacts/local_qwen15b/stage14/tiny_offline_judge_requests.jsonl`
- `stage_artifacts/local_qwen15b/stage14/offline_eval_pack_summary.md`

Formatter result:

```text
input_pairs=2
judge_requests=4
output=stage_artifacts/local_qwen15b/stage14/tiny_offline_judge_requests.jsonl
api_calls=0
```

Validator result:

```text
judge_requests=4
pairs=2
failures=0
```

JSONL parse checks:

```text
tiny_offline_eval_pairs.jsonl: jsonl_lines=2, failures=0
tiny_offline_judge_requests.jsonl: jsonl_lines=4, failures=0
```

Swap validation:

- Each pair produced `AB` and `BA` records.
- For every pair, `AB.shown_response_a_id == BA.shown_response_b_id`.
- For every pair, `AB.shown_response_b_id == BA.shown_response_a_id`.

## 4. Documentation Reorganization
No directory reorganization was performed in Stage L14.

New Stage L14 artifacts:

- `docs_for_human/local_qwen15b/stage_14.md`
- `stage_artifacts/local_qwen15b/stage14/eval_input_format.md`
- `stage_artifacts/local_qwen15b/stage14/tiny_offline_eval_pairs.jsonl`
- `stage_artifacts/local_qwen15b/stage14/build_offline_judge_requests.py`
- `stage_artifacts/local_qwen15b/stage14/validate_offline_judge_requests.py`
- `stage_artifacts/local_qwen15b/stage14/tiny_offline_judge_requests.jsonl`
- `stage_artifacts/local_qwen15b/stage14/offline_eval_pack_summary.md`

## 5. Reusable Assets
Reusable assets:

- Canonical judge input JSONL format.
- Tiny synthetic input pairs for local formatting validation.
- Formatter that emits OpenAI-compatible chat `messages`.
- A/B and B/A swap construction.
- Validator for request shape and swap consistency.
- Offline request JSONL ready for later approved single-request API testing.

The current pairs are synthetic placeholders only and are not model outputs.

## 6. Required Human Approvals for Future Stages
Still require explicit approval before:

- Any DeepSeek API call, including a single judge-template test.
- Any `.env` or secret presence check before an approved API call.
- Any paid judge request.
- Any batch or AlpacaEval-style evaluation.
- Any GPU training run.
- Loading the real Qwen2.5-1.5B-Instruct model.
- Any run expected to exceed 14GB VRAM.
- Any command expected to exceed 10 minutes.
- Any new model/data download.
- Any dependency install or upgrade.
- Deleting outputs, logs, model/data/cache artifacts.

## 7. Risks
### High
- A later DeepSeek API request will be paid/cost-incurring and must be separately approved.
- The Stage L14 synthetic inputs are not real model generations and must not be interpreted as evaluation outcomes.

### Medium
- Real static/dynamic answer generation is not yet prepared in this stage.
- Pairwise judges can be position-biased; swap validation prepares mitigation structure, but real judging still needs careful aggregation.
- Actual DeepSeek response formatting may require small adjustments after a separately approved single-request test.

### Low
- `python -m json.tool` is unsuitable for JSONL and returned `Extra data`; line-by-line parsing passed.

## 8. Recommendation
Recommended Stage L15:

Perform a single approved DeepSeek judge-template API request using one synthetic pair and one order only.

Stage L15 should:

- first check required key/config presence without printing values
- call exactly one request if approved
- cap output tokens and cost
- write raw non-secret response metadata and parsed judge JSON under `stage_artifacts/local_qwen15b/stage15/`
- stop before any batch evaluation

If API approval is not desired yet, the safer alternate Stage L15 is preparing static/dynamic answer generation config without running generation.

## 9. Executive Summary
- Stage L14 PASS.
- Offline judge input JSONL format was defined.
- Two synthetic local pairs were created.
- Four offline judge requests were generated with AB and BA swaps.
- Request validation passed with 4 requests, 2 pairs, and 0 failures.
- No DeepSeek API call, `.env` read, secret check, model loading, training, download, dependency change, deletion, or system configuration change was performed.
