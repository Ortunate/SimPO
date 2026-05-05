# Stage L4 Validation Summary

Date: 2026-05-05

Branch: `local-qwen15b-qlora`

## Scope
Validation was limited to static local data/config checks.

No model was loaded. No tokenizer was loaded. No training was run. No external dataset was downloaded. No API call was made.

## Tiny Preference Dataset
Path:

```text
stage_artifacts/local_qwen15b/stage4/tiny_pref_dataset/
```

Validation result:

```text
tiny_pref_dataset validation: {'train': 4, 'test': 2}
openai_format validation: pass
```

Expected schema:

- `prompt`
- `chosen`
- `rejected`

Each field is a non-empty list of OpenAI-format messages with:

- `role`
- `content`

## Config Placeholders
Paths:

```text
stage_artifacts/local_qwen15b/stage4/configs/qwen25_1p5b_static_qlora_tiny.placeholder.yaml
stage_artifacts/local_qwen15b/stage4/configs/qwen25_1p5b_dynamic_qlora_tiny.placeholder.yaml
```

Validation result:

```text
static config dynamic_gamma_enabled=False
dynamic config dynamic_gamma_enabled=True
```

Both configs:

- parse as YAML
- point to the local tiny preference dataset fixture
- set `use_peft: true`
- set `load_in_4bit: true`
- are explicitly marked as placeholders that must not be executed before approval

## Cache Path
Recommended local cache:

```text
stage_artifacts/local_qwen15b/hf-cache/
```

Gitignore check:

```text
.gitignore:176:stage_artifacts/**/hf-cache/
```

The cache path is ignored by git.

## Important Finding
Default Hugging Face cache under `/home/ubuntu0/.cache/huggingface` is not writable in this environment. Static validation requiring a datasets builder succeeded only after setting command-local cache variables:

```bash
HF_HOME=stage_artifacts/local_qwen15b/hf-cache
HF_DATASETS_CACHE=stage_artifacts/local_qwen15b/hf-cache/datasets
```

Future commands that touch Hugging Face or `datasets` should set a local writable cache path.
