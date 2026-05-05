# Stage L3 Dependency Install Log

Date: 2026-05-05

Branch: `local-qwen15b-qlora`

## Scope
Approved action:

- install missing QLoRA dependency
- use a domestic mirror source
- validate import and CUDA visibility with lightweight commands

Explicit non-actions:

- no model download
- no dataset download
- no Qwen2.5-1.5B model loading
- no training
- no DeepSeek API call
- no torch / CUDA / transformers / TRL / PEFT upgrade
- no WSL / driver / global system configuration change

## Mirror Source Used
PyPI mirror:

```text
https://pypi.tuna.tsinghua.edu.cn/simple
```

This was used as a command-scoped `--index-url`, not as a persistent shell-profile change.

## Installed Packages
Command:

```bash
.venv/bin/python -m pip install --no-cache-dir --no-deps --index-url https://pypi.tuna.tsinghua.edu.cn/simple bitsandbytes==0.41.2.post2
```

Result:

```text
Downloaded bitsandbytes-0.41.2.post2-py3-none-any.whl (92.6 MB)
Successfully installed bitsandbytes-0.41.2.post2
```

Follow-up dependency needed for import:

```bash
.venv/bin/python -m pip install --no-cache-dir --no-deps --index-url https://pypi.tuna.tsinghua.edu.cn/simple scipy==1.13.0
```

Result:

```text
Downloaded scipy-1.13.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (38.6 MB)
Successfully installed scipy-1.13.0
```

Both downloads were below the 0.3GB single-file threshold.

## Final Package Snapshot
```text
torch: 2.2.2
transformers: 4.44.2
datasets: 2.18.0
accelerate: 0.29.2
trl: 0.9.6
peft: 0.7.1
bitsandbytes: 0.41.2.post2
scipy: 1.13.0
deepspeed: not installed
```

`pip check` result:

```text
No broken requirements found.
```

## Validation
Default sandbox:

- `bitsandbytes` imports after `scipy` install.
- Default sandbox still warns that GPU support is unavailable because CUDA is not visible there.

Approved sandbox-external lightweight validation:

```text
torch_cuda_available: True
device: NVIDIA GeForce RTX 4090 Laptop GPU
bitsandbytes import: ok
bitsandbytes version: <unknown>
```

Additional QLoRA module import:

```text
bnb modules: Linear4bit ok, PagedAdamW8bit ok
```

Interpretation:

- Minimal QLoRA dependency readiness is now sufficient for the next approved non-model validation step.
- Default Codex sandbox remains unsuitable for PyTorch GPU visibility.
