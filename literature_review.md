# Literature Review: Do LLMs Differentiate Epistemic Belief from Non-Epistemic Belief?

## Executive Summary

This literature review synthesizes research on whether large language models (LLMs) can differentiate between **epistemic beliefs** (beliefs about knowledge, truth, and justification) and **non-epistemic beliefs** (beliefs about preferences, desires, emotions, and other mental states). The evidence suggests that while LLMs demonstrate some Theory of Mind capabilities, they exhibit significant limitations in distinguishing these belief types, particularly for first-person epistemic states and psychological mental states.

---

## 1. Research Area Overview

### 1.1 Key Concepts

**Epistemic Belief**: Beliefs about knowledge, facts, and truth. Examples:
- "I know that Paris is the capital of France"
- "I believe that it will rain tomorrow"
- "She knows where the keys are"

**Non-Epistemic Belief**: Beliefs about preferences, desires, emotions, and attitudes. Examples:
- "I prefer coffee over tea"
- "He wants to go home"
- "She feels happy about the news"

**Theory of Mind (ToM)**: The cognitive capacity to attribute mental states (beliefs, desires, intentions) to oneself and others. ToM evaluation in AI has become a key benchmark for social intelligence.

### 1.2 Why This Distinction Matters

As LLMs are deployed in healthcare, law, counseling, and education, their ability to:
1. Acknowledge users' false beliefs without dismissing them
2. Distinguish between what a user knows vs. believes
3. Track different types of mental states across conversation

...becomes critical for safe and effective human-AI interaction.

---

## 2. Key Papers and Findings

### 2.1 Core Epistemic Reasoning Research

#### Belief in the Machine: KaBLE Benchmark (Suzgun et al., 2024)

**Citation**: arXiv:2410.21195, Nature Machine Intelligence 2025

**Key Contribution**: The Knowledge and Belief Language Evaluation (KaBLE) benchmark systematically tests LLMs' ability to distinguish between fact, belief, and knowledge.

**Methodology**:
- 13,000 questions across 13 tasks
- 10 disciplines: history, literature, medicine, law, etc.
- Each factual statement paired with false version
- Tests first-person, third-person, and recursive knowledge

**Key Findings**:
| Condition | Accuracy |
|-----------|----------|
| Factual scenarios | 85.7% |
| False scenarios | 54.4% (first-person) |
| First-person belief | 54.4% |
| Third-person belief | 80.7% |
| GPT-4o on true beliefs | 98.2% |
| GPT-4o on false beliefs | 64.4% |

**Critical Insight**: LLMs struggle to affirm that someone holds a false belief, especially in first person. They exhibit a "factual bias" - preferring to correct false statements rather than acknowledge them as beliefs.

**Implications for Research Question**: LLMs do NOT robustly differentiate epistemic states. They treat "I believe X" as a prompt to fact-check rather than acknowledge the belief state.

---

#### Standards for Belief Representations in LLMs (Bowen et al., 2025)

**Citation**: arXiv:2405.21030, Minds and Machines

**Key Contribution**: Proposes four criteria for measuring belief-like representations in LLMs:
1. **Accuracy**: Representations reflect consistent internal models
2. **Coherence**: Beliefs maintain logical consistency
3. **Uniformity**: Representations are stable across contexts
4. **Use**: Beliefs functionally influence outputs

**Key Insight**: Using any criterion in isolation is insufficient. Current LLMs may have belief-like representations but lack the structured relationship between knowledge, belief, and truth that humans have.

---

### 2.2 Theory of Mind Benchmarks

#### OpenToM (Xu et al., 2024)

**Citation**: arXiv:2402.06044, ACL 2024

**Key Contribution**: Tests both physical and psychological mental states:
- **Location questions** (epistemic): Where does X think the object is?
- **Attitude questions** (non-epistemic): How does X feel about the event?

**Methodology**:
- 696 narratives with explicit personality traits
- 13,708+ questions
- Characters have stated preferences and intentions

**Key Findings**:
- LLMs excel at physical world mental states (location tracking)
- LLMs struggle with psychological world mental states (attitudes)
- Macro-averaged F1 recommended due to label imbalance

**Implications**: This benchmark explicitly distinguishes epistemic (location beliefs) from non-epistemic (attitude beliefs), making it ideal for testing our research question.

---

#### ToMBench (Chen et al., 2024)

**Citation**: arXiv:2402.15052, ACL 2024

**Key Contribution**: Comprehensive evaluation of 31 ToM abilities across 8 tasks.

**Task Categories**:
1. False Belief Task (epistemic)
2. Strange Story Task (communication)
3. Faux-pas Recognition (social cognition)
4. Emotion Tasks (non-epistemic)
5. Desire/Intention Tasks (non-epistemic)

**Key Findings**:
- GPT-4 lags behind humans by >10%
- Emotion and desire tasks show different error patterns than belief tasks
- Bilingual evaluation reveals cross-linguistic consistency

---

#### FANToM (Kim et al., 2023)

**Citation**: arXiv:2310.15421, EMNLP 2023

**Key Contribution**: Tests ToM in conversational, information-asymmetric contexts.

**Key Findings**:
- LLMs perform 70%+ worse than humans
- Chain-of-thought reasoning doesn't help
- Multiple question types targeting same reasoning reveal inconsistency

**Critical Insight**: LLM ToM may be "illusory" - pattern matching rather than genuine mental state tracking.

---

#### Kosinski (2023/2024)

**Citation**: arXiv:2302.02083, PNAS 2024

**Key Contribution**: First systematic evaluation of LLM false-belief task performance.

**Key Findings**:
- GPT-4 solved 75% of false-belief tasks (6-year-old level)
- Earlier models solved 0-20%
- ToM may emerge as unintended consequence of language model scaling

**Caveat**: Later work (FANToM, ToMBench) showed this performance is fragile and inconsistent.

---

### 2.3 Epistemic Language Understanding

#### LaBToM (2024)

**Citation**: arXiv:2408.12022

**Key Contribution**: Language-augmented Bayesian Theory of Mind model for understanding epistemic language.

**Approach**:
- Translates natural language to epistemic "language of thought"
- Uses grammar-constrained LLM decoding
- Grounds in generative model of rational action

**Key Findings**:
- LaBToM correlates strongly with human judgments on epistemic expressions
- GPT-4o and Gemini Pro struggle with epistemic language
- Modal expressions (might, could, must) are particularly challenging

**Implications**: Pure LLMs lack the grounding needed for epistemic language; hybrid approaches with explicit reasoning models may be needed.

---

### 2.4 Dynamic Belief Tracking

#### DEL-ToM (Wu et al., 2025)

**Citation**: arXiv:2505.17348, EMNLP 2025

**Key Contribution**: Uses Dynamic Epistemic Logic for structured ToM reasoning.

**Approach**:
- Decomposes ToM into belief update steps
- Process Belief Model verifies each step
- Inference-time scaling without retraining

**Key Findings**:
- Formal logical structure improves ToM performance
- More transparent and verifiable reasoning traces
- Works across model sizes

---

#### Belief History ToM (2024)

**Citation**: arXiv:2406.04800

**Key Contribution**: Tests belief tracking across temporal conditions.

**Conditions**:
- Zero Belief History: Latest beliefs only
- Finite Belief History: Known history
- Infinite Belief History: Full tracking

**Key Findings**:
- Zero history easier than finite
- Dynamic tracking remains challenging
- Smaller models sometimes outperform larger ones

---

### 2.5 Epistemic Calibration

#### Epistemic Integrity in LLMs (Ghafouri et al., 2024)

**Citation**: arXiv:2411.06528

**Key Contribution**: Addresses epistemic miscalibration - confidence vs. accuracy mismatch.

**Key Findings**:
- LLMs express high linguistic confidence even when wrong
- Stark misalignment between stated certainty and accuracy
- Critical for trustworthy deployment

---

## 3. Synthesis: Common Methodologies

### 3.1 Evaluation Approaches

| Approach | Examples | Strengths | Limitations |
|----------|----------|-----------|-------------|
| False-belief tasks | Kosinski, ToMi | Classic ToM test | May be "solved" by pattern matching |
| Narrative comprehension | OpenToM, ToMBench | Rich context | Long narratives costly to process |
| Conversational | FANToM | Naturalistic | Complex setup |
| Direct epistemic probing | KaBLE | Precise | May lack ecological validity |
| Formal logic | DEL-ToM | Verifiable | Requires structured input |

### 3.2 Common Metrics

- **Accuracy**: Overall correct responses
- **Macro-F1**: Balanced across classes (preferred for imbalanced labels)
- **Task completion rate**: All scenarios in a task correct
- **Error analysis**: First vs. third person, true vs. false beliefs

### 3.3 Standard Baselines

- **Random chance**: Task-dependent (33% for 3-way, 50% for binary)
- **Human performance**: ~85-95% across ToM benchmarks
- **GPT-4/Claude-3**: Current SOTA, ~75% on most benchmarks
- **6-year-old children**: Reference for developmental ToM

---

## 4. Standard Datasets

| Dataset | Size | Focus | Format | Availability |
|---------|------|-------|--------|--------------|
| KaBLE | 13,000 | Epistemic reasoning | JSONL | GitHub, HuggingFace |
| OpenToM | 16,008 | ToM in narratives | JSON | GitHub, HuggingFace |
| ToMBench | 2,860 | Comprehensive ToM | JSONL | GitHub |
| ToMi | Generated | Classic ToM | Text | GitHub |
| FANToM | - | Conversational ToM | - | Website |
| Hi-ToM | - | Higher-order ToM | - | HuggingFace |

---

## 5. Gaps and Opportunities

### 5.1 Identified Gaps

1. **Direct Epistemic vs. Non-Epistemic Comparison**: No benchmark explicitly contrasts performance on epistemic belief tasks vs. non-epistemic mental state tasks using matched stimuli.

2. **First-Person Epistemic States**: KaBLE shows first-person is harder, but mechanisms unknown. Why do LLMs refuse to acknowledge "I believe X (false)"?

3. **Belief Persistence**: How do LLMs handle contradictory beliefs stated at different times? Does the model maintain separate belief representations?

4. **Grounded Epistemic Reasoning**: Current LLMs lack grounding in observation and action; they can't truly "know" in the epistemological sense.

5. **Cross-Modal Consistency**: Do LLMs show same epistemic/non-epistemic patterns across different prompt formulations?

### 5.2 Research Opportunities

1. **Contrastive Evaluation**: Design matched pairs of epistemic and non-epistemic questions on same scenarios
2. **Mechanistic Analysis**: Probe internal representations for belief-type encoding
3. **Intervention Studies**: Can prompting strategies improve epistemic differentiation?
4. **Hybrid Approaches**: Combine LLMs with formal epistemic logic (like DEL-ToM)

---

## 6. Recommendations for Our Experiment

### 6.1 Primary Dataset: KaBLE

**Rationale**: Directly tests epistemic reasoning with factual vs. false belief distinction.

**Key Tasks for Experiment**:
- `confirmation-of-first-person-belief` - Tests epistemic self-awareness
- `verification-of-first-person-knowledge` - Tests knowledge vs. belief
- `confirmation-of-third-person-belief-*` - Tests perspective-taking

**Experimental Design**:
1. Evaluate LLMs on epistemic tasks
2. Analyze error patterns (factual vs. false, first vs. third person)
3. Compare with human performance from paper

### 6.2 Secondary Dataset: OpenToM

**Rationale**: Provides matched epistemic (location) vs. non-epistemic (attitude) questions.

**Key Comparison**:
- Location questions → Epistemic belief about physical world
- Attitude questions → Non-epistemic mental states (preferences, emotions)

**Experimental Design**:
1. Extract matched pairs of location and attitude questions
2. Compare accuracy across belief types
3. Analyze whether errors correlate or differ

### 6.3 Evaluation Metrics

1. **Accuracy by belief type** (epistemic vs. non-epistemic)
2. **First-person vs. third-person gap**
3. **True vs. false belief gap** (for epistemic)
4. **Macro-F1** for imbalanced classes
5. **Confidence calibration** (if model provides probabilities)

### 6.4 Models to Evaluate

Based on literature:
- GPT-4 / GPT-4o (state-of-the-art reference)
- Claude-3 Opus/Sonnet (comparison)
- Llama-3 70B (open-source comparison)
- Smaller models for scaling analysis

### 6.5 Baseline Comparisons

- Random chance
- Human performance (from papers)
- Published model scores from KaBLE, OpenToM, ToMBench papers

---

## 7. Key Takeaways

1. **LLMs show partial ToM**: They can solve many false-belief tasks but fail on subtle variations.

2. **Epistemic reasoning is fragile**: High accuracy on factual beliefs, poor on false beliefs, especially first-person.

3. **Non-epistemic states are harder**: Psychological mental states (attitudes, emotions) are more challenging than physical world beliefs.

4. **Pattern matching vs. understanding**: Evidence suggests LLMs use linguistic cues rather than genuine mental state reasoning.

5. **First-person is uniquely challenging**: LLMs struggle to acknowledge their own (or a speaker's) false beliefs.

6. **Calibration is poor**: LLMs express high confidence even on uncertain epistemic claims.

7. **Formal structure helps**: DEL-ToM shows that explicit epistemic logic improves performance.

---

## 8. References

### Primary Papers
1. Suzgun et al. (2024). "Belief in the Machine: Investigating Epistemological Blind Spots of Language Models." arXiv:2410.21195
2. Kosinski (2023). "Evaluating Large Language Models in Theory of Mind Tasks." arXiv:2302.02083
3. Xu et al. (2024). "OpenToM: A Comprehensive Benchmark for Evaluating Theory-of-Mind Reasoning." ACL 2024
4. Chen et al. (2024). "ToMBench: Benchmarking Theory of Mind in Large Language Models." ACL 2024
5. Kim et al. (2023). "FANToM: A Benchmark for Stress-Testing Machine Theory of Mind." EMNLP 2023

### Additional Papers
6. Bowen et al. (2025). "Standards for Belief Representations in LLMs." Minds and Machines
7. LaBToM (2024). "Understanding Epistemic Language with Bayesian Theory of Mind." arXiv:2408.12022
8. Wu et al. (2025). "DEL-ToM: Inference-Time Scaling for Theory-of-Mind via Dynamic Epistemic Logic." arXiv:2505.17348
9. Ghafouri et al. (2024). "Epistemic Integrity in Large Language Models." arXiv:2411.06528
10. Belief History ToM (2024). "Zero, Finite, and Infinite Belief History of ToM Reasoning in LLMs." arXiv:2406.04800
