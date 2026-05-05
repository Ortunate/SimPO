# Stage L4 Report: Tiny Local Preference Fixture and Qwen QLoRA Planning

## 1. Current Stage
Name: Stage L4 - Tiny local preference fixture and Qwen QLoRA planning

Status: PASS

Date: 2026-05-05

Branch: `local-qwen15b-qlora`

## 2. Stage Goal
Prepare the next local fallback step without crossing approval gates.

Primary goal:

- create a new local-line tiny preference dataset fixture
- create non-executable static/dynamic Qwen2.5-1.5B QLoRA config sketches
- document model/cache/mirror planning requirements
- validate local data/config shape without loading a model or tokenizer

Non-goals:

- no model download
- no dataset download
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
- latest prior report: `docs_for_human/local_qwen15b/stage_3.md`

Repository findings used:

- `alignment/data.py` loads local dataset scripts through `load_dataset(ds, split=...)`.
- `scripts/run_simpo.py` expects preference examples with OpenAI-format `prompt`, `chosen`, and `rejected` message fields.
- Prior local phase had a tiny dataset script under `stage_artifacts/stage1/local_pref_dataset/`; Stage L4 created a new local-line fixture instead of reusing old-path artifacts.

Assumption:

- The safest next step is local fixture/config preparation, not model acquisition or execution.

## 4. Plan
Planned steps:

1. Inspect data loading and prior tiny dataset patterns.
2. Create a new tiny local preference dataset script under `stage_artifacts/local_qwen15b/stage4/`.
3. Create static and dynamic Qwen2.5-1.5B QLoRA config placeholders.
4. Create model/cache/mirror planning notes.
5. Run static local validation only.
6. Write this stage report and stop.

## 5. Execution / Findings
Commands run:

```bash
sed -n '1,240p' AGENTS.md
sed -n '1,220p' docs_for_agent/local_qwen15b/local_qwen15b_line.md
sed -n '1,220p' docs_for_agent/local_qwen15b/hardware_resource_policy.md
sed -n '1,220p' docs_for_agent/local_qwen15b/mirror_download_policy.md
sed -n '1,220p' docs_for_agent/local_qwen15b/api_eval_policy.md
sed -n '1,280p' docs_for_human/local_qwen15b/stage_3.md
sed -n '1,260p' alignment/data.py
sed -n '1,260p' scripts/run_simpo.py
sed -n '1,220p' stage_artifacts/stage1/local_pref_dataset/local_pref_dataset.py
sed -n '1,220p' stage_artifacts/stage1/local-run-simpo-smoke.yaml
sed -n '1,220p' stage_artifacts/stage2/local-run-simpo-dynamic-smoke.yaml
find stage_artifacts/stage1/local_pref_dataset -maxdepth 2 -type f -print
mkdir -p stage_artifacts/local_qwen15b/stage4/tiny_pref_dataset stage_artifacts/local_qwen15b/stage4/configs
.venv/bin/python -c "<tiny dataset validation>"
.venv/bin/python -c "<yaml placeholder validation>"
git check-ignore -v stage_artifacts/local_qwen15b/hf-cache/placeholder
du -sh stage_artifacts/local_qwen15b/stage4
find stage_artifacts/local_qwen15b/stage4 -maxdepth 3 -type f | sort
git status --short --branch
mkdir -p stage_artifacts/local_qwen15b/hf-cache
env HF_HOME=stage_artifacts/local_qwen15b/hf-cache HF_DATASETS_CACHE=stage_artifacts/local_qwen15b/hf-cache/datasets TRANSFORMERS_CACHE=stage_artifacts/local_qwen15b/hf-cache/transformers .venv/bin/python -c "<tiny dataset validation>"
env HF_HOME=stage_artifacts/local_qwen15b/hf-cache HF_DATASETS_CACHE=stage_artifacts/local_qwen15b/hf-cache/datasets TRANSFORMERS_CACHE=stage_artifacts/local_qwen15b/hf-cache/transformers .venv/bin/python -c "<openai format validation>"
git check-ignore -v stage_artifacts/local_qwen15b/hf-cache/datasets/x
du -sh stage_artifacts/local_qwen15b/hf-cache stage_artifacts/local_qwen15b/stage4
```

Files changed:

- `stage_artifacts/local_qwen15b/stage4/tiny_pref_dataset/tiny_pref_dataset.py`
- `stage_artifacts/local_qwen15b/stage4/configs/qwen25_1p5b_static_qlora_tiny.placeholder.yaml`
- `stage_artifacts/local_qwen15b/stage4/configs/qwen25_1p5b_dynamic_qlora_tiny.placeholder.yaml`
- `stage_artifacts/local_qwen15b/stage4/model_download_plan.md`
- `stage_artifacts/local_qwen15b/stage4/README.md`
- `stage_artifacts/local_qwen15b/stage4/validation_summary.md`
- `docs_for_human/local_qwen15b/stage_4.md`

Key findings:

- The new tiny preference dataset has 4 train examples and 2 test examples.
- Each example contains `prompt`, `chosen`, and `rejected`.
- Each field is a non-empty list of OpenAI-format messages with `role` and `content`.
- Static placeholder config has `dynamic_gamma_enabled: false`.
- Dynamic placeholder config has `dynamic_gamma_enabled: true`.
- Both configs set `use_peft: true` and `load_in_4bit: true`.
- Both configs point to the local Stage L4 tiny dataset fixture.
- Both configs are explicitly marked as placeholders and must not be executed before separate approval.
- Recommended cache path `stage_artifacts/local_qwen15b/hf-cache/` is ignored by git.

Unexpected findings:

- Dataset builder initialization tries to write to `/home/ubuntu0/.cache/huggingface` by default, which is not writable here.
- Validation passed after setting command-local `HF_HOME` and `HF_DATASETS_CACHE` under `stage_artifacts/local_qwen15b/hf-cache/`.
- `TRANSFORMERS_CACHE` produced a deprecation warning; future commands should prefer `HF_HOME`.

## 6. Acceptance Check
| Criterion | Status | Evidence |
|---|---:|---|
| Required docs and latest report read | PASS | `sed` reads listed above |
| Data loading path inspected | PASS | `alignment/data.py`, `scripts/run_simpo.py` |
| Tiny local preference fixture created | PASS | `stage_artifacts/local_qwen15b/stage4/tiny_pref_dataset/tiny_pref_dataset.py` |
| Tiny fixture shape validated | PASS | `{'train': 4, 'test': 2}` |
| OpenAI message format validated | PASS | `openai_format validation: pass` |
| Static QLoRA placeholder config created | PASS | static YAML under `stage4/configs/` |
| Dynamic QLoRA placeholder config created | PASS | dynamic YAML under `stage4/configs/` |
| Config YAML parse validated | PASS | static false, dynamic true for `dynamic_gamma_enabled` |
| Cache path gitignore checked | PASS | `.gitignore:176:stage_artifacts/**/hf-cache/` |
| No model/data/API/training/dependency/system change | PASS | no such commands run |
| Stage L4 report written | PASS | `docs_for_human/local_qwen15b/stage_4.md` |

Overall stage result:

- PASS

## 7. Resource Usage
Model loaded: no

Tokenizer loaded: no

Dataset downloaded: no

External network used: no

GPU-heavy action run: no

API call run: no

Dependency install/upgrade: no

WSL/CUDA/driver/global config modified: no

Artifacts size:

- `stage_artifacts/local_qwen15b/stage4`: about 40 KiB
- `stage_artifacts/local_qwen15b/hf-cache`: about 4 KiB after local validation

## 8. Metrics
Loss behavior: not applicable

Gamma behavior: not applicable

Similarity behavior: not applicable

Gradient behavior: not applicable

Dataset fixture:

- train examples: 4
- test examples: 2
- schema: `prompt`, `chosen`, `rejected`

## 9. Risks
### High
- Qwen2.5-1.5B model download/loading and GPU training remain unapproved and unvalidated.

### Medium
- LoRA target modules in placeholder configs remain plausible but unverified until approved Qwen config/model inspection.
- The local tiny fixture is only a pipeline/debug aid and has no research validity.
- Future commands touching Hugging Face/datasets need a writable local cache path.

### Low
- `TRANSFORMERS_CACHE` is deprecated; prefer `HF_HOME` for future cache routing.

## 10. Recommendation
Recommended decision: Hold before model acquisition or execution.

Recommended next stage:

- Stage L5 should be a model acquisition approval package, unless the human wants an even smaller CPU-only parser/unit check first.

Narrowest next useful action:

1. Decide whether Qwen2.5-1.5B will be supplied as a pre-placed local path or downloaded from an approved mirror.
2. If download is needed, prepare a file-size/source/cache/rollback approval request before any download.
3. If a local path is supplied, inspect only config/tokenizer metadata first, then ask before model loading.

Required approvals before execution:

- model source/mirror and target cache path
- any file >= 0.3GB
- Qwen2.5-1.5B model loading
- any GPU training run
- any external dataset download
- any DeepSeek API call

## 11. Recovery / Rollback Plan
No rollback is required for Stage L4.

If this stage needs to be reverted after explicit approval, remove only:

- `stage_artifacts/local_qwen15b/stage4/`

Do not delete `.env`, prior reports, model caches, checkpoints, logs, datasets, or artifacts outside the approved rollback scope.

## 12. Executive Summary
- Stage L4 passed.
- A new local-line tiny preference dataset fixture was created with 4 train and 2 test examples.
- Static and dynamic Qwen2.5-1.5B QLoRA placeholder configs were created but not executed.
- YAML parsing and OpenAI-format message validation passed.
- The recommended Hugging Face cache path is `stage_artifacts/local_qwen15b/hf-cache/`, which is gitignored.
- No model, tokenizer, external dataset, training, API call, dependency install, or system configuration change was performed.
- Next stage should request approval for model source/cache/download planning, or inspect a human-supplied local model path if available.
