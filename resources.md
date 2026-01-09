# Resources Catalog

This document catalogs all resources gathered for the research project: **"Do LLMs differentiate epistemic belief from non-epistemic belief?"**

---

## Summary

| Resource Type | Count | Location |
|---------------|-------|----------|
| Papers | 10 | `papers/` |
| Datasets | 3 | `datasets/` |
| Code Repositories | 5 | `code/` |

---

## Papers

**Total papers downloaded**: 10

| # | Title | Authors | Year | File | arXiv | Key Contribution |
|---|-------|---------|------|------|-------|------------------|
| 1 | Belief in the Machine: Investigating Epistemological Blind Spots of Language Models | Suzgun et al. | 2024 | `papers/2410.21195_belief_in_machine_kable.pdf` | 2410.21195 | KaBLE benchmark for epistemic reasoning |
| 2 | Evaluating Large Language Models in Theory of Mind Tasks | Kosinski | 2023 | `papers/2302.02083_llm_theory_of_mind.pdf` | 2302.02083 | Foundational LLM ToM evaluation |
| 3 | OpenToM: A Comprehensive Benchmark for Evaluating Theory-of-Mind Reasoning | Xu et al. | 2024 | `papers/2402.06044_opentom.pdf` | 2402.06044 | ToM with physical/psychological states |
| 4 | ToMBench: Benchmarking Theory of Mind in Large Language Models | Chen et al. | 2024 | `papers/2402.15052_tombench.pdf` | 2402.15052 | 31 ToM abilities benchmark |
| 5 | Standards for Belief Representations in LLMs | Bowen et al. | 2025 | `papers/2405.21030_belief_representations.pdf` | 2405.21030 | Criteria for LLM belief measurement |
| 6 | Understanding Epistemic Language with Bayesian Theory of Mind | LaBToM authors | 2024 | `papers/2408.12022_labtom_epistemic.pdf` | 2408.12022 | Epistemic language understanding |
| 7 | FANToM: A Benchmark for Stress-Testing Machine ToM in Conversations | Kim et al. | 2023 | `papers/2310.15421_fantom.pdf` | 2310.15421 | Conversational ToM testing |
| 8 | Zero, Finite, and Infinite Belief History of ToM Reasoning | Authors | 2024 | `papers/2406.04800_belief_history_tom.pdf` | 2406.04800 | Temporal belief tracking |
| 9 | DEL-ToM: Inference-Time Scaling for Theory-of-Mind via Dynamic Epistemic Logic | Wu et al. | 2025 | `papers/2505.17348_del_tom.pdf` | 2505.17348 | Formal epistemic logic approach |
| 10 | Epistemic Integrity in Large Language Models | Ghafouri et al. | 2024 | `papers/2411.06528_epistemic_integrity.pdf` | 2411.06528 | Epistemic calibration |

See `papers/README.md` for detailed descriptions of each paper.

---

## Datasets

**Total datasets downloaded**: 3

| Name | Source | Size | Records | Task | Location | License |
|------|--------|------|---------|------|----------|---------|
| KaBLE | GitHub | ~8 MB | 13,000 | Epistemic reasoning | `datasets/kable/` | MIT |
| OpenToM | GitHub/HF | ~33 MB | 13,708 | Theory of Mind | `datasets/opentom/` | CC-BY-NC-4.0 |
| ToMBench | GitHub | ~3 MB | 2,860 | Comprehensive ToM | `datasets/tombench/` | - |

See `datasets/README.md` for detailed descriptions and download instructions.

### Dataset Details

#### KaBLE (Knowledge and Belief Language Evaluation)
- **13 epistemic reasoning tasks**:
  - Verification tasks (5): fact, assertion, first-person belief/knowledge, recursive knowledge
  - Belief confirmation (4): first-person, third-person (James/Mary), second-guessing
  - Recursive knowledge (4): awareness, confirmation, attribution
- **Format**: JSONL (1,000 samples per task)
- **Key for research**: Directly tests epistemic vs. doxastic distinction

#### OpenToM
- **Question types**:
  - Location (epistemic): Where does X think object is?
  - Attitude (non-epistemic): How does X feel about event?
  - Multihop: Multi-step reasoning
- **Format**: JSON with narrative and questions
- **Key for research**: Matched epistemic vs. non-epistemic comparison

#### ToMBench
- **8 tasks, 31 abilities**:
  - False Belief, Strange Story, Faux-pas, Hinting
  - Emotions, Desires, Intentions
- **Format**: JSONL
- **Key for research**: Standardized comparison baseline

---

## Code Repositories

**Total repositories cloned**: 5

| Repository | URL | Purpose | Location | Key Files |
|------------|-----|---------|----------|-----------|
| belief-in-the-machine | github.com/suzgunmirac/belief-in-the-machine | KaBLE benchmark | `code/belief-in-the-machine/` | `kable-dataset/`, `run_experiments.py` |
| OpenToM | github.com/seacowx/OpenToM | ToM narrative benchmark | `code/OpenToM/` | `data/`, `src/eval/` |
| ToMBench | github.com/zhchen18/ToMBench | Comprehensive ToM eval | `code/ToMBench/` | `data/`, `run_api.py` |
| ToMi | github.com/facebookresearch/ToMi | Classic ToM generator | `code/ToMi/` | `main.py` |
| DEL-ToM | github.com/joel-wu/DEL-ToM | Dynamic Epistemic Logic | `code/DEL-ToM/` | TBD |

See `code/README.md` for detailed descriptions and usage instructions.

---

## Resource Gathering Notes

### Search Strategy

1. **Literature Search**:
   - ArXiv searches: "LLM epistemic belief", "language model theory of mind", "LLM knowledge vs belief"
   - Semantic Scholar for citation tracking
   - Papers with Code for implementations

2. **Dataset Search**:
   - HuggingFace Datasets hub
   - GitHub repositories from papers
   - Papers with Code dataset links

3. **Code Search**:
   - Official implementations from papers
   - GitHub searches for benchmark implementations

### Selection Criteria

**Papers selected based on**:
- Direct relevance to epistemic/non-epistemic distinction
- Recency (2023-2025 preferred)
- Availability of code/data
- Publication venue (NeurIPS, ACL, EMNLP, Nature MI)

**Datasets selected based on**:
- Direct testing of epistemic reasoning (KaBLE)
- Comparison of belief types (OpenToM)
- Standardized benchmark (ToMBench)
- Availability and documentation quality

### Challenges Encountered

1. **PDF extraction**: Could not install pdfplumber due to environment constraints; used arXiv abstracts and HTML versions instead
2. **FANToM dataset**: Repository not found at expected URL; alternative access needed
3. **Large dataset sizes**: OpenToM JSON is 33MB; gitignored to keep repo small

### Gaps and Workarounds

| Gap | Workaround |
|-----|------------|
| No direct epistemic vs. non-epistemic benchmark | Will use OpenToM attitude vs. location questions |
| Limited first-person epistemic data | KaBLE has first-person tasks |
| Need human baselines | Published in paper results |

---

## Recommendations for Experiment Design

Based on gathered resources, here is the recommended experimental approach:

### 1. Primary Dataset: KaBLE

**Use for**: Testing epistemic differentiation

**Key experiments**:
```python
# Compare performance across belief types
tasks = {
    "first_person_belief": "confirmation-of-first-person-belief",
    "third_person_belief": "confirmation-of-third-person-belief-james",
    "first_person_knowledge": "verification-of-first-person-knowledge",
    "recursive_knowledge": "verification-of-recursive-knowledge"
}
```

### 2. Secondary Dataset: OpenToM

**Use for**: Epistemic vs. non-epistemic comparison

**Key experiments**:
```python
# Compare question types
epistemic_tasks = ["location_cg_fo", "location_fg_fo", "location_cg_so", "location_fg_so"]
non_epistemic_tasks = ["attitude"]
```

### 3. Evaluation Metrics

| Metric | Purpose |
|--------|---------|
| Accuracy (epistemic) | Performance on knowledge/belief tasks |
| Accuracy (non-epistemic) | Performance on attitude/preference tasks |
| Gap score | Epistemic - Non-epistemic accuracy |
| First-person gap | Third-person - First-person accuracy |
| True/False belief gap | True - False belief accuracy |

### 4. Models to Evaluate

| Model | Type | Rationale |
|-------|------|-----------|
| GPT-4 / GPT-4o | Closed | SOTA reference |
| Claude-3 Opus | Closed | Comparison |
| Llama-3 70B | Open | Reproducibility |
| Llama-3 8B | Open | Scale comparison |

### 5. Baseline Comparisons

- Random chance (33% for 3-way, 50% for binary)
- Human performance (from paper results)
- Published model scores (GPT-4: ~75% on ToM tasks)

---

## File Structure

```
llm-epistemic-belief-claude/
├── papers/
│   ├── README.md
│   ├── 2410.21195_belief_in_machine_kable.pdf
│   ├── 2302.02083_llm_theory_of_mind.pdf
│   ├── 2402.06044_opentom.pdf
│   ├── 2402.15052_tombench.pdf
│   ├── 2405.21030_belief_representations.pdf
│   ├── 2408.12022_labtom_epistemic.pdf
│   ├── 2310.15421_fantom.pdf
│   ├── 2406.04800_belief_history_tom.pdf
│   ├── 2505.17348_del_tom.pdf
│   └── 2411.06528_epistemic_integrity.pdf
├── datasets/
│   ├── README.md
│   ├── .gitignore
│   ├── kable/
│   │   └── *.jsonl (13 files)
│   ├── opentom/
│   │   └── opentom.json
│   └── tombench/
│       └── *.jsonl (20 files)
├── code/
│   ├── README.md
│   ├── belief-in-the-machine/
│   ├── OpenToM/
│   ├── ToMBench/
│   ├── ToMi/
│   └── DEL-ToM/
├── literature_review.md
├── resources.md
└── .resource_finder_complete
```

---

## Next Steps for Experiment Runner

1. **Environment Setup**:
   ```bash
   pip install torch transformers openai anthropic tqdm pandas numpy
   ```

2. **API Key Configuration**:
   ```bash
   export OPENAI_API_KEY="..."
   export ANTHROPIC_API_KEY="..."
   ```

3. **Load Datasets**:
   ```python
   import json

   # KaBLE
   with open("datasets/kable/confirmation-of-first-person-belief.jsonl") as f:
       kable = [json.loads(l) for l in f]

   # OpenToM
   with open("datasets/opentom/opentom.json") as f:
       opentom = json.load(f)
   ```

4. **Run Experiments**:
   - See `code/belief-in-the-machine/run_experiments.py` for KaBLE evaluation
   - See `code/ToMBench/run_api.py` for ToMBench evaluation

---

## Citation

If using these resources, please cite the original papers. See `papers/README.md` and `datasets/README.md` for full citation information.
