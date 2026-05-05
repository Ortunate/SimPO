# Local Qwen2.5-1.5B QLoRA Fallback Line

## Branch Purpose
This branch is dedicated to the local Qwen2.5-1.5B-Instruct QLoRA fallback route for the SimPO dynamic-gamma project.

The route is a finishable local proof-of-concept path. It should demonstrate that the project loop can run end to end at small scale:

- static SimPO QLoRA baseline
- dynamic-gamma SimPO QLoRA variant
- peak memory comparison
- loss, gamma, and similarity logging
- later AlpacaEval-style judge evaluation using DeepSeek V4 Flash after separate approval

This route must not claim to prove full fine-tuning behavior for 8B/9B models.

## Non-Goals
- No full fine-tuning locally.
- No Llama-3-8B or Gemma-2-9B local training.
- No large ablation grid.
- No benchmark claims from tiny local runs.
- No model/data/API download or execution without the approvals listed in policy docs.
- No API key setup, storage, decryption, printing, or modification.

## Repository Conventions
- Root entrypoint: `AGENTS.md`
- Local-line agent docs: `docs_for_agent/local_qwen15b/`
- Local-line human reports: `docs_for_human/local_qwen15b/`
- Local-line artifacts: `stage_artifacts/local_qwen15b/`
- Previous local phase archive: `docs_for_agent/archive_previous_local_phase/` and `docs_for_human/archive_previous_local_phase/`

## Current Reusable Implementation
The existing SimPO code already has a dynamic gamma path:

- `scripts/run_simpo.py` is the training entrypoint.
- `scripts/simpo_config.py` exposes dynamic gamma config fields.
- `scripts/simpo_trainer.py` implements the SimPO loss path and optional dynamic gamma.
- Dynamic gamma is disabled by default through `dynamic_gamma_enabled = False`.
- Dynamic gamma currently supports `sim_linear`.
- Metrics already include gamma and similarity summaries when dynamic gamma is enabled.

## Local Stage Plan
### Stage L0: Documentation Reorganization
Goal: establish this branch's local Qwen1.5B fallback documentation, archive prior local infrastructure reports, and stop before environment setup.

### Stage L1: Environment and Static Readiness Audit
Goal: verify existing environment and dependency versions without installing or upgrading large packages. Prepare static QLoRA config using local-safe placeholders.

### Stage L2: Tiny Static Path Validation
Goal: run the smallest approved dummy/tiny static SimPO path. Use CPU or tiny model first when possible. Real Qwen model loading requires approval.

### Stage L3: Tiny Dynamic Gamma Validation
Goal: run the smallest approved dynamic-gamma path and confirm gamma/similarity logging appears.

### Stage L4: Approved Qwen2.5-1.5B QLoRA Smoke
Goal: compare static vs dynamic QLoRA on tiny approved data with peak memory logging. Requires approval before model loading, data access, GPU training, and any large download.

### Stage L5: Local Fallback Evaluation Preparation
Goal: prepare AlpacaEval-style judge templates and dry-run validation. DeepSeek API calls require separate explicit approval and may only check key presence before approved calls.

### Stage L6: Final Local Fallback Report
Goal: consolidate static/dynamic logs, memory comparison, limitations, and next steps. Explicitly state that this is not evidence for 8B/9B full fine-tuning.

## Stage Gate
Do not recommend larger training or evaluation unless:

- static path runs successfully
- dynamic gamma path runs successfully
- at least one dynamic strategy survives small validation
- peak memory is measured and within local fallback budget
- logs and artifacts are reproducible enough for review
- required approvals are documented

If the gate is not met, recommend local validation, rollback, or simplification.
