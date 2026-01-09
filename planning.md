# Research Plan: Do LLMs Differentiate Epistemic Belief from Non-Epistemic Belief?

## Research Question

Do large language models (LLMs) differentiate between **epistemic beliefs** (beliefs about knowledge, truth, and facts) and **non-epistemic beliefs** (beliefs about preferences, desires, emotions, and attitudes)?

## Background and Motivation

Inspired by Vesga et al.'s argument that humans have different types of beliefs, this research investigates whether LLMs similarly distinguish between belief types. This distinction is critical for:

1. **Safe human-AI interaction**: LLMs deployed in healthcare, law, and counseling must handle users' beliefs appropriately—acknowledging false beliefs without dismissing them, understanding the difference between what someone knows vs. believes.

2. **Cognitive plausibility**: Understanding whether LLMs have human-like belief structures informs theories about emergent intelligence in language models.

3. **Improved AI design**: Identifying gaps in LLM belief processing can guide architectural and training improvements.

### Key Concepts

- **Epistemic belief**: Beliefs about knowledge, facts, and truth (e.g., "I know Paris is the capital of France")
- **Non-epistemic belief**: Beliefs about preferences, desires, and emotions (e.g., "I prefer coffee over tea", "She feels happy")

### Literature Insights

From the literature review (KaBLE paper, OpenToM, ToMBench):
- LLMs show ~85% accuracy on factual scenarios but only ~54% on first-person false beliefs
- Third-person belief tracking (~81%) is easier than first-person (~54%)
- Psychological mental states (attitudes/emotions) are harder than physical-world beliefs (location)
- Pattern matching may explain LLM ToM rather than genuine reasoning

## Hypothesis Decomposition

**Main Hypothesis**: LLMs process epistemic and non-epistemic beliefs differently, showing distinct performance patterns.

**Sub-hypotheses**:

1. **H1 (Epistemic gap)**: LLMs will show a larger performance gap between true and false epistemic beliefs compared to non-epistemic states.

2. **H2 (Perspective asymmetry)**: LLMs will perform better on third-person epistemic beliefs than first-person epistemic beliefs, consistent with KaBLE findings.

3. **H3 (Belief-type differentiation)**: LLMs will show different error patterns for epistemic tasks (location/knowledge) vs. non-epistemic tasks (attitude/preference).

4. **H4 (Factual bias)**: LLMs will exhibit "factual bias"—preferring to fact-check rather than acknowledge someone's false belief.

## Proposed Methodology

### Approach

We will conduct a comparative evaluation using two established benchmarks:

1. **KaBLE**: Tests epistemic reasoning (knowledge, belief, truth)
   - First-person vs. third-person belief confirmation
   - True vs. false belief scenarios

2. **OpenToM**: Tests Theory of Mind with matched epistemic and non-epistemic questions
   - Location questions (epistemic): "Where does X think the object is?"
   - Attitude questions (non-epistemic): "What is X's attitude toward the action?"

### Experimental Steps

1. **Data Preparation**
   - Sample from KaBLE tasks: first-person belief, third-person belief, knowledge verification
   - Sample from OpenToM: location questions and attitude questions
   - Ensure balanced true/false scenarios for KaBLE
   - Sample size: 100-200 samples per task (resource-constrained)

2. **Model Selection**
   - GPT-4.1 (via OpenAI API) - SOTA closed model
   - Claude Sonnet 4 (via Anthropic API) - comparison closed model
   - Test 2 models to identify consistent patterns vs. model-specific behaviors

3. **Evaluation Protocol**
   - Zero-shot prompting with original task format
   - Parse model responses to extract answers (A/B/C or positive/negative/neutral)
   - Calculate accuracy, precision, recall, F1 per condition
   - Run each sample once (deterministic at temperature=0)

4. **Statistical Analysis**
   - Compare accuracy across epistemic vs. non-epistemic tasks
   - Chi-squared tests for independence between belief type and accuracy
   - Effect size (Cramer's V) for practical significance
   - Error pattern analysis (qualitative)

### Baselines

1. **Random chance**: 33% for 3-way (KaBLE), 50% for binary, ~33% for 3-way (attitude)
2. **Human performance**: ~85-95% from literature
3. **Published model scores**: GPT-4 ~75% on ToM tasks (from FANToM, ToMBench)

### Evaluation Metrics

| Metric | Purpose |
|--------|---------|
| Accuracy | Overall correctness |
| Accuracy by belief type | Epistemic vs. non-epistemic comparison |
| True/False belief gap | Factual bias quantification |
| First/Third person gap | Perspective asymmetry |
| Macro-F1 | Balanced metric for imbalanced classes |

### Statistical Analysis Plan

- **Primary analysis**: Compare accuracy between epistemic and non-epistemic conditions using chi-squared test
- **Significance level**: α = 0.05
- **Multiple comparison correction**: Bonferroni for multiple comparisons
- **Effect size**: Report Cramer's V (small: 0.1, medium: 0.3, large: 0.5)

## Expected Outcomes

| Hypothesis | Support Evidence | Refute Evidence |
|------------|-----------------|-----------------|
| H1 (Epistemic gap) | Larger true-false gap for epistemic | Similar gaps across belief types |
| H2 (Perspective asymmetry) | 3rd person > 1st person accuracy | Similar accuracy across perspectives |
| H3 (Differentiation) | Different error patterns | Similar error types |
| H4 (Factual bias) | False belief rejection | Equal performance on true/false |

## Timeline and Milestones

1. Phase 1 (Planning): This document (10 min) ✓
2. Phase 2 (Implementation): Data loading, API integration (30 min)
3. Phase 3 (Experiments): Run evaluations (45 min)
4. Phase 4 (Analysis): Statistical tests, visualizations (30 min)
5. Phase 5 (Documentation): REPORT.md (20 min)

## Potential Challenges

| Challenge | Mitigation |
|-----------|------------|
| API rate limits | Use exponential backoff, cache responses |
| Response parsing | Robust regex extraction, log failures |
| Sample size constraints | Focus on effect sizes, acknowledge limitations |
| Model API unavailability | Test with available models |

## Success Criteria

1. **Minimum**: Complete evaluation on 100+ samples per condition with statistical tests
2. **Target**: Clear evidence for/against differentiation hypothesis with visualizations
3. **Stretch**: Cross-model consistency analysis showing robust findings

## Resource Requirements

- **APIs**: OpenAI (GPT-4.1), Anthropic (Claude), or OpenRouter
- **Compute**: CPU sufficient (API-based)
- **Estimated API cost**: ~$20-50 for ~2000 API calls

## Data Files

```
datasets/
├── kable/
│   ├── confirmation-of-first-person-belief.jsonl (1000 samples)
│   ├── confirmation-of-third-person-belief-james.jsonl (1000 samples)
│   ├── verification-of-first-person-knowledge.jsonl (1000 samples)
│   └── ... (13 tasks total)
├── opentom/
│   └── opentom.json (13,708 samples)
│       - attitude: 596 samples (non-epistemic)
│       - location-fo: 3576 samples (epistemic)
│       - location-so: 2384 samples (epistemic)
```
