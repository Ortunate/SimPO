# Stage L18 Local Fallback Evidence Summary

Date: 2026-05-05

## Scope
This file consolidates the local Qwen2.5-1.5B-Instruct QLoRA fallback line through Stage L17.

Stage L18 performed documentation consolidation only:

- no training
- no model loading
- no generation
- no DeepSeek API call
- no download
- no dependency change
- no system configuration change
- no deletion
- no secret read or print

## Route Status
The local fallback loop is complete at proof-of-concept scale:

- documentation and policy setup completed
- environment and dependency readiness audited
- model and small preference dataset acquired through approved mirror flow
- static QLoRA smoke path validated
- dynamic-gamma QLoRA smoke path validated
- peak VRAM sampled
- loss, gamma, and similarity logging validated
- tiny local generation completed for static/dynamic adapters
- DeepSeek judge template validated with one request
- tiny AB/BA judge batch completed on synthetic-prompt generated outputs

## Key Training Smoke Evidence
| Stage | Variant | Data scale | Max steps | Peak VRAM sample | Train loss | Eval loss | Eval reward acc | Eval gamma mean | Eval similarity mean |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| L8 | Static QLoRA | 16/8 | 5 | 11620 MiB | 2.4892 | 1.0009 | n/a | n/a | n/a |
| L8 | Dynamic QLoRA | 16/8 | 5 | 11693 MiB | 2.3154 | 0.8786 | n/a | 0.1309 | 0.9049 |
| L9 | Static QLoRA | 16/8 | 20 | 11945 MiB | 1.6594 | 0.9879 | 0.625 | n/a | n/a |
| L9 | Dynamic QLoRA | 16/8 | 20 | 11758 MiB | 1.4992 | 0.8711 | 0.500 | 0.1310 | 0.9045 |
| L10 | Static QLoRA | 64/16 | 20 | 10571 MiB | 1.3097 | 1.0390 | 0.375 | n/a | n/a |
| L11 | Dynamic QLoRA | 64/16 | 20 | 10556 MiB | 1.1609 | 0.9086 | 0.375 | 0.1297 | 0.9255 |

## Generation and Judge Evidence
Stage L16 generation smoke:

- prompts: 2 synthetic prompts
- static responses: 2
- dynamic responses: 2
- total responses: 4
- peak sampled VRAM: 3965 MiB
- training steps: 0
- DeepSeek API calls: 0

Stage L17 judge batch:

- DeepSeek V4 Flash requests: 4
- HTTP 200: 4/4
- parse failures: 0
- total tokens: 2120
- pair count: 2
- AB/BA consistent pairs: 2
- aggregate winners: tie for both pairs

## Policy Updates
Current VRAM tiering:

- 12GB sampled VRAM is a normal observation point.
- 14GB sampled or expected VRAM is the caution line.
- 15GB sampled or expected VRAM is high-risk local work.
- 16GB VRAM remains the hard local device ceiling.

API handling:

- DeepSeek key values were never printed.
- `.env` was not committed.
- API calls were only made in approved tiny stages.
- Full AlpacaEval-style evaluation was not run.

## Non-Claims
This evidence does not prove:

- benchmark performance
- model quality
- production readiness
- full fine-tuning behavior
- Llama-3-8B, Gemma-2-9B, or any 8B/9B behavior
- scalability beyond this local Qwen2.5-1.5B QLoRA fallback route

## Recommended Next Step
Stop execution and review the fallback proof-of-concept package.

If more work is needed, choose a single next path:

1. prepare a final manuscript-facing limitations section, or
2. design a larger but still bounded local generation/evaluation plan with explicit cost and resource approvals.
