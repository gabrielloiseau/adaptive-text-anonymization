"""Adaptive Text Anonymization.

Task-specific prompt optimization for LLM-based text anonymization.
"""

from adaptive_anonymization.optimizer import (
    TASK_REGISTRY,
    RobustNoImprovementStopper,
    RoundRobinSampleEvaluationPolicy,
    adagepa,
    build_task,
)
from adaptive_anonymization.models import MODEL_REGISTRY, build_lm

__all__ = [
    "TASK_REGISTRY",
    "MODEL_REGISTRY",
    "RobustNoImprovementStopper",
    "RoundRobinSampleEvaluationPolicy",
    "adagepa",
    "build_task",
    "build_lm",
]

__version__ = "0.1.0"
