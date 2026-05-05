# Stage L9 Report: Controlled 20-Step Static/Dynamic Smoke

## 1. Current Stage
Stage L9 - controlled 20-step static/dynamic Qwen2.5-1.5B QLoRA smoke

Status: PASS

Date: 2026-05-05

Branch: `local-qwen15b-qlora`

## 2. Stage Goal
在 Stage L8 已复现的正式 tiny smoke 基础上，只把 `max_steps` 从 5 增加到 20，验证 static QLoRA 与 dynamic-gamma QLoRA 在相同 `max_length: 512`、batch size 1 条件下的短程稳定性、loss、gamma/similarity 日志和显存采样。

本阶段没有提高 `max_length`、batch size、数据规模或依赖复杂度。

## 3. Execution / Findings
已读取：

- `AGENTS.md`
- `docs_for_agent/local_qwen15b/local_qwen15b_line.md`
- `docs_for_agent/local_qwen15b/hardware_resource_policy.md`
- `docs_for_agent/local_qwen15b/mirror_download_policy.md`
- `docs_for_agent/local_qwen15b/api_eval_policy.md`
- `docs_for_human/local_qwen15b/stage_8.md`

关键命令：

```bash
sed -n '1,240p' AGENTS.md
sed -n '1,220p' docs_for_agent/local_qwen15b/local_qwen15b_line.md
sed -n '1,220p' docs_for_agent/local_qwen15b/hardware_resource_policy.md
sed -n '1,220p' docs_for_agent/local_qwen15b/mirror_download_policy.md
sed -n '1,220p' docs_for_agent/local_qwen15b/api_eval_policy.md
sed -n '1,320p' docs_for_human/local_qwen15b/stage_8.md
.venv/bin/python -m py_compile scripts/run_simpo.py scripts/simpo_config.py scripts/simpo_trainer.py stage_artifacts/local_qwen15b/stage7_run_smoke.py
.venv/bin/python -c "<parse Stage L9 static/dynamic YAML with H4ArgumentParser>"
git check-ignore -v stage_artifacts/local_qwen15b/outputs/stage9_static_qlora_20step stage_artifacts/local_qwen15b/outputs/stage9_dynamic_qlora_20step
timeout 10m .venv/bin/python stage_artifacts/local_qwen15b/stage7_run_smoke.py --label static --config stage_artifacts/local_qwen15b/stage9/qwen25_1p5b_static_qlora_20step.yaml --out-dir stage_artifacts/local_qwen15b/stage9/static_20step
timeout 10m .venv/bin/python stage_artifacts/local_qwen15b/stage7_run_smoke.py --label dynamic --config stage_artifacts/local_qwen15b/stage9/qwen25_1p5b_dynamic_qlora_20step.yaml --out-dir stage_artifacts/local_qwen15b/stage9/dynamic_20step
cat stage_artifacts/local_qwen15b/outputs/stage9_static_qlora_20step/train_results.json
cat stage_artifacts/local_qwen15b/outputs/stage9_static_qlora_20step/eval_results.json
cat stage_artifacts/local_qwen15b/outputs/stage9_dynamic_qlora_20step/train_results.json
cat stage_artifacts/local_qwen15b/outputs/stage9_dynamic_qlora_20step/eval_results.json
rg -n "'loss'|train_loss|eval_loss|gamma_beta_ratio|similarity|grad_norm|rewards/|logps/" stage_artifacts/local_qwen15b/stage9/*_20step/*.log
rg -n "Traceback|CUDA out|out of memory|RuntimeError|ValueError|TypeError|NaN|nan" stage_artifacts/local_qwen15b/stage9/*_20step/*.log
rg -n "Prompt sample|Chosen sample|Rejected sample" stage_artifacts/local_qwen15b/stage9/*_20step/stdout.log
du -sh stage_artifacts/local_qwen15b/outputs/stage9_static_qlora_20step stage_artifacts/local_qwen15b/outputs/stage9_dynamic_qlora_20step
stat -c '%n %s' stage_artifacts/local_qwen15b/outputs/stage9_static_qlora_20step/adapter_model.safetensors stage_artifacts/local_qwen15b/outputs/stage9_dynamic_qlora_20step/adapter_model.safetensors
```

新增 Stage L9 configs：

- `stage_artifacts/local_qwen15b/stage9/qwen25_1p5b_static_qlora_20step.yaml`
- `stage_artifacts/local_qwen15b/stage9/qwen25_1p5b_dynamic_qlora_20step.yaml`

结果：

| Variant | Status | Peak VRAM sample | Train loss | Eval loss | Eval reward acc |
|---|---:|---:|---:|---:|---:|
| Static QLoRA | PASS | 11945 MiB | 1.6594 | 0.9879 | 0.625 |
| Dynamic gamma QLoRA | PASS | 11758 MiB | 1.4992 | 0.8711 | 0.5 |

Dynamic final eval metrics:

- `eval_gamma_beta_ratio/mean`: 0.13096913695335388
- `eval_gamma_beta_ratio/min`: 0.13096913695335388
- `eval_gamma_beta_ratio/max`: 0.13096913695335388
- `eval_similarity/mean`: 0.9044938683509827
- `eval_similarity/min`: 0.9044938683509827
- `eval_similarity/max`: 0.9044938683509827

Stage L8 vs L9:

| Variant | L8 Peak | L9 Peak | L8 train loss | L9 train loss | L8 eval loss | L9 eval loss |
|---|---:|---:|---:|---:|---:|---:|
| Static | 11620 MiB | 11945 MiB | 2.4892 | 1.6594 | 1.0009 | 0.9879 |
| Dynamic | 11693 MiB | 11758 MiB | 2.3154 | 1.4992 | 0.8786 | 0.8711 |

Stability checks:

- Both runs returned code 0.
- No Traceback/OOM/RuntimeError/TypeError was found.
- No prompt/chosen/rejected sample dumps were found.
- `nvidia-smi` peak values are wall-clock samples, not exact allocator peaks.

## 4. Documentation Reorganization
本阶段未做目录重组。新增：

- `docs_for_human/local_qwen15b/stage_9.md`
- `stage_artifacts/local_qwen15b/stage9/controlled_20step_summary.md`
- `stage_artifacts/local_qwen15b/stage9/qwen25_1p5b_static_qlora_20step.yaml`
- `stage_artifacts/local_qwen15b/stage9/qwen25_1p5b_dynamic_qlora_20step.yaml`
- `stage_artifacts/local_qwen15b/stage9/static_20step/summary.json`
- `stage_artifacts/local_qwen15b/stage9/static_20step/gpu_samples.jsonl`
- `stage_artifacts/local_qwen15b/stage9/dynamic_20step/summary.json`
- `stage_artifacts/local_qwen15b/stage9/dynamic_20step/gpu_samples.jsonl`

训练输出目录：

- `stage_artifacts/local_qwen15b/outputs/stage9_static_qlora_20step/`
- `stage_artifacts/local_qwen15b/outputs/stage9_dynamic_qlora_20step/`

输出目录已被 `.gitignore` 覆盖。

## 5. Reusable Assets
可复用资产：

- Stage L9 两个 20-step configs。
- Stage L7/L8/L9 wrapper：`stage_artifacts/local_qwen15b/stage7_run_smoke.py`。
- Stage L9 loss/gamma/similarity logs。
- Stage L9 显存采样 JSONL。
- `stage_artifacts/local_qwen15b/stage9/controlled_20step_summary.md`。

## 6. Required Human Approvals for Future Stages
后续仍需明确批准：

- 增大 `max_length`。
- 增大 batch size 或 gradient accumulation。
- 使用超过 tiny dataset 的更多数据。
- 任何预计超过 10 分钟的命令。
- 任何可能接近 16GB VRAM 的运行。
- 任何 DeepSeek API 调用或 AlpacaEval-style judge。
- 删除 outputs、logs、caches、模型或数据。

## 7. Risks
### High
- Stage L9 static 采样峰值达到 11945 MiB，dynamic 采样峰值达到 11758 MiB；距离 16GB VRAM 仍有余量，但已明显超过 8GB 警戒线。
- 20-step tiny 结果仍不是有效训练质量结论，不支持 benchmark 或 8B/9B full fine-tuning 推断。

### Medium
- Dynamic run 的采样峰值低于 static，可能来自采样时机、CUDA allocator 和运行波动；不应解释为 dynamic 一定更省显存。
- Loss 降低符合短程过小数据训练预期，但 tiny 数据太小，不能代表泛化。
- 输出 adapter 约 82M/variant，已 gitignored，但仍需要防止误提交或误用。

### Low
- `evaluation_strategy` deprecation warning 仍存在，不影响当前 smoke。

## 8. Recommendation
建议下一阶段 Stage L10 不再盲目加 steps，而是做“受控数据规模/评估准备”二选一：

1. 训练侧：保持 `max_length: 512`、batch 1，把 tiny sample 从 16/8 扩到一个仍很小的本地 subset，例如 64/16，并先静态跑 20 steps。
2. 评估侧：准备无 API 的 AlpacaEval-style 输出/judge 模板 dry-run，只做文件格式和模板校验，不调用 DeepSeek。

若继续训练侧扩展，不建议同时增加 `max_length`、batch size 和数据规模。

## 9. Executive Summary
- Stage L9 PASS。
- 已完成 static QLoRA 20-step smoke。
- 已完成 dynamic-gamma QLoRA 20-step smoke。
- Static: train_loss 1.6594，eval_loss 0.9879，采样峰值 11945 MiB。
- Dynamic: train_loss 1.4992，eval_loss 0.8711，eval gamma_beta_ratio mean 0.1310，eval similarity mean 0.9045，采样峰值 11758 MiB。
- 未下载模型/数据，未安装依赖，未调用 DeepSeek API，未做 full fine-tuning，未训练 8B/9B，未修改系统配置，未打印 secrets。
