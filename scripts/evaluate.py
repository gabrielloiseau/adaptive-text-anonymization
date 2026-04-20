#!/usr/bin/env python3
"""Evaluate one or more saved DSPy anonymizer programs on a task test split.

Example
-------
Reproduce the "Optimized Prompt" column of Table 1 for DB-Bio:

.. code-block:: bash

    python scripts/evaluate.py \\
        --task dbbio \\
        --program trained_models/dbbio/gemma_3_27b/dynamic \\
        --eval-model gemini_2_5_flash \\
        --output results/dbbio_gemma_dynamic.json

Pass ``--program`` multiple times to compare several programs on the same task.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
from pathlib import Path
from typing import Any

import dspy

from adaptive_anonymization import TASK_REGISTRY, build_lm, build_task

logger = logging.getLogger("evaluate")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--task", choices=sorted(TASK_REGISTRY), required=True)
    parser.add_argument(
        "--program",
        action="append",
        required=True,
        help="Path to a saved DSPy program directory (contains program.pkl). Can be repeated.",
    )
    parser.add_argument(
        "--eval-model",
        default="gemini_2_5_flash",
        help="Model used for task-internal judges / attackers / classifiers.",
    )
    parser.add_argument("--num-threads", type=int, default=8)
    parser.add_argument("--limit", type=int, default=None, help="Limit test set to N examples (debug).")
    parser.add_argument("--output", type=Path, default=None, help="Optional JSON output path.")
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser.parse_args()


def _extract_score(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, bool):
        return float(value)
    if isinstance(value, tuple):
        for item in reversed(value):
            score = _extract_score(item)
            if score is not None:
                return score
    return None


def evaluate_program(
    program: dspy.Module,
    task: Any,
    *,
    num_threads: int,
    limit: int | None,
) -> dict[str, float]:
    devset = task.examples_test[: limit] if limit else task.examples_test
    evaluator = dspy.Evaluate(
        devset=devset,
        num_threads=num_threads,
        display_progress=True,
        provide_traceback=True,
    )
    privacy = evaluator(program, metric=task.compute_privacy)
    utility = evaluator(program, metric=task.compute_utility)
    return {
        "n_examples": len(devset),
        "privacy": float(privacy.score),
        "utility": float(utility.score),
    }


def main() -> None:
    args = parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    os.environ.setdefault("WANDB_DISABLED", "true")

    eval_lm = build_lm(args.eval_model)
    task = build_task(args.task, eval_lm=eval_lm)

    results: dict[str, dict[str, float]] = {}
    for program_path in args.program:
        logger.info("Loading program from %s", program_path)
        program = dspy.load(program_path, allow_pickle=True)
        scores = evaluate_program(program, task, num_threads=args.num_threads, limit=args.limit)
        logger.info(
            "%s on %s test split: privacy=%.4f utility=%.4f",
            program_path,
            args.task,
            scores["privacy"],
            scores["utility"],
        )
        results[program_path] = scores

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", encoding="utf-8") as f:
            json.dump({"task": args.task, "eval_model": args.eval_model, "results": results}, f, indent=2)
        logger.info("Wrote results to %s", args.output)


if __name__ == "__main__":
    main()
