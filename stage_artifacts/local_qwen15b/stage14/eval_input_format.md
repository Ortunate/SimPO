# Stage L14 Offline Judge Input Format

Date: 2026-05-05

## Scope
This format is for API-free preparation of later DeepSeek V4 Flash pairwise judge calls.

Stage L14 files are synthetic/local formatting artifacts only. They are not model outputs and must not be reported as evaluation results.

## Canonical JSONL Input
Each line is one pairwise comparison candidate:

```json
{
  "pair_id": "synthetic-pair-001",
  "source": "synthetic_stage14",
  "instruction": "User instruction text",
  "candidate_a": {
    "id": "synthetic-pair-001-static-placeholder",
    "label": "static_placeholder",
    "text": "Assistant response A"
  },
  "candidate_b": {
    "id": "synthetic-pair-001-dynamic-placeholder",
    "label": "dynamic_placeholder",
    "text": "Assistant response B"
  },
  "provenance": {
    "stage": "L14",
    "note": "Synthetic local example for formatting validation only"
  }
}
```

## Required Fields
- `pair_id`: stable string identifier
- `source`: source family, such as `synthetic_stage14` or later `local_generation_stage_N`
- `instruction`: user instruction shown to both candidates
- `candidate_a.id`: stable response identifier
- `candidate_a.label`: human-readable candidate label
- `candidate_a.text`: candidate response text
- `candidate_b.id`: stable response identifier
- `candidate_b.label`: human-readable candidate label
- `candidate_b.text`: candidate response text
- `provenance`: object with source notes

## Offline Judge Request Output
The formatter emits two records per input pair:

- `order: "AB"` where candidate A is shown as response A
- `order: "BA"` where candidate B is shown as response A

Each output line contains:

- `request_id`
- `pair_id`
- `order`
- `source`
- `candidate_a_id`
- `candidate_b_id`
- `shown_response_a_id`
- `shown_response_b_id`
- `shown_response_a_label`
- `shown_response_b_label`
- `messages`
- `expected_output_schema`

The `messages` field is ready to be used later with an OpenAI-compatible chat completion API, but Stage L14 does not call any API.

## Interpretation Boundary
These inputs validate formatting only. They do not evaluate static or dynamic model quality.
