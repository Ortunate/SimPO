# Stage 4 Risk Register

## High

- Real 9B memory overhead remains unproven. Tiny GPU memory smoke showed 0.0 MB delta at tiny scale, but this does not guarantee full-model behavior.
- Distributed wrapper compatibility is not yet proven for the LM-head hidden-state hook used by dynamic gamma.
- Large model and dataset downloads require credentials, bandwidth, disk space, and explicit approval.
- Full training and benchmark evaluation are outside local-safe scope and must not start without human approval.

## Medium

- The primary candidate uses `google/gemma-2-9b-it`, which may require access acceptance and a compatible tokenizer/chat template path.
- The dataset is already preference-labeled, but schema or chat-template behavior must be checked on cloud before committing to a full run.
- W&B logging may require credentials or an offline fallback.
- Checkpoint frequency balances reproducibility and storage pressure; current configs use periodic step checkpointing and a small retention limit.

## Low

- The cloud package lives under `stage_artifacts/`, so it is easy to revise without changing the original repository configs.
- The static path keeps dynamic gamma explicitly disabled.
- Dynamic gamma is default-disabled in `SimPOConfig`, preserving the original behavior unless config enables it.

## Risk Controls

- Run static baseline before dynamic.
- Use a short, approved cloud smoke before full one-epoch training.
- Keep the experiment matrix to two primary runs.
- Record exact configs, logs, memory, and checkpoint paths.
- Stop on OOM, NaN/Inf, severe divergence, or hook failure.
