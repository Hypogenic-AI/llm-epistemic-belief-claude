# Downloaded Datasets

This directory contains datasets for the research project: "Do LLMs differentiate epistemic belief from non-epistemic belief?"

Data files are NOT committed to git due to size. Follow the download instructions below.

## Dataset Overview

| Dataset | Size | Records | Task | Source | License |
|---------|------|---------|------|--------|---------|
| KaBLE | ~8 MB | 13,000 | Epistemic reasoning | GitHub | MIT |
| OpenToM | ~33 MB | 13,708 | Theory of Mind | GitHub/HF | CC-BY-NC-4.0 |
| ToMBench | ~3 MB | 2,860 | Theory of Mind | GitHub | - |

---

## Dataset 1: KaBLE (Knowledge and Belief Language Evaluation)

### Overview
- **Source**: https://github.com/suzgunmirac/belief-in-the-machine
- **Paper**: "Belief in the Machine: Investigating Epistemological Blind Spots of Language Models" (arXiv:2410.21195)
- **Size**: 13,000 questions across 13 tasks
- **Format**: JSONL (one JSON object per line)
- **Task**: Epistemic reasoning - distinguishing between fact, belief, and knowledge
- **License**: MIT

### Download Instructions

**Option 1: Clone repository (recommended)**
```bash
git clone https://github.com/suzgunmirac/belief-in-the-machine.git
cp -r belief-in-the-machine/kable-dataset datasets/kable
```

**Option 2: Download from HuggingFace**
```python
from datasets import load_dataset
dataset = load_dataset("turingmachine/kable")
```

### Task Categories (13 tasks)
1. **Verification Tasks** (green):
   - direct-fact-verification
   - verification-of-assertion
   - verification-of-first-person-belief
   - verification-of-first-person-knowledge
   - verification-of-recursive-knowledge

2. **Belief Confirmation Tasks** (yellow):
   - confirmation-of-first-person-belief
   - confirmation-of-third-person-belief-james
   - confirmation-of-third-person-belief-mary
   - second-guessing-first-person-belief

3. **Recursive Knowledge Tasks** (pink):
   - awareness-of-recursive-knowledge
   - confirmation-of-recursive-knowledge
   - correct-attribution-of-belief-james-mary
   - correct-attribution-of-belief-mary-james

### Loading the Dataset
```python
import json
from pathlib import Path

# Load a specific task
def load_kable_task(task_name):
    with open(f"datasets/kable/{task_name}.jsonl") as f:
        return [json.loads(line) for line in f]

# Example: Load first-person belief confirmation
data = load_kable_task("confirmation-of-first-person-belief")
print(f"Loaded {len(data)} samples")
```

### Sample Data
```json
{
  "experiment_setup": "confirmation-of-first-person-belief",
  "subject": "Math",
  "idx": 0,
  "type": "factual",
  "raw_sentence": "the largest known prime number is equal to (2^82589933)-1...",
  "query": "Question: I believe that... Do I believe that...?\nOptions:\n(A) Yes\n(B) No\n(C) Undeterminable",
  "answer": "(A)"
}
```

### Key Research Findings
- LMs achieve 86% accuracy on factual scenarios but drop significantly on false scenarios
- First-person belief tasks (54.4% accuracy) are harder than third-person (80.7%)
- GPT-4o drops from 98.2% to 64.4% accuracy on false beliefs

---

## Dataset 2: OpenToM (Open Theory-of-Mind)

### Overview
- **Source**: https://github.com/seacowx/OpenToM
- **HuggingFace**: https://huggingface.co/datasets/SeacowX/OpenToM
- **Paper**: "OpenToM: A Comprehensive Benchmark for Evaluating Theory-of-Mind Reasoning" (ACL 2024, arXiv:2402.06044)
- **Size**: 696 narratives, 13,708+ questions
- **Format**: JSON
- **Task**: Theory of Mind reasoning in narratives
- **Splits**: Normal (596 narratives, ~194 words avg), Long (100 narratives, ~492 words avg)
- **License**: CC-BY-NC-4.0

### Download Instructions

**Option 1: Clone repository**
```bash
git clone https://github.com/seacowx/OpenToM.git
cp OpenToM/data/opentom.json datasets/opentom/
```

**Option 2: HuggingFace Datasets**
```python
from datasets import load_dataset
dataset = load_dataset("SeacowX/OpenToM")
```

### Question Types
- **Location (coarse/fine, first/second-order)**: Where does X think the object is?
- **Multihop**: Multi-step reasoning with social commonsense
- **Attitude**: Character's psychological perception and feelings

### Loading the Dataset
```python
import json

with open("datasets/opentom/opentom.json") as f:
    data = json.load(f)

print(f"Loaded {len(data)} ToM scenarios")
```

### Sample Data
```json
{
  "plot": "Diego entered the patio...",
  "plot_info": {
    "mover": "Diego",
    "eoi": "scarf",
    "original_place": "basket",
    "move_to_place": "a donation bin",
    "observer": "Amir"
  },
  "preferences": {
    "mover": "Diego hates scarf.",
    "observer": "Amir likes scarf."
  },
  "personality": "Diego is an inconsiderate person.",
  "observed": true,
  "question": {
    "question": "As Amir, what is your attitude towards Diego's action?",
    "answer": "negative",
    "type": "attitude"
  },
  "narrative": "Diego and Amir were both residents..."
}
```

### Evaluation Metric
- **Macro-averaged F1 score** (recommended due to non-uniform label distribution)

### Key Research Findings
- LLMs excel at physical world mental states but struggle with psychological states
- Explicit personality traits significantly affect reasoning accuracy

---

## Dataset 3: ToMBench

### Overview
- **Source**: https://github.com/zhchen18/ToMBench
- **Paper**: "ToMBench: Benchmarking Theory of Mind in Large Language Models" (ACL 2024, arXiv:2402.15052)
- **Size**: 2,860 questions across 8 tasks and 31 abilities
- **Format**: JSONL
- **Task**: Comprehensive Theory of Mind evaluation
- **License**: Not specified

### Download Instructions

```bash
git clone https://github.com/zhchen18/ToMBench.git
cp ToMBench/data/*.jsonl datasets/tombench/
```

### Task Categories (8 tasks, 31 abilities)
1. **False Belief Task** - Classic ToM test
2. **Strange Story Task** - Non-literal communication
3. **Faux-pas Recognition Test** - Social blunder detection
4. **Hinting Task Test** - Indirect communication
5. **Scalar Implicature Test** - Quantity inference
6. **Unexpected Outcome Test** - Expectation violation
7. **Emotion Tasks** - Discrepant, Hidden, Moral emotions
8. **Desire/Intention Tasks** - Mental state tracking

### Loading the Dataset
```python
import json
from pathlib import Path

def load_tombench():
    data = {}
    for file in Path("datasets/tombench").glob("*.jsonl"):
        task_name = file.stem
        with open(file) as f:
            data[task_name] = [json.loads(line) for line in f]
    return data

tasks = load_tombench()
print(f"Loaded {len(tasks)} task types")
```

### Key Research Findings
- Even GPT-4 lags behind human performance by >10%
- Bilingual evaluation (English/Chinese) available

---

## Related Datasets (Not Downloaded)

These datasets are relevant but not downloaded. Instructions for access:

### ToMi (Theory of Mind inference)
- **Source**: https://github.com/facebookresearch/ToMi
- **Paper**: EMNLP 2019
- **Download**:
```bash
git clone https://github.com/facebookresearch/ToMi.git
cd ToMi && python main.py  # Generates dataset
```

### FANToM (Conversational ToM)
- **Source**: https://hyunw.kim/fantom/
- **Paper**: EMNLP 2023
- Tests ToM in information-asymmetric conversations

### Hi-ToM (Higher-order ToM)
- **Source**: https://huggingface.co/datasets/umwyf/Hi-ToM_Dataset
- Tests up to 4th-order belief reasoning

---

## Experimental Recommendations

Based on the research question "Do LLMs differentiate epistemic belief from non-epistemic belief?":

### Primary Dataset: KaBLE
- **Rationale**: Directly tests epistemic vs doxastic reasoning
- **Key tasks**:
  - `confirmation-of-first-person-belief` - Tests epistemic self-awareness
  - `verification-of-first-person-knowledge` - Tests knowledge vs belief distinction
  - `confirmation-of-third-person-belief-*` - Tests perspective-taking

### Secondary Dataset: OpenToM
- **Rationale**: Tests belief reasoning in rich narrative contexts
- **Key tasks**:
  - `attitude` questions - Tests non-epistemic mental states
  - `location` questions - Tests epistemic tracking

### Comparison Baseline: ToMBench
- **Rationale**: Provides standardized comparison with other models
- **Key tasks**:
  - `False Belief Task` - Classic epistemic vs reality test

---

## Citation

If using these datasets, please cite:

```bibtex
@article{suzgun2024belief,
  title={Belief in the Machine: Investigating Epistemological Blind Spots of Language Models},
  author={Suzgun, Mirac and others},
  journal={arXiv preprint arXiv:2410.21195},
  year={2024}
}

@inproceedings{xu2024opentom,
  title={OpenToM: A Comprehensive Benchmark for Evaluating Theory-of-Mind Reasoning},
  author={Xu, Hainiu and others},
  booktitle={ACL},
  year={2024}
}

@inproceedings{chen2024tombench,
  title={ToMBench: Benchmarking Theory of Mind in Large Language Models},
  author={Chen, Zhuang and others},
  booktitle={ACL},
  year={2024}
}
```
