"""Two-stage GEPA prompt optimizer for text anonymization.

This module factors the training loop shared by the five
``run_optimization_<task>.py`` scripts of the original research repo into
a single reusable function :func:`adagepa`, plus the two custom GEPA
strategies described in the paper:

* :class:`RobustNoImprovementStopper` - early stops the warm-up stage
  after ``patience`` iterations without improvement above a threshold.
* :class:`RoundRobinSampleEvaluationPolicy` - adaptive validation
  sampling for the refinement stage, preferring examples that have been
  least evaluated.

The :data:`TASK_REGISTRY` maps short task keys (``dbbio``, ``synthpai``,
``tab``, ``pupa``, ``medqa``) to their task class, default constructor
kwargs, and recommended warm-up improvement threshold.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

import dspy
from gepa.core.data_loader import DataId, DataInst, DataLoader
from gepa.core.state import GEPAState, ProgramIdx
from gepa.strategies.eval_policy import EvaluationPolicy
from gepa.utils import StopperProtocol

from adaptive_anonymization.tasks import DBBio, MedQA, PUPA, SynthPAI, TextAnonymizationBenchmark


class RoundRobinSampleEvaluationPolicy(EvaluationPolicy[DataId, DataInst]):
    """GEPA evaluation policy that samples validation examples in round-robin order.

    Examples that have been evaluated fewer times are preferred, which
    keeps validation coverage uniform across the remaining budget during
    Stage 3 (refinement).
    """

    def __init__(self, batch_size: int = 5) -> None:
        if batch_size <= 0:
            raise ValueError("batch_size must be a positive integer")
        self.batch_size = batch_size

    def get_eval_batch(
        self,
        loader: DataLoader[DataId, DataInst],
        state: GEPAState,
        target_program_idx: ProgramIdx | None = None,
    ) -> list[DataId]:
        all_ids = list(loader.all_ids())
        if not all_ids:
            return []

        order_index = {val_id: idx for idx, val_id in enumerate(all_ids)}
        valset_evaluations = state.valset_evaluations

        def sort_key(val_id: DataId):
            eval_count = len(valset_evaluations.get(val_id, []))
            return (eval_count, order_index[val_id])

        ordered_ids = sorted(all_ids, key=sort_key)
        return ordered_ids[: self.batch_size] or ordered_ids

    def get_best_program(self, state: GEPAState) -> ProgramIdx:
        best_idx, best_score, best_coverage = -1, float("-inf"), -1
        for program_idx, scores in enumerate(state.prog_candidate_val_subscores):
            coverage = len(scores)
            avg = sum(scores.values()) / coverage if coverage else float("-inf")
            if avg > best_score or (avg == best_score and coverage > best_coverage):
                best_score = avg
                best_idx = program_idx
                best_coverage = coverage
        return best_idx

    def get_valset_score(self, program_idx: ProgramIdx, state: GEPAState) -> float:
        return state.get_program_average_val_subset(program_idx)[0]


class RobustNoImprovementStopper(StopperProtocol):
    """Stop GEPA after ``patience`` iterations without significant improvement.

    Only improvements strictly greater than ``min_improvement_threshold``
    reset the counter, which prevents slow, non-meaningful trickles from
    keeping the optimization running.
    """

    def __init__(
        self,
        max_iterations_without_improvement: int,
        min_improvement_threshold: float = 0.0,
    ) -> None:
        self.max_iterations_without_improvement = max_iterations_without_improvement
        self.min_improvement_threshold = min_improvement_threshold
        self.best_score = float("-inf")
        self.iterations_without_improvement = 0

    def __call__(self, gepa_state: GEPAState) -> bool:
        try:
            current_score = (
                max(gepa_state.program_full_scores_val_set)
                if gepa_state.program_full_scores_val_set
                else 0.0
            )
            improvement = current_score - self.best_score

            if improvement > self.min_improvement_threshold:
                self.best_score = current_score
                self.iterations_without_improvement = 0
            else:
                self.iterations_without_improvement += 1

            return self.iterations_without_improvement >= self.max_iterations_without_improvement
        except Exception:
            return False

    def reset(self) -> None:
        self.iterations_without_improvement = 0


@dataclass(frozen=True)
class TaskSpec:
    """Declarative description of a benchmark task for the unified CLI."""

    task_cls: type
    #: Optional kwargs passed through to the task constructor. If a kwarg
    #: is named ``evaluation_model`` / ``judge_llm`` / ``response_lm``, the
    #: unified CLI will fill it with the configured evaluation LM.
    kwargs: dict[str, Any] = field(default_factory=dict)
    #: Warm-up stop threshold; Stage 2 early-stops when validation
    #: improvement drops below this value across ``patience`` iterations.
    min_improvement_threshold: float = 0.05
    #: Which kwargs expect the evaluation LM (used by the CLI).
    eval_lm_kwargs: tuple[str, ...] = ()


TASK_REGISTRY: dict[str, TaskSpec] = {
    "tab": TaskSpec(
        task_cls=TextAnonymizationBenchmark,
        min_improvement_threshold=0.05,
    ),
    "synthpai": TaskSpec(
        task_cls=SynthPAI,
        min_improvement_threshold=0.05,
        eval_lm_kwargs=("evaluation_model",),
    ),
    "medqa": TaskSpec(
        task_cls=MedQA,
        min_improvement_threshold=0.05,
        eval_lm_kwargs=("evaluation_model",),
    ),
    "pupa": TaskSpec(
        task_cls=PUPA,
        min_improvement_threshold=0.05,
        eval_lm_kwargs=("judge_llm", "response_lm"),
    ),
    "dbbio": TaskSpec(
        task_cls=DBBio,
        min_improvement_threshold=0.01,
        eval_lm_kwargs=("evaluation_model",),
    ),
}


def build_task(name: str, *, eval_lm: dspy.LM | None = None, **overrides: Any):
    """Instantiate the task registered under ``name``.

    ``eval_lm`` is forwarded to every kwarg listed in
    :attr:`TaskSpec.eval_lm_kwargs` unless overridden by ``overrides``.
    """
    if name not in TASK_REGISTRY:
        available = ", ".join(sorted(TASK_REGISTRY))
        raise KeyError(f"Unknown task {name!r}. Available: {available}")

    spec = TASK_REGISTRY[name]
    kwargs: dict[str, Any] = dict(spec.kwargs)
    if eval_lm is not None:
        for eval_kwarg in spec.eval_lm_kwargs:
            kwargs.setdefault(eval_kwarg, eval_lm)
    kwargs.update(overrides)
    return spec.task_cls(**kwargs)


def adagepa(
    task: Any,
    local_llm: dspy.LM,
    *,
    budget: int = 1500,
    val_size_after_warmup: float = 0.30,
    patience: int = 5,
    seed: int = 42,
    min_improvement_threshold: float = 0.05,
    reflection_minibatch_size: int = 3,
    num_threads: int = 8,
) -> dict[str, Any]:
    """Run the two-stage GEPA pipeline described in Section 3 of the paper.

    Parameters
    ----------
    task:
        A task instance exposing ``examples_train`` / ``examples_val`` and
        ``compute_overall_score_with_feedback`` /
        ``compute_overall_score_with_rich_feedback``.
    local_llm:
        The ``dspy.LM`` that plays both the anonymizer and proposer role.
    budget:
        Total rollout budget (LLM forward passes) across both stages.
    val_size_after_warmup:
        Fraction of the validation set sampled per iteration during
        Stage 3 refinement.
    patience:
        Early-stop patience for Stage 2 warm-up.
    min_improvement_threshold:
        Improvement threshold used by the warm-up early-stopper.
    reflection_minibatch_size:
        Mini-batch size for GEPA reflective mutation.
    num_threads:
        Thread pool size for GEPA evaluation.

    Returns a dict with three DSPy programs: ``base`` (raw seed prompt),
    ``warmup`` (after Stage 2), and ``dynamic`` (after Stage 3).
    """
    ano_signature = dspy.Signature("text:str -> anonymized_text:str")
    ano_model = dspy.Predict(ano_signature)
    ano_model.set_lm(local_llm)

    gepa_warmup = dspy.GEPA(
        metric=task.compute_overall_score_with_feedback,
        max_metric_calls=budget,
        num_threads=num_threads,
        track_stats=True,
        reflection_minibatch_size=reflection_minibatch_size,
        reflection_lm=local_llm,
        seed=seed,
        gepa_kwargs={
            "stop_callbacks": RobustNoImprovementStopper(
                max_iterations_without_improvement=patience,
                min_improvement_threshold=min_improvement_threshold,
            ),
        },
    )
    gepa_ano_model_warmup = gepa_warmup.compile(
        ano_model,
        trainset=task.examples_train,
        valset=task.examples_val,
    )

    remaining_budget = (
        budget - gepa_ano_model_warmup.detailed_results.total_metric_calls
    )
    gepa_dynamic = dspy.GEPA(
        metric=task.compute_overall_score_with_rich_feedback,
        max_metric_calls=remaining_budget,
        num_threads=num_threads,
        track_stats=True,
        reflection_minibatch_size=reflection_minibatch_size,
        reflection_lm=local_llm,
        seed=seed,
        gepa_kwargs={
            "val_evaluation_policy": RoundRobinSampleEvaluationPolicy(
                batch_size=max(1, int(val_size_after_warmup * len(task.examples_val)))
            ),
        },
    )
    gepa_ano_model_dynamic = gepa_dynamic.compile(
        gepa_ano_model_warmup,
        trainset=task.examples_train,
        valset=task.examples_val,
    )

    return {
        "base": ano_model,
        "warmup": gepa_ano_model_warmup,
        "dynamic": gepa_ano_model_dynamic,
    }


__all__ = [
    "TASK_REGISTRY",
    "RobustNoImprovementStopper",
    "RoundRobinSampleEvaluationPolicy",
    "TaskSpec",
    "adagepa",
    "build_task",
]
