# Hardware and Resource Policy

## Local Node Assumption
Treat this machine as a constrained WSL development node with an RTX 4090 Laptop GPU and a 16GB VRAM working limit.

Do not treat it as equivalent to a desktop RTX 4090.

Current local VRAM policy is tiered:

- 12GB sampled VRAM is a normal observation point, not a high-risk warning by itself.
- 14GB sampled or expected VRAM is the caution line and must be called out in the stage plan/report.
- 15GB sampled or expected VRAM is high-risk local work and should include a rollback/stop plan.
- 16GB VRAM remains the hard local device ceiling.

## Default Local-Safe Work
Allowed without additional approval when expected to stay lightweight:

- repository inspection
- static analysis
- documentation and config preparation
- small scripts
- unit tests
- dummy-data tests
- CPU-only checks
- tiny non-training checks

## Human Approval Required
Ask for explicit approval before:

- any GPU training run
- loading the real Qwen2.5-1.5B-Instruct model
- any command expected to run longer than 10 minutes
- any command expected to use more than 14GB GPU VRAM
- any command expected to use more than 16GB system RAM
- any full fine-tuning run
- any 8B/9B model training run
- any dataset download
- any single file download >= 0.3GB
- any dependency install or upgrade that changes CUDA, PyTorch, Transformers, TRL, DeepSpeed, Accelerate, or system-level packages
- any WSL, CUDA, NVIDIA driver, shell profile, environment variable, or global Python environment change
- any cloud, server, paid resource, or benchmark run
- deletion of checkpoints, logs, datasets, model caches, or experiment artifacts
- modification outside this repository

If expected cost is uncertain, stop and ask before running.

## Local Training Defaults
When an approved local Qwen2.5-1.5B run is prepared:

- use QLoRA by default
- keep sequence length, batch size, and max steps minimal for smoke validation
- measure peak VRAM for static and dynamic variants using the same method
- record exact config, command, seed, output path, and log path
- prefer reversible config-only changes before code changes

## Stability Signals
Record at minimum:

- peak VRAM
- loss trend
- NaN / Inf status
- gamma mean / min / max for dynamic path
- similarity mean / min / max for dynamic path
- runtime and rough throughput when available

## WSL and System Configuration
Do not modify WSL, CUDA, NVIDIA driver, global Python, shell profile, or environment variables automatically.

If WSL memory appears insufficient, Codex may propose a `.wslconfig` change for human review, but must not apply it.
