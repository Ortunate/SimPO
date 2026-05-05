# Mirror and Download Policy

## Core Rule
Do not download models or datasets without explicit human approval.

For any single file >= 0.3GB, use a domestic mirror or approved alternate source when possible. Hugging Face model/data downloads must not default to the original global endpoint for large files.

## Pre-Download Report Required
Before any approved large download, report:

- expected source
- mirror or alternate source choice
- expected size if known
- target path
- whether the target path is gitignored
- rollback or cleanup plan
- expected runtime and bandwidth risk if known

## Failure Handling
If mirror access fails:

- stop
- report the failure
- ask before using the original global source or another alternate source

## Git Safety
Never commit:

- model weights
- datasets
- checkpoints
- caches
- generated large evaluation outputs
- `.env` files
- credentials or API keys

Before creating model/data/cache paths, confirm they are outside tracked source files or covered by `.gitignore`.

## Local Artifact Convention
New local-line artifacts should live under:

- `stage_artifacts/local_qwen15b/`

Large or generated artifacts inside that directory still require gitignore review before creation.
