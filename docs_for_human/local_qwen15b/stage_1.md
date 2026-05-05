# Stage L1 Report: DeepSeek API Configuration Connectivity Check

## 1. Current Stage
Name: Stage L1 - User-requested DeepSeek API configuration and minimal connectivity check

Status: PASS

Date: 2026-05-05

Note: The local-line plan originally places DeepSeek evaluation preparation later. This stage was performed out of the nominal sequence because the user explicitly requested `.env` protection and API calling validation. It was kept to a minimal connectivity check only.

## 2. Stage Goal
Verify that the existing DeepSeek API key configuration can support a minimal API call without exposing or modifying the secret.

Non-goals:

- no API key creation, storage, decryption, printing, or modification
- no shell profile or secret store modification
- no AlpacaEval-style judge run
- no batch evaluation
- no model download
- no dataset download
- no local model loading
- no GPU training
- no dependency installation or upgrade

## 3. Execution / Findings
Commands run:

- read required local Qwen1.5B line policy docs
- inspected `.gitignore`
- checked that `.env` exists without printing values
- checked that `DEEPSEEK_API_KEY` is present and non-empty without printing values
- checked `git ls-files -- .env .env.*`
- performed one minimal DeepSeek API request with default thinking mode
- performed one minimal DeepSeek API request with `thinking: {"type": "disabled"}`

Files inspected:

- `docs_for_agent/local_qwen15b/local_qwen15b_line.md`
- `docs_for_agent/local_qwen15b/hardware_resource_policy.md`
- `docs_for_agent/local_qwen15b/mirror_download_policy.md`
- `docs_for_agent/local_qwen15b/api_eval_policy.md`
- `docs_for_agent/local_qwen15b/stage_report_template.md`
- `.gitignore`
- `docs_for_human/local_qwen15b/stage_0.md`

Files changed:

- `.gitignore`
- `stage_artifacts/local_qwen15b/deepseek_api_connectivity_2026-05-05.md`
- `docs_for_human/local_qwen15b/stage_1.md`

Key findings:

- `.env` already existed and was already ignored.
- `DEEPSEEK_API_KEY` is present and non-empty.
- `.env` / `.env.*` are not tracked by git.
- `.gitignore` now also ignores `.env.*`, while preserving `.env.example` and `.env.template` as trackable templates.
- Official DeepSeek docs list `https://api.deepseek.com` as the OpenAI-compatible base URL and `deepseek-v4-flash` as a current model.
- The first request returned HTTP 200 but empty final content because DeepSeek V4 defaults to thinking mode and `max_tokens=4` was too small.
- The second request returned HTTP 200, model `deepseek-v4-flash`, finish reason `stop`, and content `OK.` with `thinking` disabled.

## 4. Documentation Reorganization
No documentation tree reorganization was performed in this stage.

The stage result was persisted to:

- `docs_for_human/local_qwen15b/stage_1.md`

The detailed connectivity artifact was persisted to:

- `stage_artifacts/local_qwen15b/deepseek_api_connectivity_2026-05-05.md`

## 5. Reusable Assets
Reusable DeepSeek connectivity settings:

- endpoint: `https://api.deepseek.com/chat/completions`
- model: `deepseek-v4-flash`
- minimal deterministic connectivity mode: `thinking: {"type": "disabled"}`, `stream: false`

Reusable secret-handling convention:

- store local key only in `.env`
- do not print or persist secret values
- keep `.env` and `.env.*` ignored
- use `.env.example` or `.env.template` only for non-secret templates

## 6. Required Human Approvals for Future Stages
Approval is still required before:

- any further real DeepSeek API request
- any judge-template connectivity test
- any batch evaluation
- any AlpacaEval-style evaluation
- any paid or cloud resource usage
- any API key setup or credential-management change

## 7. Risks
### High
- Full AlpacaEval-style or judge evaluation remains out of scope and would incur API cost unless separately approved.

### Medium
- DeepSeek V4 defaults to thinking mode; very small `max_tokens` can produce HTTP 200 with empty final content. Future connectivity checks should explicitly disable thinking unless reasoning output is required.

### Low
- `.env.*` is now ignored; if a future non-secret environment template uses that naming pattern, it should be named `.env.example` or `.env.template`.

## 8. Recommendation
Hold at this boundary for API work.

The DeepSeek key, endpoint, and minimal text response path are validated. Future API work should proceed only after explicit approval for the exact scope, especially any judge-template or batch evaluation.

## 9. Executive Summary
- DeepSeek API configuration validation passed.
- `.env` exists and is ignored.
- `DEEPSEEK_API_KEY` exists and is non-empty; the value was never printed or persisted.
- `.gitignore` now protects `.env.*` variants while allowing `.env.example` and `.env.template`.
- `git ls-files -- .env .env.*` showed no tracked secret files.
- A minimal `deepseek-v4-flash` API call returned HTTP 200.
- With thinking disabled, the API returned final text content `OK.`.
- No model, dataset, training, GPU-heavy command, dependency change, or system configuration change was performed.

## 2026-05-05 Update: User-Approved Paid API Call
Status: PASS

User approved a paid single DeepSeek API call with message content:

```text
你是什么模型，现在是什么时间？
```

Request settings:

- endpoint: `https://api.deepseek.com/chat/completions`
- model: `deepseek-v4-flash`
- `thinking`: disabled
- `stream`: false

Result:

- HTTP status: 200
- model returned: `deepseek-v4-flash`
- finish reason: `stop`
- prompt tokens: 12
- completion tokens: 61
- total tokens: 73

Response content:

```text
我是DeepSeek最新版本的模型，由深度求索公司创造。至于当前的具体时间，我无法直接获取实时信息，因为我的知识截止于2025年5月。如果你需要准确的时间，建议查看你的设备时钟或网络时间服务。有什么我可以帮你的吗？😊
```

Resource and safety notes:

- API call run: yes, one user-approved paid request
- API key source: `.env`
- API key printed or persisted: no
- local model loaded: no
- dataset downloaded: no
- GPU-heavy action run: no
- dependency or system configuration changed: no

Risk update:

- Medium: The model response did not provide real current time. For time-sensitive evaluation prompts, provide the current date/time in the prompt or use an external trusted clock source.

## 2026-05-05 Update: Environment and Static Readiness Audit

### 1. Current Stage
Name: Stage L1 - Environment and static readiness audit for local Qwen2.5-1.5B QLoRA fallback

Status: PASS for audit completion; PARTIAL for execution readiness

Branch: `local-qwen15b-qlora`

### 2. Stage Goal
Audit the local repository, environment, API readiness, and mirror/download readiness without changing the environment.

Non-goals respected:

- no model download
- no dataset download
- no Qwen2.5-1.5B model loading
- no training
- no GPU-heavy command
- no DeepSeek API call
- no dependency installation or upgrade
- no WSL/CUDA/driver/global system configuration change
- no secret or `.env` value printed

### 3. Exact Commands Run
Documentation and repository checks:

```bash
sed -n '1,240p' AGENTS.md
sed -n '1,240p' docs_for_agent/local_qwen15b/local_qwen15b_line.md
sed -n '1,220p' docs_for_agent/local_qwen15b/hardware_resource_policy.md
sed -n '1,220p' docs_for_agent/local_qwen15b/mirror_download_policy.md
sed -n '1,220p' docs_for_agent/local_qwen15b/api_eval_policy.md
sed -n '1,260p' docs_for_human/local_qwen15b/stage_0.md
git branch --show-current
git status --short --branch
git check-ignore -v .env
test -f .env
find docs_for_agent docs_for_human stage_artifacts/local_qwen15b -maxdepth 3 -type f | sort
sed -n '1,220p' .gitignore
sed -n '1,260p' docs_for_human/local_qwen15b/stage_1.md
git diff -- .gitignore
git ls-files docs_for_human/local_qwen15b/stage_1.md stage_artifacts/local_qwen15b/deepseek_api_connectivity_2026-05-05.md .env
```

Environment checks:

```bash
uname -a
cat /etc/os-release
cat /proc/version
which python
python --version
python -c "import os,sys; print('executable:', sys.executable); print('prefix:', sys.prefix); print('base_prefix:', sys.base_prefix); print('virtual_env:', os.environ.get('VIRTUAL_ENV', '<unset>'))"
which python3
python3 --version
python3 -c "import os,sys; print('executable:', sys.executable); print('prefix:', sys.prefix); print('base_prefix:', sys.base_prefix); print('virtual_env:', os.environ.get('VIRTUAL_ENV', '<unset>'))"
test -x .venv/bin/python
.venv/bin/python --version
.venv/bin/python -c "import os,sys; print('executable:', sys.executable); print('prefix:', sys.prefix); print('base_prefix:', sys.base_prefix); print('virtual_env:', os.environ.get('VIRTUAL_ENV', '<unset>'))"
nvidia-smi --query-gpu=name,memory.total,memory.free,driver_version --format=csv,noheader
nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader
free -h
df -h .
df -h /tmp
codex --version
.venv/bin/python -c "from importlib import metadata; pkgs=['torch','transformers','datasets','accelerate','trl','peft','bitsandbytes','deepspeed']; [print(f'{p}: {metadata.version(p)}') if True else None for p in pkgs if False]"
.venv/bin/python -c "from importlib import metadata; pkgs=['torch','transformers','datasets','accelerate','trl','peft','bitsandbytes','deepspeed']; ..."
python3 -c "from importlib import metadata; pkgs=['torch','transformers','datasets','accelerate','trl','peft','bitsandbytes','deepspeed']; ..."
.venv/bin/python -c "import importlib.util; mods=['torch','transformers','datasets','accelerate','trl','peft','bitsandbytes','deepspeed']; ..."
.venv/bin/python -c "import torch; print('torch:', torch.__version__); print('torch_cuda:', torch.version.cuda); print('cuda_available:', torch.cuda.is_available()); print('cuda_device_count:', torch.cuda.device_count()); print('device_0:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else '<none>')"
which nvcc
nvcc --version
env | awk -F= '/^(CUDA_VISIBLE_DEVICES|CUDA_HOME|CUDA_PATH|LD_LIBRARY_PATH)=/{print $1": set"}'
ls -l /dev/dxg
ls -l /usr/lib/wsl/lib/libcuda.so.1
ldconfig -p | rg 'libcuda|libnvidia-ml'
which nvidia-smi
ls -l /usr/lib/wsl/lib/nvidia-smi
ls -l /dev | rg 'dxg|nvidia|dri'
ls -l /usr/lib/wsl/lib/libnvidia-ml.so.1
```

API and mirror/download readiness checks:

```bash
env | awk -F= '/^(HF_ENDPOINT|HF_HOME|HF_HUB_CACHE|HUGGINGFACE_HUB_CACHE|HF_DATASETS_CACHE|MODELSCOPE_CACHE|MODELSCOPE_DOMAIN|TRANSFORMERS_CACHE|HF_HUB_ENABLE_HF_TRANSFER)=/{print $1": set"}'
awk -F= '/^[[:space:]]*(HF_ENDPOINT|HF_HOME|HF_HUB_CACHE|HUGGINGFACE_HUB_CACHE|HF_DATASETS_CACHE|MODELSCOPE_CACHE|MODELSCOPE_DOMAIN|TRANSFORMERS_CACHE|HF_HUB_ENABLE_HF_TRANSFER)[[:space:]]*=/{print $1": configured-in-dotenv"}' .env
awk -F= 'BEGIN{found=0} /^[[:space:]]*DEEPSEEK_API_KEY[[:space:]]*=/{if ($0 !~ /^[[:space:]]*DEEPSEEK_API_KEY[[:space:]]*=[[:space:]]*$/) found=1} END{print "DEEPSEEK_API_KEY in .env:", found ? "present" : "missing-or-empty"}' .env
env | awk -F= '/^DEEPSEEK_[A-Z0-9_]*=/{print $1": present-in-process-env"}'
awk -F= '/^[[:space:]]*DEEPSEEK_[A-Z0-9_]*[[:space:]]*=/{name=$1; gsub(/^[[:space:]]+|[[:space:]]+$/, "", name); print name": present-in-dotenv"}' .env
find . -maxdepth 3 -type f \( -name 'requirements*.txt' -o -name 'pyproject.toml' -o -name 'environment*.yml' -o -name 'setup.py' -o -name 'uv.lock' \) | sort
rg -n "bitsandbytes|deepspeed|load_in_4bit|bnb_4bit|qlora|QLoRA|use_peft|lora" . -S
test -d /home/ubuntu0/.cache/huggingface
find /home/ubuntu0/.cache/huggingface -maxdepth 2 -type d | sort
test -d /home/ubuntu0/.cache/modelscope
test -d /home/ubuntu0/.cache/huggingface/hub
sed -n '1,120p' environment.yml
sed -n '130,220p' alignment/configs.py
sed -n '1,120p' alignment/model_utils.py
find training_configs accelerate_configs -maxdepth 2 -type f | sort
```

Report/artifact write and final checks:

```bash
mkdir -p stage_artifacts/local_qwen15b/summaries
```

### 4. Environment Findings
OS / WSL:

- Ubuntu 24.04.2 LTS.
- Kernel: `5.15.167.4-microsoft-standard-WSL2`.
- WSL2 context confirmed by `/proc/version`.

Python:

- `python` command is not available in current shell.
- System `python3`: `/usr/bin/python3`, version `3.12.3`, no project training packages installed.
- Repository `.venv/bin/python`: version `3.10.19`.
- `VIRTUAL_ENV` is unset in the current shell, so the venv is not activated, but `.venv/bin/python` exists and works.

GPU / CUDA:

- `nvidia-smi` path: `/usr/lib/wsl/lib/nvidia-smi`.
- GPU: NVIDIA GeForce RTX 4090 Laptop GPU.
- Reported VRAM: 16376 MiB total, 14219 MiB free at check time.
- Driver: 595.79.
- No active compute processes were reported by `nvidia-smi --query-compute-apps`.
- `nvcc` is not installed or not on PATH.
- `/usr/lib/wsl/lib/libcuda.so.1` and `libnvidia-ml.so.1` exist.
- `/dev/dxg` was not present, and `/dev` did not show `dxg`, `nvidia`, or `dri` device nodes.
- `.venv` PyTorch is `2.2.2+cu121`, but `torch.cuda.is_available()` returned `False` and emitted `UserWarning: Can't initialize NVML`.

System resources:

- System RAM: 31 GiB total, about 30 GiB available at check time.
- Swap: 8.0 GiB total, unused at check time.
- Disk: about 943 GiB available on the repository filesystem and `/tmp`.
- Codex CLI: `codex-cli 0.128.0`; it also printed a warning that it could not update PATH due to read-only filesystem behavior.

Installed package versions in `.venv`:

- `torch`: 2.2.2
- `transformers`: 4.44.2
- `datasets`: 2.18.0
- `accelerate`: 0.29.2
- `trl`: 0.9.6
- `peft`: 0.7.1
- `bitsandbytes`: not installed
- `deepspeed`: not installed

System `python3` package status:

- target training packages are not installed in system Python.

### 5. API Key Presence Check Result
`.env` exists and is ignored by `.gitignore`.

`git check-ignore -v .env` showed:

```text
.gitignore:123:.env .env
```

`DEEPSEEK_API_KEY` is present in `.env`.

No `.env` value or secret value was printed. No DeepSeek API call was made in this audit update.

Human context recorded: paid DeepSeek API connectivity was already tested successfully outside this Codex conversation / in a separate stage update. This audit did not repeat that test.

### 6. Mirror / Download Readiness
No model or dataset download was performed.

No mirror-related environment variable was visible in the current process environment or `.env` from the checked set:

- `HF_ENDPOINT`
- `HF_HOME`
- `HF_HUB_CACHE`
- `HUGGINGFACE_HUB_CACHE`
- `HF_DATASETS_CACHE`
- `MODELSCOPE_CACHE`
- `MODELSCOPE_DOMAIN`
- `TRANSFORMERS_CACHE`
- `HF_HUB_ENABLE_HF_TRANSFER`

No Hugging Face cache directory was present at `/home/ubuntu0/.cache/huggingface`.

No ModelScope cache directory was present at `/home/ubuntu0/.cache/modelscope`.

For future downloads >= 0.3GB, Stage L2 or later must first propose:

- domestic mirror or approved alternate source
- expected size
- target path
- gitignore coverage
- cleanup/rollback plan
- fallback behavior if mirror access fails

### 7. Repository and Documentation Organization
Branch:

- `local-qwen15b-qlora`

Working tree:

- Contains expected uncommitted Stage L0 documentation reorganization.
- `.gitignore` has an existing change that ignores `.env.*` while preserving `.env.example` and `.env.template`.
- `docs_for_human/local_qwen15b/stage_1.md` and `stage_artifacts/local_qwen15b/deepseek_api_connectivity_2026-05-05.md` already existed from the prior API connectivity work.
- `.env` is not tracked by git.

Documentation layout:

- previous local phase docs are archived under `docs_for_agent/archive_previous_local_phase/`
- previous human reports are archived under `docs_for_human/archive_previous_local_phase/`
- new local-line agent docs exist under `docs_for_agent/local_qwen15b/`
- new local-line human reports exist under `docs_for_human/local_qwen15b/`
- new local-line artifact root exists under `stage_artifacts/local_qwen15b/`

### 8. Static / QLoRA Readiness Assessment
Ready:

- core SimPO code path exists
- PEFT config support exists in `alignment/configs.py` and `alignment/model_utils.py`
- 4-bit quantization config path exists through `BitsAndBytesConfig`
- `.venv` has torch / transformers / datasets / accelerate / trl / peft installed
- disk and system RAM are sufficient for planning and small local artifacts
- `.env` is ignored and DeepSeek key presence can be checked without exposing secrets

Missing or blocked:

- `bitsandbytes` is not installed, so true QLoRA cannot run yet.
- `torch.cuda.is_available()` is `False` in the current Codex shell, despite `nvidia-smi` seeing the GPU.
- `/dev/dxg` is absent, which is a likely WSL GPU device exposure issue or a sandbox/session visibility issue.
- no local Qwen2.5-1.5B model cache was confirmed.
- no mirror configuration is present.
- existing training configs target Mistral/Llama/Gemma, not Qwen2.5-1.5B QLoRA.

### 9. Acceptance Check
| Criterion | Status | Evidence |
|---|---:|---|
| Branch confirmed | PASS | `local-qwen15b-qlora` |
| Git status checked | PASS | `git status --short --branch` |
| `.env` exists and is ignored | PASS | `test -f .env`; `git check-ignore -v .env` |
| Previous docs/artifacts organized | PASS | `find docs_for_agent docs_for_human stage_artifacts/local_qwen15b` |
| OS / WSL audited | PASS | Ubuntu 24.04.2, WSL2 kernel |
| Python / venv audited | PASS | system `python3` and `.venv/bin/python` checked |
| GPU / VRAM audited with lightweight commands | PASS | `nvidia-smi` reported RTX 4090 Laptop, 16376 MiB VRAM |
| PyTorch CUDA readiness checked | PARTIAL | `.venv` torch reports CUDA unavailable |
| Package versions audited without install | PASS | metadata query completed |
| API key presence checked without secrets | PASS | `DEEPSEEK_API_KEY in .env: present` |
| No paid API call | PASS | no API command run in this update |
| Mirror/download readiness audited without download | PASS | env/cache checks only |
| Stage L1 report updated | PASS | this appended update |

Overall result:

- Stage L1 audit: PASS
- Environment readiness for Qwen2.5-1.5B QLoRA execution: PARTIAL

### 10. Resource Usage
Model loaded: no

Dataset downloaded: no

GPU-heavy action run: no

API call run: no

Dependency install/upgrade: no

WSL/CUDA/driver/global config modified: no

Expected VRAM used by this stage: none beyond lightweight `nvidia-smi` / PyTorch CUDA availability probing

### 11. Risks
#### High
- PyTorch cannot currently use CUDA in this Codex shell. Any GPU training or Qwen model loading would be blocked until this is understood.
- QLoRA cannot run without `bitsandbytes`.

#### Medium
- Mirror configuration is absent; future large downloads require planning and approval before any model/data acquisition.
- Existing configs do not yet define a Qwen2.5-1.5B QLoRA static baseline.

#### Low
- `python` is not on PATH; commands should use `.venv/bin/python` explicitly or activate the venv in a human-approved workflow.

### 12. Required Human Approvals for Stage L2
Required before execution depending on chosen Stage L2 path:

- approval for any dependency installation, especially `bitsandbytes`
- approval for any GPU diagnostic expected to access GPU beyond lightweight status checks
- approval before loading Qwen2.5-1.5B
- approval before any Qwen model download or dataset download
- approval before any single file download >= 0.3GB, with mirror/source plan
- approval before any GPU training run
- approval before any DeepSeek API request

### 13. Recommendation
Recommended next stage: Stage L2 should be a recovery/readiness stage, not a model/data download stage.

Narrowest next step:

1. Diagnose why `nvidia-smi` sees the GPU but `.venv` PyTorch reports CUDA unavailable.
2. Prepare a proposed dependency plan for `bitsandbytes` compatible with the current torch/CUDA stack, without installing until approved.
3. Draft Qwen2.5-1.5B QLoRA static config placeholders without downloading or loading the model.

Do not proceed to model/data downloads or training until CUDA visibility and QLoRA dependency readiness are resolved.

### 14. Executive Summary
- Stage L1 environment/static readiness audit completed.
- Branch remains `local-qwen15b-qlora`.
- `.env` exists, is ignored, and `DEEPSEEK_API_KEY` presence was confirmed without printing secrets.
- No API call was made in this audit update.
- `nvidia-smi` sees an RTX 4090 Laptop GPU with 16376 MiB VRAM.
- `.venv` PyTorch cannot currently use CUDA and reports `Can't initialize NVML`.
- `.venv` has torch/transformers/datasets/accelerate/trl/peft, but lacks `bitsandbytes` and `deepspeed`.
- Mirror/download configuration is not currently set.
- No model/data/API/GPU-heavy/training/dependency/system change was performed.
- Stage L2 should focus on CUDA/QLoRA readiness recovery and dependency/download planning, not execution.
