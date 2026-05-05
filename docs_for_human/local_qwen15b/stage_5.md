# Stage L5 Report: Approved Model and Data Acquisition

## 1. Current Stage
Name: Stage L5 - Approved model and data acquisition

Status: PASS

Date: 2026-05-05

Branch: `local-qwen15b-qlora`

## 2. Stage Goal
Download the local fallback model and a small UltraFeedback-style preference dataset under the project protocol.

Human approval:

- model download approved
- data download approved
- mirror source changes approved

Non-goals:

- no Qwen2.5-1.5B model loading
- no tokenizer loading
- no training
- no GPU-heavy command
- no DeepSeek API call
- no dependency install or upgrade
- no WSL/CUDA/driver/global system configuration change
- no secret or `.env` value printed

## 3. Inputs and Assumptions
Required docs read:

- `AGENTS.md`
- `docs_for_agent/local_qwen15b/local_qwen15b_line.md`
- `docs_for_agent/local_qwen15b/hardware_resource_policy.md`
- `docs_for_agent/local_qwen15b/mirror_download_policy.md`
- `docs_for_agent/local_qwen15b/api_eval_policy.md`
- latest prior report: `docs_for_human/local_qwen15b/stage_4.md`

External references checked:

- Hugging Face model listing for `Qwen/Qwen2.5-1.5B-Instruct`
- Hugging Face dataset listing for `HuggingFaceH4/ultrafeedback_binarized`
- Hugging Face dataset listing for `trl-lib/ultrafeedback_binarized`

Assumptions:

- The human's approval covers this stage's model/data download actions.
- Loading the downloaded Qwen model remains a separate approval gate.
- GPU training remains a separate approval gate.

## 4. Plan
Planned steps:

1. Confirm target paths and gitignore coverage.
2. Use domestic/alternate mirror endpoint before global Hugging Face.
3. Download `Qwen/Qwen2.5-1.5B-Instruct` to a gitignored local model path.
4. Attempt a tiny UltraFeedback Binarized sample via mirror.
5. If the primary dataset mirror path fails, use an approved smaller UltraFeedback-style alternate source through the mirror.
6. Perform non-loading integrity checks only.
7. Write report and stop.

## 5. Execution / Findings
Commands run:

```bash
sed -n '1,240p' AGENTS.md
sed -n '1,220p' docs_for_agent/local_qwen15b/local_qwen15b_line.md
sed -n '1,220p' docs_for_agent/local_qwen15b/hardware_resource_policy.md
sed -n '1,220p' docs_for_agent/local_qwen15b/mirror_download_policy.md
sed -n '1,220p' docs_for_agent/local_qwen15b/api_eval_policy.md
sed -n '1,280p' docs_for_human/local_qwen15b/stage_4.md
which huggingface-cli
.venv/bin/python -c "from importlib import metadata; ..."
.venv/bin/python -m huggingface_hub.commands.huggingface_cli --help
git check-ignore -v <model/data/cache paths>
df -h stage_artifacts/local_qwen15b /tmp
mkdir -p stage_artifacts/local_qwen15b/models stage_artifacts/local_qwen15b/data stage_artifacts/local_qwen15b/stage5
HF_ENDPOINT=https://hf-mirror.com HF_HOME=stage_artifacts/local_qwen15b/hf-cache HF_HUB_CACHE=stage_artifacts/local_qwen15b/hf-cache/hub .venv/bin/python -m huggingface_hub.commands.huggingface_cli download Qwen/Qwen2.5-1.5B-Instruct --local-dir stage_artifacts/local_qwen15b/models/Qwen2.5-1.5B-Instruct --cache-dir stage_artifacts/local_qwen15b/hf-cache/hub
HF_ENDPOINT=https://hf-mirror.com HF_HOME=stage_artifacts/local_qwen15b/hf-cache HF_DATASETS_CACHE=stage_artifacts/local_qwen15b/hf-cache/datasets .venv/bin/python -c "<stream tiny sample from HuggingFaceH4/ultrafeedback_binarized>"
ps -ef | grep -F "HuggingFaceH4/ultrafeedback_binarized"
HF_ENDPOINT=https://hf-mirror.com HF_HOME=stage_artifacts/local_qwen15b/hf-cache HF_HUB_CACHE=stage_artifacts/local_qwen15b/hf-cache/hub .venv/bin/python -m huggingface_hub.commands.huggingface_cli download trl-lib/ultrafeedback_binarized --repo-type dataset --local-dir stage_artifacts/local_qwen15b/data/trl_ultrafeedback_binarized --cache-dir stage_artifacts/local_qwen15b/hf-cache/hub
HF_HUB_DISABLE_XET=1 HF_ENDPOINT=https://hf-mirror.com HF_HOME=stage_artifacts/local_qwen15b/hf-cache HF_HUB_CACHE=stage_artifacts/local_qwen15b/hf-cache/hub .venv/bin/python -m huggingface_hub.commands.huggingface_cli download trl-lib/ultrafeedback_binarized --repo-type dataset --include 'data/*.parquet' --local-dir stage_artifacts/local_qwen15b/data/trl_ultrafeedback_binarized --cache-dir stage_artifacts/local_qwen15b/hf-cache/hub
.venv/bin/python -c "<model config non-loading check>"
.venv/bin/python -c "<safetensors metadata non-loading check>"
.venv/bin/python -c "<parquet metadata check>"
ls -lh <model/data files>
.venv/bin/python -c "<derive 16 train / 8 test JSONL tiny sample from downloaded parquet>"
env HF_HOME=stage_artifacts/local_qwen15b/hf-cache HF_DATASETS_CACHE=stage_artifacts/local_qwen15b/hf-cache/datasets .venv/bin/python -c "<load local tiny dataset script>"
find <model/data paths> -name '*.incomplete' -o -name '*.lock'
stat -c '%n %s' <key files>
du -sh <model/data/cache paths>
git status --ignored --short <model/data/cache paths>
```

Files changed:

- `.gitignore`
  - added explicit ignores for `stage_artifacts/local_qwen15b/models/`
  - added explicit ignores for `stage_artifacts/local_qwen15b/data/`
- `stage_artifacts/local_qwen15b/stage5/download_plan.md`
- `stage_artifacts/local_qwen15b/stage5/download_summary.md`
- `stage_artifacts/local_qwen15b/stage5/qwen25_1p5b_static_qlora_downloaded_tiny.placeholder.yaml`
- `stage_artifacts/local_qwen15b/stage5/qwen25_1p5b_dynamic_qlora_downloaded_tiny.placeholder.yaml`
- `docs_for_human/local_qwen15b/stage_5.md`

Ignored artifacts created:

- `stage_artifacts/local_qwen15b/models/Qwen2.5-1.5B-Instruct/`
- `stage_artifacts/local_qwen15b/data/trl_ultrafeedback_binarized/`
- `stage_artifacts/local_qwen15b/data/trl_ultrafeedback_binarized_tiny/`

Key findings:

- Model download from `hf-mirror.com` succeeded.
- Model target size is about 2.9G.
- `model.safetensors` size is 3,087,467,144 bytes.
- Non-loading config check reports:

```text
model_type: qwen2
architectures: ['Qwen2ForCausalLM']
hidden_size: 1536
num_hidden_layers: 28
num_attention_heads: 12
num_key_value_heads: 2
vocab_size: 151936
```

- Non-loading safetensors metadata check reports:

```text
safetensors_keys: 338
first_key: model.embed_tokens.weight
metadata: {'format': 'pt'}
```

- Primary dataset attempt `HuggingFaceH4/ultrafeedback_binarized` failed through `hf-mirror.com` with HTTP 520 on dataset paths-info.
- Per mirror policy, the original Hugging Face endpoint was not used after that mirror failure.
- Alternate smaller UltraFeedback-style dataset `trl-lib/ultrafeedback_binarized` succeeded through `hf-mirror.com` after setting `HF_HUB_DISABLE_XET=1`.
- Downloaded dataset files:

```text
train-00000-of-00001.parquet: 130,671,922 bytes
test-00000-of-00001.parquet: 2,144,096 bytes
```

- Parquet metadata:

```text
train rows: 62135
test rows: 1000
columns: chosen, rejected, score_chosen, score_rejected
```

- Derived local tiny sample:

```text
train.jsonl: 16 rows
test.jsonl: 8 rows
```

- Local tiny dataset script validation passed:

```text
{'train': 16, 'test': 8}
columns: {'prompt', 'rejected', 'score_chosen', 'chosen', 'score_rejected'}
roles: user assistant assistant
```

- No `.incomplete` or `.lock` files remained under model/data paths.
- Model, data, and cache paths are gitignored.

Unexpected findings:

- `huggingface-cli` was not on PATH, but the module entrypoint `.venv/bin/python -m huggingface_hub.commands.huggingface_cli` worked.
- `HuggingFaceH4/ultrafeedback_binarized` mirror metadata path returned HTTP 520.
- First `trl-lib/ultrafeedback_binarized` attempt failed because download redirected through Xet/CAS; retry with `HF_HUB_DISABLE_XET=1` succeeded.
- A local dataset script initially failed because `datasets` copies scripts into cache; it was patched to read the repo-local JSONL path explicitly.

## 6. Acceptance Check
| Criterion | Status | Evidence |
|---|---:|---|
| Required docs and latest report read | PASS | `sed` reads listed above |
| Model download approved and performed | PASS | `Qwen/Qwen2.5-1.5B-Instruct` downloaded |
| Domestic/alternate mirror used for model | PASS | `HF_ENDPOINT=https://hf-mirror.com` |
| Model path gitignored | PASS | `stage_artifacts/local_qwen15b/models/` |
| Model non-loading integrity checked | PASS | config and safetensors metadata checks |
| Primary data mirror attempted | PARTIAL | H4 dataset failed with mirror HTTP 520 |
| Alternate data source downloaded | PASS | `trl-lib/ultrafeedback_binarized` downloaded via mirror |
| Xet path avoided after failure | PASS | retry with `HF_HUB_DISABLE_XET=1` |
| Tiny local sample created | PASS | 16 train / 8 test JSONL rows |
| Local sample dataset load validated | PASS | `{'train': 16, 'test': 8}` |
| No model loading / training / API call | PASS | no such commands run |
| Stage report written | PASS | `docs_for_human/local_qwen15b/stage_5.md` |

Overall stage result:

- PASS

## 7. Resource Usage
Model downloaded: yes

Dataset downloaded: yes

Model loaded: no

Tokenizer loaded: no

GPU-heavy action run: no

API call run: no

Dependency install/upgrade: no

WSL/CUDA/driver/global config modified: no

Disk usage:

- model: about 2.9G
- data: about 127M
- cache: about 264K

Network:

- model download from mirror
- dataset download from mirror
- no DeepSeek API call

## 8. Metrics
Loss behavior: not applicable

Gamma behavior: not applicable

Similarity behavior: not applicable

Gradient behavior: not applicable

Model artifact:

- `model.safetensors`: 3,087,467,144 bytes
- safetensors keys: 338

Dataset artifact:

- train parquet rows: 62,135
- test parquet rows: 1,000
- tiny JSONL sample: 16 train / 8 test

## 9. Risks
### High
- Qwen2.5-1.5B has been downloaded but not loaded; actual QLoRA VRAM behavior remains unvalidated.
- Any future model loading or GPU training still requires explicit approval.

### Medium
- The successful dataset source is `trl-lib/ultrafeedback_binarized`, not the initially attempted `HuggingFaceH4/ultrafeedback_binarized`.
- The dataset is for local fallback smoke/debug only and should not be treated as final benchmark/training evidence.
- Local dataset script uses an explicit repo-relative path, which is acceptable for this branch but not portable outside repo-root execution.

### Low
- `huggingface-cli` is not on PATH; use `.venv/bin/python -m huggingface_hub.commands.huggingface_cli`.

## 10. Recommendation
Recommended decision: Hold before execution.

Recommended next stage:

- Stage L6 should be an approved model metadata/tokenizer-only or static QLoRA dry-load planning stage.

Narrowest next useful action:

1. Inspect tokenizer/config metadata from the downloaded local path without full model loading, if approved.
2. Confirm Qwen LoRA target modules against config/module names before training.
3. Then request explicit approval for the first real Qwen2.5-1.5B QLoRA static smoke run.

Required approvals before future execution:

- tokenizer loading, if treated as model-adjacent
- Qwen2.5-1.5B model loading
- any GPU training run
- any DeepSeek API call

## 11. Recovery / Rollback Plan
If cleanup is needed after explicit approval, remove only:

```text
stage_artifacts/local_qwen15b/models/Qwen2.5-1.5B-Instruct/
stage_artifacts/local_qwen15b/data/trl_ultrafeedback_binarized/
stage_artifacts/local_qwen15b/data/trl_ultrafeedback_binarized_tiny/
```

Do not delete:

- `.env`
- reports
- source code
- unrelated caches
- logs
- checkpoints

## 12. Executive Summary
- Stage L5 passed.
- `Qwen/Qwen2.5-1.5B-Instruct` was downloaded through `hf-mirror.com` to a gitignored local artifact path.
- The model was not loaded; only config and safetensors metadata were inspected.
- The primary H4 UltraFeedback Binarized mirror path failed with HTTP 520, so the original global endpoint was not used.
- `trl-lib/ultrafeedback_binarized` was downloaded through `hf-mirror.com` with `HF_HUB_DISABLE_XET=1`.
- A local 16/8 JSONL tiny sample was derived and validated.
- No training, GPU-heavy command, tokenizer/model loading, DeepSeek API call, dependency change, or system configuration change was performed.
- Next stage should stop at metadata/tokenizer inspection or request approval for the first static QLoRA smoke.
