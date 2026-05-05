# Local vs Server Boundary Review

Date: 2026-05-04

## Purpose

This report reviews the boundary between local-first work and server/cloud execution for the SimPO adaptive gamma project. It is a project boundary and migration-readiness assessment, not approval to start server work.

Key conclusion:

- The project should continue maximizing local preparation before any server/cloud execution.
- Stage 4 means a migration package exists for review; it does not mean Stage 5 should begin.
- Server/cloud execution is only appropriate for work that cannot be meaningfully completed on the local RTX 4090 Laptop / WSL2 development node.

## 1. What Has Been Done So Far

### Stage 0 - Project Takeover and Repository Audit

Status: PASS

Key actions completed:

- Read project instructions and templates.
- Audited repository structure.
- Identified main training entrypoint:
  - `scripts/run_simpo.py`
- Identified trainer/loss implementation:
  - `scripts/simpo_trainer.py`
- Identified config path:
  - `scripts/simpo_config.py`
- Identified static gamma handling:
  - `gamma_beta_ratio` in `SimPOConfig`
  - `self.gamma_beta_ratio` in `SimPOTrainer.simpo_loss`
- Identified chosen/rejected data flow:
  - dataset formatting in `scripts/run_simpo.py`
  - chosen/rejected concatenation and loss flow in `scripts/simpo_trainer.py`
- Proposed the lowest-risk semantic-similarity hook:
  - reuse hidden states already flowing into the LM head during the existing forward pass.

Files changed or created:

- `docs_for_human/stage_0.md`

Evidence and artifacts:

- Human-facing report: `docs_for_human/stage_0.md`

Unresolved issues:

- Exact Stage 0 command transcript is not fully repeated in this review.
- Real model memory behavior was not part of Stage 0.

### Stage 1 - Environment and Baseline Smoke Path

Status: PASS

Key actions completed:

- Prepared a repository-local Python environment.
- Repaired dependency compatibility enough for tiny local smoke tests.
- Ran local static/baseline smoke validation with tiny local model/data.
- Verified the real training entrypoint can execute on local tiny data.

Files changed or created:

- `docs_for_human/stage_1.md`
- `docs_for_agent/experiment_logs/local-static-smoke-001.md`
- `docs_for_agent/experiment_logs/local-run-simpo-smoke-001.md`
- `stage_artifacts/stage1/`

Scripts/configs prepared:

- `stage_artifacts/stage1/local-run-simpo-smoke.yaml`
- local tiny model/data artifacts under `stage_artifacts/stage1/`

Experiments or smoke tests performed:

- Trainer-level static tiny smoke.
- `scripts/run_simpo.py` local entrypoint tiny smoke.

Evidence and artifacts:

- `stage_artifacts/stage1/local-run-simpo-smoke-output/`
- `stage_artifacts/stage1/local-run-simpo-smoke-output/train_results.json`
- `stage_artifacts/stage1/local-run-simpo-smoke-output/trainer_state.json`
- experiment logs under `docs_for_agent/experiment_logs/`

Unresolved issues:

- Stage 1 validated only tiny local behavior.
- No real 8B/9B model was loaded or trained.
- No real UltraFeedback-scale run was performed.

### Stage 2 - Dynamic Gamma Prototype

Status: PASS after approved recovery

Key actions completed:

- Implemented a minimal, default-disabled dynamic gamma prototype.
- Added explicit `SimPOConfig` fields:
  - `dynamic_gamma_enabled`
  - `dynamic_gamma_strategy`
  - `dynamic_gamma_similarity_scale`
  - `dynamic_gamma_min`
  - `dynamic_gamma_max`
- Added dynamic gamma path in `SimPOTrainer`.
- Captured LM-head input hidden states through a temporary forward pre-hook.
- Detached captured hidden states to avoid creating an extra optimization path.
- Mean-pooled chosen/rejected response hidden states.
- Computed cosine similarity between chosen and rejected response embeddings.
- Mapped similarity to per-sample `gamma_beta_ratio` using `sim_linear`.
- Logged dynamic gamma and similarity metrics.
- Preserved static behavior by default.
- Repaired the local `.venv` Python runtime after explicit approval.

Files changed or created:

- `scripts/simpo_config.py`
- `scripts/simpo_trainer.py`
- `.gitignore`
- `stage_artifacts/stage2/local_dynamic_gamma_smoke.py`
- `stage_artifacts/stage2/local-run-simpo-dynamic-smoke.yaml`
- `docs_for_human/stage_2.md`
- `docs_for_agent/experiment_logs/local-dynamic-gamma-smoke-001.md`
- `docs_for_agent/experiment_logs/local-run-simpo-dynamic-smoke-001.md`

Scripts/configs prepared:

- `stage_artifacts/stage2/local_dynamic_gamma_smoke.py`
- `stage_artifacts/stage2/local-run-simpo-dynamic-smoke.yaml`

Experiments or smoke tests performed:

- CPU tiny trainer dynamic smoke.
- CPU tiny `scripts/run_simpo.py` dynamic smoke.

Evidence and artifacts:

- `stage_artifacts/stage2/local-dynamic-gamma-smoke-001-summary.json`
- `stage_artifacts/stage2/local-run-simpo-dynamic-smoke-output/`
- `stage_artifacts/stage2/local-run-simpo-dynamic-smoke-output/train_results.json`
- `stage_artifacts/stage2/local-run-simpo-dynamic-smoke-output/trainer_state.json`

Unresolved issues:

- Dynamic gamma is validated only on tiny local data.
- Compatibility with PEFT, FSDP, DeepSpeed, and full 8B/9B models is not proven.
- The only implemented dynamic strategy is `sim_linear`.

### Stage 3 - Local Stability Validation

Status: PASS after local-safe recovery

Key actions completed:

- Ran CPU tiny static vs dynamic stability comparison.
- Ran CUDA visibility diagnosis.
- Diagnosed that default execution sandbox hides CUDA devices, while sandbox-outside execution can see CUDA.
- Ran a bounded tiny GPU memory smoke after CLI approval.
- Recorded CPU and tiny GPU memory signals.

Files changed or created:

- `stage_artifacts/stage3/local_tiny_stability_compare.py`
- `stage_artifacts/stage3/local_tiny_gpu_memory_compare.py`
- `docs_for_human/stage_3.md`
- `docs_for_agent/experiment_logs/local-tiny-stability-001.md`
- `docs_for_agent/experiment_logs/local-tiny-gpu-memory-001.md`

Scripts/configs prepared:

- `stage_artifacts/stage3/local_tiny_stability_compare.py`
- `stage_artifacts/stage3/local_tiny_gpu_memory_compare.py`

Experiments or smoke tests performed:

- CPU tiny static/dynamic comparison:
  - static: PASS
  - dynamic `sim_linear`: PASS
- Tiny GPU memory smoke:
  - static: PASS
  - dynamic `sim_linear`: PASS

Evidence and artifacts:

- `stage_artifacts/stage3/local-tiny-stability-001-summary.json`
- `stage_artifacts/stage3/local-tiny-gpu-memory-001-summary.json`
- `stage_artifacts/stage3/local-tiny-gpu-memory-001-static.json`
- `stage_artifacts/stage3/local-tiny-gpu-memory-001-dynamic.json`

Important evidence:

- Tiny GPU static max reserved CUDA memory: `22.0` MB
- Tiny GPU dynamic max reserved CUDA memory: `22.0` MB
- Tiny GPU dynamic minus static max reserved delta: `0.0` MB
- This proves only tiny-scale behavior, not 8B/9B training memory.

Unresolved issues:

- Real 8B/9B memory overhead remains unknown.
- Wrapper compatibility under PEFT/FSDP/DeepSpeed remains unknown.
- Real dataset behavior remains unknown.

### Stage 4 - Cloud Readiness Preparation

Status: PASS for local-only cloud-readiness preparation

Key actions completed:

- Prepared a local cloud-readiness package.
- Chose a deliberately small primary matrix:
  - Gemma-2-9B-it static baseline
  - Gemma-2-9B-it dynamic `sim_linear`
- Prepared static and dynamic candidate configs.
- Prepared runbook, manifest, risk register, and experiment matrix.
- Statically validated JSON/YAML and argument-parser compatibility.

Files changed or created:

- `docs_for_human/stage_4.md`
- `stage_artifacts/stage4/cloud_run_package/README.md`
- `stage_artifacts/stage4/cloud_run_package/manifest.json`
- `stage_artifacts/stage4/cloud_run_package/experiment_matrix.md`
- `stage_artifacts/stage4/cloud_run_package/runbook.md`
- `stage_artifacts/stage4/cloud_run_package/risk_register.md`
- `stage_artifacts/stage4/cloud_run_package/accelerate/deepspeed_zero3_4gpu.yaml`
- `stage_artifacts/stage4/cloud_run_package/configs/gemma-2-9b-it-simpo-static.yaml`
- `stage_artifacts/stage4/cloud_run_package/configs/gemma-2-9b-it-simpo-dynamic-sim-linear.yaml`

Scripts/configs prepared:

- Stage 4 cloud package under `stage_artifacts/stage4/cloud_run_package/`

Experiments or smoke tests performed:

- No training or model execution was performed in Stage 4.
- Static validation only:
  - manifest JSON parsed
  - YAML files parsed
  - both candidate configs parsed through `H4ArgumentParser`
  - manifest references resolved

Evidence and artifacts:

- `docs_for_human/stage_4.md`
- `stage_artifacts/stage4/cloud_run_package/`

Unresolved issues:

- Stage 4 does not authorize Stage 5.
- Cloud provider, server hardware, budget, credentials, cache paths, and W&B policy are unresolved.
- Exact server dollar cost is missing.
- Real 9B smoke and full training are not performed.

## 2. What Can Still Be Done Locally

### Tier A - Safe Local Work Without Approval

These items are local-safe because they are inspection, static validation, documentation, dry-run parsing, or tiny dummy validation that does not use real models/data or heavy resources.

| Item | Why Tier A | Evidence It Would Produce | Necessary Before Server Migration |
|---|---|---|---|
| Code review of dynamic gamma implementation | Static inspection only | Review notes on hook lifetime, detach behavior, shape assumptions, logging, default-off safety | Yes |
| Static diff review against original SimPO behavior | Read-only review of `scripts/simpo_config.py` and `scripts/simpo_trainer.py` | Confirmation that static path remains equivalent when `dynamic_gamma_enabled=false` | Yes |
| Config review of Stage 4 package | Read-only config inspection | Confirmation that static/dynamic configs differ only where intended | Yes |
| Add or refine documentation on local/server boundaries | Documentation only | Clearer handoff and approval gates | Yes |
| Dry-run parser checks for candidate configs | No model load or training required | Parser compatibility evidence | Yes, already done once but repeatable |
| Tiny unit tests for gamma mapping math | Dummy tensors only | Deterministic checks for clamp, similarity normalization, and per-sample gamma | Recommended before server |
| Tiny unit tests for response pooling masks | Dummy tensors only | Evidence that prompt/pad tokens are excluded as intended | Recommended before server |
| Static check of logging keys | No training required if using direct function tests | Confirmation dynamic metrics names are stable | Recommended before server |
| Review rollback path | Documentation/static review | Clear instructions to disable dynamic gamma by config | Yes |
| Prepare experiment log skeletons for future runs | Documentation only | Ready-to-fill logs for cloud smoke/static/dynamic runs | Recommended before server |
| Review Stage 4 package for exact approval gates | Documentation/config review | Human-ready list of required approvals | Yes |

Remaining Tier A priorities:

1. Add focused local unit tests or artifact tests for dynamic gamma math and pooling.
2. Perform a code-review pass specifically for wrapper risks and static-path equivalence.
3. Tighten the Stage 4 package with explicit smoke-log templates and rollback checklist.

### Tier B - Local Work Requiring Explicit Approval

These items are still local, but require approval because they touch GPU, real model/data access, dependency changes, downloads, or AGENTS.md resource thresholds.

| Item | Why Tier B | Evidence It Would Produce | Necessary Before Server Migration |
|---|---|---|---|
| Any GPU run, even tiny | AGENTS.md requires care for GPU/resource-heavy actions; sandbox GPU access may need CLI approval | GPU visibility, memory, and runtime evidence | Optional; tiny GPU already done once |
| Tiny real dataset schema check | Real dataset access may download data and touch UltraFeedback-like assets | Evidence that `prompt/chosen/rejected` formatting works on real data | Useful but requires approval if download/access occurs |
| Real tokenizer/model config-only load | Model access/download may be large or gated | Early compatibility evidence for tokenizer/chat template | Useful but not mandatory locally |
| Any Gemma-2-9B or Llama-3-8B load | 8B/9B load requires explicit approval even if called smoke | Real model load feasibility evidence | Not required locally; server is more appropriate |
| Dependency install or upgrade | Environment-changing action under AGENTS.md | Updated environment evidence | Avoid unless blocked |
| Local PEFT/FSDP/DeepSpeed smoke with tiny model on GPU | GPU and wrapper execution may require approval | Early wrapper compatibility evidence | Useful if tightly bounded, but not strictly required |
| Any command expected to exceed 10 minutes, 8GB VRAM, or 16GB RAM | Explicit AGENTS.md threshold | Resource envelope evidence | Not recommended locally |

Recommended Tier B local work only if approved:

- A very small wrapper-focused smoke using a tiny model, not a real 8B/9B model, to check whether the LM-head hook survives common wrapping patterns.
- A tiny real-data schema check, only if dataset access is approved and bounded.

### Tier C - Not Appropriate for the Local Laptop

These items are not appropriate for the local RTX 4090 Laptop / WSL2 node because they are full-scale, long-running, or likely to exceed the local development role.

| Item | Why Tier C | Evidence It Would Produce | Necessary Before Server Migration |
|---|---|---|---|
| Full Gemma-2-9B static SimPO training | 9B full training is outside local-dev role and likely exceeds stable local memory/time budget | Baseline training metrics and checkpoint | Required for final project, but should be server-side |
| Full Gemma-2-9B dynamic SimPO training | Same as above plus dynamic gamma memory/stability risk | Dynamic training metrics, gamma/similarity distributions, checkpoint | Required for final comparison, server-side |
| Full Llama-3-8B training | 8B full training is outside local-dev role and may require gated model access/Flash Attention readiness | Alternative model evidence | Optional unless project chooses Llama path |
| Large ablation grid | Conflicts with limited-compute and minimum viable experiment strategy | Hyperparameter sensitivity | Optional; defer |
| Full AlpacaEval 2 / Arena-Hard evaluation | Benchmark runs are explicitly not local laptop work | Final benchmark metrics | Required only after successful training |
| Long unattended GPU jobs | Local machine is not a training server | Longer-run stability evidence | Should be server-side if needed |

## 3. What Truly Requires a Server

### Full Static Baseline Training

Why local is insufficient:

- It uses a 9B model candidate and full preference data.
- The local RTX 4090 Laptop has 16GB VRAM and is defined by project policy as a development node, not a full training server.
- Full training would be long-running and resource-heavy.

Minimum server/GPU assumption:

- A100/A800-class or equivalent server.
- Multi-GPU setup matching or adapting the Stage 4 DeepSpeed/FSDP plan.
- Persistent storage for model cache, dataset cache, logs, and checkpoints.

Expected inputs:

- Static config from `stage_artifacts/stage4/cloud_run_package/configs/gemma-2-9b-it-simpo-static.yaml`
- Accelerate config from `stage_artifacts/stage4/cloud_run_package/accelerate/deepspeed_zero3_4gpu.yaml`
- Approved access to `google/gemma-2-9b-it`
- Approved access to `princeton-nlp/gemma2-ultrafeedback-armorm`

Expected outputs:

- Training logs
- `train_results.json`
- `trainer_state.json`
- checkpoint/model output directory
- memory and runtime metrics

Required for project completion:

- Yes, if Gemma remains the primary model path.

### Full Dynamic `sim_linear` Training

Why local is insufficient:

- Same 9B/full-data constraints as static baseline.
- Adds real-scale validation of hidden-state capture, gamma logging, and memory overhead.

Minimum server/GPU assumption:

- Same as static baseline.
- Prefer the same hardware and environment as static to make comparison meaningful.

Expected inputs:

- Dynamic config from `stage_artifacts/stage4/cloud_run_package/configs/gemma-2-9b-it-simpo-dynamic-sim-linear.yaml`
- Same model/data/cache/logging assumptions as baseline

Expected outputs:

- Training logs
- gamma and similarity distributions
- loss/grad/reward metrics
- checkpoint/model output directory
- memory delta relative to static baseline

Required for project completion:

- Yes, because it is the core project hypothesis.

### Larger-Scale Ablation

Why local is insufficient:

- Multiple 8B/9B runs or long partial runs are outside local scope.
- Ablations can quickly become a resource grid.

Minimum server/GPU assumption:

- Same model-capable server class as full training.
- Budget must be explicitly approved.

Expected inputs:

- Additional configs for scale, clamp, or strategy variants.

Expected outputs:

- Comparative stability and performance metrics.

Required for project completion:

- Optional. The minimum project can use one static baseline and one dynamic run.

### Final Evaluation

Why local is insufficient:

- AlpacaEval 2 and Arena-Hard are final-stage benchmark tasks.
- They may require generated outputs, evaluator dependencies, API/model access, and long-running inference/evaluation.

Minimum server/GPU assumption:

- Server with enough GPU memory for inference, or approved evaluation service/API setup.

Expected inputs:

- Final static and dynamic checkpoints.
- Evaluation configs under `eval/`.

Expected outputs:

- AlpacaEval 2 length-controlled result.
- Arena-Hard result.
- Generation logs and evaluation artifacts.

Required for project completion:

- Required for final research claim.
- Not required before training migration.

## 4. Migration Plan

### Pre-Migration Local Checklist

Complete before requesting full server execution:

- Confirm Stage 0-4 reports exist:
  - `docs_for_human/stage_0.md`
  - `docs_for_human/stage_1.md`
  - `docs_for_human/stage_2.md`
  - `docs_for_human/stage_3.md`
  - `docs_for_human/stage_4.md`
- Confirm this boundary review is accepted:
  - `docs_for_human/local_vs_server_boundary_review.md`
- Review dynamic gamma code for:
  - default-disabled behavior
  - static-path equivalence
  - hidden-state detach
  - hook lifetime
  - tensor shape assumptions
  - gamma clamp behavior
  - logging keys
- Add or run focused local-safe unit tests if approved by project owner:
  - gamma mapping test
  - response pooling mask test
  - static-path no-dynamic-logs test
- Review Stage 4 package:
  - static config
  - dynamic config
  - runbook
  - risk register
  - manifest
- Prepare rollback note:
  - set `dynamic_gamma_enabled: false`
  - use static config as baseline
  - preserve original SimPO behavior

### Files, Configs, and Scripts to Package

Required:

- `scripts/run_simpo.py`
- `scripts/simpo_config.py`
- `scripts/simpo_trainer.py`
- `alignment/`
- `training_configs/`
- `accelerate_configs/`
- `stage_artifacts/stage4/cloud_run_package/`
- `docs_for_agent/experiment_log_template.md`
- `docs_for_agent/experiment_logs/`
- `docs_for_human/`
- `environment.yml`

Useful evidence package:

- `stage_artifacts/stage1/`
- `stage_artifacts/stage2/`
- `stage_artifacts/stage3/`

### Environment Requirements

Expected baseline:

- Python 3.10
- PyTorch 2.2.2 CUDA build
- Transformers 4.44.2
- Datasets 2.18.0
- Accelerate 0.29.2
- TRL 0.9.6
- PEFT 0.7.1
- DeepSpeed compatible with selected server setup
- BF16-capable GPUs

Policy:

- Do not change CUDA/PyTorch/Transformers/TRL/DeepSpeed/Accelerate versions without recording approval and reason.

### Model and Data Access Requirements

Needed before server smoke:

- Hugging Face access to `google/gemma-2-9b-it`
- Hugging Face access to `princeton-nlp/gemma2-ultrafeedback-armorm`
- Persistent `HF_HOME` or equivalent cache path
- Enough disk for:
  - model weights
  - dataset cache
  - checkpoints
  - logs

Missing evidence:

- Current report does not confirm credentials or access acceptance.
- Current report does not estimate exact disk usage.

### Logging and Checkpoint Policy

Recommended:

- Use a dedicated W&B project or approved offline logging.
- Record:
  - git commit
  - dirty diff
  - config snapshot
  - environment versions
  - memory stats
  - checkpoint path
  - train/eval metrics
  - dynamic gamma/similarity logs for dynamic run
- Keep checkpoint retention conservative at first:
  - Stage 4 configs currently use `save_steps: 400`
  - `save_total_limit: 3`

### Server Smoke-Test Concept

Do not begin with full training.

Smoke concept:

1. Verify environment imports and CUDA visibility.
2. Verify model/tokenizer access.
3. Verify dataset access and schema formatting.
4. Run a very short static training smoke with the same entrypoint/config family.
5. Confirm loss, grad norm, memory, and checkpoint/log behavior.
6. Run a very short dynamic smoke only if static smoke passes.
7. Confirm dynamic gamma and similarity logs appear and are finite.

Full commands are intentionally omitted here because server target, launcher, cache paths, and logging mode are not yet selected.

### Server Smoke Pass/Fail Criteria

Pass if:

- Environment loads without dependency errors.
- CUDA sees the expected GPUs.
- Model/tokenizer load succeeds.
- Dataset formatting succeeds.
- Static smoke completes without OOM or NaN/Inf.
- Dynamic smoke completes without OOM or NaN/Inf.
- Dynamic logs include finite:
  - `gamma_beta_ratio/mean`
  - `gamma_beta_ratio/min`
  - `gamma_beta_ratio/max`
  - `similarity/mean`
  - `similarity/min`
  - `similarity/max`
- Checkpoint/log paths are written as expected.

Fail or stop if:

- OOM occurs.
- NaN/Inf appears.
- Hidden-state hook fails under wrapper/distributed setup.
- Dataset schema or chat template is wrong.
- Memory overhead is clearly beyond the project red line.
- Logs or checkpoints are not reproducible.

### Cleanup and Rollback Policy

Cleanup:

- Do not delete checkpoints, logs, datasets, or caches without explicit human approval.
- Mark failed outputs clearly rather than removing them.

Rollback:

- Use static config with `dynamic_gamma_enabled: false`.
- Preserve Stage 4 package as the source of comparison.
- If dynamic hook fails under distributed wrappers, hold dynamic full training and investigate locally with tiny wrapper tests or narrow cloud smoke.

### Decision Gate Before Full Training

Full training should start only after:

- Human approves server/cloud use.
- Human approves 9B training.
- Human approves model and dataset downloads.
- Server smoke passes.
- Static smoke is healthy.
- Dynamic smoke is healthy.
- Logging/checkpoint policy is confirmed.
- Budget/wall-clock limit is accepted.

## 5. Immediate Next Action

Recommended immediate next action:

- continue local preparation

Reason:

- Stage 4 produced a migration package, but local preparation is not exhausted.
- Additional local-safe review and unit tests can still reduce server risk without using cloud resources.
- There is no concrete technical reason yet to stop local work and move immediately to server execution.

Specific next local preparation item:

- Perform a focused local review and, if approved as local-safe project work, add tiny unit tests for dynamic gamma math, response pooling masks, static-path equivalence, and logging-key expectations.

Human approval required for this immediate next action:

- No, if limited to static review, documentation, and tiny CPU/dummy tests.
- Yes, if it expands to GPU runs, real model loads, real dataset access, downloads, dependency changes, or any AGENTS.md resource threshold.

