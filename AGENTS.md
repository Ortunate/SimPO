# AGENTS.md

## Purpose
This branch is the local Qwen2.5-1.5B-Instruct QLoRA fallback line for the SimPO dynamic-gamma project.

The branch goal is project-completion proof of concept on a constrained local RTX 4090 Laptop WSL node:

- static QLoRA baseline vs dynamic-gamma QLoRA
- peak memory comparison
- basic loss / gamma / similarity logging
- later AlpacaEval-style judge evaluation with DeepSeek V4 Flash, only after separate approval

This branch must not claim to prove Llama-3-8B, Gemma-2-9B, or other 8B/9B full fine-tuning behavior.

Codex is the stage-level execution owner. For each approved stage, Codex should plan, execute, validate, review, persist a human-facing report, and stop at the requested stage boundary.

## Required Reading
Before starting or continuing a local Qwen1.5B fallback stage, read:

- `docs_for_agent/local_qwen15b/local_qwen15b_line.md`
- `docs_for_agent/local_qwen15b/hardware_resource_policy.md`
- `docs_for_agent/local_qwen15b/mirror_download_policy.md`
- `docs_for_agent/local_qwen15b/api_eval_policy.md`

Use these templates when reporting or logging experiments:

- `docs_for_agent/local_qwen15b/stage_report_template.md`
- `docs_for_agent/local_qwen15b/experiment_log_template.md`

Previous local infrastructure phase documents are archived under:

- `docs_for_agent/archive_previous_local_phase/`
- `docs_for_human/archive_previous_local_phase/`

If repository reality conflicts with these docs, trust the repository first, then report the mismatch explicitly.

## Operating Priorities
Apply these priorities in order:

1. Keep the fallback route finishable.
2. Prefer the smallest viable change to the existing SimPO codebase.
3. Validate locally before recommending any larger run.
4. Protect the 16GB VRAM budget and training stability.
5. Avoid broad refactors unless clearly necessary.

## Local Scope
The local machine is for:

- repository audit
- documentation and config preparation
- static analysis
- dummy-data tests
- tiny CPU or very small smoke checks
- approved Qwen2.5-1.5B QLoRA smoke runs
- memory comparison after explicit approval
- logging instrumentation validation

The local machine is not for:

- full fine-tuning
- 8B/9B model training
- large ablation grids
- benchmark chasing
- unnecessary framework migration
- broad codebase redesign

## Technical Constraints
Codex must:

- inspect the current repository before assuming implementation details
- identify the real training entrypoint and loss path before editing
- minimize intrusion into the original training pipeline
- avoid external reward models for dynamic gamma
- preserve zero extra inference-time cost
- reuse existing forward-pass artifacts when practical
- treat VRAM increase and instability as top-tier risks
- keep dynamic gamma reversible through explicit config toggles
- keep new local-line artifacts under `stage_artifacts/local_qwen15b/`
- never commit model weights, datasets, checkpoints, caches, `.env` files, credentials, or API keys

## Human Approval Gate
Human approval is required before any resource-heavy, environment-changing, secret-related, or irreversible action.

Approval is required before:

- any GPU training run
- loading the real Qwen2.5-1.5B-Instruct model
- any dataset download
- any single file download >= 0.3GB
- any command expected to run longer than 10 minutes
- any command expected to use more than 14GB GPU VRAM
- any command expected to use more than 16GB system RAM
- any full fine-tuning attempt
- any 8B/9B model training attempt
- any dependency install or upgrade that changes CUDA, PyTorch, Transformers, TRL, DeepSpeed, Accelerate, or system-level packages
- any WSL, CUDA, NVIDIA driver, shell profile, environment variable, or global Python environment change
- any cloud, server, or paid resource usage
- any benchmark run such as AlpacaEval 2 or Arena-Hard
- any DeepSeek API call beyond separately approved tiny connectivity/template checks
- any deletion of checkpoints, logs, datasets, model caches, or experiment artifacts
- any modification outside this repository

If expected cost is uncertain, stop and ask for approval before running the command.

## Hardware Policy
Treat the local RTX 4090 Laptop as a constrained 16GB VRAM development node, not as a desktop RTX 4090.

The current local VRAM policy is tiered: 12GB sampled VRAM is a normal observation point, 14GB is the caution line, and 15GB or higher is high-risk local work. Runs expected to exceed 14GB require explicit approval and caution in the stage plan/report. Runs near or above 15GB should be treated as high-risk and should have a rollback/stop plan. The 16GB VRAM device budget remains the hard local ceiling.

Default local-safe work:

- repository inspection
- static analysis
- config preparation
- small scripts
- unit tests
- dummy data tests
- CPU-only checks
- very small non-training checks

When discussing WSL memory, CUDA, GPU, or system configuration, also consult:

- `docs_for_agent/local_qwen15b/hardware_resource_policy.md`

Do not apply hardware or system configuration changes without human approval.

## Mirror and Download Policy
For any single file >= 0.3GB:

- use a domestic mirror or approved alternate source when possible
- do not default to the original Hugging Face global endpoint
- report expected source, mirror/source choice, expected size if known, target path, gitignore status, and rollback/cleanup plan before download
- if mirror access fails, stop and ask before using the original source

Do not download models or datasets without explicit human approval.

## API Policy
DeepSeek V4 Flash API evaluation is out of scope for credential setup in this conversation line.

Codex must not:

- configure API keys
- store API keys
- decrypt API keys
- print API keys or secret values
- write keys to files
- modify shell profiles or secret stores
- run full AlpacaEval-style evaluation without explicit approval

Before a future approved API call, Codex may only check whether the required key/config exists and must not print secret values.

## Human-Facing Report Persistence
After every substantive local Qwen1.5B stage-level turn, Codex must write a human-facing report to:

- `docs_for_human/local_qwen15b/stage_<N>.md`

Rules:

- Stage L0 report goes to `docs_for_human/local_qwen15b/stage_0.md`
- Continue sequentially for later local fallback stages
- Do not proceed to the next stage until the current stage report has been written
- If a stage is repeated or recovered, append a dated update section to the same stage file unless instructed otherwise
- Do not delete or overwrite existing human-facing reports without explicit human approval

Each report must include:

- stage status: PASS / FAIL / PARTIAL / BLOCKED
- key actions performed
- evidence and artifacts
- hardware/resource usage
- current risks, labeled High / Medium / Low
- recommendation
- executive summary

## Required Response Format
Every substantive stage-level reply should use:

1. Current Stage
2. Stage Goal
3. Execution / Findings
4. Documentation Reorganization
5. Reusable Assets
6. Required Human Approvals for Future Stages
7. Risks
8. Recommendation
9. Executive Summary

Risk severity must be labeled as High, Medium, or Low.
