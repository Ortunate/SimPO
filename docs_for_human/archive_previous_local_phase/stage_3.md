# Stage 3: Local Stability Validation

Date: 2026-05-04

## 1. Current Stage

Name: Stage 3 - Local Stability Validation

Status: PARTIAL

Previous stage decision:

- Reviewed latest human-facing report: `docs_for_human/stage_2.md`
- Stage 2 original status was `PARTIAL`, but its approved recovery update records `PASS after approved recovery`.
- Decision: Stage 2 is sufficiently recovered to proceed into Stage 3.

## 2. Stage Goal

Primary goal:

Compare the static SimPO path and the dynamic gamma path on local-safe tiny validation, while monitoring loss, gradient norm, gamma distribution, similarity distribution, and lightweight memory indicators.

Non-goals:

- Do not start full training.
- Do not run Llama-3-8B, Gemma-2-9B, or similarly sized model training.
- Do not download large models or datasets.
- Do not run real UltraFeedback beyond tiny/debug scope.
- Do not claim benchmark or cloud readiness from local tiny results.

## 3. Plan

Planned steps:

1. Re-read standing project instructions and latest human-facing report.
2. Decide whether Stage 2 passed, failed, or needs recovery.
3. Add a Stage 3 local artifact script without changing the core training source.
4. Run a CPU-only tiny static/dynamic comparison with synthetic data.
5. Record metrics and artifacts.
6. Write the experiment log.
7. Persist this human-facing Stage 3 report before proceeding further.

Expected evidence:

- Stage 3 script compiles.
- Static and dynamic tiny variants both complete.
- Dynamic variant logs finite gamma and similarity metrics.
- Gamma stays inside configured clamp bounds.
- Loss and gradient norms remain finite.
- Resource use stays local-safe.

## 4. Execution / Findings

Key actions performed:

- Reviewed:
  - `AGENTS.md`
  - `docs_for_agent/project_brief.md`
  - `docs_for_agent/stage_report_template.md`
  - `docs_for_agent/experiment_log_template.md`
  - `docs_for_agent/local_hardware_notes.md`
  - `docs_for_human/stage_2.md`
- Confirmed the latest completed stage is Stage 2 after approved recovery.
- Created Stage 3 artifact script:
  - `stage_artifacts/stage3/local_tiny_stability_compare.py`
- Ran static and dynamic variants in separate Python subprocesses with fixed seed before model construction.
- Created experiment log:
  - `docs_for_agent/experiment_logs/local-tiny-stability-001.md`

Commands run:

    .venv/bin/python --version
    .venv/bin/python -c "import torch, transformers, trl; print('torch', torch.__version__); print('transformers', transformers.__version__); print('trl', trl.__version__); print('cuda_available', torch.cuda.is_available())"
    free -h
    uname -a
    nvidia-smi --query-gpu=name,memory.total,memory.used,driver_version --format=csv,noheader
    .venv/bin/python -m py_compile stage_artifacts/stage3/local_tiny_stability_compare.py
    HF_HOME=stage_artifacts/stage3/hf-cache TRANSFORMERS_CACHE=stage_artifacts/stage3/hf-cache/transformers WANDB_DISABLED=true .venv/bin/python stage_artifacts/stage3/local_tiny_stability_compare.py

Files changed:

- Added `stage_artifacts/stage3/local_tiny_stability_compare.py`
- Added `docs_for_agent/experiment_logs/local-tiny-stability-001.md`
- Added `docs_for_human/stage_3.md`

Core trainer/config source changes:

- No new core training source edits were made in this Stage 3 turn.
- Existing uncommitted Stage 2 edits remain in:
  - `scripts/simpo_config.py`
  - `scripts/simpo_trainer.py`

Hardware / resource findings:

- OS context: WSL2 kernel `5.15.167.4-microsoft-standard-WSL2`
- System memory visible in WSL: 31GiB total, 29GiB available at query time
- Swap visible in WSL: 8.0GiB total
- GPU from `nvidia-smi`: NVIDIA GeForce RTX 4090 Laptop GPU
- Detected VRAM: 16376 MiB total, 3197 MiB used at query time
- Driver: 595.79
- `.venv` Python: 3.10.19
- PyTorch: 2.2.2+cu121
- Transformers: 4.44.2
- TRL: 0.9.6
- `torch.cuda.is_available()` returned `False` in the normal Python execution context, so this run was CPU-only.

Experiment result:

- Experiment ID: `local-tiny-stability-001`
- Scope: CPU tiny synthetic data
- Static variant: PASS
- Dynamic `sim_linear` variant: PASS
- Static train loss: `1.36223038037618`
- Dynamic train loss: `1.0532668928305309`
- Static loss range: `1.2182` to `1.499`
- Dynamic loss range: `0.9331` to `1.1842`
- Static max grad norm: `11.861966133117676`
- Dynamic max grad norm: `10.559185028076172`
- Dynamic gamma min/max: `0.2605389952659607` / `0.2925293445587158`
- Dynamic similarity min/max: `0.659765362739563` / `0.9156879186630249`
- CPU process max RSS:
  - static: `608.9296875` MB
  - dynamic: `608.41796875` MB
  - dynamic minus static: `-0.51171875` MB

Evidence and artifacts:

- `stage_artifacts/stage3/local-tiny-stability-001-static.json`
- `stage_artifacts/stage3/local-tiny-stability-001-dynamic.json`
- `stage_artifacts/stage3/local-tiny-stability-001-summary.json`
- `docs_for_agent/experiment_logs/local-tiny-stability-001.md`

Unexpected findings:

- The normal Python context reports `torch.cuda.is_available() == False` even though `nvidia-smi` can see the RTX 4090 Laptop GPU. This blocks direct GPU VRAM comparison without further CUDA visibility diagnosis.
- Transformers printed non-blocking deprecation warnings for `TRANSFORMERS_CACHE` and tokenizer cleanup defaults.

## 5. Acceptance Check

| Criterion | Status | Evidence |
|---|---:|---|
| Latest human-facing report reviewed | PASS | `docs_for_human/stage_2.md` reviewed; recovery update says Stage 2 PASS after approved recovery |
| Next stage selected correctly | PASS | Advanced to Stage 3 because Stage 2 recovery passed |
| No resource-heavy action without approval | PASS | CPU tiny only; no model/dataset download; no 8B/9B; no full training |
| Static tiny variant completed | PASS | `stage_artifacts/stage3/local-tiny-stability-001-static.json` |
| Dynamic tiny variant completed | PASS | `stage_artifacts/stage3/local-tiny-stability-001-dynamic.json` |
| Dynamic gamma logs present and finite | PASS | `gamma_beta_ratio/*` values present; gamma range `0.2605389952659607` to `0.2925293445587158` |
| Similarity logs present and finite | PASS | similarity range `0.659765362739563` to `0.9156879186630249` |
| Loss and gradient finite | PASS | no NaN/Inf; dynamic max loss `1.1842`, max grad norm `10.559185028076172` |
| Memory signal recorded | PARTIAL | CPU process RSS recorded; GPU VRAM overhead not measured |
| Stage 3 exit criteria fully satisfied | PARTIAL | Tiny CPU dynamic survived; real GPU/8B memory and data behavior remain unvalidated |

Overall stage result:

- PARTIAL

## 6. Risks

### High

- Real 8B/9B model memory overhead remains unknown. CPU tiny RSS is not a substitute for GPU VRAM measurement.
- CUDA visibility from Python is currently unresolved because `torch.cuda.is_available()` returned `False` while `nvidia-smi` sees the GPU.
- Compatibility with PEFT, FSDP, DeepSpeed, Llama-3-8B, Gemma-2-9B, and real UltraFeedback remains unproven.

### Medium

- Dynamic gamma currently uses LM-head input hooks; this is low-intrusion but still needs validation under wrappers or distributed setups.
- Tiny synthetic data is useful for numerical smoke/stability checks but does not represent real preference-pair distributions.
- The dynamic gamma strategy is only `sim_linear`; no curriculum or combined strategy has been validated.

### Low

- Non-blocking Transformers deprecation warnings were printed.
- Generated `__pycache__` exists under `stage_artifacts/stage3/`.

## 7. Recommendation

Recommended decision:

- Hold Stage 4.
- Continue Stage 3 with the narrowest next validation.

Reason:

The dynamic `sim_linear` path survived local CPU tiny validation and produced sane logs, but Stage 3 is not complete enough for cloud readiness. The project still needs memory-oriented validation and stronger entrypoint-level evidence before cloud packaging.

Narrow next action:

1. Keep work local.
2. Diagnose Python CUDA visibility only through local-safe inspection first.
3. If CUDA visibility can be confirmed without environment changes, run a very small GPU memory smoke that is explicitly bounded below 8GB VRAM.
4. If CUDA visibility requires environment repair or configuration changes, ask for human approval before changing anything.
5. Do not proceed to cloud/full training.

## 8. Executive Summary

- Stage 2 recovery was accepted as passed, so Stage 3 was started.
- Stage 3 ran only local-safe CPU tiny validation.
- A Stage 3 artifact script now compares static and dynamic paths in isolated subprocesses.
- Static and dynamic variants both completed 6 steps without NaN/Inf or loss/gradient guard failures.
- Dynamic gamma metrics were logged and stayed within clamp bounds.
- CPU RSS did not show an overhead signal in this tiny setup, but GPU VRAM overhead is still unknown.
- Python currently reports CUDA unavailable even though `nvidia-smi` sees the RTX 4090 Laptop GPU.
- Stage 3 is PARTIAL, not cloud-ready.
- Recommended next step is Stage 3 continuation focused on CUDA visibility and tightly bounded memory validation.

---

## Recovery Update: 2026-05-04 - CUDA Visibility and Tiny GPU Memory Smoke

### Stage Status

PASS after local-safe recovery.

### Key Actions Performed

- Continued under the standing stage protocol.
- Re-read standing instructions:
  - `AGENTS.md`
  - `docs_for_agent/project_brief.md`
  - `docs_for_agent/local_hardware_notes.md`
- Reviewed the latest human-facing report:
  - `docs_for_human/stage_3.md`
- Kept the project in Stage 3 because the previous Stage 3 result was `PARTIAL`.
- Performed local-safe CUDA visibility diagnosis.
- Ran one bounded tiny GPU memory smoke after CLI approval for sandbox-outside execution.
- Added a Stage 3 GPU memory artifact script:
  - `stage_artifacts/stage3/local_tiny_gpu_memory_compare.py`
- Added an experiment log:
  - `docs_for_agent/experiment_logs/local-tiny-gpu-memory-001.md`

### Evidence and Artifacts

Commands run:

    .venv/bin/python -c "import torch; print('torch_version', torch.__version__); print('torch_cuda_build', torch.version.cuda); print('cuda_available', torch.cuda.is_available()); print('device_count', torch.cuda.device_count()); print('cudnn_version', torch.backends.cudnn.version()); print('cuda_home', getattr(torch.utils.cpp_extension, 'CUDA_HOME', None) if hasattr(torch.utils, 'cpp_extension') else 'no_cpp_extension')"
    .venv/bin/python -m torch.utils.collect_env
    which nvidia-smi
    ls -l /dev/dxg
    ls -l /usr/lib/wsl/lib
    nvidia-smi
    find /dev -maxdepth 1 -name dxg -o -name '*nvidia*'
    printenv LD_LIBRARY_PATH
    printenv CUDA_VISIBLE_DEVICES
    printenv NVIDIA_VISIBLE_DEVICES
    .venv/bin/python -c 'import ctypes; lib=ctypes.CDLL("libcuda.so.1"); print("load_libcuda ok"); print("cuInit", lib.cuInit(0))'
    ldd .venv/lib/python3.10/site-packages/torch/lib/libtorch_cuda.so
    .venv/bin/python -c 'import torch, ctypes; print("torch", torch.__version__); print("torch_cuda_build", torch.version.cuda); print("cuda_available", torch.cuda.is_available()); print("device_count", torch.cuda.device_count()); lib=ctypes.CDLL("libcuda.so.1"); print("cuInit", lib.cuInit(0))'
    .venv/bin/python -m py_compile stage_artifacts/stage3/local_tiny_gpu_memory_compare.py
    HF_HOME=stage_artifacts/stage3/hf-cache WANDB_DISABLED=true .venv/bin/python stage_artifacts/stage3/local_tiny_gpu_memory_compare.py

Artifacts:

- `stage_artifacts/stage3/local_tiny_gpu_memory_compare.py`
- `stage_artifacts/stage3/local-tiny-gpu-memory-001-static.json`
- `stage_artifacts/stage3/local-tiny-gpu-memory-001-dynamic.json`
- `stage_artifacts/stage3/local-tiny-gpu-memory-001-summary.json`
- `docs_for_agent/experiment_logs/local-tiny-gpu-memory-001.md`

### Hardware / Resource Usage

- No full training was started.
- No 8B/9B model was loaded or trained.
- No external model or dataset was downloaded.
- No dependency was installed or upgraded.
- No WSL, CUDA, NVIDIA driver, shell profile, global environment, or system setting was changed.
- No cloud or paid resource was used.
- CUDA visibility diagnosis was read-only.
- Tiny GPU memory smoke used:
  - random tiny GPT-2 model
  - local synthetic 3-pair dataset
  - 3 training steps per variant
  - batch size 1
  - checkpoint saving disabled
  - W&B disabled
  - memory guard: fail if max reserved CUDA memory exceeds 1024 MB
- The GPU smoke required CLI approval only because CUDA device access was unavailable inside the execution sandbox.

Hardware findings:

- `nvidia-smi` visible GPU:
  - NVIDIA GeForce RTX 4090 Laptop GPU
  - 16376 MiB VRAM
  - driver 595.79
  - CUDA Version 13.2 reported by driver capability
- Inside the default execution sandbox:
  - `torch.cuda.is_available()` returned `False`
  - `torch.cuda.device_count()` returned `0`
  - `/dev/dxg` was not visible
  - `ctypes.CDLL("libcuda.so.1")` loaded, but `cuInit(0)` returned `100`
- Outside the execution sandbox with CLI approval:
  - `torch.cuda.is_available()` returned `True`
  - `torch.cuda.device_count()` returned `1`
  - `cuInit(0)` returned `0`

Interpretation:

- CUDA is usable on the local machine when the sandbox exposes the GPU.
- The earlier CUDA failure was an execution-sandbox visibility issue, not evidence that the local WSL/GPU stack is globally broken.

### Experiment Result

Experiment ID:

- `local-tiny-gpu-memory-001`

Run status:

- PASS

Static variant:

- global steps: `3`
- train loss: `1.3161539634068806`
- loss values: `[1.4129, 1.2753, 1.2603]`
- max grad norm: `12.718899726867676`
- max reserved CUDA memory: `22.0` MB

Dynamic `sim_linear` variant:

- global steps: `3`
- train loss: `1.0114065806070964`
- loss values: `[1.0948, 0.969, 0.9704]`
- max grad norm: `11.186634063720703`
- gamma mean values: `[0.27681225538253784, 0.27203166484832764, 0.2836344242095947]`
- gamma min/max: `0.27203166484832764` / `0.2836344242095947`
- similarity min/max: `0.7309247255325317` / `0.8237468004226685`
- max reserved CUDA memory: `22.0` MB

Memory delta:

- dynamic minus static max reserved CUDA memory: `0.0` MB

### Acceptance Check

| Criterion | Status | Evidence |
|---|---:|---|
| Stage 3 recovery path selected | PASS | Previous Stage 3 report was `PARTIAL`; continued Stage 3 rather than Stage 4 |
| CUDA visibility diagnosed without environment changes | PASS | sandbox CUDA unavailable; sandbox-outside CUDA available with `device_count=1` |
| Tiny GPU memory smoke bounded below 8GB VRAM | PASS | script guard at 1024 MB; observed max reserved 22.0 MB |
| Static GPU tiny variant completed | PASS | `local-tiny-gpu-memory-001-static.json` |
| Dynamic GPU tiny variant completed | PASS | `local-tiny-gpu-memory-001-dynamic.json` |
| Dynamic gamma and similarity finite | PASS | gamma and similarity ranges logged within bounds |
| Memory overhead signal recorded | PASS | static and dynamic both max reserved 22.0 MB; delta 0.0 MB |
| No resource-heavy action performed without approval | PASS | only tiny GPU smoke; sandbox-outside execution approved through CLI |
| Stage 3 local validation exit criteria | PASS | dynamic `sim_linear` survived CPU and tiny GPU local validation; local memory overhead did not exceed guard |

Overall recovery result:

- PASS

### Current Risks

#### High

- Tiny GPU memory smoke still does not prove 8B/9B memory overhead or full training feasibility.
- PEFT, FSDP, DeepSpeed, real UltraFeedback, and long-run stability remain unvalidated.

#### Medium

- GPU access depends on sandbox/device exposure; GPU tests may require CLI approval when the default sandbox hides `/dev/dxg`.
- LM-head hidden-state hook compatibility under model wrappers remains a specific validation target for later stages.

#### Low

- Non-blocking Transformers tokenizer cleanup deprecation warning was printed.
- Stage artifact scripts and JSON outputs are untracked files.

### Recommendation

Recommended decision:

- Proceed to Stage 4 as a local-only cloud-readiness preparation stage.

Boundaries for Stage 4:

- Do not start cloud usage.
- Do not start full training.
- Do not run 8B/9B training without explicit human approval.
- Do not download large models or datasets without explicit human approval.
- Focus on reproducible configs, final experiment matrix, logging/checkpoint conventions, risk register, and exact approval gates.

### Executive Summary

- Stage 3 was recovered from `PARTIAL` to `PASS` for local validation.
- CPU tiny validation had already passed; this update adds CUDA visibility diagnosis and tiny GPU memory evidence.
- CUDA is available outside the execution sandbox, so the earlier Python CUDA failure was sandbox visibility, not a global machine failure.
- The tiny GPU memory smoke passed for both static and dynamic paths.
- Dynamic `sim_linear` logged sane gamma/similarity values and stayed within clamp bounds.
- Static and dynamic variants both used 22.0 MB max reserved CUDA memory in the tiny smoke, giving 0.0 MB observed delta at this scale.
- This does not validate 8B/9B memory or real dataset behavior.
- Next recommended stage is Stage 4 local-only cloud-readiness preparation, with no cloud/full-training action yet.
