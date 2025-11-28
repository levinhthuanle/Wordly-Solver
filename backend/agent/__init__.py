"""Agent registry exposing the available solver implementations."""

from __future__ import annotations

from functools import lru_cache
from typing import Dict, Type

from schema.solve_request import SolverStrategy
from .base import Agent
from .entropy import EntropyAgent
from .random import RandomAgent
from .frequency import FrequencyAgent
from .better_entropy import BetterEntropyAgent

_STRATEGY_FACTORIES: Dict[SolverStrategy, Type[Agent]] = {
    SolverStrategy.ENTROPY: EntropyAgent,
    SolverStrategy.RANDOM: RandomAgent,
    SolverStrategy.FREQUENCY: FrequencyAgent,
    SolverStrategy.BETTER_ENTROPY: BetterEntropyAgent,
}

# Cache and return agent instances based on strategy
@lru_cache(maxsize=None)
def _build_agent(strategy: SolverStrategy) -> Agent:
    try:
        factory = _STRATEGY_FACTORIES[strategy]
    except KeyError as exc:  # pragma: no cover - programming errors
        raise ValueError(f"Unsupported solver strategy: {strategy}") from exc
    return factory()


def get_agent(strategy: SolverStrategy | None = None) -> Agent:
    """Return a cached agent instance for the requested strategy."""

    selected = strategy or SolverStrategy.ENTROPY
    try:
        return _build_agent(selected)
    except FileNotFoundError as exc:  # pragma: no cover - configuration errors
        msg = f"Dictionary file not found at {exc.filename!s}" if exc.filename else str(exc)
        raise RuntimeError(msg) from exc


# Lists all the public names of this.
__all__ = [
    "Agent",
    "EntropyAgent",
    "RandomAgent",
    "FrequencyAgent",
    "SolverStrategy",
    "get_agent",
]