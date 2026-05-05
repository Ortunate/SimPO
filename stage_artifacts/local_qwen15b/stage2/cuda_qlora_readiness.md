# Stage L2 CUDA / QLoRA Readiness Notes

Date: 2026-05-05

Branch: `local-qwen15b-qlora`

## Scope
This artifact records lightweight readiness diagnostics only.

No model was loaded. No dataset was downloaded. No training was run. No dependency was installed or upgraded. No API call was made.

## CUDA Visibility Result
Default sandbox check:

```text
torch: 2.2.2+cu121
torch_cuda: 12.1
cuda_available: False
device_count: 0
warning: Can't initialize NVML
```

Approved sandbox-external lightweight check:

```text
torch: 2.2.2+cu121
torch_cuda: 12.1
cuda_available: True
device_count: 1
device_0: NVIDIA GeForce RTX 4090 Laptop GPU
```

Interpretation:

- The local CUDA stack is visible to PyTorch outside the default Codex sandbox.
- The Stage L1 CUDA failure is best treated as a Codex sandbox/device-visibility limitation, not as proof that WSL CUDA is broken.
- Future GPU checks, model loading, and training must still require explicit human approval and should run only within the approved command scope.

## Hardware Snapshot
Lightweight `nvidia-smi` check:

```text
NVIDIA GeForce RTX 4090 Laptop GPU, 16376 MiB total VRAM, 14037 MiB free, driver 595.79
```

System RAM:

```text
31 GiB total, about 29 GiB available, 8 GiB swap
```

## QLoRA Dependency Status
Installed in `.venv`:

- torch: 2.2.2
- transformers: 4.44.2
- datasets: 2.18.0
- accelerate: 0.29.2
- trl: 0.9.6
- peft: 0.7.1

Missing:

- bitsandbytes
- deepspeed

For the local single-GPU Qwen2.5-1.5B QLoRA fallback, `bitsandbytes` is the immediate blocker. `deepspeed` is not required for the first local fallback smoke path unless a later approved plan chooses it.

## Narrow Recovery Path
1. Do not start with model or data downloads.
2. Ask for approval to install only the minimal missing QLoRA dependency after presenting the exact package/version plan.
3. After installation approval and completion, run a lightweight import/CUDA check for `bitsandbytes`.
4. Only then request approval for Qwen2.5-1.5B model acquisition/loading.
5. Keep first execution to static QLoRA on tiny/local debug data before dynamic gamma.
