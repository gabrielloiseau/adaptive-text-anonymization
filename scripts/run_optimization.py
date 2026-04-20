#!/usr/bin/env python3
"""Unified entry point for adaptive text anonymization optimization.

This script replaces the five near-duplicate ``run_optimization_<task>.py``
scripts of the original research repo with a single configurable CLI:

.. code-block:: bash

    python scripts/run_optimization.py \\
        --task dbbio --model gemma_3_27b \\
        --budget 1500 --patience 5 --seed 42 \\
        --output-dir trained_models

The script persists three DSPy programs (``base``, ``warmup``,
``dynamic``) to ``<output-dir>/<task>/<model>/<stage>/``.
"""

from __future__ import annotations

import argparse
import logging
import os
from pathlib import Path

import dspy

from adaptive_anonymization import MODEL_REGISTRY, TASK_REGISTRY, adagepa, build_lm, build_task

logger = logging.getLogger("run_optimization")

DEFAULT_EVAL_MODEL = "gemini_2_5_flash"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--task",
        choices=sorted(TASK_REGISTRY),
        required=True,
        help="Benchmark task to optimize against.",
    )
    parser.add_argument(
        "--model",
        choices=sorted(MODEL_REGISTRY),
        required=True,
        help="Anonymizer backbone (the model that also acts as proposer).",
    )
    parser.add_argument(
        "--eval-model",
        choices=sorted(MODEL_REGISTRY),
        default=DEFAULT_EVAL_MODEL,
        help="Model used for task-internal evaluation (judges, attackers, classifiers).",
    )
    parser.add_argument(
        "--budget",
        type=int,
        default=1500,
        help="Maximum number of LLM forward passes across both GEPA stages.",
    )
    parser.add_argument(
        "--patience",
        type=int,
        default=5,
        help="Early-stop patience for Stage 2 (warm-up).",
    )
    parser.add_argument(
        "--val-size-after-warmup",
        type=float,
        default=0.30,
        help="Fraction of the validation set sampled at each Stage 3 iteration.",
    )
    parser.add_argument(
        "--min-improvement-threshold",
        type=float,
        default=None,
        help=(
            "Warm-up improvement threshold. Defaults to the task-specific value "
            "declared in TASK_REGISTRY."
        ),
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("trained_models"),
        help="Root directory in which <task>/<model>/<stage> folders are created.",
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    os.environ.setdefault("WANDB_DISABLED", "true")

    task_spec = TASK_REGISTRY[args.task]
    min_improvement_threshold = (
        args.min_improvement_threshold
        if args.min_improvement_threshold is not None
        else task_spec.min_improvement_threshold
    )

    logger.info("Building eval LM: %s", args.eval_model)
    eval_lm = build_lm(args.eval_model)

    logger.info("Building task: %s", args.task)
    task = build_task(args.task, eval_lm=eval_lm)

    logger.info("Building anonymizer LM: %s", args.model)
    local_lm = build_lm(args.model)

    logger.info(
        "Running adagepa(budget=%d, patience=%d, threshold=%.3f, seed=%d)",
        args.budget,
        args.patience,
        min_improvement_threshold,
        args.seed,
    )
    programs = adagepa(
        task,
        local_llm=local_lm,
        budget=args.budget,
        val_size_after_warmup=args.val_size_after_warmup,
        patience=args.patience,
        seed=args.seed,
        min_improvement_threshold=min_improvement_threshold,
    )

    out_root = args.output_dir / args.task / args.model
    out_root.mkdir(parents=True, exist_ok=True)
    for stage, program in programs.items():
        stage_dir = out_root / stage
        stage_dir.mkdir(parents=True, exist_ok=True)
        logger.info("Saving %s stage to %s", stage, stage_dir)
        program.save(str(stage_dir), save_program=True)

    logger.info("Done. Artifacts written under %s", out_root)


if __name__ == "__main__":
    main()
