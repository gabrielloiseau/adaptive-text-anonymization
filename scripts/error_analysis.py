#!/usr/bin/env python3
"""
Error analysis script for anonymization models.

Presents concrete failure cases in both privacy and utility dimensions
across optimized models. Supports TAB, SynthPAI, MedQA, DBBio, and PUPA datasets.
"""

import argparse
import os
import sys
from dataclasses import dataclass, field
from typing import Any

import dspy

os.environ.setdefault("WANDB_DISABLED", "true")


from adaptive_anonymization.tasks import (
    DBBio,
    MedQA,
    PUPA,
    SynthPAI,
    TextAnonymizationBenchmark,
)
from adaptive_anonymization.models import build_lm


def _get_eval_llm():
    return build_lm(os.environ.get("ADAPTIVE_ANON_EVAL_MODEL", "gemini_2_5_flash"))


DATASET_CONFIG = {
    "tab": {
        "task_class": TextAnonymizationBenchmark,
        "task_kwargs": {},
        "privacy_failure_threshold": 1.0,  # < 1.0 means some entities not masked
        "utility_failure_threshold": 0.5,
        "utility_is_boolean": False,
        "privacy_is_boolean": False,
    },
    "synthpai": {
        "task_class": SynthPAI,
        "task_kwargs": {"evaluation_model": None},  # Set at runtime
        "privacy_failure_threshold": 1.0,
        "utility_failure_threshold": 0.3,
        "utility_is_boolean": False,
        "privacy_is_boolean": True,
    },
    "medqa": {
        "task_class": MedQA,
        "task_kwargs": {
            "train_size": 111,
            "val_size": 111,
            "test_size": 111,
            "evaluation_model": None,
        },
        "privacy_failure_threshold": 0.5,
        "utility_failure_threshold": 1.0,
        "utility_is_boolean": True,
        "privacy_is_boolean": False,
    },
    "dbbio": {
        "task_class": DBBio,
        "task_kwargs": {
            "train_size": 111,
            "val_size": 111,
            "test_size": 111,
            "evaluation_model": None,
        },
        "privacy_failure_threshold": 1.0,
        "utility_failure_threshold": 1.0,
        "utility_is_boolean": True,
        "privacy_is_boolean": True,
    },
    "pupa": {
        "task_class": PUPA,
        "task_kwargs": {
            "judge_llm": None,
            "response_lm": None,
        },
        "privacy_failure_threshold": 0.5,
        "utility_failure_threshold": 1.0,
        "utility_is_boolean": True,
        "privacy_is_boolean": False,
    },
}


@dataclass
class EvalResult:
    idx: int
    gold: dspy.Example
    pred: Any
    privacy_score: float
    utility_score: float
    privacy_fail: bool
    utility_fail: bool
    extra_context: dict = field(default_factory=dict)


def _normalize_score(score: Any) -> float:
    """Extract numeric score from various return types."""
    if isinstance(score, (int, float)):
        return float(score)
    if isinstance(score, bool):
        return 1.0 if score else 0.0
    if isinstance(score, tuple):
        for item in reversed(score):
            if isinstance(item, (int, float)):
                return float(item)
    return 0.0


def _get_remaining_entities_tab(gold: dspy.Example, pred: Any) -> list[str]:
    """Entities that should have been masked but still appear in anonymized text."""
    remaining = []
    for entity in gold.entity_mentions:
        if entity["identifier_type"] != "NO_MASK" and entity["span_text"] in pred.anonymized_text:
            remaining.append(entity["span_text"])
    return list(set(remaining))


def run_error_analysis(
    model_path: str,
    dataset: str,
    limit: int | None = None,
    max_privacy_failures: int = 5,
    max_utility_failures: int = 5,
    verbose: bool = True,
) -> list[EvalResult]:
    """
    Run error analysis on a model for a given dataset.

    Returns list of EvalResult for all evaluated examples.
    """
    dataset = dataset.lower()
    if dataset not in DATASET_CONFIG:
        raise ValueError(
            f"Unknown dataset '{dataset}'. "
            f"Choose from: {list(DATASET_CONFIG.keys())}"
        )

    config = DATASET_CONFIG[dataset].copy()
    eval_llm = _get_eval_llm()

    # Inject evaluation model for tasks that need it
    if "evaluation_model" in config["task_kwargs"]:
        config["task_kwargs"]["evaluation_model"] = eval_llm
    if "judge_llm" in config["task_kwargs"]:
        config["task_kwargs"]["judge_llm"] = eval_llm
        config["task_kwargs"]["response_lm"] = eval_llm

    task = config["task_class"](**config["task_kwargs"])
    examples = task.examples_test
    if limit:
        examples = examples[:limit]

    model = dspy.load(model_path, allow_pickle=True)

    results: list[EvalResult] = []

    for idx, gold in enumerate(examples):
        try:
            pred = model(text=gold.text)
        except Exception as e:
            if verbose:
                print(f"Error on example {idx}: {e}", file=sys.stderr)
            continue

        try:
            utility_score = _normalize_score(task.compute_utility(gold, pred))
            privacy_score = _normalize_score(task.compute_privacy(gold, pred))
        except Exception as e:
            if verbose:
                print(f"Error evaluating example {idx}: {e}", file=sys.stderr)
            continue

        privacy_fail = privacy_score < config["privacy_failure_threshold"]
        utility_fail = utility_score < config["utility_failure_threshold"]

        extra: dict = {}
        if dataset == "tab":
            extra["remaining_entities"] = _get_remaining_entities_tab(gold, pred)

        results.append(
            EvalResult(
                idx=idx,
                gold=gold,
                pred=pred,
                privacy_score=privacy_score,
                utility_score=utility_score,
                privacy_fail=privacy_fail,
                utility_fail=utility_fail,
                extra_context=extra,
            )
        )

    return results


def _truncate(text: str, max_len: int = 300) -> str:
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def format_failure_case(result: EvalResult, dataset: str, failure_type: str) -> str:
    """Format a single failure case for display."""
    lines = []
    lines.append(f"  [Example {result.idx}]")
    lines.append(f"  Original text: {_truncate(result.gold.text, 350)}")
    lines.append(f"  Anonymized:    {_truncate(result.pred.anonymized_text, 350)}")
    lines.append(f"  Privacy score: {result.privacy_score:.3f}  |  Utility score: {result.utility_score:.3f}")

    if dataset == "tab" and result.extra_context.get("remaining_entities"):
        lines.append(f"  Unmasked entities: {result.extra_context['remaining_entities']}")
    elif dataset == "dbbio":
        lines.append(f"  True person: {result.gold.people}  |  True occupation: {result.gold.label}")
    elif dataset == "medqa":
        lines.append(f"  Correct answer: {result.gold.label}")
    elif dataset == "synthpai":
        lines.append(f"  Target attribute: {result.gold.target_attribute}")
    elif dataset == "pupa":
        lines.append(f"  PII to protect: {result.gold.pii_str}")

    if failure_type == "privacy":
        if dataset == "tab":
            lines.append("  → FAIL: Some entities were not properly masked.")
        elif dataset == "dbbio":
            lines.append("  → FAIL: Attacker can identify the person from the anonymized text.")
        elif dataset == "synthpai":
            lines.append("  → FAIL: Private attribute can be inferred from anonymized text.")
        elif dataset == "medqa":
            lines.append("  → FAIL: Writing style too similar to original (low privacy).")
        elif dataset == "pupa":
            lines.append("  → FAIL: PII leaked in anonymized prompt.")
    else:
        if dataset == "tab":
            lines.append("  → FAIL: Semantic similarity too low (utility degraded).")
        elif dataset == "dbbio":
            lines.append("  → FAIL: Occupation cannot be inferred from anonymized text.")
        elif dataset == "synthpai":
            lines.append("  → FAIL: Text changed too much (low ROUGE / utility).")
        elif dataset == "medqa":
            lines.append("  → FAIL: Correct medical answer cannot be derived.")
        elif dataset == "pupa":
            lines.append("  → FAIL: Response quality degraded.")

    return "\n".join(lines)


def print_error_report(
    results: list[EvalResult],
    dataset: str,
    model_path: str,
    max_privacy_failures: int = 10,
    max_utility_failures: int = 10,
) -> None:
    """Print formatted error analysis report."""
    privacy_failures = [r for r in results if r.privacy_fail]
    utility_failures = [r for r in results if r.utility_fail]
    both_failures = [r for r in results if r.privacy_fail and r.utility_fail]

    n = len(results)
    avg_privacy = sum(r.privacy_score for r in results) / n if n else 0
    avg_utility = sum(r.utility_score for r in results) / n if n else 0

    print("=" * 80)
    print("ERROR ANALYSIS REPORT")
    print("=" * 80)
    print(f"Model:  {model_path}")
    print(f"Dataset: {dataset.upper()}")
    print(f"Examples evaluated: {n}")
    print()
    print("Aggregate scores:")
    print(f"  Average privacy: {avg_privacy:.3f}")
    print(f"  Average utility: {avg_utility:.3f}")
    print()
    print("Failure counts:")
    print(f"  Privacy failures: {len(privacy_failures)} ({100 * len(privacy_failures) / n:.1f}%)")
    print(f"  Utility failures: {len(utility_failures)} ({100 * len(utility_failures) / n:.1f}%)")
    print(f"  Both dimensions:  {len(both_failures)} ({100 * len(both_failures) / n:.1f}%)")
    print()

    if privacy_failures:
        print("-" * 80)
        print("PRIVACY FAILURE CASES (sensitive data leaked or insufficiently anonymized)")
        print("-" * 80)
        for r in privacy_failures[:max_privacy_failures]:
            print(format_failure_case(r, dataset, "privacy"))
            print()
        if len(privacy_failures) > max_privacy_failures:
            print(f"  ... and {len(privacy_failures) - max_privacy_failures} more.")
        print()

    if utility_failures:
        print("-" * 80)
        print("UTILITY FAILURE CASES (task-relevant information lost or degraded)")
        print("-" * 80)
        for r in utility_failures[:max_utility_failures]:
            print(format_failure_case(r, dataset, "utility"))
            print()
        if len(utility_failures) > max_utility_failures:
            print(f"  ... and {len(utility_failures) - max_utility_failures} more.")
        print()

    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description="Error analysis for anonymization models: concrete failure cases in privacy and utility.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python error_analysis.py --model-path trained_models/dbbio/qwen_3_30b/dynamic --dataset dbbio
  python error_analysis.py --model-path trained_models/medqa/gemma_3_27b/dynamic --dataset medqa --limit 30
  python error_analysis.py -m trained_models/tab/mistral_small/dynamic -d tab --max-failures 10
        """,
    )
    parser.add_argument(
        "-m",
        "--model-path",
        required=True,
        help="Path to the saved DSPy model (e.g., trained_models/dbbio/qwen_3_30b/dynamic)",
    )
    parser.add_argument(
        "-d",
        "--dataset",
        required=True,
        choices=list(DATASET_CONFIG.keys()),
        help="Dataset to evaluate on: tab, synthpai, medqa, dbbio, pupa",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of test examples (default: all)",
    )
    parser.add_argument(
        "--max-failures",
        type=int,
        default=10,
        help="Max number of failure cases to show per dimension (default: 5)",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress per-example error messages",
    )

    args = parser.parse_args()

    if not os.path.isdir(args.model_path):
        print(f"Error: model path '{args.model_path}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    results = run_error_analysis(
        model_path=args.model_path,
        dataset=args.dataset,
        limit=args.limit,
        max_privacy_failures=args.max_failures,
        max_utility_failures=args.max_failures,
        verbose=not args.quiet,
    )

    if not results:
        print("No results. Check model path and dataset.", file=sys.stderr)
        sys.exit(1)

    print_error_report(
        results=results,
        dataset=args.dataset,
        model_path=args.model_path,
        max_privacy_failures=args.max_failures,
        max_utility_failures=args.max_failures,
    )


if __name__ == "__main__":
    main()
