# Stage L8 Report: Formal Smoke Configs and Reproducibility Check

## 1. Current Stage
Stage L8 - formal local smoke configs and reproducibility check

Status: PASS

Date: 2026-05-05

Branch: `local-qwen15b-qlora`

## 2. Stage Goal
把 Stage L7 已跑通的 static/dynamic tiny smoke 固化为正式 local Qwen2.5-1.5B QLoRA fallback 配置，并复跑一次验证可复现性。

本阶段仍限定为 tiny 数据、5 steps、batch size 1、`max_length: 512`。未扩大训练规模，未下载，未安装依赖，未调用 DeepSeek API，未修改系统配置。

## 3. Execution / Findings
已读取：

- `AGENTS.md`
- `docs_for_agent/local_qwen15b/local_qwen15b_line.md`
- `docs_for_agent/local_qwen15b/hardware_resource_policy.md`
- `docs_for_agent/local_qwen15b/mirror_download_policy.md`
- `docs_for_agent/local_qwen15b/api_eval_policy.md`
- `docs_for_human/local_qwen15b/stage_7.md`

关键命令：

```bash
sed -n '1,240p' AGENTS.md
sed -n '1,220p' docs_for_agent/local_qwen15b/local_qwen15b_line.md
sed -n '1,220p' docs_for_agent/local_qwen15b/hardware_resource_policy.md
sed -n '1,220p' docs_for_agent/local_qwen15b/mirror_download_policy.md
sed -n '1,220p' docs_for_agent/local_qwen15b/api_eval_policy.md
sed -n '1,280p' docs_for_human/local_qwen15b/stage_7.md
.venv/bin/python -m py_compile scripts/run_simpo.py scripts/simpo_config.py scripts/simpo_trainer.py stage_artifacts/local_qwen15b/stage7_run_smoke.py
.venv/bin/python -c "<parse Stage L8 static/dynamic YAML with H4ArgumentParser>"
git check-ignore -v stage_artifacts/local_qwen15b/outputs/stage8_static_qlora_tiny_smoke stage_artifacts/local_qwen15b/outputs/stage8_dynamic_qlora_tiny_smoke
timeout 10m .venv/bin/python stage_artifacts/local_qwen15b/stage7_run_smoke.py --label static --config stage_artifacts/local_qwen15b/stage8/qwen25_1p5b_static_qlora_tiny_smoke.yaml --out-dir stage_artifacts/local_qwen15b/stage8/static_repro
timeout 10m .venv/bin/python stage_artifacts/local_qwen15b/stage7_run_smoke.py --label dynamic --config stage_artifacts/local_qwen15b/stage8/qwen25_1p5b_dynamic_qlora_tiny_smoke.yaml --out-dir stage_artifacts/local_qwen15b/stage8/dynamic_repro
cat stage_artifacts/local_qwen15b/outputs/stage8_static_qlora_tiny_smoke/train_results.json
cat stage_artifacts/local_qwen15b/outputs/stage8_static_qlora_tiny_smoke/eval_results.json
cat stage_artifacts/local_qwen15b/outputs/stage8_dynamic_qlora_tiny_smoke/train_results.json
cat stage_artifacts/local_qwen15b/outputs/stage8_dynamic_qlora_tiny_smoke/eval_results.json
rg -n "Prompt sample|Chosen sample|Rejected sample" stage_artifacts/local_qwen15b/stage8/static_repro/stdout.log stage_artifacts/local_qwen15b/stage8/dynamic_repro/stdout.log
du -sh stage_artifacts/local_qwen15b/outputs/stage8_static_qlora_tiny_smoke stage_artifacts/local_qwen15b/outputs/stage8_dynamic_qlora_tiny_smoke
git status --ignored --short stage_artifacts/local_qwen15b/outputs/stage8_static_qlora_tiny_smoke stage_artifacts/local_qwen15b/outputs/stage8_dynamic_qlora_tiny_smoke stage_artifacts/local_qwen15b/stage8
```

代码和配置变更：

- `scripts/simpo_config.py`
  - 新增 `log_train_samples: bool = True`。
- `scripts/run_simpo.py`
  - 只有 `training_args.log_train_samples` 为 true 时才打印随机训练样本。
- 新增正式 static 配置：
  - `stage_artifacts/local_qwen15b/stage8/qwen25_1p5b_static_qlora_tiny_smoke.yaml`
- 新增正式 dynamic 配置：
  - `stage_artifacts/local_qwen15b/stage8/qwen25_1p5b_dynamic_qlora_tiny_smoke.yaml`

复现结果：

| Variant | Status | Peak VRAM | Train loss | Eval loss |
|---|---:|---:|---:|---:|
| Static QLoRA | PASS | 11620 MiB | 2.4892 | 1.0009 |
| Dynamic gamma QLoRA | PASS | 11693 MiB | 2.3154 | 0.8786 |

Dynamic metrics:

- eval `gamma_beta_ratio/mean`: 0.1309451162815094
- eval `gamma_beta_ratio/min`: 0.1309451162815094
- eval `gamma_beta_ratio/max`: 0.1309451162815094
- eval `similarity/mean`: 0.9048781991004944
- eval `similarity/min`: 0.9048781991004944
- eval `similarity/max`: 0.9048781991004944

Stage L7 vs L8 peak memory:

| Variant | L7 Peak | L8 Peak | Delta |
|---|---:|---:|---:|
| Static QLoRA | 11626 MiB | 11620 MiB | -6 MiB |
| Dynamic QLoRA | 11695 MiB | 11693 MiB | -2 MiB |

Log hygiene:

- `log_train_samples: false` 生效。
- Stage L8 stdout 中未再出现 `Prompt sample`、`Chosen sample`、`Rejected sample`。

## 4. Documentation Reorganization
本阶段未做新的目录重组。新增 Stage L8 文档和 artifacts：

- `docs_for_human/local_qwen15b/stage_8.md`
- `stage_artifacts/local_qwen15b/stage8/repro_summary.md`
- `stage_artifacts/local_qwen15b/stage8/qwen25_1p5b_static_qlora_tiny_smoke.yaml`
- `stage_artifacts/local_qwen15b/stage8/qwen25_1p5b_dynamic_qlora_tiny_smoke.yaml`
- `stage_artifacts/local_qwen15b/stage8/static_repro/summary.json`
- `stage_artifacts/local_qwen15b/stage8/static_repro/gpu_samples.jsonl`
- `stage_artifacts/local_qwen15b/stage8/dynamic_repro/summary.json`
- `stage_artifacts/local_qwen15b/stage8/dynamic_repro/gpu_samples.jsonl`

训练输出目录：

- `stage_artifacts/local_qwen15b/outputs/stage8_static_qlora_tiny_smoke/`
- `stage_artifacts/local_qwen15b/outputs/stage8_dynamic_qlora_tiny_smoke/`

上述输出目录已被 `.gitignore` 覆盖。

## 5. Reusable Assets
可复用资产：

- Stage L8 两个正式 smoke YAML。
- Stage L7/L8 wrapper：`stage_artifacts/local_qwen15b/stage7_run_smoke.py`。
- Qwen tokenizer/model 兼容修复后的 `scripts/run_simpo.py` 和 `scripts/simpo_trainer.py`。
- `log_train_samples` 开关，可用于后续减少本地日志样本暴露。
- `stage_artifacts/local_qwen15b/stage8/repro_summary.md` 作为 tiny fallback 可复现证据。

## 6. Required Human Approvals for Future Stages
后续仍需单独明确批准：

- 增大 `max_steps`、`max_length`、batch size、gradient accumulation 或数据规模。
- 任何预计超过 10 分钟的训练/评估命令。
- 任何可能接近或超过 16GB VRAM 的运行。
- 任何新模型/数据下载。
- 任何 DeepSeek API 调用。
- 任何 AlpacaEval-style judge 或 benchmark run。
- 删除模型、数据、outputs、logs、checkpoints 或 caches。

## 7. Risks
### High
- 即使是 tiny 5-step 配置，峰值显存仍约 11.6GB，明显超过 8GB 预警线。扩大序列长度或 batch size 有高 OOM 风险。
- Stage L8 adapter 输出只是 smoke 产物，不能作为训练质量或 benchmark 结论。

### Medium
- dynamic gamma 当前只比 static 高约 73 MiB，但这个增量只在 `max_length: 512`、batch 1、tiny 数据下成立。
- adapter 输出目录约 82M/variant，已 gitignored，但后续需要避免误提交。
- logs 更干净，但仍包含训练参数和路径；不要公开含本地路径的原始日志。

### Low
- `evaluation_strategy` deprecation warning 仍存在，不影响当前版本 smoke。

## 8. Recommendation
建议下一阶段 Stage L9 进入“受控小规模扩展计划”，不要直接大幅训练。

推荐 Stage L9 二选一：

1. 更保守：只做 10-step static/dynamic smoke，保持 `max_length: 512`、batch 1，对比显存与 loss 稳定性。
2. 稍大但仍受控：先只提高 `max_steps` 到 20，不提高 max length 或 batch size。

不建议在当前 16GB VRAM 节点上同时提高 `max_length` 和 batch size。

## 9. Executive Summary
- Stage L8 PASS。
- 已将 L7 成功 smoke 固化为正式 Stage L8 static/dynamic YAML。
- 已复跑 static/dynamic，loss 指标与 L7 一致，峰值显存几乎一致。
- Stage L8 static: train_loss 2.4892，eval_loss 1.0009，峰值 11620 MiB。
- Stage L8 dynamic: train_loss 2.3154，eval_loss 0.8786，eval gamma_beta_ratio mean 0.1309，eval similarity mean 0.9049，峰值 11693 MiB。
- 新增 `log_train_samples` 开关，并确认正式 smoke 日志不再打印 prompt/chosen/rejected 样本。
- 未下载模型/数据，未安装依赖，未调用 DeepSeek API，未做 full fine-tuning，未训练 8B/9B，未修改系统配置，未打印 secrets。
