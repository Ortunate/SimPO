# Stage 4: Cloud Readiness

Date: 2026-05-04

## 1. Current Stage

Name: Stage 4 - Cloud Readiness

Status: PASS for local-only cloud-readiness preparation

Decision from previous stage:

- Reviewed latest human-facing report: `docs_for_human/stage_3.md`
- Stage 3 recovery update records `PASS after local-safe recovery`
- Decision: proceed to Stage 4, limited to local preparation only

## 2. Stage Goal

Primary goal:

Prepare a minimal, reviewable cloud-run package for the adaptive gamma SimPO experiment, including reproducible configs, experiment matrix, runbook, checkpoint/logging conventions, risk register, and approval gates.

Non-goals:

- Do not start cloud usage.
- Do not start full training.
- Do not run Llama-3-8B, Gemma-2-9B, or similarly sized model training locally.
- Do not download large models or datasets.
- Do not run AlpacaEval 2, Arena-Hard, or other benchmark jobs.
- Do not install or upgrade dependencies.

## 3. Plan

Planned steps:

1. Re-read standing project instructions and latest Stage 3 report.
2. Inspect existing repository training configs and accelerate configs.
3. Choose the smallest viable cloud candidate matrix.
4. Prepare local-only cloud-readiness package under `stage_artifacts/stage4/`.
5. Static-validate JSON/YAML and parser compatibility.
6. Persist the Stage 4 human-facing report before any further progression.

Expected evidence:

- Cloud-readiness package files exist.
- Static and dynamic candidate configs are explicit and parseable.
- Dynamic config enables only the validated `sim_linear` strategy.
- Runbook includes approval gates and expected artifacts.
- No training or resource-heavy action is executed.

## 4. Execution / Findings

Key actions performed:

- Reviewed:
  - `AGENTS.md`
  - `docs_for_agent/project_brief.md`
  - `docs_for_agent/stage_report_template.md`
  - `docs_for_agent/experiment_log_template.md`
  - `docs_for_human/stage_3.md`
- Inspected existing repository files:
  - `scripts/run_simpo.py`
  - `scripts/simpo_config.py`
  - `training_configs/gemma-2-9b-it-simpo.yaml`
  - `training_configs/llama-3-8b-instruct-simpo.yaml`
  - `training_configs/llama-3-8b-instruct-simpo-v2.yaml`
  - `accelerate_configs/deepspeed_zero3.yaml`
  - `accelerate_configs/fsdp.yaml`
  - `accelerate_configs/multi_gpu.yaml`
  - `README.md`
  - `environment.yml`
- Prepared the Stage 4 package:
  - `stage_artifacts/stage4/cloud_run_package/`

Files changed:

- Added `stage_artifacts/stage4/cloud_run_package/README.md`
- Added `stage_artifacts/stage4/cloud_run_package/manifest.json`
- Added `stage_artifacts/stage4/cloud_run_package/experiment_matrix.md`
- Added `stage_artifacts/stage4/cloud_run_package/runbook.md`
- Added `stage_artifacts/stage4/cloud_run_package/risk_register.md`
- Added `stage_artifacts/stage4/cloud_run_package/accelerate/deepspeed_zero3_4gpu.yaml`
- Added `stage_artifacts/stage4/cloud_run_package/configs/gemma-2-9b-it-simpo-static.yaml`
- Added `stage_artifacts/stage4/cloud_run_package/configs/gemma-2-9b-it-simpo-dynamic-sim-linear.yaml`
- Added `docs_for_human/stage_4.md`

Primary candidate matrix:

| Run ID | Type | Model | Dataset | Gamma Mode |
|---|---|---|---|---|
| `stage4-gemma-2-9b-it-simpo-static` | baseline | `google/gemma-2-9b-it` | `princeton-nlp/gemma2-ultrafeedback-armorm` | static |
| `stage4-gemma-2-9b-it-simpo-dynamic-sim-linear` | dynamic | `google/gemma-2-9b-it` | `princeton-nlp/gemma2-ultrafeedback-armorm` | `sim_linear` |

Why Gemma primary:

- The repository already has a Gemma SimPO config.
- The project brief lists Gemma-2-9B as a candidate base model.
- The repository README reports Gemma as less prone to forgetting in the existing SimPO experiments.
- The existing Gemma config uses `attn_implementation: eager`, avoiding an immediate Flash Attention dependency gate in the candidate config.

Deferred candidates:

- Llama-3-8B-Instruct static/dynamic is deferred because it expands the primary matrix and may require gated access plus Flash Attention readiness.
- Curriculum and combined strategies are deferred because only `sim_linear` has been implemented and locally validated.

Commands run:

    rg --files -g '*.yaml' -g '*.yml' -g '*.json' -g '*.sh' -g '*.md' | sort | sed -n '1,220p'
    find . -maxdepth 3 -type d | sort | sed -n '1,180p'
    sed -n '1,260p' scripts/run_simpo.py
    sed -n '1,180p' scripts/simpo_config.py
    find training_configs -maxdepth 3 -type f | sort
    find scripts -maxdepth 2 -type f | sort
    sed -n '260,520p' scripts/run_simpo.py
    sed -n '1,220p' environment.yml
    sed -n '1,260p' training_configs/llama-3-8b-instruct-simpo-v2.yaml
    sed -n '1,220p' accelerate_configs/multi_gpu.yaml
    git diff -- scripts/simpo_config.py scripts/simpo_trainer.py | sed -n '1,260p'
    git rev-parse --abbrev-ref HEAD
    git rev-parse --short HEAD
    .venv/bin/python -m json.tool stage_artifacts/stage4/cloud_run_package/manifest.json
    .venv/bin/python -c 'import yaml, pathlib; paths=list(pathlib.Path("stage_artifacts/stage4/cloud_run_package").rglob("*.yaml")); [yaml.safe_load(path.read_text()) for path in paths]; print("yaml_ok", len(paths), "files")'
    find stage_artifacts/stage4/cloud_run_package -type f | sort
    rg -n "dynamic_gamma|model_name_or_path|dataset_mixer|save_steps|output_dir|run_name" stage_artifacts/stage4/cloud_run_package/configs
    rg -n "Do not run|approval|9B|download|full training|Stage 4" stage_artifacts/stage4/cloud_run_package
    PYTHONPATH=scripts:. .venv/bin/python -c 'from alignment import H4ArgumentParser, ModelArguments, DataArguments; from simpo_config import SimPOConfig; import pathlib; parser=H4ArgumentParser((ModelArguments, DataArguments, SimPOConfig)); paths=["stage_artifacts/stage4/cloud_run_package/configs/gemma-2-9b-it-simpo-static.yaml", "stage_artifacts/stage4/cloud_run_package/configs/gemma-2-9b-it-simpo-dynamic-sim-linear.yaml"]; [parser.parse_yaml_file(yaml_file=str(pathlib.Path(p).resolve())) for p in paths]; print("h4_parse_ok", len(paths), "configs")'
    .venv/bin/python -c 'import json, pathlib; root=pathlib.Path("."); m=json.loads(pathlib.Path("stage_artifacts/stage4/cloud_run_package/manifest.json").read_text()); refs=[m["accelerate_config"]]+[r["config"] for r in m["runs"]]; missing=[p for p in refs if not (root/p).exists()]; print("manifest_refs_ok", not missing, "refs", len(refs)); print("missing", missing)'

Validation findings:

- `manifest.json` parses successfully.
- 3 YAML files parse successfully.
- Both Gemma candidate configs parse through `H4ArgumentParser`.
- Manifest references resolve to existing files.
- Runbook and manifest explicitly require human approval before cloud use, downloads, or 9B training.

Non-blocking warnings:

- `H4ArgumentParser` static parse printed a Hugging Face cache warning for `/home/ubuntu0/.cache/huggingface/hub`; the runbook sets `HF_HOME` for approved cloud execution.
- Transformers warns that `evaluation_strategy` is deprecated in favor of `eval_strategy`; this mirrors existing repo configs and was not changed to avoid unrelated churn.
- The sandboxed Python context again warned that NVML could not initialize; Stage 3 already diagnosed this as sandbox device visibility, not a global CUDA failure.

Experiment logs:

- No new experiment log was created in Stage 4 because no training, smoke run, benchmark, or model execution was performed. Only static config/package validation was run.

## 5. Acceptance Check

| Criterion | Status | Evidence |
|---|---:|---|
| Latest report reviewed | PASS | `docs_for_human/stage_3.md` reviewed; recovery update says Stage 3 PASS |
| Stage 4 selected correctly | PASS | Stage 3 passed; Stage 4 limited to local preparation |
| Cloud package prepared | PASS | `stage_artifacts/stage4/cloud_run_package/` |
| Minimal experiment matrix defined | PASS | `experiment_matrix.md` contains static + dynamic Gemma only |
| Static baseline config prepared | PASS | `configs/gemma-2-9b-it-simpo-static.yaml` |
| Dynamic config prepared | PASS | `configs/gemma-2-9b-it-simpo-dynamic-sim-linear.yaml` |
| Dynamic strategy matches validated implementation | PASS | `dynamic_gamma_strategy: sim_linear` |
| JSON/YAML static validation | PASS | `json.tool` OK; `yaml_ok 3 files` |
| Parser compatibility | PASS | `h4_parse_ok 2 configs` |
| Approval gates documented | PASS | `manifest.json`, `README.md`, `runbook.md`, `risk_register.md` |
| No resource-heavy action | PASS | no training, no download, no install, no cloud use |
| Exact dollar cost known | PARTIAL | cloud provider/server not selected; package defines run count and resource class but not dollar cost |

Overall stage result:

- PASS for local-only cloud-readiness preparation

## 6. Risks

### High

- Real 9B memory overhead remains unknown. Stage 3 tiny GPU delta was 0.0 MB, but that does not prove full-model overhead.
- Cloud/full training requires explicit human approval, model/data download approval, credentials, budget, and server choice.
- PEFT/FSDP/DeepSpeed wrapper compatibility for the LM-head hidden-state hook remains unproven at real scale.

### Medium

- Exact dollar cost and wall-clock runtime are unknown until a provider/server is selected and a short approved cloud smoke is run.
- The primary dataset and model may require Hugging Face access acceptance and cache planning.
- W&B logging may require credentials or an offline logging decision.
- `evaluation_strategy` deprecation warning should eventually be addressed, but changing it now would create unnecessary config drift from existing repository style.

### Low

- Stage 4 artifacts are under `stage_artifacts/`, so they are easy to revise or discard.
- Static config explicitly disables dynamic gamma.
- Dynamic config keeps the validated clamp range `[0.0, 0.5]`.

## 7. Recommendation

Recommended decision:

- Hold before Stage 5.
- Escalate to human supervisor for explicit cloud/training decisions.

Specific human decisions required before any Stage 5 execution:

1. Approve or reject the Stage 4 package as the cloud candidate.
2. Select cloud/server target and GPU count.
3. Set budget or wall-clock limit.
4. Approve model and dataset downloads.
5. Confirm Hugging Face access and cache path.
6. Confirm W&B project/entity or offline logging.
7. Approve a short cloud smoke before any full one-epoch run.
8. Approve full 9B static baseline run only after the cloud smoke is healthy.
9. Approve dynamic 9B run only after static baseline is healthy.

Do not proceed to full training, benchmark evaluation, or cloud resource use without those approvals.

## 8. Executive Summary

- Stage 4 local cloud-readiness preparation is complete.
- The cloud package is under `stage_artifacts/stage4/cloud_run_package/`.
- The matrix is intentionally minimal: Gemma static baseline plus Gemma dynamic `sim_linear`.
- Configs are based on existing repository conventions and parse through the repo argument parser.
- Runbook, manifest, and risk register explicitly block unapproved cloud, downloads, and 9B training.
- No resource-heavy action was performed.
- Stage 5 is not authorized by this report.
- Next step is human review and explicit approval decisions for cloud/server, budget, downloads, credentials, smoke, and then full training.

---

## Local-First Update: 2026-05-04 - Dynamic Gamma Unit Checks and Code Review

### Stage Status

PASS for continued local preparation.

### Stage Goal

Continue Stage 4 without moving to Stage 5 by completing local-safe readiness work identified in `docs_for_human/local_vs_server_boundary_review.md`.

### Key Actions Performed

- Re-read standing project instructions:
  - `AGENTS.md`
  - `docs_for_agent/project_brief.md`
- Reviewed latest local/server boundary report:
  - `docs_for_human/local_vs_server_boundary_review.md`
- Kept the project in Stage 4.
- Did not request server/cloud approval.
- Did not run training.
- Did not download models or datasets.
- Did not load any real model or real dataset.
- Added a focused Stage 4 code review artifact:
  - `stage_artifacts/stage4/dynamic_gamma_code_review.md`
- Added a CPU/dummy unit-check artifact:
  - `stage_artifacts/stage4/local_dynamic_gamma_unit_checks.py`
- Added a corresponding experiment/check log:
  - `docs_for_agent/experiment_logs/local-dynamic-gamma-unit-checks-001.md`

### Evidence and Artifacts

Commands run:

    .venv/bin/python -m py_compile stage_artifacts/stage4/local_dynamic_gamma_unit_checks.py
    .venv/bin/python stage_artifacts/stage4/local_dynamic_gamma_unit_checks.py

Validation result:

- PASS: Python syntax compile.
- PASS: local dynamic gamma unit checks.

Unit checks passed:

- `test_static_loss_matches_full_gamma_tensor`
- `test_response_pooling_ignores_masked_tokens`
- `test_dynamic_gamma_mapping_and_clamp`
- `test_lm_head_hook_detaches_and_removes`
- `test_metric_key_contract_static_and_dynamic`

Focused review result:

- No blocking issue found in the reviewed local scope.
- Static path remains default-disabled and preserves scalar `gamma_beta_ratio` behavior.
- Dynamic gamma helper math and clamp behavior are deterministic under dummy tests.
- Response pooling ignores masked prompt/pad positions.
- LM-head hook captures detached hidden states and is removed after context exit.
- Static metrics do not include dynamic keys; dynamic metrics include expected gamma/similarity keys.

### Hardware / Resource Usage

- CPU/dummy tensor checks only.
- No GPU use.
- No full training.
- No 8B/9B model load or training.
- No real UltraFeedback access.
- No dependency install or upgrade.
- No cloud or paid resource.
- No model or dataset download.
- No command expected to exceed 10 minutes, 8GB VRAM, or 16GB system RAM.

### Acceptance Check

| Criterion | Status | Evidence |
|---|---:|---|
| Continue local-first Stage 4 rather than Stage 5 | PASS | Work stayed in Stage 4 local preparation |
| Static gamma equivalence checked | PASS | `test_static_loss_matches_full_gamma_tensor` |
| Response mask pooling checked | PASS | `test_response_pooling_ignores_masked_tokens` |
| Dynamic gamma mapping and clamp checked | PASS | `test_dynamic_gamma_mapping_and_clamp` |
| LM-head hook detach/removal checked | PASS | `test_lm_head_hook_detaches_and_removes` |
| Dynamic logging-key contract checked | PASS | `test_metric_key_contract_static_and_dynamic` |
| No resource-heavy action | PASS | CPU/dummy only |
| Human-facing report persisted | PASS | this update appended to `docs_for_human/stage_4.md` |

Overall update result:

- PASS

### Current Risks

#### High

- Real 8B/9B memory behavior remains unvalidated.
- DeepSpeed/FSDP/PEFT wrapper compatibility remains unvalidated.
- Real dataset behavior remains unvalidated.

#### Medium

- The LM-head hook still assumes the wrapped model exposes `get_output_embeddings()` in a way compatible with forward pre-hooks.
- The only implemented dynamic strategy remains `sim_linear`.

#### Low

- The unit-check run printed a non-blocking Hugging Face cache warning during imports.

### Recommendation

Recommended decision:

- Continue local preparation.

Narrow next local actions:

1. Review whether the Stage 4 cloud package should include explicit smoke-log templates.
2. Consider a tiny CPU entrypoint regression check only if needed; this has already been covered by earlier stages.
3. Do not request server/cloud approval until the human supervisor explicitly wants to move past local preparation.

### Executive Summary

- Stage 4 remains active as local preparation.
- A focused dynamic gamma code review artifact was added.
- A CPU/dummy unit-check script was added and passed.
- The checks cover static equivalence, response masking, dynamic gamma clamp behavior, LM-head hook safety, and metric-key contracts.
- No resource-heavy action was performed.
- Stage 5 remains unauthorized.
- The immediate next action remains continued local preparation or human review, not server execution.
