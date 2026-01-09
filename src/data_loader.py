"""
Data loading and preprocessing for epistemic belief experiments.
Loads KaBLE and OpenToM datasets and prepares samples for evaluation.
"""

import json
import random
from pathlib import Path
from typing import List, Dict, Any

# Set random seed for reproducibility
random.seed(42)

DATASET_DIR = Path(__file__).parent.parent / "datasets"


def load_kable_task(task_name: str, sample_size: int = None) -> List[Dict[str, Any]]:
    """
    Load a KaBLE task from JSONL file.

    Args:
        task_name: Name of the task file (without .jsonl extension)
        sample_size: Number of samples to load (None = all)

    Returns:
        List of task samples
    """
    filepath = DATASET_DIR / "kable" / f"{task_name}.jsonl"
    samples = []

    with open(filepath, 'r') as f:
        for line in f:
            samples.append(json.loads(line))

    if sample_size and sample_size < len(samples):
        samples = random.sample(samples, sample_size)

    return samples


def load_opentom(sample_size_per_type: int = None) -> Dict[str, List[Dict[str, Any]]]:
    """
    Load OpenToM dataset and organize by question type.

    Args:
        sample_size_per_type: Number of samples per question type (None = all)

    Returns:
        Dictionary with question types as keys and sample lists as values
    """
    filepath = DATASET_DIR / "opentom" / "opentom.json"

    with open(filepath, 'r') as f:
        data = json.load(f)

    # Organize by question type
    by_type = {}
    for sample in data:
        qtype = sample['question']['type']
        if qtype not in by_type:
            by_type[qtype] = []
        by_type[qtype].append(sample)

    # Sample if requested
    if sample_size_per_type:
        for qtype in by_type:
            if len(by_type[qtype]) > sample_size_per_type:
                by_type[qtype] = random.sample(by_type[qtype], sample_size_per_type)

    return by_type


def prepare_kable_samples(sample_size: int = 100) -> Dict[str, List[Dict]]:
    """
    Prepare balanced samples from KaBLE for evaluation.

    Returns samples organized by:
    - first_person_belief: First-person belief confirmation (epistemic, 1st person)
    - third_person_belief: Third-person belief confirmation (epistemic, 3rd person)
    - first_person_knowledge: First-person knowledge verification (epistemic)

    Each sample includes both factual (true) and non-factual (false) beliefs.
    """
    tasks = {
        "first_person_belief": "confirmation-of-first-person-belief",
        "third_person_belief": "confirmation-of-third-person-belief-james",
        "first_person_knowledge": "verification-of-first-person-knowledge",
    }

    prepared = {}
    for name, task_file in tasks.items():
        samples = load_kable_task(task_file, sample_size * 2)  # Get more to balance

        # Balance true (factual) and false (non-factual) scenarios
        factual = [s for s in samples if s.get('type') == 'factual']
        non_factual = [s for s in samples if s.get('type') == 'false']

        # Take equal samples from each
        n = min(sample_size // 2, len(factual), len(non_factual))
        balanced = random.sample(factual, n) + random.sample(non_factual, n)
        random.shuffle(balanced)

        prepared[name] = balanced

    return prepared


def prepare_opentom_samples(sample_size: int = 100) -> Dict[str, List[Dict]]:
    """
    Prepare samples from OpenToM for evaluation.

    Returns:
    - location: Location questions (epistemic - where someone thinks something is)
    - attitude: Attitude questions (non-epistemic - how someone feels)
    """
    data = load_opentom()

    prepared = {}

    # Location questions (epistemic) - only Yes/No format for cleaner comparison
    location_samples = data.get('location-fo', []) + data.get('location-so', [])
    # Filter to only Yes/No answers
    location_samples = [s for s in location_samples
                       if s['question']['answer'] in ['Yes', 'No']]
    if len(location_samples) > sample_size:
        location_samples = random.sample(location_samples, sample_size)
    prepared['location'] = location_samples

    # Attitude questions (non-epistemic)
    attitude_samples = data.get('attitude', [])
    if len(attitude_samples) > sample_size:
        attitude_samples = random.sample(attitude_samples, sample_size)
    prepared['attitude'] = attitude_samples

    return prepared


def get_kable_prompt_and_answer(sample: Dict) -> tuple:
    """Extract prompt and expected answer from KaBLE sample."""
    return sample['query'], sample['answer']


def get_opentom_prompt_and_answer(sample: Dict) -> tuple:
    """
    Create prompt and get expected answer from OpenToM sample.

    For OpenToM, we need to construct the prompt from the narrative and question.
    """
    narrative = sample['narrative']
    question = sample['question']['question']
    answer = sample['question']['answer']
    qtype = sample['question']['type']

    if 'location' in qtype:
        # Location question - answer is Yes/No
        prompt = f"""Read the following story and answer the question.

Story:
{narrative}

Question: {question}

Answer with only "Yes" or "No".
Answer:"""
    else:
        # Attitude question - answer is positive/negative/neutral
        prompt = f"""Read the following story and answer the question about the character's attitude.

Story:
{narrative}

Question: {question}

Answer with only one of: "positive", "negative", or "neutral".
Answer:"""

    return prompt, answer


if __name__ == "__main__":
    # Test data loading
    print("Testing data loaders...")

    # Test KaBLE
    kable = prepare_kable_samples(sample_size=10)
    for task, samples in kable.items():
        print(f"KaBLE {task}: {len(samples)} samples")
        if samples:
            sample = samples[0]
            prompt, answer = get_kable_prompt_and_answer(sample)
            print(f"  Type: {sample.get('type')}")
            print(f"  Expected: {answer}")

    print()

    # Test OpenToM
    opentom = prepare_opentom_samples(sample_size=10)
    for task, samples in opentom.items():
        print(f"OpenToM {task}: {len(samples)} samples")
        if samples:
            sample = samples[0]
            prompt, answer = get_opentom_prompt_and_answer(sample)
            print(f"  Question type: {sample['question']['type']}")
            print(f"  Expected: {answer}")
