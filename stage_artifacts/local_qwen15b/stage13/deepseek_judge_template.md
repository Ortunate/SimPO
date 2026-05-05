# Stage L13 API-Free DeepSeek Judge Template Draft

Date: 2026-05-05

## Scope
This is a local, API-free template draft for later AlpacaEval-style pairwise judging with DeepSeek V4 Flash.

This file does not contain credentials and must not be used to make an API call without explicit approval.

## Intended Later API Settings
- Judge model: `deepseek-v4-flash`
- API style: OpenAI-compatible chat completion
- Secret source: existing local environment/config only
- Secret handling: presence checks only; never print values
- API calls: require explicit approval for each connectivity, template, tiny batch, or full judge stage

## Pairwise Judge System Message
You are an impartial evaluator. Compare two assistant responses to the same user instruction.

Judge only the final answer quality. Do not favor response A or B by position. Consider correctness, completeness, helpfulness, instruction following, clarity, and safety. Ignore style differences that do not affect usefulness.

Return only valid JSON matching the requested schema. Do not include chain-of-thought. Use a brief public rationale.

## Pairwise Judge User Template
```text
User instruction:
{instruction}

Assistant response A:
{response_a}

Assistant response B:
{response_b}

Return JSON with:
- winner: "A", "B", or "tie"
- score_a: integer from 1 to 10
- score_b: integer from 1 to 10
- confidence: number from 0.0 to 1.0
- rationale: one or two concise sentences, no private reasoning
```

## Expected Output
```json
{
  "winner": "A",
  "score_a": 8,
  "score_b": 6,
  "confidence": 0.74,
  "rationale": "Response A is more complete and follows the instruction more directly. Response B is partially correct but omits an important constraint."
}
```

## Validation Rules
- Output must parse as JSON.
- `winner` must be one of `A`, `B`, or `tie`.
- `score_a` and `score_b` must be integers between 1 and 10.
- `confidence` must be a number between 0.0 and 1.0.
- `rationale` must be a non-empty string.
- No extra fields are allowed in strict mode.

## Later Approval Gates
Before any real API request:

- confirm exact API scope
- confirm max request count
- confirm expected cost envelope
- confirm whether thinking/reasoning output should be disabled
- check key/config presence without printing values
- write a separate report for the approved API stage
