"""
Main experiment runner for epistemic belief differentiation study.

This script:
1. Loads samples from KaBLE and OpenToM datasets
2. Evaluates LLM responses using OpenAI API
3. Saves results for analysis
"""

import os
import sys
import json
import random
from datetime import datetime
from pathlib import Path
from tqdm import tqdm

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from data_loader import (
    prepare_kable_samples,
    prepare_opentom_samples,
    get_kable_prompt_and_answer,
    get_opentom_prompt_and_answer,
)
from evaluator import LLMEvaluator

# Set random seed
random.seed(42)

# Configuration
SAMPLE_SIZE = 100  # Samples per task (balanced for KaBLE)
RESULTS_DIR = Path(__file__).parent.parent / "results"


def run_kable_evaluation(evaluator: LLMEvaluator, sample_size: int = SAMPLE_SIZE):
    """
    Run evaluation on KaBLE dataset.

    Evaluates:
    - first_person_belief: First-person belief confirmation (epistemic, 1st person)
    - third_person_belief: Third-person belief confirmation (epistemic, 3rd person)
    - first_person_knowledge: Knowledge verification (epistemic)
    """
    print("\n" + "=" * 60)
    print("KaBLE EVALUATION")
    print("=" * 60)

    samples = prepare_kable_samples(sample_size)

    for task_name, task_samples in samples.items():
        print(f"\nEvaluating {task_name} ({len(task_samples)} samples)...")

        for sample in tqdm(task_samples, desc=task_name):
            try:
                result = evaluator.evaluate_kable_sample(sample, task_name)
            except Exception as e:
                print(f"Error on sample: {e}")
                continue

        # Print intermediate results
        task_results = [r for r in evaluator.results if r.task_type == task_name]
        if task_results:
            accuracy = sum(r.correct for r in task_results) / len(task_results)
            print(f"  {task_name} accuracy: {accuracy:.2%}")


def run_opentom_evaluation(evaluator: LLMEvaluator, sample_size: int = SAMPLE_SIZE):
    """
    Run evaluation on OpenToM dataset.

    Evaluates:
    - location: Location questions (epistemic - where someone thinks something is)
    - attitude: Attitude questions (non-epistemic - how someone feels)
    """
    print("\n" + "=" * 60)
    print("OpenToM EVALUATION")
    print("=" * 60)

    samples = prepare_opentom_samples(sample_size)

    for task_name, task_samples in samples.items():
        print(f"\nEvaluating {task_name} ({len(task_samples)} samples)...")

        for sample in tqdm(task_samples, desc=task_name):
            try:
                result = evaluator.evaluate_opentom_sample(sample, task_name)
            except Exception as e:
                print(f"Error on sample: {e}")
                continue

        # Print intermediate results
        task_results = [r for r in evaluator.results if r.task_type == task_name]
        if task_results:
            accuracy = sum(r.correct for r in task_results) / len(task_results)
            print(f"  {task_name} accuracy: {accuracy:.2%}")


def main():
    """Main experiment runner."""
    print("=" * 60)
    print("EPISTEMIC BELIEF DIFFERENTIATION EXPERIMENT")
    print(f"Start time: {datetime.now().isoformat()}")
    print("=" * 60)

    # Create results directory
    RESULTS_DIR.mkdir(exist_ok=True)

    # Initialize evaluator
    evaluator = LLMEvaluator()
    print(f"Model: {evaluator.model}")

    # Run evaluations
    run_kable_evaluation(evaluator, SAMPLE_SIZE)
    run_opentom_evaluation(evaluator, SAMPLE_SIZE)

    # Print summary
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)

    summary = evaluator.get_summary()
    print(f"\nTotal samples: {summary['total']}")
    print(f"Overall accuracy: {summary['overall_accuracy']:.2%}")

    print("\nResults by task:")
    for task, task_summary in summary['by_task'].items():
        print(f"\n  {task}:")
        print(f"    N: {task_summary['n']}")
        print(f"    Accuracy: {task_summary['accuracy']:.2%}")
        print(f"    By belief type:")
        for btype, bsummary in task_summary['by_belief_type'].items():
            print(f"      {btype}: {bsummary['accuracy']:.2%} (n={bsummary['n']})")

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = RESULTS_DIR / f"experiment_results_{timestamp}.json"
    evaluator.save_results(str(results_file))
    print(f"\nResults saved to: {results_file}")

    # Also save a copy as latest
    latest_file = RESULTS_DIR / "latest_results.json"
    evaluator.save_results(str(latest_file))

    return summary


if __name__ == "__main__":
    main()
