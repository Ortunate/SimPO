# Project Brief

## Project
基于语义相似度自适应边界的大语言模型 SimPO 对齐优化研究  
Adaptive Margin Scheduling Based on Semantic Similarity

## Core objective
Improve SimPO by replacing or augmenting its static global gamma / margin behavior with adaptive scheduling based on semantic similarity between chosen and rejected responses.

The project must preserve:

- zero extra inference-time cost
- near-zero training memory overhead
- minimal intrusion into the existing SimPO training code
- practical finishability under limited compute

## Research motivation
Static global margin can be suboptimal because:

- hard samples may receive abnormal or overly aggressive gradients
- easy samples may be under-trained
- one global boundary cannot adapt to pair difficulty

The proposed signal is semantic similarity between chosen and rejected responses. High similarity suggests a harder preference pair; low similarity suggests an easier pair.

## Base models
Candidate base models:

- Llama-3-8B-Instruct
- Gemma-2-9B

Final choice must consider local feasibility, repository compatibility, licensing/access, and server availability.

## Dataset
Primary dataset:

- UltraFeedback

Local stages may use sampled or tiny debug subsets. Local results are for feasibility and stability only, not final performance claims.

## Evaluation
Target benchmarks:

- AlpacaEval 2, length-controlled
- Arena-Hard

These are final-stage evaluation targets. Do not use local laptop runs to claim final benchmark improvement.

## Core algorithm idea
Replace or augment static gamma with dynamic gamma scheduling.

Candidate strategies:

1. Static baseline
   - original SimPO behavior
   - required for comparison

2. Similarity-based linear strategy
   - compute semantic similarity between chosen and rejected responses
   - map similarity to gamma adjustment
   - expected direction: higher similarity -> smaller or more cautious effective margin

3. Curriculum strategy
   - adjust base gamma as training progresses
   - expected direction: gradually increase training strictness after early stabilization

4. Combined strategy
   - similarity-based adjustment plus curriculum base schedule

5. Safety gating
   - clamp / threshold gamma values
   - prevent exploding gradients or unstable loss geometry

## Semantic signal constraints
The semantic signal must:

- not use an external reward model
- not add inference-time cost
- preferably reuse hidden states from the existing training forward pass
- avoid retaining unnecessary tensors
- be implemented so it can be disabled cleanly

Codex must verify where hidden states can be extracted with the least memory and code-risk cost.

## Hardware policy
### Local node
Environment:

- Win11
- WSL2
- RTX 4090 Laptop
- 64GB RAM

Codex must not assume desktop RTX 4090 capacity. It must check actual GPU, CUDA, driver, and VRAM through the environment before making training-size decisions.

Use local node for:

- environment and dependency validation
- repository audit
- baseline smoke run
- dynamic gamma implementation
- tiny / small-sample validation
- memory comparison
- loss and gradient stability checks

Do not use local node for:

- final training
- large experiment grids
- full benchmark runs
- repeated long training attempts without a clear gate

### Cloud node
Expected server class:

- A800 / A100 or equivalent

Use cloud only after local gate passes.

## Project phases
### Phase 0: Project takeover and repository audit
Goals:

- confirm repository structure
- identify training entrypoints
- identify loss implementation
- identify gamma / margin handling
- identify chosen / rejected data flow
- identify lowest-risk hook point for semantic similarity

Exit criteria:

- stage report completed
- no code changes unless necessary for inspection
- implementation plan proposed

### Phase 1: Environment and baseline smoke path
Goals:

- install or verify dependencies
- run minimal baseline path
- record memory, loss, and logs
- establish baseline evidence

Exit criteria:

- baseline smoke run passes or blocker is diagnosed
- exact commands and logs are recorded
- memory measurement method is defined

### Phase 2: Dynamic gamma prototype
Goals:

- implement dynamic gamma in a minimal, reversible way
- support static baseline and at least one dynamic strategy
- keep feature toggle/config explicit
- log gamma statistics

Exit criteria:

- code path runs on tiny data
- dynamic behavior can be disabled
- no obvious correctness break

### Phase 3: Local stability validation
Goals:

- compare static vs dynamic on small data
- monitor loss, grad norm, gamma distribution, memory
- detect instability early

Exit criteria:

- at least one dynamic strategy survives local validation
- memory overhead is acceptable or failure is diagnosed
- recommended cloud candidate is identified or project is narrowed

### Phase 4: Cloud readiness
Goals:

- prepare reproducible training config
- define final experiment matrix
- define checkpoint and logging conventions
- minimize experiment count

Exit criteria:

- cloud run package is ready
- risks are explicit
- expected cost and outputs are clear

### Phase 5: Full training and evaluation
Goals:

- run final training
- run target evaluations
- collect results
- consolidate findings

Exit criteria:

- results are reproducible
- success/failure is honestly assessed
- code and report are packaged

## Success criteria
Minimum project success:

- baseline reproduced or reasonably matched
- dynamic gamma implemented cleanly
- local validation shows stable training behavior
- memory overhead is measured and controlled
- final report can explain whether the hypothesis is supported

Target research success:

- dynamic strategy improves AlpacaEval 2 length-controlled win rate over baseline by roughly 1-2 absolute percentage points
- no unacceptable memory or inference-time cost is introduced

## Hard failure conditions
Treat these as stop-and-review conditions:

- dynamic gamma repeatedly causes NaN / Inf / severe divergence
- memory overhead clearly violates the project red line
- implementation requires broad framework migration
- local stage expands into full training
- results cannot be reproduced from configs and logs

## Management split
Codex handles:

- stage-level planning
- execution
- validation
- review
- summaries

Human supervisor handles:

- project-level direction
- risk acceptance
- scope decisions
- cloud migration approval
- final completion judgment

## Local hardware clarification

The local machine is a constrained development node.

Known expected local constraints:
- RTX 4090 Laptop class GPU, likely 16GB VRAM
- WSL2 environment
- System RAM may be capped by WSL configuration, commonly around 50% of host RAM unless configured otherwise

This means local work must default to:
- repository audit
- tiny / dummy runs
- minimal smoke validation
- small code-level checks
- memory instrumentation
- dynamic-gamma code path validation

Local work must not default to real 8B/9B training.

Any attempt to run Llama-3-8B, Gemma-2-9B, or another similarly sized model locally requires explicit human approval, even for a smoke test.

## Local run tiers

### Tier 0: Always allowed
Allowed without extra approval:
- read files
- inspect repository structure
- inspect configs
- run lightweight shell commands
- create small documentation files
- run static checks
- run tiny unit tests
- prepare scripts without executing heavy commands

### Tier 1: Ask before running
Requires human approval:
- GPU commands expected to use more than 8GB VRAM
- commands expected to run longer than 10 minutes
- commands expected to use more than 16GB system RAM
- installing or upgrading major ML dependencies
- downloading models, datasets, or artifacts larger than 1GB
- any real 8B/9B model load or training attempt
- any run on real UltraFeedback data beyond tiny/debug samples

### Tier 2: Not allowed on local node unless explicitly overridden
Not allowed by default:
- full training
- large ablation grids
- full UltraFeedback training
- AlpacaEval 2 or Arena-Hard benchmark runs
- long unattended GPU jobs
- broad framework migration

## Human report policy

Codex must persist every stage report under:

- `docs_for_human/stage_<N>.md`

The report must be written before proceeding to the next stage.

If earlier stages were completed before this rule was added, Codex must backfill those reports from the conversation context before continuing.
