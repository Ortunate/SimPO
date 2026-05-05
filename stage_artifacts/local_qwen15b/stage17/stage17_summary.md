# Stage L17 Summary: Tiny DeepSeek Judge Batch on Stage L16 Outputs

Date: 2026-05-05

## Scope
Tiny approved DeepSeek V4 Flash judge batch over Stage L16 synthetic-prompt generated outputs.

This stage performed exactly 4 API requests:

- 2 generated static/dynamic pairs
- AB and BA order for each pair

No local model loading, generation, training, download, dependency change, deletion, or system configuration change was performed.

## Request Result
- Request source: `stage_artifacts/local_qwen15b/stage16/tiny_generation/generated_offline_judge_requests.jsonl`
- API calls: 4
- Status: 4/4 HTTP 200
- Parse failures: 0
- Model: `deepseek-v4-flash`
- Max tokens per request: 256

Secret handling:

- `.env` existed.
- DeepSeek key presence was true.
- No key value was printed or written.
- No `.env` value was printed or written.

## Usage
- Prompt tokens: 1754
- Completion tokens: 366
- Total tokens: 2120

## Per-Request Summary
| Request | Order | Status | Winner | Mapped winner | Total tokens |
|---|---:|---:|---:|---:|---:|
| `l16-synthetic-gen-001-ab` | AB | 200 | tie | tie | 515 |
| `l16-synthetic-gen-001-ba` | BA | 200 | tie | tie | 517 |
| `l16-synthetic-gen-002-ab` | AB | 200 | tie | tie | 544 |
| `l16-synthetic-gen-002-ba` | BA | 200 | tie | tie | 544 |

## Aggregation
- Pair count: 2
- Consistent pairs: 2
- Inconsistent pairs: 0
- Winner counts:
  - tie: 2

Pair summaries:

- `l16-synthetic-gen-001`: AB=tie, BA=tie, aggregate=tie
- `l16-synthetic-gen-002`: AB=tie, BA=tie, aggregate=tie

## Boundary
This is a tiny paid judge smoke over synthetic prompts and smoke adapter outputs.

It does not establish benchmark performance, model quality, or 8B/9B full fine-tuning behavior.
