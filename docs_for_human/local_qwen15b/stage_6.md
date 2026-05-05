# Stage L6 Report: Static Code Readiness and Run-Gate Audit

## 1. Current Stage
Stage L6 - static code readiness and run-gate audit

Status: PASS

Date: 2026-05-05

Branch: `local-qwen15b-qlora`

## 2. Stage Goal
在已完成模型/数据下载的基础上，静态确认本地 Qwen2.5-1.5B QLoRA fallback 线的训练入口、数据路径、QLoRA 配置、dynamic gamma 复用点和下一阶段执行闸门。

本阶段只做低风险静态审计和轻量文件准备，不加载真实 Qwen 模型，不加载 tokenizer，不训练，不下载，不调用 DeepSeek API。

## 3. Execution / Findings
已读取：

- `AGENTS.md`
- `docs_for_agent/local_qwen15b/local_qwen15b_line.md`
- `docs_for_agent/local_qwen15b/hardware_resource_policy.md`
- `docs_for_agent/local_qwen15b/mirror_download_policy.md`
- `docs_for_agent/local_qwen15b/api_eval_policy.md`
- `docs_for_human/local_qwen15b/stage_5.md`

执行过的关键命令：

```bash
pwd && git branch --show-current && git status --short
sed -n '1,260p' AGENTS.md
find docs_for_agent/local_qwen15b -maxdepth 1 -type f -print | sort
ls -1 docs_for_human/local_qwen15b | sort
sed -n '1,260p' docs_for_agent/local_qwen15b/local_qwen15b_line.md
sed -n '1,260p' docs_for_agent/local_qwen15b/hardware_resource_policy.md
sed -n '1,260p' docs_for_agent/local_qwen15b/mirror_download_policy.md
sed -n '1,260p' docs_for_agent/local_qwen15b/api_eval_policy.md
sed -n '1,320p' docs_for_human/local_qwen15b/stage_5.md
rg -n "dynamic_gamma|gamma|SimPO|simpo_loss|loss_type|DPOTrainer|SFTTrainer" scripts README.md training_configs
rg --files | rg '(^scripts/|training_configs|config|yaml|yml|README|requirements|pyproject|setup)'
find stage_artifacts/local_qwen15b -maxdepth 3 -type f -print | sort
sed -n '1,340p' scripts/run_simpo.py
sed -n '1,120p' scripts/simpo_config.py
sed -n '240,840p' scripts/simpo_trainer.py
sed -n '1,220p' alignment/model_utils.py
sed -n '140,290p' alignment/data.py
.venv/bin/python -c "<parse Stage L5 static/dynamic YAML with H4ArgumentParser>"
nl -ba scripts/run_simpo.py | sed -n '120,285p'
nl -ba scripts/simpo_config.py | sed -n '60,78p'
nl -ba scripts/simpo_trainer.py | sed -n '575,870p'
nl -ba alignment/model_utils.py | sed -n '35,115p'
nl -ba alignment/data.py | sed -n '180,260p'
mkdir -p stage_artifacts/local_qwen15b/stage6
.venv/bin/python -c "<inspect safetensors keys without loading tensors>"
.venv/bin/python -c "<inspect tokenizer_config.json metadata without AutoTokenizer load>"
```

主要发现：

- 真实训练入口仍是 `scripts/run_simpo.py`。
- `scripts/run_simpo.py` 会先读取 dataset，再调用 `get_tokenizer()`，之后才构造 `SimPOTrainer` 并进入 `trainer.train()`。
- 现有 Stage L5 静态/动态 YAML 可被 `H4ArgumentParser` 正常解析。
- QLoRA 4-bit 配置由 `alignment/model_utils.py` 中的 `get_quantization_config()` 接入。
- PEFT LoRA 配置由 `get_peft_config()` 接入。
- safetensors key 静态检查确认 Qwen2.5-1.5B checkpoint 中存在计划使用的 LoRA target modules：`q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`。
- `tokenizer_config.json` 静态元数据存在 chat template，`tokenizer_class` 为 `Qwen2Tokenizer`，`pad_token` 为 `<|endoftext|>`，`eos_token` 为 `<|im_end|>`。

## 4. Documentation Reorganization
本阶段未继续重组文档目录。L0 已完成的组织结构仍然存在：

- agent docs: `docs_for_agent/local_qwen15b/`
- human reports: `docs_for_human/local_qwen15b/`
- previous local phase archives: `docs_for_agent/archive_previous_local_phase/`, `docs_for_human/archive_previous_local_phase/`
- local artifacts: `stage_artifacts/local_qwen15b/`

本阶段新增轻量 artifacts：

- `stage_artifacts/local_qwen15b/stage6/static_code_readiness.md`
- `stage_artifacts/local_qwen15b/stage6/next_stage_approval_packet.md`

## 5. Reusable Assets
可复用实现：

- `scripts/run_simpo.py`: 当前训练入口。
- `scripts/simpo_config.py`: 已有 `dynamic_gamma_enabled`、`dynamic_gamma_strategy`、`dynamic_gamma_similarity_scale`、`dynamic_gamma_min`、`dynamic_gamma_max`。
- `scripts/simpo_trainer.py`: 已有 SimPO loss、dynamic gamma hidden-state hook、gamma/similarity metrics。
- `alignment/model_utils.py`: 已有 QLoRA quantization 和 PEFT LoRA config 接入点。
- `alignment/data.py`: 可读取本地 tiny dataset script 并进入现有 prompt/chosen/rejected 处理流。
- `stage_artifacts/local_qwen15b/stage5/*.placeholder.yaml`: 可作为下一阶段 smoke run 的候选配置，但仍需显式批准后执行。

## 6. Required Human Approvals for Future Stages
Stage L7 如要执行静态 smoke，需要显式批准：

- 加载本地 Qwen2.5-1.5B tokenizer。
- 以 4-bit QLoRA 方式加载真实 Qwen2.5-1.5B 模型。
- 运行 GPU 训练 smoke。
- 记录 GPU 峰值显存。
- 如果命令预计超过 10 分钟或超过 8GB VRAM，需要再次停下确认。

dynamic gamma smoke 应在静态 smoke PASS 后另行批准。

DeepSeek API 调用仍需单独明确批准。本阶段没有 API 调用，也没有读取或打印 `.env` 值。

## 7. Risks
### High
- 下一阶段首次真实模型加载和 4-bit CUDA/bitsandbytes 路径仍未验证，存在环境或显存失败风险。
- dynamic gamma 会额外捕获 LM head 输入 hidden states，可能增加显存峰值；必须先跑静态 baseline。

### Medium
- `scripts/run_simpo.py` 在训练前会打印随机样本内容，未来日志可能包含数据样本，需要只写入本地 artifacts，不上传。
- 默认 Hugging Face cache 目录不可写；未来执行必须显式设置 `HF_HOME`、`HF_HUB_CACHE`、`HF_DATASETS_CACHE`。
- `evaluation_strategy` 在当前 Transformers 版本中已发出 deprecation warning，短期不阻塞 smoke，但后续可改为 `eval_strategy`。

### Low
- 当前 tiny dataset 仅用于 fallback smoke/debug，不支持任何 benchmark 或大模型行为证明。

## 8. Recommendation
建议下一阶段设为 Stage L7：只运行静态 Qwen2.5-1.5B QLoRA tiny smoke。

执行顺序建议：

1. 人类明确批准 tokenizer/model loading 与 GPU training smoke。
2. 使用 Stage L5 静态 placeholder YAML，保持 `max_steps: 5`、batch size 1、`max_length: 512`。
3. 先跑静态路径并记录显存、loss、NaN/Inf、输出目录。
4. 静态 PASS 后再申请 Stage L8 dynamic gamma tiny smoke。

不建议下一步直接运行 dynamic gamma，因为静态 QLoRA 路径尚未在真实 Qwen 模型上验证。

## 9. Executive Summary
- Stage L6 PASS。
- 本阶段完成静态代码路径和执行闸门审计。
- 训练入口、QLoRA 接入、SimPO loss、dynamic gamma 实现和日志指标都已定位。
- Stage L5 的静态/动态 placeholder YAML 能被现有 parser 解析。
- Qwen2.5-1.5B safetensors metadata 静态检查确认 LoRA target modules 存在。
- 本阶段新增了 Stage L6 readiness artifact 和 Stage L7 approval packet。
- 未加载模型，未加载 tokenizer，未训练，未下载，未安装依赖，未调用 API，未打印 secrets，未运行 GPU-heavy 动作。
