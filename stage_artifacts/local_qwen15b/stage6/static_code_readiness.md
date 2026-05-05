# Stage L6 Static Code Readiness

Date: 2026-05-05

## Scope
This artifact records static readiness only. No real Qwen2.5-1.5B model loading, tokenizer loading, GPU training, dataset download, dependency change, or DeepSeek API call was performed.

## Entrypoint
- Training entrypoint: `scripts/run_simpo.py`
- Argument parser: `H4ArgumentParser((ModelArguments, DataArguments, SimPOConfig))`
- Dataset load path: `alignment.data.get_datasets()`
- Tokenizer load path: `alignment.model_utils.get_tokenizer()`
- Model load path: `SimPOTrainer(model=<model path>, model_init_kwargs=...)`

Important gate: `scripts/run_simpo.py` calls `get_tokenizer()` before trainer construction, so even a nominal dry run of `scripts/run_simpo.py` loads tokenizer files and should remain behind the next approval boundary if treated as model-adjacent.

## QLoRA Readiness
- Quantization config is created by `alignment.model_utils.get_quantization_config()`.
- `load_in_4bit: true` maps to `BitsAndBytesConfig(load_in_4bit=True)`.
- Local smoke configs use `nf4`, nested quantization, and `paged_adamw_8bit`.
- PEFT config is created by `alignment.model_utils.get_peft_config()`.

Static safetensors key inspection confirmed the planned LoRA target names exist in the downloaded Qwen2.5-1.5B checkpoint:

- `q_proj`
- `k_proj`
- `v_proj`
- `o_proj`
- `gate_proj`
- `up_proj`
- `down_proj`

## Dynamic Gamma Readiness
- Config fields exist in `scripts/simpo_config.py` and default to disabled.
- Static baseline path leaves `dynamic_gamma_enabled: false`.
- Dynamic path enables `dynamic_gamma_enabled: true` with `dynamic_gamma_strategy: sim_linear`.
- The implementation reuses the existing concatenated forward pass.
- The dynamic path captures LM head input hidden states with a forward pre-hook, computes chosen/rejected response embedding cosine similarity, converts it into a per-sample `gamma_beta_ratio`, and passes that into `simpo_loss()`.
- Metrics already include gamma and similarity summaries when dynamic gamma is enabled.

## Dataset Readiness
- Local tiny dataset path: `stage_artifacts/local_qwen15b/data/trl_ultrafeedback_binarized_tiny`
- Splits: `train`, `test`
- Expected columns before formatting: `prompt`, `chosen`, `rejected`, `score_chosen`, `score_rejected`
- `run_simpo.py` keeps `prompt`, `chosen`, and `rejected`, applies the model chat template, then renames formatted columns for `SimPOTrainer`.

## Cache Requirement
Default `/home/ubuntu0/.cache/huggingface` is not writable in this environment. Future approved execution should set:

```bash
HF_HOME=stage_artifacts/local_qwen15b/hf-cache
HF_HUB_CACHE=stage_artifacts/local_qwen15b/hf-cache/hub
HF_DATASETS_CACHE=stage_artifacts/local_qwen15b/hf-cache/datasets
```

For dataset download/use through the mirror, keep:

```bash
HF_ENDPOINT=https://hf-mirror.com
HF_HUB_DISABLE_XET=1
```

## Stage L7 Gate
Before running either local smoke config, request explicit approval for:

- tokenizer loading from the local Qwen2.5-1.5B path
- real Qwen2.5-1.5B 4-bit model loading
- GPU training smoke run
- expected VRAM measurement

