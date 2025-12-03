"""Unit tests for the KBeamAgent implementation."""

from agent.k_beam import KBeamAgent
from schema.solve_request import GuessFeedback, SolveParameters, SolveRequest


def _make_agent(words: list[str], beam_width: int = 50) -> KBeamAgent:
    """Create a KBeamAgent with the given word list and beam width."""
    agent = KBeamAgent(beam_width=beam_width)
    agent.all_words = set(word.upper() for word in words)
    return agent


def test_kbeam_respects_beam_width():
    """Beam ranking should not exceed the configured beam width."""

    words = ["CRANE", "SLATE", "BLOOM", "PRIME"]
    agent = _make_agent(words, beam_width=2)

    ranked = agent._rank_with_beam(
        candidates=sorted(agent.all_words),
        history=[],
        parameters=SolveParameters(),
    )

    assert len(ranked) <= 2
    assert set(ranked).issubset(agent.all_words)


def test_kbeam_returns_filtered_candidate_when_only_one_remains():
    """If history narrows to one answer, the agent must return it."""

    agent = _make_agent(["CRATE", "SLATE", "GRAZE"], beam_width=3)
    history = [GuessFeedback(guess="CRATE", feedback="22222")]
    request = SolveRequest(history=history)

    response = agent.solve(request)

    assert response.next_guess == "CRATE"
    assert response.remaining_candidates == 1
    assert response.suggestions == ["CRATE"]
