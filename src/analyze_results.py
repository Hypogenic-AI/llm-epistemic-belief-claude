"""
Statistical analysis and visualization for epistemic belief experiments.
"""

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from pathlib import Path

# Set style for plots
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12

RESULTS_DIR = Path(__file__).parent.parent / "results"
FIGURES_DIR = Path(__file__).parent.parent / "figures"


def load_results(filepath: str = None) -> dict:
    """Load experiment results from JSON."""
    if filepath is None:
        filepath = RESULTS_DIR / "latest_results.json"
    with open(filepath) as f:
        return json.load(f)


def create_results_dataframe(data: dict) -> pd.DataFrame:
    """Convert results to DataFrame for analysis."""
    records = []
    for result in data['results']:
        records.append({
            'task_type': result['task_type'],
            'belief_type': result['belief_type'],
            'correct': result['correct'],
            'expected': result['expected'],
            'parsed_answer': result['parsed_answer'],
        })
    return pd.DataFrame(records)


def compute_accuracy_with_ci(df: pd.DataFrame, confidence: float = 0.95) -> dict:
    """
    Compute accuracy with confidence interval using Wilson score.

    Wilson score interval is better for proportions near 0 or 1.
    """
    n = len(df)
    p = df['correct'].mean()

    # Wilson score interval
    z = stats.norm.ppf((1 + confidence) / 2)
    denominator = 1 + z**2 / n
    centre = (p + z**2 / (2 * n)) / denominator
    margin = z * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denominator

    return {
        'accuracy': p,
        'n': n,
        'ci_lower': max(0, centre - margin),
        'ci_upper': min(1, centre + margin),
    }


def chi_squared_test(df1: pd.DataFrame, df2: pd.DataFrame) -> dict:
    """
    Perform chi-squared test for independence between two groups.

    Tests whether accuracy differs significantly between groups.
    """
    # Create contingency table
    correct1 = df1['correct'].sum()
    incorrect1 = len(df1) - correct1
    correct2 = df2['correct'].sum()
    incorrect2 = len(df2) - correct2

    contingency = np.array([[correct1, incorrect1], [correct2, incorrect2]])

    chi2, p_value, dof, expected = stats.chi2_contingency(contingency)

    # Cramer's V for effect size
    n = contingency.sum()
    min_dim = min(contingency.shape) - 1
    cramers_v = np.sqrt(chi2 / (n * min_dim)) if n * min_dim > 0 else 0

    return {
        'chi2': chi2,
        'p_value': p_value,
        'dof': dof,
        'cramers_v': cramers_v,
        'effect_interpretation': interpret_cramers_v(cramers_v),
    }


def interpret_cramers_v(v: float) -> str:
    """Interpret Cramer's V effect size."""
    if v < 0.1:
        return "negligible"
    elif v < 0.3:
        return "small"
    elif v < 0.5:
        return "medium"
    else:
        return "large"


def analyze_hypothesis_1(df: pd.DataFrame) -> dict:
    """
    H1: LLMs show larger true-false gap for epistemic beliefs.

    Compare true-false accuracy gap across belief tasks.
    """
    results = {}

    # KaBLE tasks (epistemic)
    kable_tasks = ['first_person_belief', 'third_person_belief', 'first_person_knowledge']

    for task in kable_tasks:
        task_df = df[df['task_type'] == task]
        factual = task_df[task_df['belief_type'] == 'factual']
        false = task_df[task_df['belief_type'] == 'false']

        if len(factual) > 0 and len(false) > 0:
            factual_acc = factual['correct'].mean()
            false_acc = false['correct'].mean()
            gap = factual_acc - false_acc

            # Chi-squared test for significance
            test_result = chi_squared_test(factual, false)

            results[task] = {
                'factual_accuracy': factual_acc,
                'false_accuracy': false_acc,
                'gap': gap,
                **test_result
            }

    return results


def analyze_hypothesis_2(df: pd.DataFrame) -> dict:
    """
    H2: Third-person epistemic beliefs easier than first-person.

    Compare first_person_belief vs third_person_belief accuracy.
    """
    first_person = df[df['task_type'] == 'first_person_belief']
    third_person = df[df['task_type'] == 'third_person_belief']

    first_acc = compute_accuracy_with_ci(first_person)
    third_acc = compute_accuracy_with_ci(third_person)
    test_result = chi_squared_test(first_person, third_person)

    return {
        'first_person': first_acc,
        'third_person': third_acc,
        'gap': third_acc['accuracy'] - first_acc['accuracy'],
        **test_result
    }


def analyze_hypothesis_3(df: pd.DataFrame) -> dict:
    """
    H3: Different patterns for epistemic vs non-epistemic tasks.

    Compare location (epistemic) vs attitude (non-epistemic) in OpenToM.
    """
    location = df[df['task_type'] == 'location']
    attitude = df[df['task_type'] == 'attitude']

    location_acc = compute_accuracy_with_ci(location)
    attitude_acc = compute_accuracy_with_ci(attitude)
    test_result = chi_squared_test(location, attitude)

    return {
        'location_epistemic': location_acc,
        'attitude_non_epistemic': attitude_acc,
        'gap': location_acc['accuracy'] - attitude_acc['accuracy'],
        **test_result
    }


def create_accuracy_comparison_plot(df: pd.DataFrame):
    """Create bar plot comparing accuracies across tasks."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # KaBLE tasks
    kable_data = []
    for task in ['first_person_belief', 'third_person_belief', 'first_person_knowledge']:
        task_df = df[df['task_type'] == task]
        for btype in ['factual', 'false']:
            subset = task_df[task_df['belief_type'] == btype]
            if len(subset) > 0:
                acc = compute_accuracy_with_ci(subset)
                kable_data.append({
                    'task': task.replace('_', '\n'),
                    'belief_type': btype,
                    'accuracy': acc['accuracy'],
                    'ci_lower': acc['ci_lower'],
                    'ci_upper': acc['ci_upper'],
                })

    kable_df = pd.DataFrame(kable_data)

    # Plot KaBLE results
    ax1 = axes[0]
    width = 0.35
    tasks = kable_df['task'].unique()
    x = np.arange(len(tasks))

    factual = kable_df[kable_df['belief_type'] == 'factual']
    false = kable_df[kable_df['belief_type'] == 'false']

    bars1 = ax1.bar(x - width/2, factual['accuracy'], width, label='Factual (True)',
                    color='#2ecc71', alpha=0.8)
    bars2 = ax1.bar(x + width/2, false['accuracy'], width, label='False',
                    color='#e74c3c', alpha=0.8)

    # Error bars - ensure non-negative values
    factual_yerr_lower = np.maximum(0, factual['accuracy'].values - factual['ci_lower'].values)
    factual_yerr_upper = np.maximum(0, factual['ci_upper'].values - factual['accuracy'].values)
    false_yerr_lower = np.maximum(0, false['accuracy'].values - false['ci_lower'].values)
    false_yerr_upper = np.maximum(0, false['ci_upper'].values - false['accuracy'].values)

    ax1.errorbar(x - width/2, factual['accuracy'].values,
                yerr=[factual_yerr_lower, factual_yerr_upper],
                fmt='none', color='black', capsize=3)
    ax1.errorbar(x + width/2, false['accuracy'].values,
                yerr=[false_yerr_lower, false_yerr_upper],
                fmt='none', color='black', capsize=3)

    ax1.set_ylabel('Accuracy')
    ax1.set_title('KaBLE: Epistemic Belief Tasks\n(True vs False Beliefs)')
    ax1.set_xticks(x)
    ax1.set_xticklabels(tasks, fontsize=10)
    ax1.legend()
    ax1.set_ylim(0, 1.1)
    ax1.axhline(y=0.33, color='gray', linestyle='--', label='Random chance', alpha=0.5)

    # OpenToM comparison
    ax2 = axes[1]
    opentom_data = []
    for task in ['location', 'attitude']:
        task_df = df[df['task_type'] == task]
        acc = compute_accuracy_with_ci(task_df)
        opentom_data.append({
            'task': task.capitalize(),
            'accuracy': acc['accuracy'],
            'ci_lower': acc['ci_lower'],
            'ci_upper': acc['ci_upper'],
        })

    opentom_df = pd.DataFrame(opentom_data)

    colors = ['#3498db', '#9b59b6']
    bars = ax2.bar(opentom_df['task'], opentom_df['accuracy'],
                   color=colors, alpha=0.8)

    opentom_yerr_lower = np.maximum(0, opentom_df['accuracy'].values - opentom_df['ci_lower'].values)
    opentom_yerr_upper = np.maximum(0, opentom_df['ci_upper'].values - opentom_df['accuracy'].values)
    ax2.errorbar(opentom_df['task'], opentom_df['accuracy'].values,
                yerr=[opentom_yerr_lower, opentom_yerr_upper],
                fmt='none', color='black', capsize=5)

    ax2.set_ylabel('Accuracy')
    ax2.set_title('OpenToM: Epistemic vs Non-Epistemic\n(Location vs Attitude)')
    ax2.set_ylim(0, 1.1)
    ax2.axhline(y=0.5, color='gray', linestyle='--', label='Binary chance', alpha=0.5)

    # Add task type labels
    ax2.bar_label(bars, ['Epistemic', 'Non-Epistemic'], padding=3, fontsize=10)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'accuracy_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()

    print(f"Saved: {FIGURES_DIR / 'accuracy_comparison.png'}")


def create_gap_analysis_plot(df: pd.DataFrame):
    """Create plot showing true-false gaps across tasks."""
    fig, ax = plt.subplots(figsize=(10, 6))

    # Calculate gaps for each task
    tasks = ['first_person_belief', 'third_person_belief', 'first_person_knowledge']
    gaps = []
    labels = []

    for task in tasks:
        task_df = df[df['task_type'] == task]
        factual = task_df[task_df['belief_type'] == 'factual']['correct'].mean()
        false = task_df[task_df['belief_type'] == 'false']['correct'].mean()
        gap = factual - false
        gaps.append(gap * 100)  # Convert to percentage
        labels.append(task.replace('_', '\n'))

    colors = ['#e74c3c' if g > 0 else '#2ecc71' for g in gaps]
    bars = ax.bar(labels, gaps, color=colors, alpha=0.8, edgecolor='black')

    ax.set_ylabel('Accuracy Gap (Factual - False) %')
    ax.set_title('Factual Bias: True vs False Belief Performance Gap')
    ax.axhline(y=0, color='black', linewidth=0.5)

    # Add value labels
    for bar, gap in zip(bars, gaps):
        height = bar.get_height()
        ax.annotate(f'{gap:.1f}%',
                   xy=(bar.get_x() + bar.get_width() / 2, height),
                   xytext=(0, 3 if height > 0 else -15),
                   textcoords="offset points",
                   ha='center', va='bottom' if height > 0 else 'top',
                   fontsize=12, fontweight='bold')

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'gap_analysis.png', dpi=150, bbox_inches='tight')
    plt.close()

    print(f"Saved: {FIGURES_DIR / 'gap_analysis.png'}")


def create_perspective_comparison_plot(df: pd.DataFrame):
    """Create plot comparing first-person vs third-person beliefs."""
    fig, ax = plt.subplots(figsize=(8, 6))

    # Get data
    first_person = df[df['task_type'] == 'first_person_belief']
    third_person = df[df['task_type'] == 'third_person_belief']

    # Overall accuracy
    categories = ['First-Person', 'Third-Person']
    accuracies = [first_person['correct'].mean(), third_person['correct'].mean()]

    colors = ['#f39c12', '#27ae60']
    bars = ax.bar(categories, [a * 100 for a in accuracies], color=colors, alpha=0.8,
                  edgecolor='black', linewidth=1.5)

    ax.set_ylabel('Accuracy (%)')
    ax.set_title('Perspective Asymmetry in Epistemic Belief Confirmation\n(KaBLE Dataset)')
    ax.set_ylim(0, 110)

    # Add value labels
    for bar, acc in zip(bars, accuracies):
        height = bar.get_height()
        ax.annotate(f'{acc:.1%}',
                   xy=(bar.get_x() + bar.get_width() / 2, height),
                   xytext=(0, 3),
                   textcoords="offset points",
                   ha='center', va='bottom',
                   fontsize=14, fontweight='bold')

    # Add gap annotation
    gap = accuracies[1] - accuracies[0]
    mid_y = (accuracies[0] + accuracies[1]) / 2 * 100
    ax.annotate('', xy=(1, accuracies[1] * 100), xytext=(0, accuracies[0] * 100),
               arrowprops=dict(arrowstyle='<->', color='red', lw=2))
    ax.annotate(f'Gap: {gap:.1%}', xy=(0.5, mid_y), ha='center', fontsize=12,
               color='red', fontweight='bold')

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'perspective_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()

    print(f"Saved: {FIGURES_DIR / 'perspective_comparison.png'}")


def run_full_analysis():
    """Run complete analysis and generate all outputs."""
    FIGURES_DIR.mkdir(exist_ok=True)

    # Load data
    data = load_results()
    df = create_results_dataframe(data)

    print("=" * 60)
    print("STATISTICAL ANALYSIS")
    print("=" * 60)

    # H1: True-False Gap Analysis
    print("\n--- H1: True vs False Belief Gap ---")
    h1_results = analyze_hypothesis_1(df)
    for task, result in h1_results.items():
        print(f"\n{task}:")
        print(f"  Factual accuracy: {result['factual_accuracy']:.2%}")
        print(f"  False accuracy: {result['false_accuracy']:.2%}")
        print(f"  Gap: {result['gap']:.2%}")
        print(f"  Chi-squared: {result['chi2']:.2f}, p={result['p_value']:.4f}")
        print(f"  Effect size (Cramer's V): {result['cramers_v']:.3f} ({result['effect_interpretation']})")

    # H2: Perspective Asymmetry
    print("\n--- H2: First vs Third Person ---")
    h2_results = analyze_hypothesis_2(df)
    print(f"  First-person accuracy: {h2_results['first_person']['accuracy']:.2%}")
    print(f"  Third-person accuracy: {h2_results['third_person']['accuracy']:.2%}")
    print(f"  Gap: {h2_results['gap']:.2%}")
    print(f"  Chi-squared: {h2_results['chi2']:.2f}, p={h2_results['p_value']:.4f}")
    print(f"  Effect size: {h2_results['cramers_v']:.3f} ({h2_results['effect_interpretation']})")

    # H3: Epistemic vs Non-Epistemic
    print("\n--- H3: Epistemic vs Non-Epistemic (OpenToM) ---")
    h3_results = analyze_hypothesis_3(df)
    print(f"  Location (epistemic): {h3_results['location_epistemic']['accuracy']:.2%}")
    print(f"  Attitude (non-epistemic): {h3_results['attitude_non_epistemic']['accuracy']:.2%}")
    print(f"  Gap: {h3_results['gap']:.2%}")
    print(f"  Chi-squared: {h3_results['chi2']:.2f}, p={h3_results['p_value']:.4f}")
    print(f"  Effect size: {h3_results['cramers_v']:.3f} ({h3_results['effect_interpretation']})")

    # Generate visualizations
    print("\n--- Generating Visualizations ---")
    create_accuracy_comparison_plot(df)
    create_gap_analysis_plot(df)
    create_perspective_comparison_plot(df)

    # Save analysis summary
    analysis_summary = {
        'model': data['model'],
        'total_samples': len(df),
        'overall_accuracy': df['correct'].mean(),
        'h1_true_false_gap': h1_results,
        'h2_perspective_asymmetry': h2_results,
        'h3_epistemic_vs_non_epistemic': h3_results,
    }

    with open(RESULTS_DIR / 'analysis_summary.json', 'w') as f:
        json.dump(analysis_summary, f, indent=2, default=float)

    print(f"\nSaved analysis summary: {RESULTS_DIR / 'analysis_summary.json'}")

    return analysis_summary


if __name__ == "__main__":
    run_full_analysis()
