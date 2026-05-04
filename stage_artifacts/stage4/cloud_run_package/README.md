# Stage 4 Cloud Readiness Package

Date: 2026-05-04

This package is a local-only cloud-readiness artifact for the adaptive gamma SimPO project. It prepares a minimal candidate experiment set and run conventions, but it is not approval to start cloud usage, full training, model downloads, dataset downloads, or benchmark runs.

## Scope

Primary candidate:

- Base model: `google/gemma-2-9b-it`
- Dataset: `princeton-nlp/gemma2-ultrafeedback-armorm`
- Entrypoint: `scripts/run_simpo.py`
- Distributed config: `accelerate/deepspeed_zero3_4gpu.yaml`
- Strategy set:
  - static SimPO baseline
  - dynamic gamma `sim_linear`

## Files

- `manifest.json`: machine-readable package index and approval gates.
- `experiment_matrix.md`: minimal experiment matrix and promotion criteria.
- `runbook.md`: commands and operator checklist. Commands are not approved for local execution.
- `risk_register.md`: stage risks and stop conditions.
- `configs/gemma-2-9b-it-simpo-static.yaml`: static baseline candidate config.
- `configs/gemma-2-9b-it-simpo-dynamic-sim-linear.yaml`: dynamic candidate config.
- `accelerate/deepspeed_zero3_4gpu.yaml`: copied cloud candidate accelerate config.

## Execution Boundary

Do not run these configs on the local laptop. Running either training config requires explicit human approval because it involves a 9B model, large dataset access, likely model/data downloads, and substantial GPU memory.

The next safe action is human review of this package and selection of cloud hardware, credentials, budget, and approval scope.
