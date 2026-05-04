# Dynamic Gamma Focused Code Review

Date: 2026-05-04

## Scope

Review target:

- `scripts/simpo_config.py`
- `scripts/simpo_trainer.py`

Review purpose:

- Confirm local-first readiness items from `docs_for_human/local_vs_server_boundary_review.md`.
- Focus on static-path safety, dynamic gamma math, hidden-state capture, logging, and rollback behavior.

## Findings

No blocking issue was found in the reviewed local scope.

### Static Path

- `dynamic_gamma_enabled` defaults to `False`.
- When disabled, `concatenated_forward` uses `nullcontext()` and does not register the LM-head hook.
- `simpo_loss` still uses scalar `self.gamma_beta_ratio` when no per-sample tensor is provided.
- Unit check evidence: scalar static gamma and full per-sample gamma tensor produce identical losses/rewards.

### Dynamic Gamma Math

- Similarity is cosine similarity between mean-pooled chosen/rejected response embeddings.
- Similarity is normalized from `[-1, 1]` to `[0, 1]`.
- Higher similarity reduces the effective gamma/beta ratio under `sim_linear`.
- Min/max clamps are applied after the linear adjustment.
- Unit check evidence: clamp behavior is deterministic for similarity `1.0` and `-1.0`.

### Response Masking

- Pooling mask is `labels != label_pad_token_id`.
- This matches the existing trainer convention that response labels are unmasked and prompt/pad labels are `label_pad_token_id`.
- Unit check evidence: large masked hidden-state values do not affect the pooled response similarity.

### Hidden-State Capture

- The hook is registered only for the dynamic path.
- The hook is registered as a temporary forward pre-hook on `model.get_output_embeddings()`.
- Captured hidden states are detached immediately.
- The hook handle is removed in a `finally` block.
- Unit check evidence: capture occurs, captured tensor is detached, and the hook no longer fires after context exit.

### Logging Contract

- Static metrics do not include dynamic gamma or similarity keys.
- Dynamic metrics include:
  - `gamma_beta_ratio/mean`
  - `gamma_beta_ratio/min`
  - `gamma_beta_ratio/max`
  - `similarity/mean`
  - `similarity/min`
  - `similarity/max`
- Unit check evidence: static/dynamic metric-key contract passes using dummy tensors.

## Remaining Non-Blocking Risks

### High

- Real 8B/9B memory behavior remains unvalidated.
- Distributed wrapper behavior under DeepSpeed/FSDP/PEFT remains unvalidated.

### Medium

- The hidden-state hook assumes the wrapped model exposes a usable `get_output_embeddings()` module and that the LM-head pre-hook sees the final hidden states.
- The current implementation validates only `sim_linear`.

### Low

- The dynamic implementation is intentionally non-differentiable with respect to the similarity signal because captured hidden states are detached.

## Rollback

Rollback without code changes:

- Set `dynamic_gamma_enabled: false` in config.
- Use the static Stage 4 baseline config:
  - `stage_artifacts/stage4/cloud_run_package/configs/gemma-2-9b-it-simpo-static.yaml`

Rollback with code revert:

- Revert the Stage 2 edits in:
  - `scripts/simpo_config.py`
  - `scripts/simpo_trainer.py`

Do not delete reports, logs, checkpoints, datasets, or stage artifacts without explicit human approval.
