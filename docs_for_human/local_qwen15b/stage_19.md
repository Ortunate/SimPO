# Stage L19 Report: Bounded 50-Prompt Local Fallback Evaluation

## 1. Current Stage
Stage L19 - bounded local evaluation over 50 prompts.

Status: PASS

Date: 2026-05-05

Branch: `local-qwen15b-qlora`

## 2. Stage Goal
Execute the approved bounded local evaluation plan for the local Qwen2.5-1.5B-Instruct QLoRA fallback line:

- prepare 50 local prompts without downloading new data
- generate static and dynamic adapter responses with deterministic decoding
- build AB/BA judge requests
- run the approved DeepSeek V4 Flash bounded judge batch
- aggregate static/dynamic/tie/invalid metrics
- stop after this one stage

This stage is not an AlpacaEval benchmark and does not support any 8B/9B or full fine-tuning claim.

## 3. Execution / Findings
Read/used first:

- `AGENTS.md`
- `docs_for_agent/local_qwen15b/local_qwen15b_line.md`
- `docs_for_agent/local_qwen15b/hardware_resource_policy.md`
- `docs_for_agent/local_qwen15b/api_eval_policy.md`
- `docs_for_human/local_qwen15b/stage_18.md`

Key commands run:

```bash
git branch --show-current
git status --short
find docs_for_human/local_qwen15b -maxdepth 1 -type f -name 'stage_*.md' -printf '%f\n' | sort -V | tail -5
find docs_for_agent/local_qwen15b -maxdepth 1 -type f -printf '%f\n' | sort
sed -n '1,220p' docs_for_agent/local_qwen15b/local_qwen15b_line.md
sed -n '1,220p' docs_for_agent/local_qwen15b/hardware_resource_policy.md
sed -n '1,220p' docs_for_agent/local_qwen15b/api_eval_policy.md
sed -n '1,260p' docs_for_human/local_qwen15b/stage_18.md
find stage_artifacts/local_qwen15b -maxdepth 3 -type f | sort | tail -120
find stage_artifacts/local_qwen15b -maxdepth 3 -type d | sort | tail -120
find . -maxdepth 4 -type f \( -name '*judge*' -o -name '*generation*' -o -name '*eval*' \) | sort | head -200
sed -n '1,280p' stage_artifacts/local_qwen15b/stage16/run_tiny_generation_smoke.py
sed -n '1,260p' stage_artifacts/local_qwen15b/stage16/build_generation_eval_pairs.py
sed -n '1,320p' stage_artifacts/local_qwen15b/stage17/run_tiny_deepseek_judge_batch.py
sed -n '1,280p' stage_artifacts/local_qwen15b/stage14/build_offline_judge_requests.py
find stage_artifacts/local_qwen15b/data -maxdepth 4 -type f | sort
find eval -maxdepth 4 -type f | sort | head -100
mkdir -p stage_artifacts/local_qwen15b/stage19/bounded_eval50
chmod +x stage_artifacts/local_qwen15b/stage19/*.py
.venv/bin/python -m py_compile stage_artifacts/local_qwen15b/stage19/prepare_eval_prompts.py stage_artifacts/local_qwen15b/stage19/run_bounded_generation.py stage_artifacts/local_qwen15b/stage19/build_eval_pairs.py stage_artifacts/local_qwen15b/stage19/run_bounded_deepseek_judge.py
.venv/bin/python stage_artifacts/local_qwen15b/stage19/prepare_eval_prompts.py --input stage_artifacts/local_qwen15b/data/trl_ultrafeedback_binarized_64_16/test.jsonl --output stage_artifacts/local_qwen15b/stage19/bounded_eval50/prompts.jsonl --limit 50
.venv/bin/python -c "import pyarrow, datasets; print('pyarrow ok'); print('datasets ok')"
du -h stage_artifacts/local_qwen15b/data/trl_ultrafeedback_binarized/data/test-00000-of-00001.parquet
.venv/bin/python stage_artifacts/local_qwen15b/stage19/prepare_eval_prompts.py --input stage_artifacts/local_qwen15b/data/trl_ultrafeedback_binarized/data/test-00000-of-00001.parquet --output stage_artifacts/local_qwen15b/stage19/bounded_eval50/prompts.jsonl --limit 50
.venv/bin/python stage_artifacts/local_qwen15b/stage19/run_bounded_generation.py --model-path stage_artifacts/local_qwen15b/models/Qwen2.5-1.5B-Instruct --prompts stage_artifacts/local_qwen15b/stage19/bounded_eval50/prompts.jsonl --out-dir stage_artifacts/local_qwen15b/stage19/bounded_eval50/generation --prompt-count 50 --max-new-tokens 256
nvidia-smi --query-gpu=name,memory.total,memory.used --format=csv,noheader,nounits
.venv/bin/python -c "import torch; print('torch', torch.__version__); print('cuda_available', torch.cuda.is_available()); print('cuda_version', torch.version.cuda); print('device_count', torch.cuda.device_count())"
env | sort | grep -E 'CUDA|NVIDIA|LD_LIBRARY|WSL|CONDA|VIRTUAL_ENV'
ldconfig -p | grep -E 'libcuda|libnvidia-ml' | head -20
ls -l /usr/lib/wsl/lib/libcuda.so.1 /usr/lib/wsl/lib/libnvidia-ml.so.1
.venv/bin/python -c "import torch; print(torch.cuda.is_available()); torch.cuda.init(); print('initialized')"
LD_LIBRARY_PATH=/usr/lib/wsl/lib .venv/bin/python -c "import torch; print('cuda_available', torch.cuda.is_available()); print('device_count', torch.cuda.device_count()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'no device')"
ls -l /dev/dxg /dev/nvidia0 /dev/nvidiactl /dev/nvidia-uvm
which nvidia-smi
file $(which nvidia-smi)
uname -a
.venv/bin/python -c "import torch; print('cuda_available', torch.cuda.is_available()); print('device_count', torch.cuda.device_count()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'no device')"
.venv/bin/python stage_artifacts/local_qwen15b/stage19/run_bounded_generation.py --model-path stage_artifacts/local_qwen15b/models/Qwen2.5-1.5B-Instruct --prompts stage_artifacts/local_qwen15b/stage19/bounded_eval50/prompts.jsonl --out-dir stage_artifacts/local_qwen15b/stage19/bounded_eval50/generation --prompt-count 50 --max-new-tokens 256
wc -l stage_artifacts/local_qwen15b/stage19/bounded_eval50/generation/responses.jsonl
nvidia-smi --query-gpu=memory.used,utilization.gpu --format=csv,noheader,nounits
.venv/bin/python stage_artifacts/local_qwen15b/stage19/build_eval_pairs.py --responses stage_artifacts/local_qwen15b/stage19/bounded_eval50/generation/responses.jsonl --output stage_artifacts/local_qwen15b/stage19/bounded_eval50/eval_pairs.jsonl
cat stage_artifacts/local_qwen15b/stage19/bounded_eval50/generation/summary.json
.venv/bin/python stage_artifacts/local_qwen15b/stage14/build_offline_judge_requests.py --input stage_artifacts/local_qwen15b/stage19/bounded_eval50/eval_pairs.jsonl --output stage_artifacts/local_qwen15b/stage19/bounded_eval50/judge_requests.jsonl
.venv/bin/python -m py_compile stage_artifacts/local_qwen15b/stage19/run_bounded_deepseek_judge.py
.venv/bin/python stage_artifacts/local_qwen15b/stage19/run_bounded_deepseek_judge.py --request-jsonl stage_artifacts/local_qwen15b/stage19/bounded_eval50/judge_requests.jsonl --out-dir stage_artifacts/local_qwen15b/stage19/bounded_eval50/judge --env-file .env --max-tokens 256 --max-requests 110 --max-retries 10
cat stage_artifacts/local_qwen15b/stage19/bounded_eval50/judge/aggregate.json
cat stage_artifacts/local_qwen15b/stage19/bounded_eval50/judge/metadata.json
wc -l stage_artifacts/local_qwen15b/stage19/bounded_eval50/judge/judge_results.jsonl stage_artifacts/local_qwen15b/stage19/bounded_eval50/judge_requests.jsonl stage_artifacts/local_qwen15b/stage19/bounded_eval50/eval_pairs.jsonl
.venv/bin/python -m py_compile stage_artifacts/local_qwen15b/stage19/summarize_bounded_eval.py
.venv/bin/python stage_artifacts/local_qwen15b/stage19/summarize_bounded_eval.py --generation-summary stage_artifacts/local_qwen15b/stage19/bounded_eval50/generation/summary.json --responses stage_artifacts/local_qwen15b/stage19/bounded_eval50/generation/responses.jsonl --judge-metadata stage_artifacts/local_qwen15b/stage19/bounded_eval50/judge/metadata.json --out-json stage_artifacts/local_qwen15b/stage19/bounded_eval50/bounded_eval_summary.json --out-md stage_artifacts/local_qwen15b/stage19/bounded_eval50/bounded_eval_summary.md
cat stage_artifacts/local_qwen15b/stage19/bounded_eval50/bounded_eval_summary.json
git status --short
```

Execution notes:

- The planned 50-prompt set could not be prepared from `trl_ultrafeedback_binarized_64_16/test.jsonl` because that local subset had only 16 examples.
- Recovery path used the already local full test parquet: `stage_artifacts/local_qwen15b/data/trl_ultrafeedback_binarized/data/test-00000-of-00001.parquet` at 2.1 MB.
- No new dataset or model download was performed.
- The first in-sandbox GPU generation attempt failed because the sandbox did not expose CUDA device access to Torch.
- `nvidia-smi` could see the GPU, but in-sandbox Torch reported `cuda_available False`.
- A sandbox-external lightweight Torch check confirmed `cuda_available True` and `NVIDIA GeForce RTX 4090 Laptop GPU`.
- The approved generation run was then executed sandbox-external so Torch could access WSL GPU. Outputs were still written only under repository stage artifacts.

## 4. Documentation Reorganization
No documentation reorganization was performed in Stage L19.

New Stage L19 files/artifacts:

- `docs_for_human/local_qwen15b/stage_19.md`
- `stage_artifacts/local_qwen15b/stage19/prepare_eval_prompts.py`
- `stage_artifacts/local_qwen15b/stage19/run_bounded_generation.py`
- `stage_artifacts/local_qwen15b/stage19/build_eval_pairs.py`
- `stage_artifacts/local_qwen15b/stage19/run_bounded_deepseek_judge.py`
- `stage_artifacts/local_qwen15b/stage19/summarize_bounded_eval.py`
- `stage_artifacts/local_qwen15b/stage19/bounded_eval50/prompts.jsonl`
- `stage_artifacts/local_qwen15b/stage19/bounded_eval50/generation/responses.jsonl`
- `stage_artifacts/local_qwen15b/stage19/bounded_eval50/generation/summary.json`
- `stage_artifacts/local_qwen15b/stage19/bounded_eval50/generation/gpu_samples.json`
- `stage_artifacts/local_qwen15b/stage19/bounded_eval50/eval_pairs.jsonl`
- `stage_artifacts/local_qwen15b/stage19/bounded_eval50/judge_requests.jsonl`
- `stage_artifacts/local_qwen15b/stage19/bounded_eval50/judge/judge_results.jsonl`
- `stage_artifacts/local_qwen15b/stage19/bounded_eval50/judge/aggregate.json`
- `stage_artifacts/local_qwen15b/stage19/bounded_eval50/judge/metadata.json`
- `stage_artifacts/local_qwen15b/stage19/bounded_eval50/bounded_eval_summary.json`
- `stage_artifacts/local_qwen15b/stage19/bounded_eval50/bounded_eval_summary.md`

## 5. Reusable Assets
Reused assets:

- base model: `stage_artifacts/local_qwen15b/models/Qwen2.5-1.5B-Instruct`
- static adapter: `stage_artifacts/local_qwen15b/outputs/stage10_static_64_16_20step`
- dynamic adapter: `stage_artifacts/local_qwen15b/outputs/stage11_dynamic_64_16_20step`
- local UltraFeedback test parquet already downloaded in previous approved stages
- Stage L14 judge request builder for AB/BA formatting
- Stage L16 generation script structure
- Stage L17 DeepSeek judge batch script structure

Generation result:

- prompts: 50
- responses: 100
- static responses: 50
- dynamic responses: 50
- max new tokens: 256
- decoding: deterministic greedy (`do_sample=False`)
- total generation time: 1105.933 s
- sampled peak VRAM: 6402 MiB
- training steps: 0
- API calls during generation: 0

Response length:

- static average length: 753.54 chars
- dynamic average length: 767.66 chars
- empty responses: 0 for both variants

Judge result:

- judge model: `deepseek-v4-flash`
- primary judge requests: 100
- retries used: 0
- total API calls: 100
- HTTP failures: 0
- parse failures: 0
- prompt tokens: 63390
- completion tokens: 7886
- total tokens: 71276
- pair count: 50
- AB/BA consistent pairs: 38
- AB/BA consistency rate: 0.76
- inconsistent pairs: 12
- static wins among consistent pairs: 2
- dynamic wins among consistent pairs: 1
- ties among consistent pairs: 35
- dynamic win rate over all consistent pairs: 0.0263
- dynamic win rate over non-tie consistent pairs: 0.3333

Interpretation:

- The bounded evaluation pipeline is valid end to end at 50 prompts.
- The result is heavily tie-dominated.
- There is no evidence here that the dynamic adapter outperforms the static adapter.
- The 0.76 AB/BA consistency rate is acceptable as a bounded smoke-style eval signal, but below the stronger 0.80 gate previously proposed for treating the package as a clean stop/result gate.

## 6. Required Human Approvals for Future Stages
Future approvals are still required before:

- expanding to 100 prompts
- any additional DeepSeek API call
- any AlpacaEval/Arena-Hard/benchmark-style run
- any new model/data download
- any dependency install or upgrade
- any GPU training run
- any new real model loading or generation run
- any command expected to exceed 10 minutes
- any run expected to exceed 14GB VRAM
- any deletion of model/data/cache/checkpoint/log/evaluation artifacts
- any claim beyond the local Qwen2.5-1.5B QLoRA fallback proof-of-concept and bounded-eval evidence

## 7. Risks
### High
- This is not a full AlpacaEval benchmark and must not be reported as one.
- This result does not support any 8B/9B or full fine-tuning behavior claim.
- The judge comparison is tie-heavy and does not support a dynamic-gamma quality win.

### Medium
- Prompt source is local UltraFeedback test data, not a held-out AlpacaEval prompt set. This supports fallback evidence better than synthetic prompts but remains weaker than a real AlpacaEval-style prompt source.
- AB/BA consistency is 76%, below the stronger 80% stop/use-as-clean-result gate.
- The local adapters are tiny 20-step smoke artifacts; generation quality is not expected to be representative of a mature tuned model.
- External `nvidia-smi` sampling may miss short VRAM spikes, though observed sampled peak was low.

### Low
- Transformers emitted repeated warnings that `top_k=20` is present while `do_sample=False`; deterministic greedy decoding remained active.
- The initial in-sandbox CUDA failure was an execution-environment access issue; sandbox-external Torch confirmed GPU visibility and completed the run.

## 8. Recommendation
Do not expand to 100 prompts by default.

Recommended next step:

- Treat Stage L19 as the bounded fallback evaluation package.
- Use it to support only these claims: local fallback route works end to end, generation/judge aggregation works at 50-prompt scale, and the current tiny static/dynamic adapters are broadly tie-heavy under this judge.
- Do not claim dynamic-gamma superiority from this result.
- Shift attention to the 8B dynamic A100 route if the project needs meaningful model-quality evidence.

## 9. Executive Summary
- Stage L19 PASS.
- Implemented the bounded 50-prompt local evaluation plan.
- No model or dataset download was performed.
- No dependency install or upgrade was performed.
- No training was performed.
- Real model loading and GPU generation were performed as approved.
- DeepSeek V4 Flash judge was called 100 times as part of the approved bounded eval.
- No secret values or `.env` contents were printed.
- Generation completed 100 responses with sampled peak VRAM 6402 MiB.
- Judge parsing and HTTP status were clean: 0 parse failures, 0 HTTP failures.
- Final judge aggregate: static 2, dynamic 1, tie 35, inconsistent 12, AB/BA consistency 76%.
- The result validates the fallback evaluation pipeline but does not support dynamic-gamma quality superiority or any benchmark/full fine-tuning claim.
