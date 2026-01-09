# Do LLMs Differentiate Epistemic Belief from Non-Epistemic Belief?

This repository contains research investigating whether large language models (LLMs) distinguish between epistemic beliefs (about knowledge/facts) and non-epistemic beliefs (about preferences/attitudes/emotions).

## Key Findings

Using GPT-4.1 on KaBLE and OpenToM benchmarks (500 samples total):

- **Factual Bias**: 100% accuracy on true beliefs vs 74% on first-person false beliefs (p<0.001)
- **Perspective Asymmetry**: Third-person beliefs (97%) > First-person beliefs (87%) (p=0.019)
- **Critical Failure**: 0% accuracy on first-person false knowledge statements
- **Epistemic Advantage**: Location tasks (65%) > Attitude tasks (53%), though not significant (p=0.114)

**Bottom line**: LLMs partially differentiate belief types but exhibit systematic biases that compromise nuanced mental state reasoning.

## Quick Start

```bash
# Create environment
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt

# Run experiments
export OPENAI_API_KEY="your-key"
python src/run_experiments.py

# Analyze results
python src/analyze_results.py
```

## Results

| Task | Accuracy | Key Insight |
|------|----------|-------------|
| First-person belief | 87% | Struggles with false beliefs |
| Third-person belief | 97% | Easier perspective-taking |
| First-person knowledge | 49% | Complete failure on false (0%) |
| Location (epistemic) | 65% | Moderately challenging |
| Attitude (non-epistemic) | 53% | Near chance, very challenging |

## Project Structure

```
├── REPORT.md           # Full research report
├── planning.md         # Experimental design
├── src/                # Python implementation
├── results/            # Experiment outputs
├── figures/            # Visualizations
└── datasets/           # KaBLE and OpenToM data
```

## Citation

Based on datasets from:
- Suzgun et al. (2024). KaBLE Benchmark
- Xu et al. (2024). OpenToM Benchmark

## License

Research code for academic purposes. See individual dataset licenses.
