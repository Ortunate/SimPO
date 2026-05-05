# Stage L10 Report: 12GB Warning Line and Static 64/16 Data-Scale Smoke

## 1. Current Stage
Stage L10 - update VRAM warning line to 12GB and run static 64/16 data-scale smoke

Status: PASS

Date: 2026-05-05

Branch: `local-qwen15b-qlora`

## 2. Stage Goal
按 human 更新，将本地显存警戒线从 8GB 提高到 12GB，并在 standing protocols 下做一个受控数据规模扩展：

- 只跑 static QLoRA。
- 使用从已下载本地 parquet 派生的 64/16 subset。
- 保持 `max_steps: 20`。
- 保持 `max_length: 512`。
- 保持 batch size 1。

本阶段不运行 dynamic gamma，不调用 DeepSeek API，不下载模型/数据，不安装依赖，不修改系统配置。

## 3. Execution / Findings
已读取：

- `AGENTS.md`
- `docs_for_agent/local_qwen15b/local_qwen15b_line.md`
- `docs_for_agent/local_qwen15b/hardware_resource_policy.md`
- `docs_for_agent/local_qwen15b/mirror_download_policy.md`
- `docs_for_agent/local_qwen15b/api_eval_policy.md`
- `docs_for_human/local_qwen15b/stage_9.md`

关键命令：

```bash
sed -n '1,260p' AGENTS.md
sed -n '1,240p' docs_for_agent/local_qwen15b/hardware_resource_policy.md
sed -n '1,220p' docs_for_agent/local_qwen15b/local_qwen15b_line.md
sed -n '1,260p' docs_for_agent/local_qwen15b/mirror_download_policy.md
sed -n '1,320p' docs_for_human/local_qwen15b/stage_9.md
rg -n "8GB|12GB|16GB|VRAM" AGENTS.md docs_for_agent/local_qwen15b/hardware_resource_policy.md
.venv/bin/python - <<'PY'  # derive local 64/16 JSONL subset from existing parquet
HF_HOME=stage_artifacts/local_qwen15b/hf-cache HF_DATASETS_CACHE=stage_artifacts/local_qwen15b/hf-cache/datasets .venv/bin/python -c "<load 64/16 local dataset>"
.venv/bin/python -c "<parse Stage L10 static YAML with H4ArgumentParser>"
git check-ignore -v stage_artifacts/local_qwen15b/data/trl_ultrafeedback_binarized_64_16/train.jsonl stage_artifacts/local_qwen15b/outputs/stage10_static_64_16_20step
timeout 10m .venv/bin/python stage_artifacts/local_qwen15b/stage7_run_smoke.py --label static --config stage_artifacts/local_qwen15b/stage10/qwen25_1p5b_static_qlora_64_16_20step.yaml --out-dir stage_artifacts/local_qwen15b/stage10/static_64_16_20step
cat stage_artifacts/local_qwen15b/outputs/stage10_static_64_16_20step/train_results.json
cat stage_artifacts/local_qwen15b/outputs/stage10_static_64_16_20step/eval_results.json
rg -n "'loss'|train_loss|eval_loss|grad_norm|rewards/|logps/" stage_artifacts/local_qwen15b/stage10/static_64_16_20step/*.log
rg -n "Traceback|CUDA out|out of memory|RuntimeError|ValueError|TypeError|NaN|nan" stage_artifacts/local_qwen15b/stage10/static_64_16_20step/*.log
rg -n "Prompt sample|Chosen sample|Rejected sample" stage_artifacts/local_qwen15b/stage10/static_64_16_20step/stdout.log
du -sh stage_artifacts/local_qwen15b/data/trl_ultrafeedback_binarized_64_16 stage_artifacts/local_qwen15b/outputs/stage10_static_64_16_20step stage_artifacts/local_qwen15b/stage10/static_64_16_20step
stat -c '%n %s' stage_artifacts/local_qwen15b/outputs/stage10_static_64_16_20step/adapter_model.safetensors
```

Policy/doc updates:

- `AGENTS.md`
  - Human approval threshold changed from expected `>8GB GPU VRAM` to expected `>12GB GPU VRAM`.
  - Added current warning line: 12GB GPU VRAM.
  - Kept 16GB VRAM as the hard local device budget.
- `docs_for_agent/local_qwen15b/hardware_resource_policy.md`
  - Same 12GB warning line update.
  - Same expected `>12GB GPU VRAM` approval threshold.

Dataset derivation:

- Source: existing local `stage_artifacts/local_qwen15b/data/trl_ultrafeedback_binarized/data/*.parquet`
- Target: `stage_artifacts/local_qwen15b/data/trl_ultrafeedback_binarized_64_16/`
- Train rows: 64
- Test rows: 16
- Size: about 356K
- Gitignore: covered by `stage_artifacts/local_qwen15b/data/`

Config added:

- `stage_artifacts/local_qwen15b/stage10/qwen25_1p5b_static_qlora_64_16_20step.yaml`

Run result:

| Variant | Status | Peak VRAM sample | Train loss | Eval loss | Eval reward acc |
|---|---:|---:|---:|---:|---:|
| Static QLoRA 64/16 | PASS | 10571 MiB | 1.3097 | 1.0390 | 0.375 |

The sampled peak was below the updated 12GB warning line.

Stability checks:

- Return code: 0.
- No Traceback/OOM/RuntimeError/TypeError found.
- No prompt/chosen/rejected sample dumps found.
- Adapter file size: 73,911,112 bytes.
- Output directory size: about 82M.

## 4. Documentation Reorganization
No directory reorganization was performed.

New Stage L10 artifacts:

- `docs_for_human/local_qwen15b/stage_10.md`
- `stage_artifacts/local_qwen15b/stage10/static_64_16_summary.md`
- `stage_artifacts/local_qwen15b/stage10/qwen25_1p5b_static_qlora_64_16_20step.yaml`
- `stage_artifacts/local_qwen15b/stage10/static_64_16_20step/summary.json`
- `stage_artifacts/local_qwen15b/stage10/static_64_16_20step/gpu_samples.jsonl`

Ignored generated artifacts:

- `stage_artifacts/local_qwen15b/data/trl_ultrafeedback_binarized_64_16/`
- `stage_artifacts/local_qwen15b/outputs/stage10_static_64_16_20step/`
- Stage L10 `.log` files under the run directory.

## 5. Reusable Assets
Reusable assets:

- Updated 12GB warning-line policy in `AGENTS.md` and `hardware_resource_policy.md`.
- 64/16 local subset for additional controlled smoke tests.
- Stage L10 static 20-step config.
- Stage L10 static loss/eval/VRAM logs.
- Existing Stage L7 wrapper for future measured runs.

## 6. Required Human Approvals for Future Stages
Still require explicit approval before:

- Any run expected to exceed 12GB VRAM.
- Any command expected to exceed 10 minutes.
- Increasing `max_length`.
- Increasing batch size or gradient accumulation.
- Running dynamic on the 64/16 subset.
- Using a larger dataset subset.
- Any DeepSeek API call or AlpacaEval-style judge.
- Any new model/data download.
- Deleting outputs, logs, model/data/cache artifacts.

## 7. Risks
### High
- 12GB is still close to this machine's 16GB VRAM hard budget. Earlier 20-step runs reached about 11.9GB; future dynamic or longer-sequence runs may cross the warning line.
- 64/16 static smoke is still not a training-quality result and does not support benchmark or 8B/9B full fine-tuning claims.

### Medium
- The 64/16 subset came from the first rows of the local parquet files, not a curated representative split.
- The observed lower peak versus Stage L9 likely reflects sample lengths and wall-clock sampling, not a guaranteed memory reduction.
- Dataset and output artifacts are ignored, but still should not be manually committed or reused as final checkpoints.

### Low
- `evaluation_strategy` deprecation warning remains non-blocking.

## 8. Recommendation
Next recommended Stage L11:

- Run dynamic-gamma QLoRA on the same 64/16 subset with the same 20-step, `max_length: 512`, batch 1 constraints.
- Stop if observed peak crosses the updated 12GB warning line by a meaningful margin.
- Compare static 64/16 vs dynamic 64/16 gamma/similarity and sampled VRAM.

Do not increase `max_length`, batch size, or dataset size in the same stage.

## 9. Executive Summary
- Stage L10 PASS.
- VRAM warning line was updated to 12GB in project policy docs.
- 16GB remains the hard local VRAM budget.
- A local 64/16 preference subset was derived from already downloaded data.
- Static QLoRA 20-step on 64/16 completed successfully.
- Peak VRAM sample: 10571 MiB, below the new 12GB warning line.
- Train loss: 1.3097; eval loss: 1.0390; eval reward accuracy: 0.375.
- No download, dependency install, DeepSeek API call, full fine-tuning, 8B/9B training, system config change, or secret exposure occurred.
