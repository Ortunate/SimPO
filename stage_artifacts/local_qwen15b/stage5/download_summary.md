# Stage L5 Download Summary

Date: 2026-05-05

Branch: `local-qwen15b-qlora`

## Scope
Human approved model and data downloads for this step.

No model was loaded. No tokenizer was loaded. No training was run. No GPU-heavy command was run. No DeepSeek API call was made.

## Model
Downloaded model:

```text
Qwen/Qwen2.5-1.5B-Instruct
```

Source:

```text
HF_ENDPOINT=https://hf-mirror.com
```

Target:

```text
stage_artifacts/local_qwen15b/models/Qwen2.5-1.5B-Instruct/
```

Size:

```text
2.9G stage_artifacts/local_qwen15b/models/Qwen2.5-1.5B-Instruct
model.safetensors bytes: 3087467144
```

Non-loading checks:

```text
model_type: qwen2
architectures: ['Qwen2ForCausalLM']
hidden_size: 1536
num_hidden_layers: 28
num_attention_heads: 12
num_key_value_heads: 2
vocab_size: 151936
safetensors_keys: 338
first_key: model.embed_tokens.weight
metadata: {'format': 'pt'}
```

## Data
First attempted source:

```text
HuggingFaceH4/ultrafeedback_binarized
```

Result:

- failed through `hf-mirror.com` with HTTP 520 on dataset paths-info
- original Hugging Face endpoint was not used after mirror failure

Successful alternate data source:

```text
trl-lib/ultrafeedback_binarized
```

Source:

```text
HF_ENDPOINT=https://hf-mirror.com
HF_HUB_DISABLE_XET=1
```

Target:

```text
stage_artifacts/local_qwen15b/data/trl_ultrafeedback_binarized/
```

Downloaded files:

```text
train-00000-of-00001.parquet bytes: 130671922
test-00000-of-00001.parquet bytes: 2144096
```

Downloaded data size:

```text
127M stage_artifacts/local_qwen15b/data
```

Parquet metadata:

```text
train rows: 62135
test rows: 1000
columns: chosen, rejected, score_chosen, score_rejected
```

Tiny local sample derived from downloaded parquet:

```text
stage_artifacts/local_qwen15b/data/trl_ultrafeedback_binarized_tiny/train.jsonl: 16 rows
stage_artifacts/local_qwen15b/data/trl_ultrafeedback_binarized_tiny/test.jsonl: 8 rows
```

Local tiny dataset validation:

```text
{'train': 16, 'test': 8}
columns: {'prompt', 'rejected', 'score_chosen', 'chosen', 'score_rejected'}
roles: user assistant assistant
```

## Gitignore Status
Protected paths:

```text
stage_artifacts/local_qwen15b/models/
stage_artifacts/local_qwen15b/data/
stage_artifacts/**/hf-cache/
```

`git status --ignored` reports these paths as ignored.

## Stage L5 Config Placeholders
Created:

```text
stage_artifacts/local_qwen15b/stage5/qwen25_1p5b_static_qlora_downloaded_tiny.placeholder.yaml
stage_artifacts/local_qwen15b/stage5/qwen25_1p5b_dynamic_qlora_downloaded_tiny.placeholder.yaml
```

Both are non-executable placeholders until model loading and GPU training are separately approved.

## Rollback / Cleanup Plan
If cleanup is approved later, remove only:

```text
stage_artifacts/local_qwen15b/models/Qwen2.5-1.5B-Instruct/
stage_artifacts/local_qwen15b/data/trl_ultrafeedback_binarized/
stage_artifacts/local_qwen15b/data/trl_ultrafeedback_binarized_tiny/
```

Do not remove reports, `.env`, source code, unrelated caches, logs, or checkpoints.
