# Stage L4 Model / Cache Planning Notes

Date: 2026-05-05

## Scope
This is a planning artifact only.

No model was downloaded. No dataset was downloaded. No Qwen2.5-1.5B model was loaded. No training was run. No API call was made.

## Candidate Model
Target model:

```text
Qwen/Qwen2.5-1.5B-Instruct
```

This route is for local fallback proof-of-concept only and must not be used to claim 8B/9B full fine-tuning behavior.

## Required Approval Before Download or Loading
Before any model acquisition or loading:

- approve model source or local path
- approve mirror or alternate source
- approve target cache path
- approve expected download size and file list when known
- approve rollback / cleanup plan
- approve real Qwen model loading

## Recommended Cache Path
Use:

```text
stage_artifacts/local_qwen15b/hf-cache/
```

Reason:

- default Hugging Face cache path showed a write warning in Stage L3
- this path is under the local-line artifact root
- `.gitignore` already ignores `stage_artifacts/**/hf-cache/`

## Mirror Preference
For files >= 0.3GB, use a domestic mirror or approved alternate source when possible.

Candidate approaches to confirm before execution:

- approved domestic Hugging Face mirror endpoint
- ModelScope mirror/source, if the exact Qwen2.5-1.5B-Instruct artifact is available
- pre-placed local model directory supplied by the human

If mirror access fails, stop and ask before using the original global source.

## Cleanup Plan
For any future approved model download, cleanup should remove only the approved cache directory or target model path.

Do not delete:

- `.env`
- reports
- source code
- checkpoints or logs not created by the approved stage
- datasets or model files outside the approved target
