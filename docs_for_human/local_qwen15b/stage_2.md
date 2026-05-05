# Stage L2 Report: CUDA / QLoRA Readiness Recovery Planning

## 1. Current Stage
Name: Stage L2 - CUDA / QLoRA readiness recovery planning

Status: PASS for recovery diagnosis and planning; BLOCKED for execution until approvals/dependencies are resolved

Date: 2026-05-05

Branch: `local-qwen15b-qlora`

## 2. Stage Goal
Choose the narrowest recovery path after Stage L1 and execute only low-risk readiness actions.

Primary goal:

- determine whether the Stage L1 CUDA failure is a local CUDA failure or a Codex sandbox visibility issue
- identify the minimal missing dependency for QLoRA
- prepare non-executable placeholder configs for future static/dynamic QLoRA runs
- stop before dependency installation, model/data download, model loading, training, or API calls

Non-goals:

- no model download
- no dataset download
- no Qwen2.5-1.5B model loading
- no training
- no GPU-heavy command
- no DeepSeek API call
- no dependency installation or upgrade
- no WSL/CUDA/driver/global system configuration change
- no secret or `.env` value printed

## 3. Inputs and Assumptions
Required docs read:

- `AGENTS.md`
- `docs_for_agent/local_qwen15b/local_qwen15b_line.md`
- `docs_for_agent/local_qwen15b/hardware_resource_policy.md`
- `docs_for_agent/local_qwen15b/mirror_download_policy.md`
- `docs_for_agent/local_qwen15b/api_eval_policy.md`
- `docs_for_agent/local_qwen15b/stage_report_template.md`
- `docs_for_agent/local_qwen15b/experiment_log_template.md`
- latest prior report: `docs_for_human/local_qwen15b/stage_1.md`

Key Stage L1 inputs:

- `nvidia-smi` saw RTX 4090 Laptop GPU.
- `.venv` PyTorch reported CUDA unavailable under the default Codex sandbox.
- `bitsandbytes` was not installed.
- No mirror configuration was present.

Assumption:

- The next useful stage is a recovery/readiness planning stage, not model/data download or training.

## 4. Plan
Planned steps:

1. Reconfirm branch and local resource snapshot with lightweight commands.
2. Re-run default sandbox PyTorch CUDA availability check.
3. Run one approved sandbox-external lightweight PyTorch CUDA availability check to isolate sandbox effects.
4. Inspect existing QLoRA-related config and code paths.
5. Write lightweight Stage L2 artifacts under `stage_artifacts/local_qwen15b/stage2/`.
6. Stop after writing this report and final git status check.

Expected evidence:

- CUDA visibility comparison between default sandbox and approved sandbox-external diagnostic.
- QLoRA missing dependency list.
- Placeholder static/dynamic QLoRA config sketches that are explicitly non-executable until approvals.

## 5. Execution / Findings
Commands run:

```bash
sed -n '1,240p' AGENTS.md
find docs_for_agent/local_qwen15b -maxdepth 1 -type f | sort
sed -n '1,220p' docs_for_agent/local_qwen15b/local_qwen15b_line.md
sed -n '1,220p' docs_for_agent/local_qwen15b/hardware_resource_policy.md
sed -n '1,220p' docs_for_agent/local_qwen15b/mirror_download_policy.md
sed -n '1,220p' docs_for_agent/local_qwen15b/api_eval_policy.md
sed -n '1,220p' docs_for_agent/local_qwen15b/stage_report_template.md
sed -n '1,220p' docs_for_agent/local_qwen15b/experiment_log_template.md
find docs_for_human/local_qwen15b -maxdepth 1 -type f -name 'stage_*.md' | sort
sed -n '1,260p' docs_for_human/local_qwen15b/stage_1.md
tail -n 220 docs_for_human/local_qwen15b/stage_1.md
git status --short --branch
git branch --show-current
uname -a
free -h
nvidia-smi --query-gpu=name,memory.total,memory.free,driver_version --format=csv,noheader
.venv/bin/python -c "from importlib import metadata; pkgs=['torch','transformers','datasets','accelerate','trl','peft','bitsandbytes','deepspeed']; ..."
.venv/bin/python -c "import torch; print('torch:', torch.__version__); print('torch_cuda:', torch.version.cuda); print('cuda_available:', torch.cuda.is_available()); print('device_count:', torch.cuda.device_count())"
.venv/bin/python -c "import torch; print('torch:', torch.__version__); print('torch_cuda:', torch.version.cuda); print('cuda_available:', torch.cuda.is_available()); print('device_count:', torch.cuda.device_count()); print('device_0:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else '<none>')"
sed -n '1,220p' training_configs/mistral-7b-instruct-simpo.yaml
sed -n '1,220p' training_configs/gemma-2-9b-it-simpo.yaml
sed -n '130,220p' alignment/configs.py
sed -n '1,125p' alignment/model_utils.py
sed -n '1,140p' scripts/simpo_config.py
find accelerate_configs -maxdepth 1 -type f -print -exec sed -n '1,120p' {} \;
mkdir -p stage_artifacts/local_qwen15b/stage2
```

Note:

- The second PyTorch CUDA command was run as an approved sandbox-external lightweight diagnostic.
- It did not train, load a model, download data, call an API, or allocate a large tensor.

Files inspected:

- `AGENTS.md`
- `docs_for_agent/local_qwen15b/*`
- `docs_for_human/local_qwen15b/stage_1.md`
- `training_configs/mistral-7b-instruct-simpo.yaml`
- `training_configs/gemma-2-9b-it-simpo.yaml`
- `alignment/configs.py`
- `alignment/model_utils.py`
- `scripts/simpo_config.py`
- `accelerate_configs/*`

Files changed:

- `stage_artifacts/local_qwen15b/stage2/cuda_qlora_readiness.md`
- `stage_artifacts/local_qwen15b/stage2/dependency_approval_plan.md`
- `stage_artifacts/local_qwen15b/stage2/qwen25_1p5b_static_qlora.placeholder.yaml`
- `stage_artifacts/local_qwen15b/stage2/qwen25_1p5b_dynamic_qlora.placeholder.yaml`
- `docs_for_human/local_qwen15b/stage_2.md`

Key findings:

- Default Codex sandbox still reports PyTorch CUDA unavailable:

```text
torch: 2.2.2+cu121
torch_cuda: 12.1
cuda_available: False
device_count: 0
warning: Can't initialize NVML
```

- Approved sandbox-external lightweight diagnostic reports CUDA available:

```text
torch: 2.2.2+cu121
torch_cuda: 12.1
cuda_available: True
device_count: 1
device_0: NVIDIA GeForce RTX 4090 Laptop GPU
```

- Therefore, the Stage L1 CUDA failure is best treated as a Codex default sandbox device-visibility limitation, not as proof that WSL CUDA is broken.
- `bitsandbytes` is still not installed and remains the immediate QLoRA blocker.
- `deepspeed` is also not installed, but it is not required for the first single-GPU local Qwen2.5-1.5B QLoRA fallback smoke path unless a later approved plan chooses it.
- Existing repository code already supports `use_peft`, `load_in_4bit`, `BitsAndBytesConfig`, and LoRA config construction.
- Existing training configs are for Mistral/Llama/Gemma and are not suitable as-is for local Qwen2.5-1.5B QLoRA.

Unexpected findings:

- None beyond confirming that sandbox-external CUDA works.

## 6. Acceptance Check
| Criterion | Status | Evidence |
|---|---:|---|
| Required docs and latest report read | PASS | `sed` reads listed above |
| Narrowest recovery stage selected | PASS | Stage L2 CUDA / QLoRA readiness recovery planning |
| Default sandbox CUDA behavior rechecked | PASS | PyTorch CUDA unavailable with NVML warning |
| Sandbox-external CUDA behavior checked with approval | PASS | PyTorch CUDA available, 1 RTX 4090 Laptop GPU |
| QLoRA dependency blocker identified | PASS | `bitsandbytes: not installed` |
| Existing config/code support inspected | PASS | `alignment/configs.py`, `alignment/model_utils.py`, `scripts/simpo_config.py` |
| Non-executable placeholder configs created | PASS | static/dynamic placeholder YAML under `stage_artifacts/local_qwen15b/stage2/` |
| No model/data/API/training/dependency/system change | PASS | no such commands run |
| Stage L2 report written | PASS | `docs_for_human/local_qwen15b/stage_2.md` |

Overall stage result:

- PASS for recovery diagnosis and planning
- BLOCKED for execution until human approval for dependency installation and later model/data actions

## 7. Resource Usage
Model loaded: no

Dataset downloaded: no

GPU-heavy action run: no

API call run: no

Dependency install/upgrade: no

WSL/CUDA/driver/global config modified: no

Peak VRAM:

- no training/model allocation measured
- `nvidia-smi` lightweight snapshot reported 16376 MiB total and 14037 MiB free

System RAM:

- 31 GiB total
- about 29 GiB available at check time
- 8 GiB swap

Runtime:

- all commands were short readiness checks

## 8. Metrics
Loss behavior: not applicable

Gamma behavior: not applicable

Similarity behavior: not applicable

Gradient behavior: not applicable

CUDA readiness:

- default sandbox: FAIL
- approved sandbox-external diagnostic: PASS

QLoRA dependency readiness:

- `bitsandbytes`: missing

## 9. Risks
### High
- `bitsandbytes` is missing; QLoRA cannot run until an approved dependency install succeeds.
- Any future GPU operation must be run under explicit approval because default Codex sandbox cannot expose CUDA to PyTorch.

### Medium
- Placeholder Qwen LoRA target modules are plausible but unverified until approved model/config inspection.
- No mirror/source plan has been approved for Qwen2.5-1.5B model acquisition.
- No tiny local preference dataset path has been selected for the first static smoke run.

### Low
- Existing accelerate configs target multi-GPU/FSDP/DeepSpeed patterns and should not be reused directly for the first local single-GPU QLoRA fallback smoke.

## 10. Recommendation
Recommended decision: Hold execution; proceed next only with explicit approval.

Recommended next stage:

- Stage L3 should be dependency readiness approval and minimal `bitsandbytes` installation/import validation, if the human approves.

Narrowest next approved action:

1. Approve a minimal `bitsandbytes` install into `.venv`.
2. Validate import and CUDA visibility with lightweight commands.
3. Do not download or load Qwen2.5-1.5B yet.

Required approvals before Stage L3 execution:

- dependency installation approval for `bitsandbytes`
- approval for the exact package source/version plan
- approval for any sandbox-external lightweight CUDA validation after install

Approvals still required later:

- model download or model loading
- any dataset download
- any single file >= 0.3GB
- any GPU training run
- any DeepSeek API call

## 11. Recovery / Rollback Plan
No rollback is required for Stage L2 because only reports and lightweight planning artifacts were added.

If the placeholder configs are not wanted, remove only:

- `stage_artifacts/local_qwen15b/stage2/qwen25_1p5b_static_qlora.placeholder.yaml`
- `stage_artifacts/local_qwen15b/stage2/qwen25_1p5b_dynamic_qlora.placeholder.yaml`

Do not delete prior reports, `.env`, caches, logs, datasets, checkpoints, or model files without explicit approval.

## 12. Executive Summary
- Stage L2 completed the narrowest recovery diagnosis after Stage L1.
- Default Codex sandbox cannot expose CUDA to `.venv` PyTorch.
- Approved sandbox-external lightweight diagnostic confirms PyTorch can see the RTX 4090 Laptop GPU.
- The immediate QLoRA blocker is missing `bitsandbytes`.
- Existing code supports PEFT and 4-bit quantization configuration, but existing training configs are not Qwen QLoRA configs.
- Static and dynamic Qwen2.5-1.5B QLoRA placeholder configs were created as non-executable planning artifacts.
- No model, dataset, training, API call, dependency install, or system change was performed.
- Next stage should request explicit approval for minimal `bitsandbytes` installation and import/CUDA validation only.
