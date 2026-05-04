# AGENTS.md

## Purpose
This repository supports a SimPO research project: adaptive gamma / margin scheduling based on semantic similarity.

Codex is the stage-level execution owner. For each stage, Codex should plan, execute, validate, review, and summarize without waiting for micro-instructions when the next step is clear.

## Required reading
Before starting or continuing a stage, read:

- `docs_for_agent/project_brief.md`

Use these templates when reporting or logging experiments:

- `docs_for_agent/stage_report_template.md`
- `docs_for_agent/experiment_log_template.md`

If repository reality conflicts with these docs, trust the repository first, then report the mismatch explicitly.

## Operating priorities
Apply these priorities in order:

1. Keep the project finishable.
2. Prefer the smallest viable change to the existing SimPO codebase.
3. Validate locally before recommending cloud-scale training.
4. Protect memory budget and training stability.
5. Avoid broad refactors unless clearly necessary.

## Local-vs-cloud boundary
The local machine is for:

- repository audit
- environment setup
- baseline smoke tests
- code instrumentation
- dynamic gamma integration
- small-sample debugging
- stability checks
- memory comparison
- minimal ablation only

The local machine is not for:

- full-scale final training
- large ablation grids
- benchmark chasing
- unnecessary framework migration
- broad codebase redesign

## Technical constraints
Codex must:

- inspect the current repository before assuming implementation details
- identify the real training entrypoints and loss path before editing
- minimize intrusion into the original training pipeline
- avoid external reward models
- preserve zero extra inference-time cost
- reuse existing forward-pass artifacts when practical
- treat VRAM increase and training instability as top-tier risks
- prefer reversible implementation steps

## Stage gate for cloud migration
Do not recommend cloud full training unless all are true:

- baseline training path runs successfully
- dynamic gamma path runs successfully
- at least one dynamic strategy survives small-sample validation
- memory overhead is not clearly beyond the project red line
- configs, logs, and checkpoints are reproducible enough for migration

If the gate is not met, recommend local validation, rollback, or simplification.

## Required reporting format
Every substantive stage-level reply should use:

1. Current Stage
2. Stage Goal
3. Plan
4. Execution / Findings
5. Acceptance Check
6. Risks
7. Recommendation
8. Executive Summary

Risk severity must be labeled as High, Medium, or Low.

## Validation policy
For code changes:

- run the smallest meaningful validation first
- prefer smoke tests before expensive runs
- record commands, configs, logs, and artifacts
- state PASS / FAIL explicitly
- when failing, recommend the narrowest recovery path

## Completion standard
A stage is not complete because code was changed. A stage is complete only when:

- the intended behavior is validated or the failure is diagnosed
- evidence is recorded
- risks are reviewed
- the next action is clear

## Human approval gate

Human approval is required before any resource-heavy, environment-changing, or irreversible action.

Resource-heavy actions include, but are not limited to:

- any command expected to run longer than 10 minutes
- any command expected to use more than 8GB GPU VRAM
- any command expected to use more than 16GB system RAM
- any training run using Llama-3-8B, Gemma-2-9B, or another similarly sized model
- any run using real UltraFeedback data beyond tiny/debug samples
- any download larger than 1GB
- any dependency installation or upgrade that changes CUDA, PyTorch, Transformers, TRL, DeepSpeed, Accelerate, or system-level packages
- any change to WSL, CUDA, NVIDIA driver, shell profile, environment variables, or global Python environment
- any cloud, server, or paid resource usage
- any benchmark run such as AlpacaEval 2 or Arena-Hard
- any deletion of checkpoints, logs, datasets, or experiment artifacts
- any modification outside this repository

If an action may be resource-heavy but the expected cost is uncertain, Codex must stop and ask for approval before running it.

## Local hardware policy

The local machine must be treated as a constrained development node, not a training server.

The detected RTX 4090 Laptop GPU must not be treated as equivalent to a desktop RTX 4090. Codex must verify actual VRAM and system RAM before proposing training commands.

Default local-safe work:
- repository inspection
- static analysis
- config preparation
- small scripts
- unit tests
- dummy data tests
- tiny model tests
- CPU-only or very small GPU smoke checks

Human approval is required before any real 8B/9B model training attempt, even if it is described as a smoke test.

## Human-facing report persistence

After every stage-level turn, Codex must write a human-facing report to:

- `docs_for_human/stage_<N>.md`

where `<N>` is the current stage number.

Rules:
- Stage 0 report goes to `docs_for_human/stage_0.md`
- Stage 1 report goes to `docs_for_human/stage_1.md`
- Continue sequentially for later stages
- Do not proceed to the next stage until the current stage report has been written
- If a stage is repeated or recovered, append a dated update section to the same stage file unless instructed otherwise
- Do not delete or overwrite existing human-facing reports without explicit human approval

Each human-facing report must include:
- stage status: PASS / FAIL / PARTIAL / BLOCKED
- key actions performed
- evidence and artifacts
- hardware/resource usage
- current risks
- recommendation
- executive summary

## Local hardware notes
When discussing WSL memory, CUDA, GPU, or system configuration, also consult:

- `docs_for_agent/local_hardware_notes.md`

Do not apply hardware or system configuration changes without human approval.
