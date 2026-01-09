"""
LLM evaluation module for epistemic belief experiments.
Handles API calls to OpenAI models and response parsing.
"""

import os
import re
import json
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import openai


# Configuration
DEFAULT_MODEL = "gpt-4.1"  # Use GPT-4.1 as SOTA reference
FALLBACK_MODEL = "gpt-4o-mini"  # Fallback if quota issues
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds


@dataclass
class EvaluationResult:
    """Result from a single evaluation."""
    sample_id: str
    task_type: str
    belief_type: str  # 'factual' or 'false' for KaBLE, 'location' or 'attitude' for OpenToM
    prompt: str
    expected: str
    response: str
    parsed_answer: str
    correct: bool
    model: str
    timestamp: str


class LLMEvaluator:
    """Evaluator for LLM epistemic belief experiments."""

    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model
        self.client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.results: List[EvaluationResult] = []

    def call_api(self, prompt: str, temperature: float = 0) -> str:
        """
        Call OpenAI API with retry logic.

        Args:
            prompt: The prompt to send
            temperature: Sampling temperature (0 for deterministic)

        Returns:
            Model response text
        """
        for attempt in range(MAX_RETRIES):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    max_tokens=100,  # Short responses expected
                )
                return response.choices[0].message.content.strip()

            except openai.RateLimitError as e:
                if attempt < MAX_RETRIES - 1:
                    print(f"Rate limited, waiting {RETRY_DELAY * (attempt + 1)}s...")
                    time.sleep(RETRY_DELAY * (attempt + 1))
                else:
                    raise e

            except openai.APIError as e:
                if attempt < MAX_RETRIES - 1:
                    print(f"API error: {e}, retrying...")
                    time.sleep(RETRY_DELAY)
                else:
                    raise e

        return ""

    def parse_kable_answer(self, response: str) -> str:
        """
        Parse KaBLE response to extract (A), (B), or (C).

        KaBLE expects responses ending with "So, the answer is (A/B/C)."
        """
        response = response.upper()

        # Look for explicit answer patterns
        patterns = [
            r"THE ANSWER IS\s*\(([ABC])\)",
            r"ANSWER:\s*\(([ABC])\)",
            r"\(([ABC])\)\s*$",
            r"^([ABC])$",
            r"^([ABC])\.",
        ]

        for pattern in patterns:
            match = re.search(pattern, response)
            if match:
                return f"({match.group(1)})"

        # Check for yes/no that maps to A/B
        if "YES" in response and "NO" not in response:
            return "(A)"
        if "NO" in response and "YES" not in response:
            return "(B)"

        return "(?))"  # Unknown/unparseable

    def parse_opentom_location_answer(self, response: str) -> str:
        """Parse OpenToM location response (Yes/No)."""
        response = response.lower().strip()

        if response.startswith("yes"):
            return "Yes"
        if response.startswith("no"):
            return "No"

        # Check within response
        if "yes" in response and "no" not in response:
            return "Yes"
        if "no" in response and "yes" not in response:
            return "No"

        return "Unknown"

    def parse_opentom_attitude_answer(self, response: str) -> str:
        """Parse OpenToM attitude response (positive/negative/neutral)."""
        response = response.lower().strip()

        # Direct matches
        if response.startswith("positive"):
            return "positive"
        if response.startswith("negative"):
            return "negative"
        if response.startswith("neutral"):
            return "neutral"

        # Check within response
        if "positive" in response and "negative" not in response and "neutral" not in response:
            return "positive"
        if "negative" in response and "positive" not in response and "neutral" not in response:
            return "negative"
        if "neutral" in response:
            return "neutral"

        return "unknown"

    def evaluate_kable_sample(
        self,
        sample: Dict,
        task_type: str,
    ) -> EvaluationResult:
        """
        Evaluate a single KaBLE sample.

        Args:
            sample: KaBLE sample dictionary
            task_type: Task name (first_person_belief, third_person_belief, etc.)

        Returns:
            EvaluationResult with evaluation details
        """
        prompt = sample['query']
        expected = sample['answer']
        belief_type = sample.get('type', 'unknown')  # 'factual' or 'false'

        response = self.call_api(prompt)
        parsed = self.parse_kable_answer(response)
        correct = parsed == expected

        result = EvaluationResult(
            sample_id=f"{sample.get('subject', 'unknown')}_{sample.get('idx', 0)}",
            task_type=task_type,
            belief_type=belief_type,
            prompt=prompt[:500],  # Truncate for logging
            expected=expected,
            response=response,
            parsed_answer=parsed,
            correct=correct,
            model=self.model,
            timestamp=datetime.now().isoformat(),
        )

        self.results.append(result)
        return result

    def evaluate_opentom_sample(
        self,
        sample: Dict,
        task_type: str,  # 'location' or 'attitude'
    ) -> EvaluationResult:
        """
        Evaluate a single OpenToM sample.

        Args:
            sample: OpenToM sample dictionary
            task_type: 'location' (epistemic) or 'attitude' (non-epistemic)

        Returns:
            EvaluationResult with evaluation details
        """
        from data_loader import get_opentom_prompt_and_answer

        prompt, expected = get_opentom_prompt_and_answer(sample)

        response = self.call_api(prompt)

        if task_type == 'location':
            parsed = self.parse_opentom_location_answer(response)
        else:
            parsed = self.parse_opentom_attitude_answer(response)

        correct = parsed.lower() == expected.lower()

        result = EvaluationResult(
            sample_id=f"{task_type}_{sample.get('plot_info', {}).get('mover', 'unknown')}",
            task_type=task_type,
            belief_type=sample['question']['type'],
            prompt=prompt[:500],
            expected=expected,
            response=response,
            parsed_answer=parsed,
            correct=correct,
            model=self.model,
            timestamp=datetime.now().isoformat(),
        )

        self.results.append(result)
        return result

    def get_summary(self) -> Dict:
        """Get summary statistics from all results."""
        if not self.results:
            return {}

        # Group by task type
        by_task = {}
        for r in self.results:
            if r.task_type not in by_task:
                by_task[r.task_type] = []
            by_task[r.task_type].append(r)

        summary = {
            "total": len(self.results),
            "overall_accuracy": sum(r.correct for r in self.results) / len(self.results),
            "by_task": {},
        }

        for task, results in by_task.items():
            task_summary = {
                "n": len(results),
                "accuracy": sum(r.correct for r in results) / len(results),
                "by_belief_type": {},
            }

            # Group by belief type within task
            by_belief = {}
            for r in results:
                if r.belief_type not in by_belief:
                    by_belief[r.belief_type] = []
                by_belief[r.belief_type].append(r)

            for belief, bresults in by_belief.items():
                task_summary["by_belief_type"][belief] = {
                    "n": len(bresults),
                    "accuracy": sum(r.correct for r in bresults) / len(bresults),
                }

            summary["by_task"][task] = task_summary

        return summary

    def save_results(self, filepath: str):
        """Save results to JSON file."""
        data = {
            "model": self.model,
            "timestamp": datetime.now().isoformat(),
            "summary": self.get_summary(),
            "results": [asdict(r) for r in self.results],
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)


def test_api_connection():
    """Test API connection with a simple prompt."""
    evaluator = LLMEvaluator()
    try:
        response = evaluator.call_api("Say 'Hello' and nothing else.")
        print(f"API test successful: {response}")
        return True
    except Exception as e:
        print(f"API test failed: {e}")
        return False


if __name__ == "__main__":
    print("Testing evaluator...")
    test_api_connection()
