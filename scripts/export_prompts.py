#!/usr/bin/env python3
"""Export the final optimized prompt for each saved anonymizer program.

For every ``trained_models/<task>/<model>/dynamic/`` directory, load the
DSPy program, extract the predictor's optimized instruction string, and
write it to ``prompts/<task>/<model>.md``. Run once after training (or
after copying the bundled ``trained_models/`` directory) to refresh the
``prompts/`` tree. The resulting Markdown files are human-readable and
meant to be committed alongside the trained programs.

Example
-------

.. code-block:: bash

    python scripts/export_prompts.py --root trained_models --output prompts

Pass ``--stage {base,warmup,dynamic}`` to export prompts from a different
optimization stage.
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

import dspy

logger = logging.getLogger("export_prompts")

DEFAULT_STAGE = "dynamic"
# Nice-looking display names keyed by `<model>` folder name. Used only in
# the human-readable markdown headers; extend as needed.
MODEL_DISPLAY_NAMES = {
    "mistral_small": "Mistral-Small-3.2-24B",
    "gemma_3_27b": "Gemma-3-27B-it",
    "qwen_3_30b": "Qwen3-30B-A3B",
    "qwen_2_5_7b": "Qwen-2.5-7B",
    "qwen_2_7b": "Qwen-2.5-7B",
}
TASK_DISPLAY_NAMES = {
    "dbbio": "DB-Bio",
    "synthpai": "SynthPAI",
    "tab": "TAB",
    "pupa": "PUPA",
    "medqa": "MedQA",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("trained_models"),
        help="Root of the trained_models/<task>/<model>/<stage>/ tree.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("prompts"),
        help="Directory in which prompts/<task>/<model>.md files are written.",
    )
    parser.add_argument(
        "--stage",
        default=DEFAULT_STAGE,
        choices=("base", "warmup", "dynamic"),
        help="Which optimization stage to export.",
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser.parse_args()


def _extract_instruction(program: dspy.Module) -> str:
    """Return the optimized instruction string stored on ``program``.

    Works both for raw ``dspy.Predict`` objects and for compiled modules
    that expose a ``predictors()`` method.
    """
    if hasattr(program, "signature"):
        return program.signature.instructions
    predictors = program.predictors() if hasattr(program, "predictors") else []
    if not predictors:
        raise RuntimeError(f"Could not locate any predictor on {program!r}.")
    return predictors[0].signature.instructions


def export_one(program_path: Path, output_path: Path, task: str, model: str, stage: str) -> None:
    program = dspy.load(str(program_path), allow_pickle=True)
    instruction = _extract_instruction(program)

    task_name = TASK_DISPLAY_NAMES.get(task, task)
    model_name = MODEL_DISPLAY_NAMES.get(model, model)

    body = (
        f"# {task_name} - {model_name}\n\n"
        f"- Task: `{task}`\n"
        f"- Model: `{model}` ({model_name})\n"
        f"- Stage: `{stage}`\n"
        f"- Source: `{program_path.as_posix()}`\n\n"
        "## Optimized prompt\n\n"
        "```\n"
        f"{instruction.strip()}\n"
        "```\n"
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(body, encoding="utf-8")


def main() -> None:
    args = parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    if not args.root.is_dir():
        raise SystemExit(f"trained_models root {args.root} does not exist")

    exported, skipped, failed = 0, 0, 0
    for task_dir in sorted(p for p in args.root.iterdir() if p.is_dir()):
        for model_dir in sorted(p for p in task_dir.iterdir() if p.is_dir()):
            program_dir = model_dir / args.stage
            if not (program_dir / "program.pkl").is_file():
                logger.debug("Skipping %s (no %s/program.pkl)", model_dir, args.stage)
                skipped += 1
                continue

            out_path = args.output / task_dir.name / f"{model_dir.name}.md"
            try:
                export_one(
                    program_path=program_dir,
                    output_path=out_path,
                    task=task_dir.name,
                    model=model_dir.name,
                    stage=args.stage,
                )
            except Exception as exc:  # noqa: BLE001 - surface per-file errors
                logger.error("Failed to export %s: %s", program_dir, exc)
                failed += 1
                continue

            logger.info("Exported %s -> %s", program_dir, out_path)
            exported += 1

    logger.info("Done: %d exported, %d skipped, %d failed", exported, skipped, failed)


if __name__ == "__main__":
    main()
