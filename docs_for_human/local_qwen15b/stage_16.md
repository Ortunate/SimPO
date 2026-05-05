# Stage L16 Report: Tiny Static/Dynamic Local Generation Smoke

## 1. Current Stage
Stage L16 - tiny local generation smoke for static and dynamic adapters

Status: PASS

Date: 2026-05-05

Branch: `local-qwen15b-qlora`

## 2. Stage Goal
Run the approved tiny local generation smoke:

- use 2 synthetic prompts
- load local Qwen2.5-1.5B-Instruct
- load Stage L10 static adapter
- load Stage L11 dynamic adapter
- generate deterministic responses
- write response JSONL
- prepare offline static/dynamic judge pairs with AB/BA swaps

This stage does not train, does not call DeepSeek API, does not run batch evaluation, does not download files, does not change dependencies, and does not modify system configuration.

## 3. Execution / Findings
Read first:

- `AGENTS.md`
- `docs_for_agent/local_qwen15b/local_qwen15b_line.md`
- `docs_for_agent/local_qwen15b/hardware_resource_policy.md`
- `docs_for_agent/local_qwen15b/api_eval_policy.md`
- `docs_for_agent/local_qwen15b/mirror_download_policy.md`
- `docs_for_human/local_qwen15b/stage_15.md`
- `stage_artifacts/local_qwen15b/stage15/answer_generation_plan.json`

Key commands run:

```bash
sed -n '1,240p' AGENTS.md
sed -n '1,220p' docs_for_agent/local_qwen15b/local_qwen15b_line.md
sed -n '1,180p' docs_for_agent/local_qwen15b/hardware_resource_policy.md
sed -n '1,220p' docs_for_agent/local_qwen15b/api_eval_policy.md
sed -n '1,260p' docs_for_agent/local_qwen15b/mirror_download_policy.md
sed -n '1,420p' docs_for_human/local_qwen15b/stage_15.md
cat stage_artifacts/local_qwen15b/stage15/answer_generation_plan.json
git status --short
.venv/bin/python -m py_compile stage_artifacts/local_qwen15b/stage16/run_tiny_generation_smoke.py
.venv/bin/python -c "<line-by-line JSONL parse for synthetic_generation_prompts.jsonl>"
test -f stage_artifacts/local_qwen15b/models/Qwen2.5-1.5B-Instruct/config.json && test -f stage_artifacts/local_qwen15b/outputs/stage10_static_64_16_20step/adapter_model.safetensors && test -f stage_artifacts/local_qwen15b/outputs/stage11_dynamic_64_16_20step/adapter_model.safetensors
git check-ignore -v stage_artifacts/local_qwen15b/models/Qwen2.5-1.5B-Instruct/model.safetensors stage_artifacts/local_qwen15b/outputs/stage10_static_64_16_20step/adapter_model.safetensors stage_artifacts/local_qwen15b/outputs/stage11_dynamic_64_16_20step/adapter_model.safetensors stage_artifacts/local_qwen15b/stage16/tiny_generation/tiny_generation_responses.jsonl
nvidia-smi --query-gpu=name,memory.total,memory.used --format=csv,noheader,nounits
timeout 10m .venv/bin/python stage_artifacts/local_qwen15b/stage16/run_tiny_generation_smoke.py --model-path stage_artifacts/local_qwen15b/models/Qwen2.5-1.5B-Instruct --prompts stage_artifacts/local_qwen15b/stage16/synthetic_generation_prompts.jsonl --out-dir stage_artifacts/local_qwen15b/stage16/tiny_generation --max-new-tokens 128
cat stage_artifacts/local_qwen15b/stage16/tiny_generation/summary.json
cat stage_artifacts/local_qwen15b/stage16/tiny_generation/gpu_samples.json
sed -n '1,8p' stage_artifacts/local_qwen15b/stage16/tiny_generation/tiny_generation_responses.jsonl
.venv/bin/python -c "<validate generated response JSONL shape>"
du -sh stage_artifacts/local_qwen15b/stage16
nvidia-smi --query-gpu=name,memory.total,memory.used --format=csv,noheader,nounits
.venv/bin/python -m py_compile stage_artifacts/local_qwen15b/stage16/build_generation_eval_pairs.py
.venv/bin/python stage_artifacts/local_qwen15b/stage16/build_generation_eval_pairs.py --responses stage_artifacts/local_qwen15b/stage16/tiny_generation/tiny_generation_responses.jsonl --output stage_artifacts/local_qwen15b/stage16/tiny_generation/generated_eval_pairs.jsonl
.venv/bin/python stage_artifacts/local_qwen15b/stage14/build_offline_judge_requests.py --input stage_artifacts/local_qwen15b/stage16/tiny_generation/generated_eval_pairs.jsonl --output stage_artifacts/local_qwen15b/stage16/tiny_generation/generated_offline_judge_requests.jsonl
.venv/bin/python -c "<validate generated_eval_pairs.jsonl>"
.venv/bin/python stage_artifacts/local_qwen15b/stage14/validate_offline_judge_requests.py --input stage_artifacts/local_qwen15b/stage16/tiny_generation/generated_offline_judge_requests.jsonl
.venv/bin/python -c "<validate generated_offline_judge_requests.jsonl>"
find stage_artifacts/local_qwen15b/stage16 -maxdepth 3 -type f | sort
```

Generation summary:

```json
{
  "api_calls": 0,
  "training_steps": 0,
  "prompt_count": 2,
  "response_count": 4,
  "max_new_tokens": 128,
  "peak_memory_used_mib": 3965
}
```

Variant summary:

| Variant | Adapter | Records | Duration | Memory after load | Peak sampled VRAM |
|---|---|---:|---:|---:|---:|
| static_64_16_20step | Stage L10 static | 2 | 19.671 s | 3850 MiB | 3965 MiB |
| dynamic_64_16_20step | Stage L11 dynamic | 2 | 16.209 s | 3873 MiB | 3965 MiB |

Generated response validation:

```text
rows 4
variants ['dynamic_64_16_20step', 'static_64_16_20step']
prompt_ids ['synthetic-gen-001', 'synthetic-gen-002']
empty_responses 0
```

Offline judge pair preparation:

```text
prompt_groups=2
pairs=2
failures=0
```

Offline judge request preparation:

```text
input_pairs=2
judge_requests=4
api_calls=0
```

Offline judge request validation:

```text
judge_requests=4
pairs=2
failures=0
orders ['AB', 'BA']
```

Warnings observed:

- `do_sample=False` with model `top_k=20` emitted a non-blocking generation warning.
- PEFT/4-bit loading emitted a non-blocking bitsandbytes `save_pretrained` compatibility warning. No 4-bit base model save was requested.

## 4. Documentation Reorganization
No directory reorganization was performed in Stage L16.

New Stage L16 artifacts:

- `docs_for_human/local_qwen15b/stage_16.md`
- `stage_artifacts/local_qwen15b/stage16/synthetic_generation_prompts.jsonl`
- `stage_artifacts/local_qwen15b/stage16/run_tiny_generation_smoke.py`
- `stage_artifacts/local_qwen15b/stage16/build_generation_eval_pairs.py`
- `stage_artifacts/local_qwen15b/stage16/tiny_generation/summary.json`
- `stage_artifacts/local_qwen15b/stage16/tiny_generation/gpu_samples.json`
- `stage_artifacts/local_qwen15b/stage16/tiny_generation/tiny_generation_responses.jsonl`
- `stage_artifacts/local_qwen15b/stage16/tiny_generation/generated_eval_pairs.jsonl`
- `stage_artifacts/local_qwen15b/stage16/tiny_generation/generated_offline_judge_requests.jsonl`
- `stage_artifacts/local_qwen15b/stage16/stage16_summary.md`

Generated Python `__pycache__` files also exist under Stage L16 from syntax compilation and should not be committed.

## 5. Reusable Assets
Reusable assets:

- Tiny synthetic prompt set.
- Static/dynamic deterministic generation script.
- Response JSONL output contract.
- GPU memory samples for tiny generation.
- Static/dynamic response pairing script.
- AB/BA offline judge requests built from actual Stage L16 generated outputs.

## 6. Required Human Approvals for Future Stages
Still require explicit approval before:

- Any DeepSeek API call using Stage L16 generated outputs.
- Any batch or AlpacaEval-style paid evaluation.
- Any additional local generation run.
- Any GPU training run.
- Any run expected to exceed 14GB VRAM.
- Any command expected to exceed 10 minutes.
- Increasing prompt count, `max_new_tokens`, or generation batch size.
- Any new model/data download.
- Any dependency install or upgrade.
- Deleting outputs, logs, model/data/cache artifacts, or generated stage artifacts.

## 7. Risks
### High
- The adapters are tiny smoke adapters, not trained models suitable for quality claims.
- Stage L16 generated outputs must not be interpreted as benchmark evidence or 8B/9B full fine-tuning evidence.

### Medium
- The generated answers are visibly smoke-level and may contain incomplete or imprecise content.
- A later DeepSeek judge run over these outputs would still be paid and would evaluate only synthetic prompts, not a real benchmark.
- The external VRAM sample is not an exact allocator peak, though the observed peak was far below the 14GB caution line.

### Low
- Non-blocking generation and bitsandbytes warnings were observed.
- `__pycache__` files were generated by syntax checks.

## 8. Recommendation
Recommended Stage L17:

Run a tiny approved DeepSeek judge batch over the 2 Stage L16 generated pairs, using both AB and BA requests.

Stage L17 should:

- call exactly 4 DeepSeek requests if approved
- use `stage_artifacts/local_qwen15b/stage16/tiny_generation/generated_offline_judge_requests.jsonl`
- parse all judge JSON outputs
- aggregate AB/BA consistency
- write a clear limitation note that this is synthetic-prompt smoke evaluation only
- stop before any benchmark-scale evaluation

If avoiding API cost, the alternate Stage L17 is an offline aggregation script only with placeholder judge outputs.

## 9. Executive Summary
- Stage L16 PASS.
- Local Qwen2.5-1.5B plus Stage L10 static adapter generated 2 responses.
- Local Qwen2.5-1.5B plus Stage L11 dynamic adapter generated 2 responses.
- Total responses: 4.
- Peak sampled VRAM: 3965 MiB, far below the 14GB caution line.
- Training steps: 0.
- DeepSeek API calls: 0.
- Generated responses were paired into 2 static/dynamic judge pairs and 4 AB/BA offline judge requests with 0 validation failures.
- No download, dependency change, training, DeepSeek API call, deletion, or system configuration change was performed.
