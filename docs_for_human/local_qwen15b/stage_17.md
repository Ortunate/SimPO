# Stage L17 Report: Tiny DeepSeek Judge Batch on Stage L16 Outputs

## 1. Current Stage
Stage L17 - tiny approved DeepSeek judge batch over Stage L16 generated outputs

Status: PASS

Date: 2026-05-05

Branch: `local-qwen15b-qlora`

## 2. Stage Goal
Run the approved tiny DeepSeek V4 Flash judge batch over Stage L16 generated static/dynamic outputs:

- use `stage_artifacts/local_qwen15b/stage16/tiny_generation/generated_offline_judge_requests.jsonl`
- execute exactly 4 API requests
- parse all judge JSON outputs
- aggregate AB/BA consistency
- write limitation notes
- stop before any benchmark-scale evaluation

This stage does not load local models, does not generate new answers, does not train, does not download files, does not change dependencies, and does not modify system configuration.

## 3. Execution / Findings
Read first:

- `AGENTS.md`
- `docs_for_agent/local_qwen15b/api_eval_policy.md`
- `docs_for_agent/local_qwen15b/hardware_resource_policy.md`
- `docs_for_agent/local_qwen15b/local_qwen15b_line.md`
- `docs_for_agent/local_qwen15b/mirror_download_policy.md`
- `docs_for_human/local_qwen15b/stage_16.md`
- `stage_artifacts/local_qwen15b/stage16/tiny_generation/generated_offline_judge_requests.jsonl`

Key commands run:

```bash
sed -n '1,240p' AGENTS.md
sed -n '1,220p' docs_for_agent/local_qwen15b/api_eval_policy.md
sed -n '1,180p' docs_for_agent/local_qwen15b/hardware_resource_policy.md
sed -n '1,220p' docs_for_agent/local_qwen15b/local_qwen15b_line.md
sed -n '1,260p' docs_for_agent/local_qwen15b/mirror_download_policy.md
sed -n '1,460p' docs_for_human/local_qwen15b/stage_16.md
sed -n '1,8p' stage_artifacts/local_qwen15b/stage16/tiny_generation/generated_offline_judge_requests.jsonl
git status --short
.venv/bin/python -m py_compile stage_artifacts/local_qwen15b/stage17/run_tiny_deepseek_judge_batch.py
.venv/bin/python -c "<validate Stage L16 generated_offline_judge_requests.jsonl request/pair/order counts>"
git check-ignore -v .env stage_artifacts/local_qwen15b/stage17/tiny_judge_batch/judge_results.jsonl stage_artifacts/local_qwen15b/stage16/tiny_generation/generated_offline_judge_requests.jsonl
.venv/bin/python stage_artifacts/local_qwen15b/stage17/run_tiny_deepseek_judge_batch.py --request-jsonl stage_artifacts/local_qwen15b/stage16/tiny_generation/generated_offline_judge_requests.jsonl --out-dir stage_artifacts/local_qwen15b/stage17/tiny_judge_batch --max-tokens 256 --max-requests 4
cat stage_artifacts/local_qwen15b/stage17/tiny_judge_batch/metadata.json
cat stage_artifacts/local_qwen15b/stage17/tiny_judge_batch/aggregate.json
.venv/bin/python -c "<print per-request status/winner/token summary>"
.venv/bin/python -c "<count parse-error and non-2xx rows>"
find stage_artifacts/local_qwen15b/stage17 -maxdepth 3 -type f | sort
du -sh stage_artifacts/local_qwen15b/stage17
```

Input validation:

```text
requests 4
pairs ['l16-synthetic-gen-001', 'l16-synthetic-gen-002']
orders ['AB', 'BA']
```

Batch execution result:

```text
env_file_exists: yes
deepseek_key_present: yes
api_calls: 4
all_status_2xx: yes
parse_failures: 0
pair_count: 2
consistent_pairs: 2
```

Usage:

```json
{
  "prompt_tokens": 1754,
  "completion_tokens": 366,
  "total_tokens": 2120
}
```

Per-request summary:

| Request | Order | Status | Winner | Mapped winner | Total tokens |
|---|---:|---:|---:|---:|---:|
| `l16-synthetic-gen-001-ab` | AB | 200 | tie | tie | 515 |
| `l16-synthetic-gen-001-ba` | BA | 200 | tie | tie | 517 |
| `l16-synthetic-gen-002-ab` | AB | 200 | tie | tie | 544 |
| `l16-synthetic-gen-002-ba` | BA | 200 | tie | tie | 544 |

Aggregate:

```json
{
  "pair_count": 2,
  "consistent_pairs": 2,
  "inconsistent_pairs": 0,
  "winner_counts": {
    "tie": 2
  }
}
```

Pair summaries:

- `l16-synthetic-gen-001`: AB=tie, BA=tie, aggregate=tie.
- `l16-synthetic-gen-002`: AB=tie, BA=tie, aggregate=tie.

Secret handling:

- `.env` existence was checked.
- DeepSeek key presence was checked.
- No key value was printed.
- No key value was written to artifacts.
- `.env` content was not printed.
- `.env` was not modified.

## 4. Documentation Reorganization
No directory reorganization was performed in Stage L17.

New Stage L17 artifacts:

- `docs_for_human/local_qwen15b/stage_17.md`
- `stage_artifacts/local_qwen15b/stage17/run_tiny_deepseek_judge_batch.py`
- `stage_artifacts/local_qwen15b/stage17/tiny_judge_batch/judge_results.jsonl`
- `stage_artifacts/local_qwen15b/stage17/tiny_judge_batch/metadata.json`
- `stage_artifacts/local_qwen15b/stage17/tiny_judge_batch/aggregate.json`
- `stage_artifacts/local_qwen15b/stage17/stage17_summary.md`

Generated Python `__pycache__` files also exist under Stage L17 from syntax compilation and should not be committed.

## 5. Reusable Assets
Reusable assets:

- Tiny DeepSeek batch judge runner with non-secret logging.
- Parsed 4-request judge result JSONL.
- AB/BA aggregation logic.
- Tiny synthetic-prompt static/dynamic judge summary.
- Token usage metadata for a 4-request judge batch.

## 6. Required Human Approvals for Future Stages
Still require explicit approval before:

- Any additional DeepSeek API call.
- Any larger or benchmark-style paid evaluation.
- Any local model loading or generation run.
- Any GPU training run.
- Any run expected to exceed 14GB VRAM.
- Any command expected to exceed 10 minutes.
- Any new model/data download.
- Any dependency install or upgrade.
- Deleting outputs, logs, model/data/cache artifacts, or generated stage artifacts.

## 7. Risks
### High
- This stage incurred paid API usage, limited to exactly 4 requests and 2120 total tokens.
- The judged responses come from synthetic prompts and tiny smoke adapters; this is not benchmark evidence and not a model-quality claim.

### Medium
- Both pairs aggregated to tie, but this does not imply equivalence beyond these two synthetic prompts.
- The generated answers were smoke-level and partially weak/incomplete, limiting interpretability.
- Future larger evaluation needs a real prompt source, generation controls, cost cap, and aggregation policy.

### Low
- Python `__pycache__` files were generated by syntax checks.

## 8. Recommendation
Recommended Stage L18:

Create a local fallback final evidence report that consolidates:

- L8-L11 training smoke evidence
- L12 comparison table
- L13-L14 judge template/input preparation
- L15 single API connectivity/template result
- L16 local generation smoke
- L17 tiny judge batch
- limitations and non-claims

Do not run more training, generation, or API calls in Stage L18 unless separately requested.

## 9. Executive Summary
- Stage L17 PASS.
- Exactly 4 DeepSeek V4 Flash judge requests were executed over Stage L16 generated outputs.
- All 4 requests returned HTTP 200.
- Parse failures: 0.
- Total token usage: 2120.
- AB/BA aggregation was consistent for 2/2 pairs.
- Both synthetic-prompt pairs aggregated to tie.
- No local model loading, generation, training, download, dependency change, deletion, or system configuration change was performed.
- No API key or `.env` value was printed or written.
