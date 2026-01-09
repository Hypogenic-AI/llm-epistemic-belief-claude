# Cloned Repositories

This directory contains code repositories cloned for the research project: "Do LLMs differentiate epistemic belief from non-epistemic belief?"

## Repository Overview

| Repository | Purpose | Key Files | Paper |
|------------|---------|-----------|-------|
| belief-in-the-machine | KaBLE benchmark evaluation | `kable-dataset/`, `run_experiments.py` | arXiv:2410.21195 |
| OpenToM | ToM narrative benchmark | `data/`, `src/` | arXiv:2402.06044 |
| ToMBench | Comprehensive ToM evaluation | `data/`, `run_api.py` | arXiv:2402.15052 |
| ToMi | Classic ToM dataset generator | `main.py` | EMNLP 2019 |
| DEL-ToM | Dynamic Epistemic Logic ToM | TBD | arXiv:2505.17348 |

---

## 1. belief-in-the-machine (KaBLE)

**URL**: https://github.com/suzgunmirac/belief-in-the-machine
**License**: MIT

### Purpose
Evaluating epistemological blind spots in language models - specifically their ability to differentiate between fact, belief, and knowledge.

### Directory Structure
```
belief-in-the-machine/
├── kable-dataset/           # 13 JSONL files with 13,000 questions
├── figures/                 # Visualizations from paper
├── run_experiments.py       # Main evaluation script
├── requirements.txt         # Dependencies
└── README.md
```

### Key Files
- `kable-dataset/*.jsonl` - The KaBLE benchmark data
- `run_experiments.py` - Script to evaluate LLMs on KaBLE

### Usage
```bash
cd belief-in-the-machine
pip install -r requirements.txt
export OPENAI_API_KEY="your-key"
python run_experiments.py
```

### Relevance
**Primary codebase** for our research. Directly tests epistemic reasoning.

---

## 2. OpenToM

**URL**: https://github.com/seacowx/OpenToM
**License**: CC-BY-NC-4.0

### Purpose
Benchmark for evaluating Theory-of-Mind reasoning with rich narratives, personality traits, and psychological mental states.

### Directory Structure
```
OpenToM/
├── data/
│   ├── opentom.json         # 596 normal narratives
│   ├── opentom_long.json    # 100 long narratives
│   └── opentom_data/        # Additional data files
├── src/
│   ├── eval/                # Evaluation scripts
│   ├── generation/          # Data generation code
│   └── utils/
├── assets/
└── README.md
```

### Key Files
- `data/opentom.json` - Main benchmark dataset
- `src/eval/` - Evaluation code for different LLMs

### Usage
```python
from datasets import load_dataset
dataset = load_dataset("SeacowX/OpenToM")
```

### Relevance
Tests non-epistemic mental states (attitudes, preferences) alongside epistemic ones (beliefs about locations).

---

## 3. ToMBench

**URL**: https://github.com/zhchen18/ToMBench
**License**: Not specified

### Purpose
Comprehensive Theory of Mind benchmark covering 8 tasks and 31 abilities from the ATOMS framework.

### Directory Structure
```
ToMBench/
├── data/                    # 20 JSONL task files
├── figures/                 # Visualizations
├── prompts.py              # Evaluation prompts
├── run_api.py              # API-based evaluation
├── run_huggingface.py      # Local model evaluation
├── get_results.py          # Results aggregation
└── README.md
```

### Key Files
- `data/*.jsonl` - Task-specific evaluation data
- `run_api.py` - Evaluate OpenAI/Anthropic models
- `run_huggingface.py` - Evaluate local HuggingFace models
- `prompts.py` - Prompt templates

### Usage
```bash
cd ToMBench
bash eval_api.sh        # For API models
bash eval_huggingface.sh # For local models
python get_results.py   # Aggregate results
```

### Relevance
Provides standardized ToM comparison across multiple ability types.

---

## 4. ToMi

**URL**: https://github.com/facebookresearch/ToMi
**License**: Not specified (Facebook Research)

### Purpose
Classic Theory of Mind dataset generator from EMNLP 2019. Foundation for many subsequent benchmarks.

### Directory Structure
```
ToMi/
├── main.py                  # Dataset generator
├── data_generation/         # Generation logic
├── stories/                 # Story templates
├── data/                    # Generated data (after running main.py)
└── README.md
```

### Key Files
- `main.py` - Run to generate train/val/test splits
- `data/` - Output directory for generated data

### Usage
```bash
cd ToMi
pip install tqdm
python main.py
# Generates: data/train.txt, data/val.txt, data/test.txt
```

### Output Format
```
story_text
question: Where does Sally think the ball is?
answer: basket
```

### Relevance
Provides baseline ToM questions. Good for comparison with newer benchmarks.

---

## 5. DEL-ToM

**URL**: https://github.com/joel-wu/DEL-ToM
**License**: Not specified

### Purpose
Inference-time scaling for Theory-of-Mind reasoning using Dynamic Epistemic Logic.

### Key Contribution
- Decomposes ToM into verifiable belief updates
- Uses formal epistemic logic for structured reasoning
- Process Belief Model (PBM) verifier

### Relevance
Provides formal epistemic logic approach - directly relevant to distinguishing epistemic from non-epistemic beliefs.

---

## Recommended Usage for Research

### For Epistemic vs Non-Epistemic Belief Experiments

1. **Primary Evaluation**: Use `belief-in-the-machine`
   - Directly tests epistemic reasoning
   - 13 tasks covering first/third person, knowledge vs belief
   - Clear experimental setup

2. **Complementary Evaluation**: Use `OpenToM`
   - Tests psychological mental states (non-epistemic)
   - Attitude questions probe preferences, emotions
   - Compare with epistemic location questions

3. **Baseline Comparison**: Use `ToMBench`
   - Standardized across multiple LLMs
   - Published benchmark scores for comparison

4. **Formal Analysis**: Consider `DEL-ToM`
   - If exploring formal epistemic logic approaches

### Suggested Experiment Flow

```python
# 1. Load KaBLE for epistemic tasks
from pathlib import Path
import json

kable_tasks = {
    "epistemic": [
        "verification-of-first-person-knowledge",
        "confirmation-of-first-person-belief",
    ],
    "third_person": [
        "confirmation-of-third-person-belief-james",
        "confirmation-of-third-person-belief-mary",
    ]
}

# 2. Load OpenToM for non-epistemic comparison
with open("OpenToM/data/opentom.json") as f:
    opentom = json.load(f)

# Filter by question type
attitude_qs = [x for x in opentom if x["question"]["type"] == "attitude"]
location_qs = [x for x in opentom if x["question"]["type"].startswith("location")]

# 3. Run LLM evaluation
# - Compare performance on epistemic (KaBLE) vs non-epistemic (attitude)
# - Analyze first-person vs third-person differences
```

---

## Dependencies

Common dependencies across repositories:
```
torch
transformers
openai
anthropic
tqdm
pandas
numpy
```

Install all:
```bash
pip install torch transformers openai anthropic tqdm pandas numpy
```

---

## Notes

- All repositories cloned with `--depth 1` for minimal footprint
- Large data files may need separate download (see datasets/README.md)
- API keys required for OpenAI/Anthropic evaluations
