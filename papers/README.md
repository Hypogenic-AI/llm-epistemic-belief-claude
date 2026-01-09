# Downloaded Papers

This directory contains academic papers relevant to the research question: "Do LLMs differentiate epistemic belief from non-epistemic belief?"

## Papers Index

| # | File | Title | Year | Key Contribution |
|---|------|-------|------|------------------|
| 1 | 2410.21195_belief_in_machine_kable.pdf | Belief in the Machine: Investigating Epistemological Blind Spots of Language Models | 2024 | KaBLE benchmark for epistemic reasoning |
| 2 | 2302.02083_llm_theory_of_mind.pdf | Evaluating Large Language Models in Theory of Mind Tasks | 2023 | Foundational ToM evaluation (Kosinski) |
| 3 | 2402.06044_opentom.pdf | OpenToM: A Comprehensive Benchmark for Evaluating Theory-of-Mind Reasoning | 2024 | ToM in narrative contexts (ACL 2024) |
| 4 | 2402.15052_tombench.pdf | ToMBench: Benchmarking Theory of Mind in Large Language Models | 2024 | 31 ToM abilities benchmark (ACL 2024) |
| 5 | 2405.21030_belief_representations.pdf | Standards for Belief Representations in LLMs | 2025 | Criteria for measuring LLM beliefs |
| 6 | 2408.12022_labtom_epistemic.pdf | Understanding Epistemic Language with Bayesian Theory of Mind | 2024 | LaBToM model for epistemic language |
| 7 | 2310.15421_fantom.pdf | FANToM: A Benchmark for Stress-Testing Machine ToM in Conversations | 2023 | Conversational ToM benchmark (EMNLP) |
| 8 | 2406.04800_belief_history_tom.pdf | Zero, Finite, and Infinite Belief History of ToM Reasoning in LLMs | 2024 | Belief tracking across time |
| 9 | 2505.17348_del_tom.pdf | DEL-ToM: Inference-Time Scaling for Theory-of-Mind via Dynamic Epistemic Logic | 2025 | Dynamic epistemic logic for ToM |
| 10 | 2411.06528_epistemic_integrity.pdf | Epistemic Integrity in Large Language Models | 2024 | Epistemic miscalibration in LLMs |

---

## Paper Summaries

### 1. Belief in the Machine (KaBLE) - arXiv:2410.21195
**Authors**: Suzgun, Gur, Bianchi, Ho, Icard, Jurafsky, Zou
**Published**: Nature Machine Intelligence 2025

**Key Contributions**:
- Introduces KaBLE dataset: 13,000 questions across 13 epistemic reasoning tasks
- Tests distinction between fact, belief, and knowledge
- Evaluates 24 LLMs including GPT-4, Claude-3, Llama-3

**Key Findings**:
- LMs achieve 86% on factual scenarios but struggle with false scenarios
- First-person belief tasks (54.4%) harder than third-person (80.7%)
- GPT-4o: 98.2% → 64.4% accuracy drop on false beliefs
- LMs lack robust understanding that knowledge requires truth

**Relevance**: Directly tests the epistemic/non-epistemic distinction. Primary dataset for our research.

---

### 2. Evaluating LLMs in Theory of Mind Tasks - arXiv:2302.02083
**Author**: Kosinski
**Published**: PNAS 2024

**Key Contributions**:
- Custom battery of 640 prompts across 40 false-belief tasks
- Tests 11 LLMs from 2022-2023 era

**Key Findings**:
- GPT-4 solved 75% of tasks (matching 6-year-old children)
- Older models solved 0-20% of tasks
- Suggests ToM may emerge as unintended consequence of scale

**Relevance**: Foundational work establishing LLMs have some ToM capabilities to build upon.

---

### 3. OpenToM - arXiv:2402.06044
**Authors**: Xu, Zhao, Zhu, Du, He
**Published**: ACL 2024

**Key Contributions**:
- 696 narratives with 16,008 questions
- Tests both physical and psychological mental states
- Characters have explicit personality traits and intentions

**Key Findings**:
- LLMs excel at physical world mental states
- LLMs struggle with psychological world mental states
- Attitude questions are particularly challenging

**Relevance**: Tests non-epistemic beliefs (attitudes, preferences) vs epistemic beliefs (knowledge, location).

---

### 4. ToMBench - arXiv:2402.15052
**Authors**: Chen et al.
**Published**: ACL 2024

**Key Contributions**:
- 8 tasks evaluating 31 distinct ToM abilities
- Bilingual (English/Chinese) evaluation
- Standardized multiple-choice format

**Key Findings**:
- Even GPT-4 lags behind humans by >10%
- Covers emotions, desires, intentions, beliefs
- Built from ATOMS framework

**Relevance**: Provides comprehensive baseline for ToM comparison.

---

### 5. Standards for Belief Representations - arXiv:2405.21030
**Authors**: Dillon Bowen et al.
**Published**: Minds and Machines 2025

**Key Contributions**:
- Proposes 4 criteria for LLM belief measurement:
  1. Accuracy - representations reflect consistent internal models
  2. Coherence - beliefs maintain logical consistency
  3. Uniformity - representations are stable and reproducible
  4. Use - beliefs functionally influence outputs

**Key Findings**:
- Individual criteria insufficient in isolation
- Need unified theoretical foundation for belief study

**Relevance**: Theoretical framework for understanding what counts as "belief" in LLMs.

---

### 6. LaBToM (Epistemic Language) - arXiv:2408.12022
**Authors**: Multiple
**Published**: 2024

**Key Contributions**:
- Language-augmented Bayesian Theory-of-Mind model
- Combines LLM decoding with generative model of rational action
- Tests epistemic language understanding

**Key Findings**:
- LaBToM correlates strongly with human judgments
- GPT-4o and Gemini Pro struggle on epistemic expressions
- Grounding in agent reasoning improves predictions

**Relevance**: Shows importance of grounding epistemic language in cognitive models.

---

### 7. FANToM - arXiv:2310.15421
**Authors**: Kim et al.
**Published**: EMNLP 2023

**Key Contributions**:
- Tests ToM in conversational, information-asymmetric contexts
- Multiple question types targeting same underlying reasoning
- Exploits natural information asymmetry in dialogues

**Key Findings**:
- LLMs perform 70%+ worse than humans
- Chain-of-thought and fine-tuning don't help much
- Identifies illusory ToM capabilities

**Relevance**: Shows LLM ToM may be superficial pattern-matching.

---

### 8. Belief History ToM - arXiv:2406.04800
**Authors**: Multiple
**Published**: 2024

**Key Contributions**:
- Tests three conditions: Zero, Finite, Infinite belief history
- "Pick the Right Stuff" game benchmark
- Evaluates 6 LLMs

**Key Findings**:
- Zero belief history easier than finite
- Smaller models sometimes outperform larger ones
- Dynamic belief tracking is challenging

**Relevance**: Tests how LLMs track evolving belief states over time.

---

### 9. DEL-ToM - arXiv:2505.17348
**Authors**: Wu et al.
**Published**: EMNLP 2025

**Key Contributions**:
- Uses Dynamic Epistemic Logic for ToM reasoning
- Inference-time scaling rather than architectural changes
- Process Belief Model (PBM) verifier

**Key Findings**:
- Decomposing ToM into belief updates improves performance
- More transparent reasoning traces
- Works across model sizes

**Relevance**: Formal epistemic logic approach to ToM.

---

### 10. Epistemic Integrity - arXiv:2411.06528
**Authors**: Ghafouri et al.
**Published**: 2024

**Key Contributions**:
- Addresses epistemic miscalibration in LLMs
- New human-labeled dataset for linguistic assertiveness
- Reduces error rates by 50% vs previous benchmarks

**Key Findings**:
- LLMs express high confidence even when wrong
- Stark misalignment between linguistic confidence and accuracy
- Critical for high-stakes applications

**Relevance**: Shows LLMs don't properly calibrate epistemic certainty.

---

## Reading Order Recommendation

For the research question "Do LLMs differentiate epistemic belief from non-epistemic belief?":

1. **Start with**: 2410.21195 (KaBLE) - Core epistemic reasoning evaluation
2. **Then read**: 2302.02083 (Kosinski) - Foundational ToM understanding
3. **Compare with**: 2402.06044 (OpenToM) - Epistemic vs psychological states
4. **Theoretical grounding**: 2405.21030 (Belief Representations) - What counts as belief
5. **Advanced**: 2408.12022 (LaBToM) - Epistemic language modeling
6. **Optional**: Others for specific aspects (DEL-ToM for formal logic, FANToM for conversations)

---

## Key Themes Across Papers

1. **Epistemic vs Doxastic**: Clear distinction between knowledge (requires truth) and belief (may be false)
2. **First vs Third Person**: LLMs struggle more with first-person belief acknowledgment
3. **Physical vs Psychological**: LLMs better at physical world than psychological states
4. **Static vs Dynamic**: Dynamic belief tracking remains challenging
5. **Overconfidence**: LLMs express certainty that doesn't match accuracy
