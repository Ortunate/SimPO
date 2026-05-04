# Stage 4 Runbook

This runbook is for human-approved cloud execution only. Do not run these commands on the local laptop.

## Preflight Checklist

- Human approval granted for cloud/server use.
- Human approval granted for 9B model training.
- Human approval granted for model and dataset downloads.
- Cloud node has enough GPUs for the selected accelerate config.
- Hugging Face access is configured for `google/gemma-2-9b-it` and `princeton-nlp/gemma2-ultrafeedback-armorm`.
- W&B logging target is chosen, or `report_to` is changed to an approved offline logging mode.
- Repository state is captured:
  - commit hash
  - dirty diff or patch file
  - copied configs
- Disk space is checked for model, dataset cache, logs, and checkpoints.
- A short approved cloud smoke is completed before a full one-epoch run.

## Environment

Use the repository dependency intent from `environment.yml` and prior local validation:

- Python 3.10
- PyTorch 2.2.2 CUDA build
- Transformers 4.44.2
- Datasets 2.18.0
- Accelerate 0.29.2
- TRL 0.9.6
- PEFT 0.7.1

Do not change CUDA, PyTorch, Transformers, TRL, DeepSpeed, or Accelerate versions without recording the reason and approval.

## Commands

These commands are examples for an approved cloud node:

```bash
export ACCELERATE_LOG_LEVEL=info
export WANDB_PROJECT=simpo-adaptive-gamma
export HF_HOME=/path/to/persistent/hf-cache

accelerate launch \
  --config_file stage_artifacts/stage4/cloud_run_package/accelerate/deepspeed_zero3_4gpu.yaml \
  scripts/run_simpo.py \
  stage_artifacts/stage4/cloud_run_package/configs/gemma-2-9b-it-simpo-static.yaml

accelerate launch \
  --config_file stage_artifacts/stage4/cloud_run_package/accelerate/deepspeed_zero3_4gpu.yaml \
  scripts/run_simpo.py \
  stage_artifacts/stage4/cloud_run_package/configs/gemma-2-9b-it-simpo-dynamic-sim-linear.yaml
```

## Recommended Execution Order

1. Run static baseline first.
2. Confirm dataset formatting, loss, grad norm, memory, and checkpoint behavior.
3. Run dynamic `sim_linear` only if the static run is healthy.
4. Compare dynamic memory and stability against static before considering evaluation.

## Expected Outputs

Each approved run should produce:

- `train_results.json`
- `trainer_state.json`
- `all_results.json` if available
- final model under `output_dir`
- model config under `output_dir`
- W&B or offline logs
- checkpoint artifacts according to `save_steps` and `save_total_limit`
- stage-level experiment log using `docs_for_agent/experiment_log_template.md`

## Post-Run Review

After each run:

- persist an experiment log under `docs_for_agent/experiment_logs/`
- update the human-facing stage report
- summarize OOM/NaN/loss/grad/gamma/memory behavior
- do not start benchmark evaluation until training stability and outputs are reviewed
