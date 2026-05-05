# Stage L19 Bounded Eval Summary

- Status: PASS
- Prompts: 50
- Responses: 100
- Generation duration: 1105.933 s
- Peak sampled VRAM: 6402 MiB
- Judge API calls: 100
- Judge model: deepseek-v4-flash
- Judge total tokens: 71276
- Parse failures: 0
- HTTP failures: 0
- AB/BA consistency: 0.76
- Winner counts: {'dynamic': 1, 'inconsistent': 12, 'static': 2, 'tie': 35}
- Dynamic win rate over all consistent pairs: 0.0263
- Dynamic win rate over non-tie consistent pairs: 0.3333

## Response Length
- dynamic_64_16_20step: count=50, avg_chars=767.66, min=2, max=1559, empty=0
- static_64_16_20step: count=50, avg_chars=753.54, min=2, max=1563, empty=0

## Gate Assessment
- generation_complete: True
- parse_failure_rate_ok: True
- http_ok: True
- ab_ba_consistency_ge_80: False
- ab_ba_consistency_ge_75: True
- expand_to_100_recommended: False

## Recommendation
Do not expand to 100 prompts by default. Treat Stage L19 as a bounded fallback evaluation package: pipeline-valid, neutral/tie-heavy result, no dynamic superiority claim.
