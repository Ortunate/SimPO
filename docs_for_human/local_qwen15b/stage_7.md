# Stage L7 Report: Approved Static and Dynamic QLoRA Tiny Smoke

## 1. Current Stage
Stage L7 - approved static and dynamic Qwen2.5-1.5B QLoRA tiny smoke

Status: PASS

Date: 2026-05-05

Branch: `local-qwen15b-qlora`

## 2. Stage Goal
在已批准的范围内，加载本地 Qwen2.5-1.5B-Instruct，使用 tiny UltraFeedback-style 数据执行 static QLoRA 与 dynamic-gamma QLoRA smoke，对比基本 loss、gamma/similarity 日志与峰值显存。

本阶段不是 full fine-tuning，不做 8B/9B 训练，不调用 DeepSeek API，不下载模型或数据，不安装依赖，不修改 WSL/CUDA/driver/global 配置。

## 3. Execution / Findings
已读取：

- `AGENTS.md`
- `docs_for_agent/local_qwen15b/local_qwen15b_line.md`
- `docs_for_agent/local_qwen15b/hardware_resource_policy.md`
- `docs_for_agent/local_qwen15b/mirror_download_policy.md`
- `docs_for_agent/local_qwen15b/api_eval_policy.md`
- `docs_for_human/local_qwen15b/stage_6.md`

关键执行命令：

```bash
sed -n '1,240p' AGENTS.md
sed -n '1,220p' docs_for_agent/local_qwen15b/local_qwen15b_line.md
sed -n '1,220p' docs_for_agent/local_qwen15b/hardware_resource_policy.md
sed -n '1,220p' docs_for_agent/local_qwen15b/mirror_download_policy.md
sed -n '1,220p' docs_for_agent/local_qwen15b/api_eval_policy.md
sed -n '1,280p' docs_for_human/local_qwen15b/stage_6.md
nvidia-smi --query-gpu=name,memory.used,memory.total --format=csv,noheader,nounits
.venv/bin/python -m py_compile scripts/run_simpo.py scripts/simpo_trainer.py stage_artifacts/local_qwen15b/stage7_run_smoke.py
timeout 10m .venv/bin/python stage_artifacts/local_qwen15b/stage7_run_smoke.py --label static --config stage_artifacts/local_qwen15b/stage5/qwen25_1p5b_static_qlora_downloaded_tiny.placeholder.yaml --out-dir stage_artifacts/local_qwen15b/stage7/static_success_candidate
timeout 10m .venv/bin/python stage_artifacts/local_qwen15b/stage7_run_smoke.py --label dynamic --config stage_artifacts/local_qwen15b/stage5/qwen25_1p5b_dynamic_qlora_downloaded_tiny.placeholder.yaml --out-dir stage_artifacts/local_qwen15b/stage7/dynamic_success_candidate
rg -n "loss|train_loss|eval_loss|gamma_beta_ratio|similarity|rewards/|logps/" stage_artifacts/local_qwen15b/stage7/*_success_candidate/*.log
cat stage_artifacts/local_qwen15b/outputs/static_qlora_downloaded_tiny/train_results.json
cat stage_artifacts/local_qwen15b/outputs/static_qlora_downloaded_tiny/eval_results.json
cat stage_artifacts/local_qwen15b/outputs/dynamic_qlora_downloaded_tiny/train_results.json
cat stage_artifacts/local_qwen15b/outputs/dynamic_qlora_downloaded_tiny/eval_results.json
git status --ignored --short stage_artifacts/local_qwen15b/outputs stage_artifacts/local_qwen15b/stage7
```

本阶段新增或修改：

- `scripts/run_simpo.py`
- `scripts/simpo_trainer.py`
- `stage_artifacts/local_qwen15b/stage7_run_smoke.py`
- `stage_artifacts/local_qwen15b/stage7/smoke_summary.md`
- `docs_for_human/local_qwen15b/stage_7.md`

为让 Qwen2.5-1.5B 路径跑通，做了 4 个最小兼容修复：

- Qwen tokenizer 没有 `bos_token` 时，不再对 `text_chosen/text_rejected` 调用 `startswith(None)`。
- Qwen tokenizer 没有 `bos_token_id` 时，不再把 `None` prepend 到 token id 序列。
- `model_init_kwargs["torch_dtype"]` 已经是 `torch.dtype` 时，不再按字符串二次解析。
- tokenization map 禁用旧缓存，避免复用前序失败尝试产生的坏 tokenized cache。

## 4. Documentation Reorganization
本阶段未做新的目录重组。L0 结构保持不变：

- agent docs: `docs_for_agent/local_qwen15b/`
- human reports: `docs_for_human/local_qwen15b/`
- artifacts: `stage_artifacts/local_qwen15b/`

Stage L7 轻量 artifact：

- `stage_artifacts/local_qwen15b/stage7/smoke_summary.md`
- `stage_artifacts/local_qwen15b/stage7/static_success_candidate/summary.json`
- `stage_artifacts/local_qwen15b/stage7/static_success_candidate/gpu_samples.jsonl`
- `stage_artifacts/local_qwen15b/stage7/dynamic_success_candidate/summary.json`
- `stage_artifacts/local_qwen15b/stage7/dynamic_success_candidate/gpu_samples.jsonl`

训练输出目录已被 gitignore：

- `stage_artifacts/local_qwen15b/outputs/static_qlora_downloaded_tiny/`
- `stage_artifacts/local_qwen15b/outputs/dynamic_qlora_downloaded_tiny/`

## 5. Reusable Assets
本阶段确认可复用：

- `scripts/run_simpo.py` 作为真实训练入口。
- `scripts/simpo_trainer.py` 的 static SimPO loss 路径。
- `scripts/simpo_trainer.py` 的 dynamic gamma hidden-state hook 与 per-sample gamma path。
- Stage L5 的本地 Qwen2.5-1.5B 模型与 tiny preference dataset。
- Stage L7 wrapper 可继续用于下一步显存采样和日志归档。

## 6. Required Human Approvals for Future Stages
后续仍需单独批准：

- 任何超过 tiny smoke 的训练步数、序列长度或 batch size 增加。
- 任何预计超过 10 分钟的命令。
- 任何可能接近或超过 16GB VRAM 的运行。
- 任何新模型/数据下载。
- 任何 DeepSeek API 调用或 AlpacaEval-style judge run。
- 删除 checkpoints、outputs、logs、caches 或模型/数据 artifacts。

## 7. Risks
### High
- static 与 dynamic successful runs 的峰值显存均超过 8GB 预警线：static 11626 MiB，dynamic 11695 MiB。虽然低于 16GB VRAM，但后续稍微增大 `max_length`、batch size 或 steps 都可能触发 OOM。
- 本阶段输出 adapter artifact，但这是 tiny smoke 产物，不能被解读为有效训练结果。

### Medium
- dynamic gamma 比 static 峰值高约 69 MiB；当前 tiny 条件下可接受，但长序列/大 batch 的增量仍需重新测量。
- `run_simpo.py` 会在 stdout 中打印样本内容；日志应继续保留本地，不应上传或公开。
- bitsandbytes 当前版本提示不支持保存 4-bit converted full model；本阶段保存的是 PEFT adapter，smoke 未因此失败。

### Low
- `evaluation_strategy` 有 deprecation warning，短期不影响当前 Transformers 4.44.2 smoke。

## 8. Recommendation
建议下一阶段 Stage L8：做更干净的对比复现实验包，而不是直接扩大训练。

推荐 L8 范围：

1. 将 Stage L7 的成功配置从 placeholder 晋级为正式 local smoke config。
2. 加入显式 `remove_unused_columns: false` 与更清晰的 output/log 命名。
3. 准备一个小型 comparison report，固定 static/dynamic 的 seed、steps、dataset slice、max_length。
4. 可选：再跑一次 static/dynamic 复现，确认峰值显存和指标稳定。

不建议立刻提高 batch size 或 max_length；当前 512 长度、batch 1 已经达到约 11.7GB 峰值。

## 9. Executive Summary
- Stage L7 PASS。
- 已完成本地 Qwen2.5-1.5B-Instruct static QLoRA tiny smoke。
- 已完成本地 Qwen2.5-1.5B-Instruct dynamic-gamma QLoRA tiny smoke。
- static: train_loss 2.4892，eval_loss 1.0009，峰值显存 11626 MiB。
- dynamic: train_loss 2.3154，eval_loss 0.8786，eval gamma_beta_ratio mean 0.1309，eval similarity mean 0.9049，峰值显存 11695 MiB。
- dynamic 比 static 峰值高约 69 MiB。
- 本阶段修复了 Qwen BOS token 兼容、dtype 兼容和 stale tokenization cache 问题。
- 未下载模型/数据，未安装依赖，未调用 DeepSeek API，未做 full fine-tuning，未训练 8B/9B，未修改系统配置，未打印 secrets。
