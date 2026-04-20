"""Language model registry for adaptive text anonymization.

All models are built via ``dspy.LM`` and use OpenRouter's OpenAI-compatible
API (``api_base=https://openrouter.ai/api/v1``). Set ``OPENROUTER_API_KEY``
only; see ``.env.example`` at the repo root.

Use :func:`build_lm` (or access :data:`MODEL_REGISTRY` directly) to obtain
a configured ``dspy.LM`` for one of the keys listed in :data:`MODEL_REGISTRY`.
"""

from __future__ import annotations

import os
from typing import Callable

import dspy

DEFAULT_MAX_TOKENS = 25_000


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(
            f"Environment variable {name} is not set. "
            f"Copy .env.example to .env and fill it in, or export the variable."
        )
    return value


def _openrouter_lm(model: str) -> Callable[[], dspy.LM]:
    def factory() -> dspy.LM:
        _require_env("OPENROUTER_API_KEY")
        return dspy.LM(
            model,
            api_base="https://openrouter.ai/api/v1",
            max_tokens=DEFAULT_MAX_TOKENS,
        )

    return factory


MODEL_REGISTRY: dict[str, Callable[[], dspy.LM]] = {
    # Anonymizer backbones (open-source, main paper).
    "mistral_small": _openrouter_lm(
        "openrouter/mistralai/mistral-small-3.2-24b-instruct-2506"
    ),
    "gemma_3_27b": _openrouter_lm("openrouter/google/gemma-3-27b-it"),
    "qwen_3_30b": _openrouter_lm(
        "openrouter/qwen/qwen3-30b-a3b-instruct-2507"
    ),
    # SLM-study backbone (appendix).
    "qwen_2_5_7b": _openrouter_lm("openrouter/qwen/qwen-2.5-7b-instruct"),
    # Evaluation / judge / attacker backbones (OpenRouter-routed Mistral Medium
    # 3.1 aligns with the former native ``mistral-medium-2508`` eval stack).
    "mistral_medium": _openrouter_lm("openrouter/mistralai/mistral-medium-3.1"),
    "gemini_2_5_flash": _openrouter_lm("openrouter/google/gemini-2.5-flash"),
}


def build_lm(name: str) -> dspy.LM:
    """Return a configured ``dspy.LM`` for the registered ``name``."""
    if name not in MODEL_REGISTRY:
        available = ", ".join(sorted(MODEL_REGISTRY))
        raise KeyError(f"Unknown model {name!r}. Available: {available}")
    return MODEL_REGISTRY[name]()
