# Stage L3 Mirror and Cache Plan

Date: 2026-05-05

## What Changed
For Stage L3 dependency installation, the package source was changed command-locally to:

```text
https://pypi.tuna.tsinghua.edu.cn/simple
```

No shell profile, global pip config, WSL config, driver config, or `.env` secret file was modified.

## Future PyPI Dependency Installs
Use command-scoped mirror settings unless the human explicitly requests persistent configuration:

```bash
.venv/bin/python -m pip install --index-url https://pypi.tuna.tsinghua.edu.cn/simple <package>
```

Prefer exact versions and avoid upgrading torch, CUDA, transformers, TRL, accelerate, or PEFT unless separately approved.

## Future Hugging Face / Model Downloads
No model or dataset was downloaded in Stage L3.

For future Qwen2.5-1.5B download planning, propose one of:

- a domestic Hugging Face mirror endpoint, if available and approved
- ModelScope or another approved alternate source
- an existing local model path, if the human has already placed files locally

Before any single file >= 0.3GB, report:

- expected source
- mirror or alternate source choice
- expected size
- target path
- gitignore coverage
- rollback / cleanup plan

## Cache Path Recommendation
The default Hugging Face cache path produced a warning:

```text
There was a problem when trying to write in your cache folder (/home/ubuntu0/.cache/huggingface/hub).
```

Recommended future cache path:

```text
stage_artifacts/local_qwen15b/hf-cache/
```

This path matches the repository `.gitignore` pattern:

```text
stage_artifacts/**/hf-cache/
```

Do not create or populate model caches without download/model approval.

## Secret Handling
Do not store API keys or secrets in mirror/cache config artifacts.

Do not print `.env` values.
