# Local Phase Final Report for ChatGPT / Project Supervisor

Date: 2026-05-04

This report closes the local phase for project-level review. It is self-contained and decision-oriented. It does not authorize server/cloud execution.

## 1. Executive Summary

- The local phase completed repository takeover, baseline smoke validation, dynamic gamma prototype implementation, local stability validation, cloud-readiness packaging, and local/server boundary review.
- The main training entrypoint is `scripts/run_simpo.py`; dynamic gamma code exists in `scripts/simpo_config.py` and `scripts/simpo_trainer.py`.
- The static SimPO path is preserved by default because `dynamic_gamma_enabled` defaults to `False`.
- Tiny local static and dynamic runs passed through both trainer-level and `scripts/run_simpo.py` entrypoint paths.
- CPU tiny validation and a bounded tiny GPU memory smoke passed; at tiny scale, static and dynamic both used 22.0 MB max reserved CUDA memory.
- Focused dummy/unit checks passed for static gamma equivalence, response masking, dynamic gamma clamp behavior, LM-head hook detach/removal, and metric-key contracts.
- A local-only Stage 4 cloud-readiness package exists under `stage_artifacts/stage4/cloud_run_package/`.
- No local run proves full 8B/9B training feasibility, real UltraFeedback behavior, final benchmark improvement, or DeepSpeed/FSDP/PEFT wrapper compatibility.
- Local work has reached diminishing returns for no-approval work: remaining local tasks are mostly review/documentation or optional approved tiny checks.
- Migration planning is appropriate, but server/cloud execution is not authorized until human decisions are made.
- Highest remaining risks are real 8B/9B memory overhead, distributed wrapper compatibility, server cost, credential/access readiness, and final benchmark uncertainty.

## 2. Local Phase Timeline

| Stage | Status | Key Actions | Files Changed or Created | Evidence / Artifacts | Unresolved Issues |
|---|---|---|---|---|---|
| Stage 0 - Project takeover and repository audit | PASS | Read instructions, audited repo, identified entrypoint/loss/config/data flow, proposed hook point | `docs_for_human/stage_0.md` | `docs_for_human/stage_0.md` | Raw transcript not fully persisted; real model memory not assessed |
| Stage 1 - Environment and baseline smoke | PASS | Created `.venv`, installed minimal deps, fixed compatibility, ran static tiny trainer and entrypoint smokes | `docs_for_human/stage_1.md`, `docs_for_agent/experiment_logs/local-static-smoke-001.md`, `docs_for_agent/experiment_logs/local-run-simpo-smoke-001.md`, `stage_artifacts/stage1/` | `local-static-smoke-001`, `local-run-simpo-smoke-001`, `stage_artifacts/stage1/local-run-simpo-smoke-output/train_results.json` | Tiny only; no real 8B/9B or real UltraFeedback; exact entrypoint peak VRAM not recorded |
| Stage 2 - Dynamic gamma prototype | PASS after approved recovery | Added default-disabled dynamic gamma config/trainer path, repaired local Python runtime, ran CPU tiny dynamic smokes | `scripts/simpo_config.py`, `scripts/simpo_trainer.py`, `.gitignore`, `docs_for_human/stage_2.md`, Stage 2 scripts/logs/artifacts | `stage_artifacts/stage2/local-dynamic-gamma-smoke-001-summary.json`, `stage_artifacts/stage2/local-run-simpo-dynamic-smoke-output/`, experiment logs | Real 8B/9B memory and wrapper compatibility unknown; only `sim_linear` implemented |
| Stage 3 - Local stability validation | PASS after local-safe recovery | Ran CPU tiny static/dynamic comparison, diagnosed CUDA sandbox visibility, ran approved tiny GPU memory smoke | `docs_for_human/stage_3.md`, `stage_artifacts/stage3/local_tiny_stability_compare.py`, `stage_artifacts/stage3/local_tiny_gpu_memory_compare.py`, experiment logs | CPU tiny PASS; tiny GPU static/dynamic max reserved CUDA memory both 22.0 MB; delta 0.0 MB | Tiny scale only; DeepSpeed/FSDP/PEFT, real data, long-run stability unknown |
| Stage 4 - Cloud readiness preparation | PASS for local-only preparation | Prepared minimal Gemma static/dynamic cloud package, validated JSON/YAML/parser compatibility | `docs_for_human/stage_4.md`, `stage_artifacts/stage4/cloud_run_package/` | `manifest.json`, static/dynamic Gemma configs, runbook, risk register, `h4_parse_ok 2 configs` | No cloud/server selected; no dollar cost; no full training authorization |
| Stage 4 local-first update | PASS for continued local preparation | Added focused code review and CPU/dummy unit checks | `stage_artifacts/stage4/dynamic_gamma_code_review.md`, `stage_artifacts/stage4/local_dynamic_gamma_unit_checks.py`, `docs_for_agent/experiment_logs/local-dynamic-gamma-unit-checks-001.md`, updated `docs_for_human/stage_4.md` | Five dummy/unit checks passed | Real distributed/large-model behavior still unknown |
| Boundary review | Completed | Clarified local/server boundary and recommended continued local preparation before server execution | `docs_for_human/local_vs_server_boundary_review.md` | Project boundary review report | Not a stage report; does not authorize server execution |

Source of truth:

- `docs_for_human/stage_0.md`
- `docs_for_human/stage_1.md`
- `docs_for_human/stage_2.md`
- `docs_for_human/stage_3.md`
- `docs_for_human/stage_4.md`
- `docs_for_human/local_vs_server_boundary_review.md`

Missing information is marked above where not recorded.

## 3. Repository / Code State

Current branch before this report commit:

- `main`

Current commit before this report commit:

- `1b3e8f3`

Dirty/uncommitted changes before this report commit:

- Modified tracked files:
  - `.gitignore`
  - `scripts/simpo_config.py`
  - `scripts/simpo_trainer.py`
- Untracked project/report artifacts:
  - `AGENTS.md`
  - `docs_for_agent/`
  - `docs_for_human/`
  - `stage_artifacts/`
  - `.codex` empty file

Important code changes:

- `scripts/simpo_config.py`
  - Adds `dynamic_gamma_enabled`
  - Adds `dynamic_gamma_strategy`
  - Adds `dynamic_gamma_similarity_scale`
  - Adds `dynamic_gamma_min`
  - Adds `dynamic_gamma_max`
- `scripts/simpo_trainer.py`
  - Adds optional per-sample `gamma_beta_ratio` to `SimPOTrainer.simpo_loss`
  - Adds LM-head hidden-state capture via `_capture_lm_head_hidden_states`
  - Adds `_response_embedding_similarity`
  - Adds `_compute_dynamic_gamma_beta_ratio`
  - Adds dynamic gamma/similarity metrics in `get_batch_loss_metrics`

Baseline/static path:

- Preserved by default.
- `dynamic_gamma_enabled=False` means no LM-head hook is registered and `simpo_loss` uses scalar `self.gamma_beta_ratio`.
- Dummy/unit evidence exists in `stage_artifacts/stage4/local_dynamic_gamma_unit_checks.py`.

Configs/scripts for local execution:

- `stage_artifacts/stage1/local-run-simpo-smoke.yaml`
- `stage_artifacts/stage2/local-run-simpo-dynamic-smoke.yaml`
- `stage_artifacts/stage2/local_dynamic_gamma_smoke.py`
- `stage_artifacts/stage3/local_tiny_stability_compare.py`
- `stage_artifacts/stage3/local_tiny_gpu_memory_compare.py`
- `stage_artifacts/stage4/local_dynamic_gamma_unit_checks.py`

Configs/scripts for cloud preparation:

- `stage_artifacts/stage4/cloud_run_package/`
- `stage_artifacts/stage4/cloud_run_package/configs/gemma-2-9b-it-simpo-static.yaml`
- `stage_artifacts/stage4/cloud_run_package/configs/gemma-2-9b-it-simpo-dynamic-sim-linear.yaml`
- `stage_artifacts/stage4/cloud_run_package/accelerate/deepspeed_zero3_4gpu.yaml`

Files that should not be committed without cleanup or explicit policy:

- Tiny model weights:
  - `stage_artifacts/stage1/local_tiny_gpt2/model.safetensors`
  - `stage_artifacts/stage1/local-run-simpo-smoke-output/model.safetensors`
  - `stage_artifacts/stage2/local-run-simpo-dynamic-smoke-output/model.safetensors`
- Training output binaries:
  - `stage_artifacts/stage1/local-run-simpo-smoke-output/training_args.bin`
  - `stage_artifacts/stage2/local-run-simpo-dynamic-smoke-output/training_args.bin`
- Dataset/cache Arrow files:
  - `stage_artifacts/stage1/hf-cache/**/*.arrow`
  - `stage_artifacts/stage2/hf-cache/**/*.arrow`
- Cache directories:
  - `stage_artifacts/stage1/hf-cache/`
  - `stage_artifacts/stage2/hf-cache/`
  - `stage_artifacts/stage3/hf-cache/`
- Local runtimes/environments:
  - `.venv/`
  - `.uv-python/`

No credentials, `.env`, W&B secrets, or token files were identified in the inspected project files. The `.venv` path contains a `wandb` executable, but `.venv/` is ignored and should not be committed.

## 4. What Local Work Achieved

### Actually Executed and Validated

- Repository audit:
  - training entrypoint, trainer/loss path, config path, gamma handling, and chosen/rejected flow identified.
- Environment/resource assessment:
  - WSL2 context identified.
  - RTX 4090 Laptop GPU with 16376 MiB VRAM identified under approved GPU-visible context.
  - WSL-visible system RAM about 31 GiB and 8 GiB swap recorded.
- Baseline static smoke:
  - trainer-level tiny static smoke passed.
  - real `scripts/run_simpo.py` tiny static smoke passed.
- Dynamic gamma prototype:
  - default-disabled config fields and trainer path implemented.
  - CPU tiny trainer dynamic smoke passed.
  - CPU tiny entrypoint dynamic smoke passed.
- Local stability:
  - CPU tiny static/dynamic comparison passed.
  - tiny GPU memory smoke passed after CLI approval.
  - dynamic tiny GPU max reserved memory matched static at 22.0 MB.
- Local unit/dummy checks:
  - static gamma equivalence passed.
  - response pooling mask behavior passed.
  - dynamic gamma clamp behavior passed.
  - LM-head hook detach/removal passed.
  - metric key contract passed.
- Documentation/stage gate:
  - stage reports persisted under `docs_for_human/`.
  - experiment logs persisted under `docs_for_agent/experiment_logs/`.
  - local/server boundary review created.

### Prepared but Not Executed

- Stage 4 cloud-readiness package:
  - minimal Gemma static/dynamic matrix.
  - static and dynamic Gemma configs.
  - DeepSpeed Zero3 4-GPU accelerate config.
  - runbook, manifest, experiment matrix, risk register.
- Server smoke concept:
  - environment/model/data/log/checkpoint smoke before full training.
- Full training configs:
  - prepared for review only; not executed.

### Planned but Not Yet Done

- Real model/tokenizer access validation.
- Real UltraFeedback schema/access validation.
- DeepSpeed/FSDP/PEFT wrapper compatibility check.
- Server smoke.
- Full static baseline training.
- Full dynamic training.
- AlpacaEval 2 / Arena-Hard final evaluation.

## 5. What Local Work Cannot Reliably Prove

Local hardware constraints:

- GPU is an RTX 4090 Laptop GPU with 16376 MiB VRAM, not a desktop RTX 4090 and not an A100/A800/H100 server GPU.
- WSL-visible memory was about 31 GiB with 8 GiB swap, below the host RAM expected in the project brief.
- CUDA visibility depends on execution context; default sandbox hid CUDA, while approved sandbox-outside commands saw one GPU.

What local runs cannot prove:

- Full 8B/9B SimPO training feasibility.
- Real 9B memory overhead from dynamic hidden-state capture.
- DeepSpeed/FSDP/PEFT wrapper compatibility.
- Stability over full UltraFeedback-scale data.
- Throughput or wall-clock cost for full training.
- Final AlpacaEval 2 or Arena-Hard improvement.
- Whether dynamic gamma improves benchmark quality.

Missing evidence:

- Real 8B/9B model load/run evidence.
- Real dataset access and schema evidence.
- Cloud/server memory traces.
- Full baseline checkpoint.
- Full dynamic checkpoint.
- Final benchmark outputs.
- Cost and runtime estimates from a selected server.

## 6. Remaining Local Options

### Tier A: Safe Local Work Without Approval

| Remaining Item | Evidence Produced | Necessary Before Server Migration |
|---|---|---|
| Static review of `scripts/simpo_trainer.py` and `scripts/simpo_config.py` | Review notes and risk list | Useful; already partially done |
| Config review of Stage 4 package | Confirmation config diffs are intentional | Useful; already done once |
| Documentation cleanup | Cleaner handoff, fewer project-level ambiguities | Optional |
| Dry-run parser checks | Config/parser compatibility | Useful; already done once |
| Tiny CPU/dummy tests | Function-level correctness evidence | Useful; already done for core gamma logic |
| Smoke-log template preparation | Reproducible future logging | Optional |

Conclusion:

- Most high-value Tier A work is complete.
- Remaining Tier A work is incremental and not a blocker for migration planning.

### Tier B: Local Work Requiring Explicit Human Approval

| Remaining Item | Why Approval Is Required | Evidence Produced | Necessary Before Server Migration |
|---|---|---|---|
| Any GPU run | GPU/resource approval policy and sandbox device exposure | Memory/runtime evidence | Not necessary; tiny GPU already done |
| Any real model loading | 8B/9B or gated model access/download risk | Model/tokenizer compatibility | Not necessary locally; better on server |
| Any real dataset access | dataset download/access risk | schema and formatting evidence | Useful but can be part of server smoke |
| Any dependency installation | environment-changing action | environment readiness | Avoid unless blocked |
| Any command exceeding AGENTS.md thresholds | explicit resource threshold | resource envelope evidence | Not recommended locally |

Conclusion:

- Tier B local work is optional and approval-gated.
- It should not delay project-level review unless the supervisor specifically wants more local evidence.

### Tier C: Not Appropriate for Local Laptop

| Remaining Item | Evidence Produced | Necessary Before Server Migration |
|---|---|---|
| Full 8B/9B static training | baseline checkpoint and full training metrics | Must be server-side |
| Full 8B/9B dynamic training | dynamic checkpoint, gamma/similarity distributions, memory delta | Must be server-side |
| Full UltraFeedback training | real-scale training behavior | Must be server-side |
| Large ablations | hyperparameter sensitivity | Optional and server-side |
| Final AlpacaEval 2 / Arena-Hard | final research metrics | Server-side or approved evaluation setup |
| Long unattended GPU jobs | long-run stability | Server-side |

Conclusion:

- These are the main reasons to migrate.
- They should not run on the local RTX 4090 Laptop / WSL2 node.

## 7. Server / Cloud Requirements

Assumptions for this table:

- Current Stage 4 configs use full fine-tuning style SimPO, BF16, `max_length: 2048`, `max_prompt_length: 1800`, gradient checkpointing, DeepSpeed/Accelerate, and checkpointing.
- Current configs do not use LoRA/QLoRA.
- If LoRA/QLoRA is introduced later, requirements may drop, but that would be a scope/config change.
- Exact full training feasibility cannot be proven from local evidence.

| Scenario | GPU Model/Class | GPU Count | Per-GPU VRAM | System RAM | CPU | Disk | Expected Use Case | Expected Limitation | Enough for Llama-3-8B | Enough for Gemma-2-9B | Cost-Control Strategy |
|---|---:|---:|---:|---:|---:|---:|---|---|---|---|---|
| Minimum configuration for cloud/server smoke test | A100/A800 40GB or similar 40GB+ datacenter GPU | 1 | 40GB+ | 128GB | 16 vCPU | 500GB SSD | Environment import, CUDA visibility, tokenizer/model access, dataset schema, 1-5 step smoke with reduced settings | Not a reliable full training configuration; single-GPU full fine-tune may still OOM or be too slow | Likely enough for smoke only, not proven for full run | Likely enough for smoke only, not proven for full run | Hard cap `max_steps`, no full epoch, stop after schema/model/memory check |
| Minimum configuration for one serious 8B/9B training run | A100/A800 40GB class | 4 | 40GB | 256GB | 32 vCPU | 1-2TB SSD | One full static or dynamic run using DeepSpeed Zero3-style setup | May be slower and memory-tighter than 80GB GPUs; dynamic overhead still needs monitoring | Expected feasible with careful config, not locally proven | Expected feasible with careful config, not locally proven | Run static first, retain limited checkpoints, stop on OOM/NaN |
| Recommended configuration for efficient full baseline + dynamic comparison | A100/A800 80GB class, or H100 80GB if available | 4 | 80GB | 512GB | 48-64 vCPU | 2TB SSD | Static baseline plus one dynamic `sim_linear` comparison with comparable settings | Higher cost; still requires smoke before full runs | Yes, expected | Yes, expected | Run two-primary-run matrix only; compare memory before adding ablations |
| Optional stronger configuration if budget permits | H100 80GB or 8x A100/A800 80GB | 8 | 80GB | 512GB-1TB | 64+ vCPU | 2-4TB SSD | Faster full baseline + dynamic training, optional follow-up ablation or evaluation generation | Cost can grow quickly; may be overkill for minimum viable project | Yes | Yes | Use only after baseline/dynamic pass; avoid large grids until evidence supports them |

Notes:

- A100/A800 40GB and 80GB should be treated differently. 80GB materially reduces memory risk and batch/sequence pressure.
- Single-GPU 40GB may be enough for smoke or LoRA/QLoRA-style experiments, but current prepared configs are not LoRA/QLoRA.
- Multi-GPU is recommended for full fine-tuning under the current repository style.
- Server smoke should be short and explicitly approved before any full run.

## 8. Cost-Control Strategy

- Start with server smoke only:
  - verify environment, CUDA, model/tokenizer access, dataset schema, logging, and checkpoint path.
- Run static baseline first:
  - do not run dynamic until static path is healthy on the target server.
- Run one dynamic strategy first:
  - only `sim_linear`, no curriculum or combined strategy until there is real-run evidence.
- Use minimal `max_steps` for smoke:
  - do not start a full epoch until smoke passes.
- Avoid large ablations:
  - no grid over gamma scale, beta, learning rate, or model family until baseline/dynamic are both stable.
- Control checkpoint frequency:
  - retain enough for recovery, but avoid excessive storage.
- Stop criteria:
  - OOM
  - NaN/Inf
  - hidden-state hook failure
  - severe loss/grad divergence
  - memory overhead clearly beyond budget
  - logging/checkpoint failure
- Preserve artifacts:
  - exact configs
  - git commit and diff
  - environment versions
  - train/eval metrics
  - memory traces
  - W&B/offline logs
  - checkpoint paths
  - failure logs

## 9. Migration Plan

### Repo Workflow

- Human connects to the Linux server over SSH from Win11 or macOS.
- VS Code Remote SSH is optional; plain SSH plus terminal is sufficient.
- Clone or update the repository:
  - use the pushed branch/commit from this local phase handoff.
  - do not rely on uncommitted local files.
- Record:
  - branch
  - commit hash
  - dirty diff, if any

### Environment Setup Concept

- Use a normal Linux server environment, not WSL.
- Prefer conda or a server-local venv with Python 3.10.
- Align with the known dependency envelope:
  - PyTorch 2.2.2 CUDA build or a deliberate server-compatible equivalent
  - Transformers 4.44.2
  - Datasets 2.18.0
  - Accelerate 0.29.2
  - TRL 0.9.6
  - PEFT 0.7.1
  - DeepSpeed compatible with the selected CUDA/PyTorch stack
- Do not change CUDA/PyTorch/Transformers/TRL/DeepSpeed/Accelerate versions without recording the reason.

### Credentials and Access

- Hugging Face access is needed for:
  - `google/gemma-2-9b-it`
  - `princeton-nlp/gemma2-ultrafeedback-armorm`
  - any optional Llama model/dataset path if selected
- W&B access is needed if `report_to: [wandb]` is kept.
- If W&B is not approved, switch to an offline logging policy before execution.
- Credentials, tokens, `.env`, and secrets must not be stored in git.

### Model/Data Download Strategy

- Use a persistent `HF_HOME` or equivalent cache directory outside git.
- Preflight available disk before downloads.
- Do not put model weights, datasets, or HF cache directories under tracked source paths.
- Record exact model/dataset revisions when possible.

### Checkpoint and Log Directory Strategy

- Use output paths outside git-tracked source or under a clearly ignored run directory.
- Preserve:
  - configs
  - logs
  - `train_results.json`
  - `trainer_state.json`
  - checkpoint metadata
- Do not delete failed-run artifacts without approval.

### Long Job Management

- Use `tmux`, `screen`, or a job scheduler if available.
- Keep command transcripts.
- Make runs reproducible from:
  - git commit
  - config path
  - environment versions
  - cache path
  - random seed

### What Should Not Be Stored in Git

- Model weights
- Dataset caches
- Checkpoints
- Large logs
- `.env` files
- tokens or credentials
- W&B secrets
- virtual environments
- Python runtime installs
- HF cache directories

## 10. Proposed Next Decision

Recommended immediate next decision:

- request server quotes based on recommended config

Why:

- The no-approval local work has reached diminishing returns.
- Stage 5 execution is not yet authorized, and the project still needs human decisions about budget and hardware.
- Requesting quotes does not start training, download data/models, or consume cloud compute.
- Quotes can compare the minimum serious configuration against the recommended efficient configuration:
  - 4x A100/A800 40GB for one serious run
  - 4x A100/A800 80GB or 4x H100 80GB for efficient static + dynamic comparison

This decision should precede any server smoke execution approval.

## 11. Questions for ChatGPT / Project Supervisor

1. What is the maximum budget for server smoke?
2. What is the maximum budget for one full static run?
3. What is the maximum budget for one full dynamic run?
4. Should the primary model remain Gemma-2-9B-it, or should Llama-3-8B-Instruct be prioritized instead?
5. Is the project aiming for minimum viable completion or best chance of publishable benchmark improvement?
6. Should W&B be used, or should logging be file/offline only?
7. What wall-clock limit is acceptable for server smoke?
8. What wall-clock limit is acceptable for a full run?
9. Should server smoke include both static and dynamic paths before full static training?
10. Should LoRA/QLoRA be considered as a cost-reduction fallback, even though current configs are full fine-tuning style?
11. Are model/dataset Hugging Face access approvals already available?
12. Is the preferred server class A100/A800 40GB, A100/A800 80GB, H100 80GB, or another available option?
13. How many checkpoints should be retained during full training?
14. What is the acceptable stop threshold for dynamic memory overhead relative to static?
15. Should final evaluation include both AlpacaEval 2 and Arena-Hard, or should one be prioritized first?

