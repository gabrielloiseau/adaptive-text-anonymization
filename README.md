# Adaptive Text Anonymization

Reproduction code for **"Adaptive Text Anonymization: Learning Privacy-Utility Trade-offs via Prompt Optimization"**. We learn task-specific, privacy-utility-aware anonymization
prompts with a two-stage GEPA pipeline ([Agrawal et al., 2025](https://arxiv.org/abs/2507.19457))
that (i) warm-starts a small open-source LLM against a scalar reward, then
(ii) refines it with rich, task-aware natural-language feedback.

## Contents

```
adaptive-text-anonymization/
├── src/adaptive_anonymization/
│   ├── tasks.py                     # DBBio, SynthPAI, TAB, PUPA, MedQA
│   ├── optimizer.py                 # two-stage GEPA
│   └── models.py                    # dspy.LM registry (keys via .env)
├── scripts/
│   ├── run_optimization.py
│   ├── evaluate.py                  # evaluate any saved program on a task
│   ├── export_prompts.py            # dump final prompts as Markdown
│   ├── error_analysis.py            # per-example failure analysis
│   └── plots.py                     # learning curves + Pareto frontiers
├── trained_models/                  # created by run_optimization (gitignored)
│   └── <task>/<model>/{base,warmup,dynamic}/{program.pkl,metadata.json}
├── prompts/                         # extracted final (dynamic-stage) prompts
│   └── <task>/<model>.md
├── pyproject.toml
└── .env.example
```

## Installation

The project targets Python 3.13 and is managed with [`uv`](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/<your-org>/adaptive-text-anonymization.git
cd adaptive-text-anonymization

uv sync                    # creates .venv/ and installs all dependencies
cp .env.example .env       # then fill in the API keys you plan to use
```

Required environment variables (all are read from `os.environ`; none are
hardcoded in the source):

| Variable               | Purpose                                                                 |
| ---------------------- | ----------------------------------------------------------------------- |
| `OPENROUTER_API_KEY`   | All registered models (Mistral, Gemma, Qwen, Gemini eval backbone)   |

## Reproducing the paper

Set `PYTHONPATH=./src` (or activate the uv-managed venv) before running any
script. Every CLI accepts `--help`.

### Optimized prompts (Table 1, main paper)

Run the two-stage GEPA pipeline for any (task, model) pair:

```bash
python scripts/run_optimization.py \
    --task dbbio --model gemma_3_27b \
    --budget 1500 --patience 5 --seed 42 \
    --output-dir trained_models
```

The unified CLI replaces five near-duplicate per-task scripts. Supported
tasks: `dbbio`, `synthpai`, `tab`, `pupa`, `medqa`. Supported anonymizer
models: `mistral_small`, `gemma_3_27b`, `qwen_3_30b`, `qwen_2_5_7b`
(SLM appendix). Three DSPy programs are saved per run under
`trained_models/<task>/<model>/{base,warmup,dynamic}/`.

Evaluate a saved program on the held-out test split:

```bash
python scripts/evaluate.py \
    --task dbbio \
    --program trained_models/dbbio/gemma_3_27b/dynamic \
    --output results/dbbio_gemma_dynamic.json
```

### SLM appendix (Qwen-2.5-7B)

Same `run_optimization.py` CLI with `--model qwen_2_5_7b`.

### Extracted prompts

The final (dynamic-stage) prompts learned per (task, model) are shipped in
`prompts/<task>/<model>.md`. To regenerate them after training:

```bash
python scripts/export_prompts.py --root trained_models --output prompts
```

### Learning-curve and Pareto-frontier plots

```bash
python scripts/plots.py         # helpers used to produce Figures in the paper
```

## Citation

If you use this work, please cite:

```bibtex
@misc{loiseau2026adaptivetextanonymization,
      title={Adaptive Text Anonymization: Learning Privacy-Utility Trade-offs via Prompt Optimization}, 
      author={Gabriel Loiseau and Damien Sileo and Damien Riquet and Maxime Meyer and Marc Tommasi},
      year={2026},
      eprint={2602.20743},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2602.20743}, 
}
```
