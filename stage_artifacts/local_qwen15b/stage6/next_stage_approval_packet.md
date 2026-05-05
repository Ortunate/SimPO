# Stage L7 Approval Packet Draft

## Recommended Next Stage
Stage L7: approved static Qwen2.5-1.5B QLoRA smoke run.

## Why Static First
The static run validates the existing QLoRA/data/tokenization/model path before dynamic gamma adds the hidden-state capture hook and per-sample gamma computation. Dynamic gamma should run only after the static path finishes without load, tokenization, loss, optimizer, or save-path errors.

## Proposed Static Smoke Config
Use:

```text
stage_artifacts/local_qwen15b/stage5/qwen25_1p5b_static_qlora_downloaded_tiny.placeholder.yaml
```

Key limits:

- `max_steps: 5`
- `per_device_train_batch_size: 1`
- `per_device_eval_batch_size: 1`
- `gradient_accumulation_steps: 1`
- `max_length: 512`
- `max_prompt_length: 384`
- `load_in_4bit: true`
- `save_strategy: "no"`
- `report_to: []`

## Proposed Command
Do not run without explicit approval:

```bash
HF_HOME=stage_artifacts/local_qwen15b/hf-cache \
HF_HUB_CACHE=stage_artifacts/local_qwen15b/hf-cache/hub \
HF_DATASETS_CACHE=stage_artifacts/local_qwen15b/hf-cache/datasets \
HF_ENDPOINT=https://hf-mirror.com \
HF_HUB_DISABLE_XET=1 \
.venv/bin/python scripts/run_simpo.py stage_artifacts/local_qwen15b/stage5/qwen25_1p5b_static_qlora_downloaded_tiny.placeholder.yaml
```

## Metrics To Capture
- command start/end time
- `nvidia-smi` before and after
- peak allocated/reserved VRAM if logged or added by a lightweight wrapper
- train loss
- eval loss if eval runs
- NaN/Inf presence
- output directory contents
- whether the run saved only allowed small adapter/config/log artifacts

## Stop Conditions
Stop immediately if:

- expected VRAM rises above 8GB before explicit continuation approval
- model loading fails with CUDA/quantization/bitsandbytes errors
- dataset formatting fails
- loss becomes NaN/Inf
- output path begins producing large checkpoint artifacts unexpectedly
- any command appears likely to exceed 10 minutes

