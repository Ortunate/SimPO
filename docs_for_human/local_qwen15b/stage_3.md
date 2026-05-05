# Stage L3 Report: Minimal QLoRA Dependency Installation and Validation

## 1. Current Stage
Name: Stage L3 - Minimal QLoRA dependency installation and validation

Status: PASS

Date: 2026-05-05

Branch: `local-qwen15b-qlora`

## 2. Stage Goal
Install the minimal missing QLoRA dependency under the approved local Qwen2.5-1.5B fallback-line protocol, using a domestic mirror source, then validate import and CUDA readiness with lightweight checks.

Non-goals:

- no model download
- no dataset download
- no Qwen2.5-1.5B model loading
- no training
- no GPU-heavy command
- no DeepSeek API call
- no torch / CUDA / transformers / TRL / accelerate / PEFT upgrade
- no WSL / CUDA / NVIDIA driver / global system configuration change
- no secret or `.env` value printed

## 3. Inputs and Assumptions
Required docs read:

- `AGENTS.md`
- `docs_for_agent/local_qwen15b/local_qwen15b_line.md`
- `docs_for_agent/local_qwen15b/hardware_resource_policy.md`
- `docs_for_agent/local_qwen15b/mirror_download_policy.md`
- `docs_for_agent/local_qwen15b/api_eval_policy.md`
- latest prior report: `docs_for_human/local_qwen15b/stage_2.md`

Human approval:

- approved dependency installation
- approved mirror source changes

Stage L2 starting point:

- sandbox-external PyTorch CUDA check passed
- `bitsandbytes` was missing
- QLoRA could not run until `bitsandbytes` was installed

## 4. Plan
Planned steps:

1. Inspect current pip/tool state and installed package versions.
2. Install only `bitsandbytes==0.41.2.post2`, matching `environment.yml`, from a domestic PyPI mirror.
3. If a minimal import dependency is missing, install the repo-pinned version only.
4. Validate package metadata, import behavior, `pip check`, and lightweight CUDA visibility.
5. Persist a dependency install log and mirror/cache plan under `stage_artifacts/local_qwen15b/stage3/`.
6. Stop before model/data download, model loading, training, or API calls.

## 5. Execution / Findings
Commands run:

```bash
sed -n '1,240p' AGENTS.md
sed -n '1,220p' docs_for_agent/local_qwen15b/local_qwen15b_line.md
sed -n '1,220p' docs_for_agent/local_qwen15b/hardware_resource_policy.md
sed -n '1,220p' docs_for_agent/local_qwen15b/mirror_download_policy.md
sed -n '1,220p' docs_for_agent/local_qwen15b/api_eval_policy.md
sed -n '1,280p' docs_for_human/local_qwen15b/stage_2.md
.venv/bin/python -m pip --version
.venv/bin/python -m pip config list
which uv
uv --version
.venv/bin/python -c "from importlib import metadata; ..."
git status --short --branch
.venv/bin/python -m pip install --no-cache-dir --no-deps --index-url https://pypi.tuna.tsinghua.edu.cn/simple bitsandbytes==0.41.2.post2
.venv/bin/python -c "from importlib import metadata; ..."
.venv/bin/python -c "import bitsandbytes as bnb; ..."
.venv/bin/python -c "import torch; ..."
.venv/bin/python -m pip check
nvidia-smi --query-gpu=name,memory.total,memory.free,driver_version --format=csv,noheader
rg -n "scipy==" environment.yml
.venv/bin/python -c "from importlib import metadata ..."
.venv/bin/python -m pip install --no-cache-dir --no-deps --index-url https://pypi.tuna.tsinghua.edu.cn/simple scipy==1.13.0
.venv/bin/python -c "from importlib import metadata; ..."
.venv/bin/python -c "import bitsandbytes as bnb; ..."
.venv/bin/python -m pip check
.venv/bin/python -c "from transformers import BitsAndBytesConfig; ..."
.venv/bin/python -c "import torch; ...; import bitsandbytes as bnb; ..."
.venv/bin/python -c "from bitsandbytes.nn import Linear4bit; from bitsandbytes.optim import PagedAdamW8bit; ..."
```

Sandbox-external commands:

- `pip install bitsandbytes==0.41.2.post2`
- `pip install scipy==1.13.0`
- lightweight CUDA + `bitsandbytes` import validation
- lightweight `Linear4bit` and `PagedAdamW8bit` import validation

Files changed:

- `.venv/` package environment changed by approved dependency installation
- `stage_artifacts/local_qwen15b/stage3/dependency_install_log.md`
- `stage_artifacts/local_qwen15b/stage3/mirror_and_cache_plan.md`
- `docs_for_human/local_qwen15b/stage_3.md`

Key findings:

- Existing pip version: `pip 26.1` in `.venv`.
- Existing `uv` version: `0.10.0`.
- `pip config list` showed no configured mirror source, only a cache ownership warning.
- `bitsandbytes` was not installed at stage start.
- Installed `bitsandbytes==0.41.2.post2` from Tsinghua PyPI mirror.
- Initial `bitsandbytes` import exposed missing `scipy`.
- `environment.yml` pins `scipy==1.13.0`; installed that exact version from Tsinghua PyPI mirror.
- Both downloaded wheels were under the 0.3GB threshold:
  - `bitsandbytes`: 92.6 MB
  - `scipy`: 38.6 MB
- `pip check` reports no broken requirements.
- Default Codex sandbox still cannot expose CUDA to PyTorch; that limitation remains.
- Sandbox-external lightweight check confirms:

```text
torch_cuda_available: True
device: NVIDIA GeForce RTX 4090 Laptop GPU
bitsandbytes import: ok
bitsandbytes version: <unknown>
```

- Additional QLoRA module check passed:

```text
bnb modules: Linear4bit ok, PagedAdamW8bit ok
```

- `BitsAndBytesConfig(load_in_4bit=True, ...)` can be constructed.

Unexpected findings:

- `bitsandbytes==0.41.2.post2` does not expose `__version__`; import still succeeds.
- Default Hugging Face cache path warning appeared during `BitsAndBytesConfig` validation:

```text
There was a problem when trying to write in your cache folder (/home/ubuntu0/.cache/huggingface/hub).
```

No model/data cache was created or populated.

## 6. Acceptance Check
| Criterion | Status | Evidence |
|---|---:|---|
| Required docs and latest report read | PASS | `sed` reads listed above |
| Human-approved dependency install used | PASS | `bitsandbytes==0.41.2.post2` installed |
| Domestic mirror used | PASS | `https://pypi.tuna.tsinghua.edu.cn/simple` |
| No single file >= 0.3GB downloaded | PASS | 92.6 MB and 38.6 MB wheels |
| Core stack preserved | PASS | torch / transformers / datasets / accelerate / trl / peft unchanged |
| `bitsandbytes` import validated | PASS | sandbox-external import ok |
| QLoRA modules import validated | PASS | `Linear4bit`, `PagedAdamW8bit` import ok |
| `pip check` clean | PASS | no broken requirements |
| No model/data/API/training/system change | PASS | no such commands run |
| Stage report written | PASS | `docs_for_human/local_qwen15b/stage_3.md` |

Overall stage result:

- PASS

## 7. Resource Usage
Model loaded: no

Dataset downloaded: no

GPU-heavy action run: no

API call run: no

Dependency install/upgrade: yes

- installed `bitsandbytes==0.41.2.post2`
- installed `scipy==1.13.0`

WSL/CUDA/driver/global config modified: no

Mirror source changed:

- command-local PyPI index URL only
- no persistent shell profile or global pip config change
- `.env` was not modified

Peak VRAM:

- no model/training allocation measured
- lightweight `nvidia-smi` snapshot reported 16376 MiB total and 13921 MiB free

System RAM:

- no high-RAM command run

Runtime:

- dependency installs and checks were short

## 8. Metrics
Loss behavior: not applicable

Gamma behavior: not applicable

Similarity behavior: not applicable

Gradient behavior: not applicable

Dependency readiness:

- `bitsandbytes`: installed and importable
- `scipy`: installed and importable
- `deepspeed`: not installed, not required for first local single-GPU QLoRA smoke

CUDA readiness:

- default Codex sandbox: still not CUDA-ready
- sandbox-external lightweight check: CUDA-ready

## 9. Risks
### High
- Future model loading and GPU training still require explicit approval and should not run under the default Codex sandbox because PyTorch cannot see CUDA there.

### Medium
- `bitsandbytes==0.41.2.post2` imports and exposes QLoRA modules, but real 4-bit model loading remains unvalidated until a separately approved Qwen loading stage.
- Hugging Face default cache path is not writable; future model/data acquisition needs an approved cache path such as `stage_artifacts/local_qwen15b/hf-cache/`.
- Qwen2.5-1.5B model source/mirror and tiny dataset path remain unselected.

### Low
- `bitsandbytes` version is reported through package metadata but not through `bnb.__version__`.

## 10. Recommendation
Recommended decision: Proceed only to a planning or tiny local-data preparation stage next.

Recommended next stage:

- Stage L4 should prepare the model/data acquisition plan and local cache/mirror setup, or create a tiny local preference dataset fixture if no download is desired yet.

Do not proceed directly to Qwen2.5-1.5B loading or training without separate approval.

Required approvals for future execution:

- Qwen2.5-1.5B model source/mirror and any file >= 0.3GB
- target cache path and cleanup plan
- model loading approval
- any GPU training run
- any dataset download
- any DeepSeek API call

## 11. Recovery / Rollback Plan
If rollback is needed, uninstall only the Stage L3 additions from `.venv` after explicit human approval:

```bash
.venv/bin/python -m pip uninstall bitsandbytes scipy
```

Do not delete reports, `.env`, model caches, checkpoints, datasets, or logs without explicit approval.

## 12. Executive Summary
- Stage L3 passed.
- `bitsandbytes==0.41.2.post2` was installed from the Tsinghua PyPI mirror.
- `scipy==1.13.0` was installed because it is required for `bitsandbytes` import and is pinned in `environment.yml`.
- No core ML stack package was upgraded.
- `pip check` reports no broken requirements.
- Sandbox-external lightweight validation confirms CUDA visibility and `bitsandbytes` import success.
- QLoRA modules `Linear4bit` and `PagedAdamW8bit` import successfully.
- No model, dataset, training, API call, or system configuration change was performed.
- Next stage should handle model/data source planning or tiny local fixture preparation, not Qwen execution yet.
