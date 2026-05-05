# Stage L16 Summary: Tiny Static/Dynamic Local Generation Smoke

Date: 2026-05-05

## Scope
Tiny local generation smoke with the existing Stage L10 static adapter and Stage L11 dynamic adapter.

No training, DeepSeek API call, batch evaluation, download, dependency change, deletion, or system configuration change was performed.

## Inputs
- Prompts: `stage_artifacts/local_qwen15b/stage16/synthetic_generation_prompts.jsonl`
- Prompt count: 2
- Base model: `stage_artifacts/local_qwen15b/models/Qwen2.5-1.5B-Instruct`
- Static adapter: `stage_artifacts/local_qwen15b/outputs/stage10_static_64_16_20step`
- Dynamic adapter: `stage_artifacts/local_qwen15b/outputs/stage11_dynamic_64_16_20step`

## Generation Result
- Response path: `stage_artifacts/local_qwen15b/stage16/tiny_generation/tiny_generation_responses.jsonl`
- Response count: 4
- Variants:
  - `static_64_16_20step`: 2 responses
  - `dynamic_64_16_20step`: 2 responses
- Empty responses: 0
- API calls: 0
- Training steps: 0
- Max new tokens: 128

## Resource Result
- Peak sampled VRAM: 3965 MiB
- Static duration: 19.671 s
- Dynamic duration: 16.209 s
- GPU memory after final cleanup: about 1762 MiB

## Offline Judge Preparation
- Generated eval pairs: `stage_artifacts/local_qwen15b/stage16/tiny_generation/generated_eval_pairs.jsonl`
- Pair count: 2
- Generated offline judge requests: `stage_artifacts/local_qwen15b/stage16/tiny_generation/generated_offline_judge_requests.jsonl`
- Judge request count: 4
- Orders: `AB`, `BA`
- Validator failures: 0
- API calls during judge prep: 0

## Warnings
- Generation emitted a non-blocking `top_k` warning because the model generation config contains `top_k=20` while `do_sample=False`.
- Loading PEFT on a 4-bit model emitted a non-blocking bitsandbytes `save_pretrained` compatibility warning. No save of the 4-bit base model was requested by the stage script.

## Boundary
These responses are tiny smoke outputs from very small adapters. They are not benchmark evidence and do not prove static/dynamic quality differences or 8B/9B full fine-tuning behavior.
