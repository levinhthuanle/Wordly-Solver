"""Performance benchmarking tests for solver algorithms.

This module tests and compares the efficiency of all solver strategies across multiple metrics:
- Search Time: Average time per suggestion
- Memory Usage: Peak memory consumption
- Expanded Nodes: Number of words evaluated
- Average Guesses: How many attempts to solve

Run with: pytest tests/test_performance.py -v -s
"""

import os
import time
import tracemalloc
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
from statistics import mean, median
from typing import Dict, List, Tuple

import pytest
from agent import get_agent
from agent.base import Agent as BaseAgent
from schema import SolverStrategy
from schema.solve_request import SolveRequest
from word_manager.word_manager import wordlist


class PerformanceMetrics:
    """Container for performance measurements."""

    def __init__(self, strategy: str):
        self.strategy = strategy
        self.times: List[float] = []
        self.memory_peaks: List[float] = []
        self.guesses_per_game: List[int] = []
        self.solved_games = 0
        self.total_games = 0
        self.failures: List[str] = []

    def add_game(
        self, time_taken: float, memory_mb: float, guesses: int, solved: bool, answer: str
    ):
        """Record metrics from a single game."""
        self.times.append(time_taken)
        self.memory_peaks.append(memory_mb)
        self.guesses_per_game.append(guesses)
        self.total_games += 1
        if solved:
            self.solved_games += 1
        else:
            self.failures.append(answer)

    @property
    def avg_time(self) -> float:
        return mean(self.times) if self.times else 0

    @property
    def avg_memory(self) -> float:
        return mean(self.memory_peaks) if self.memory_peaks else 0

    @property
    def avg_guesses(self) -> float:
        return mean(self.guesses_per_game) if self.guesses_per_game else 0

    @property
    def median_guesses(self) -> float:
        return median(self.guesses_per_game) if self.guesses_per_game else 0

    @property
    def success_rate(self) -> float:
        return (self.solved_games / self.total_games * 100) if self.total_games else 0

    def summary(self) -> Dict:
        """Get summary statistics."""
        return {
            "strategy": self.strategy,
            "avg_time_ms": round(self.avg_time * 1000, 2),
            "avg_memory_mb": round(self.avg_memory, 2),
            "avg_guesses": round(self.avg_guesses, 2),
            "median_guesses": self.median_guesses,
            "success_rate": round(self.success_rate, 2),
            "total_games": self.total_games,
            "solved_games": self.solved_games,
            "failed_games": self.total_games - self.solved_games,
        }


def simulate_game(agent, answer: str, max_attempts: int = 1000) -> Tuple[bool, int, float, float]:
    """
    Simulate a complete Wordle game.

    Returns: (solved, num_guesses, time_taken, peak_memory_mb)
    """
    history = []

    # Start memory tracking
    tracemalloc.start()
    start_time = time.perf_counter()

    for attempt in range(max_attempts):
        try:
            # Get suggestion
            guess = agent.solve(SolveRequest(history=history)).next_guess

            if not guess or len(guess) != 5:
                break

            # Generate feedback
            feedback = wordlist.get_feedback_pattern(guess, answer)

            # Add to history
            history.append({"guess": guess, "feedback": feedback})

            # Check if solved
            if feedback == "22222":  # All correct
                end_time = time.perf_counter()
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                return True, len(history), end_time - start_time, peak / 1024 / 1024

        except Exception as e:
            print(f"Error during game: {e}")
            break

    # Game not solved
    end_time = time.perf_counter()
    try:
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        memory_mb = peak / 1024 / 1024
    except:
        memory_mb = 0
    return False, len(history), end_time - start_time, memory_mb


@pytest.fixture
def test_words():
    """Get a sample of words for testing."""
    import random

    # Use a fixed seed for reproducibility
    random.seed(42)
    all_words = wordlist.words
    # Sample 100 words for faster testing (increase for production benchmarks)
    # return random.sample(all_words, min(100, len(all_words)))
    # Stress test: all words
    return random.sample(all_words, 1000)
    # Relaxed test
    # return random.sample(all_words, min(1000, len(all_words)))


@pytest.fixture
def all_strategies():
    """All available solver strategies."""
    # BETTER_ENTROPY is currently disabled due to performance issues
    return [
        SolverStrategy.BETTER_ENTROPY,
        SolverStrategy.RANDOM,
        SolverStrategy.FREQUENCY,
        SolverStrategy.ENTROPY,
        SolverStrategy.K_BEAM,
    ]


def test_algorithm_performance(test_words, all_strategies):
    """
    Benchmark all algorithms across multiple games.

    This test runs each algorithm against the same set of words and collects:
    - Time per game
    - Memory usage
    - Number of guesses
    - Success rate
    """
    print("\n" + "=" * 80)
    print("ALGORITHM PERFORMANCE BENCHMARK")
    print("=" * 80)
    print(f"Testing {len(test_words)} random words with max 6 attempts\n")

    results: Dict[str, PerformanceMetrics] = {}

    # Run benchmark for each strategy
    for strategy in all_strategies:
        print(f"\nTesting {strategy.value.upper()} (parallel)...")
        metrics = run_parallel_benchmark(strategy, test_words)

        results[strategy.value] = metrics
        summary = metrics.summary()
        print(f"  ✓ Completed: {summary['solved_games']}/{summary['total_games']} solved")
        print(f"    Avg time: {summary['avg_time_ms']:.2f}ms")
        print(f"    Avg guesses: {summary['avg_guesses']:.2f}")

    # Print comparison table
    print("\n" + "=" * 80)
    print("RESULTS SUMMARY")
    print("=" * 80)
    print(
        f"{'Strategy':<20} {'Avg Time':<12} {'Avg Memory':<12} {'Avg Guesses':<12} {'Success Rate':<12}"
    )
    print("-" * 80)

    for strategy_name, metrics in results.items():
        summary = metrics.summary()
        print(
            f"{strategy_name:<20} {summary['avg_time_ms']:>8.2f}ms  "
            f"{summary['avg_memory_mb']:>8.2f}MB  "
            f"{summary['avg_guesses']:>10.2f}  "
            f"{summary['success_rate']:>10.2f}%"
        )

    # Generate visualizations
    try:
        generate_performance_charts(results, test_words)
        print("\nPerformance charts saved to: tests/performance_charts.html")
    except Exception as e:
        print(f"\nCould not generate charts: {e}")

    # Print insights
    print_performance_insights(results)

    # Assert all algorithms can solve at least some games
    for strategy_name, metrics in results.items():
        assert metrics.solved_games > 0, f"{strategy_name} failed to solve any games"


DEFAULT_MAX_WORKERS = os.cpu_count()


def run_parallel_benchmark(
    strategy: SolverStrategy,
    test_words: List[str],
    max_attempts: int = 100,
    max_workers: int | None = None,
) -> PerformanceMetrics:
    """Execute all games for a strategy in parallel with a progress bar."""

    metrics = PerformanceMetrics(strategy.value)
    total_games = len(test_words)
    if total_games == 0:
        return metrics

    worker_count = max_workers or DEFAULT_MAX_WORKERS
    start_time = time.perf_counter()

    print(f"  → Spawning {worker_count} worker(s) for {total_games} games")

    with ProcessPoolExecutor(
        max_workers=worker_count,
        initializer=_performance_worker_init,
        initargs=(strategy.value,),
    ) as executor:
        futures = [
            executor.submit(_play_game_worker, answer, max_attempts) for answer in test_words
        ]

        completed = 0
        solved = 0
        for future in as_completed(futures):
            solved_flag, guesses, time_taken, memory_mb, answer = future.result()
            metrics.add_game(time_taken, memory_mb, guesses, solved_flag, answer)
            completed += 1
            if solved_flag:
                solved += 1
            _render_progress_bar(
                strategy.value,
                completed,
                total_games,
                solved,
                start_time,
            )

    print()  # move to next line after progress bar
    return metrics


def _render_progress_bar(
    strategy_label: str,
    completed: int,
    total: int,
    solved: int,
    start_time: float,
    width: int = 30,
) -> None:
    """Render an in-place textual progress bar showing solved words."""

    percent = completed / total if total else 1
    filled = int(width * percent)
    bar = "█" * filled + "-" * (width - filled)

    elapsed = time.perf_counter() - start_time
    eta = ((elapsed / completed) * (total - completed)) if completed else 0.0

    line = (
        f"\r[{strategy_label.upper():<10}] |{bar}| "
        f"Solved {solved}/{total} ({percent * 100:5.1f}%) "
        f"Elapsed {elapsed:6.1f}s ETA {eta:6.1f}s"
    )
    print(line, end="", flush=True)


_WORKER_AGENT: BaseAgent | None = None


def _performance_worker_init(strategy_value: str) -> None:
    """Process initializer to build a solver agent once per worker."""

    global _WORKER_AGENT
    strategy = SolverStrategy(strategy_value)
    _WORKER_AGENT = get_agent(strategy)


def _play_game_worker(answer: str, max_attempts: int) -> Tuple[bool, int, float, float, str]:
    """Worker entry point for ProcessPoolExecutor."""

    if _WORKER_AGENT is None:  # pragma: no cover - safety
        raise RuntimeError("Worker agent is not initialized")

    _WORKER_AGENT.reset()
    solved, guesses, time_taken, memory_mb = simulate_game(_WORKER_AGENT, answer, max_attempts)
    return solved, guesses, time_taken, memory_mb, answer


def generate_performance_charts(results: Dict[str, PerformanceMetrics], test_words: List[str]):
    """Generate HTML charts for visualization."""
    try:
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
    except ImportError:
        print("\n️Install plotly for visualizations: uv pip install plotly")
        return

    # Prepare data
    strategies = list(results.keys())
    avg_times = [results[s].avg_time * 1000 for s in strategies]  # Convert to ms
    avg_memory = [results[s].avg_memory for s in strategies]
    avg_guesses = [results[s].avg_guesses for s in strategies]
    success_rates = [results[s].success_rate for s in strategies]

    # Create subplots
    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=(
            "Average Search Time (ms)",
            "Average Memory Usage (MB)",
            "Average Number of Guesses",
            "Success Rate (%)",
        ),
        specs=[[{"type": "bar"}, {"type": "bar"}], [{"type": "bar"}, {"type": "bar"}]],
    )

    # Time chart
    fig.add_trace(
        go.Bar(x=strategies, y=avg_times, name="Time (ms)", marker_color="indianred"), row=1, col=1
    )

    # Memory chart
    fig.add_trace(
        go.Bar(x=strategies, y=avg_memory, name="Memory (MB)", marker_color="lightsalmon"),
        row=1,
        col=2,
    )

    # Guesses chart
    fig.add_trace(
        go.Bar(x=strategies, y=avg_guesses, name="Avg Guesses", marker_color="lightblue"),
        row=2,
        col=1,
    )

    # Success rate chart
    fig.add_trace(
        go.Bar(x=strategies, y=success_rates, name="Success Rate", marker_color="lightgreen"),
        row=2,
        col=2,
    )

    # Update layout
    fig.update_layout(
        title_text=f"Solver Algorithm Performance Comparison ({len(test_words)} games)",
        showlegend=False,
        height=800,
    )

    # Add guess distribution box plot
    fig_box = go.Figure()
    for strategy_name, metrics in results.items():
        fig_box.add_trace(go.Box(y=metrics.guesses_per_game, name=strategy_name, boxmean="sd"))

    fig_box.update_layout(
        title="Distribution of Guesses per Game",
        yaxis_title="Number of Guesses",
        xaxis_title="Strategy",
        height=500,
    )

    # Save combined HTML
    with open("tests/performance_charts.html", "w") as f:
        f.write("<html><head><title>Performance Analysis</title></head><body>")
        f.write("<h1>Wordly Solver Algorithm Performance Analysis</h1>")
        f.write(fig.to_html(full_html=False, include_plotlyjs="cdn"))
        f.write("<br><hr><br>")
        f.write(fig_box.to_html(full_html=False, include_plotlyjs="cdn"))
        f.write("<br><hr><br>")
        f.write(_render_guess_distribution_table(results))
        f.write("</body></html>")


def print_performance_insights(results: Dict[str, PerformanceMetrics]):
    """Print analysis and insights from the benchmark results."""
    print("\n" + "=" * 80)
    print("INSIGHTS & ANALYSIS")
    print("=" * 80)

    # Find best in each category
    best_time = min(results.items(), key=lambda x: x[1].avg_time)
    best_memory = min(results.items(), key=lambda x: x[1].avg_memory)
    best_guesses = min(results.items(), key=lambda x: x[1].avg_guesses)
    best_success = max(results.items(), key=lambda x: x[1].success_rate)

    print("\nBest Performers:")
    print(f"  Fastest: {best_time[0]} ({best_time[1].avg_time * 1000:.2f}ms avg)")
    print(f"  Most Memory Efficient: {best_memory[0]} ({best_memory[1].avg_memory:.2f}MB avg)")
    print(f"  Fewest Guesses: {best_guesses[0]} ({best_guesses[1].avg_guesses:.2f} avg)")
    print(f"  Highest Success: {best_success[0]} ({best_success[1].success_rate:.1f}%)")

    print("\nKey Observations:")

    # Speed comparison
    times = {k: v.avg_time for k, v in results.items()}
    fastest = min(times.values())
    slowest = max(times.values())
    if slowest > 0:
        speedup = slowest / fastest
        print(f"  • The fastest algorithm is {speedup:.1f}x faster than the slowest")

    # Guess efficiency
    guesses = {k: v.avg_guesses for k, v in results.items()}
    best_guess = min(guesses.values())
    worst_guess = max(guesses.values())
    print(f"  • Guess count ranges from {best_guess:.2f} to {worst_guess:.2f} attempts")

    # Success rates
    success_rates = {k: v.success_rate for k, v in results.items()}
    if max(success_rates.values()) - min(success_rates.values()) > 10:
        print(
            f"  • Significant variation in success rates ({min(success_rates.values()):.1f}% - {max(success_rates.values()):.1f}%)"
        )

    # Strategy-specific insights
    print("\n📋 Strategy Analysis:")
    for name, metrics in results.items():
        print(f"\n  {name.upper()}:")
        if metrics.avg_guesses < 4:
            print(f"    Excellent efficiency ({metrics.avg_guesses:.2f} avg guesses)")
        elif metrics.avg_guesses < 5:
            print(f"    Good efficiency ({metrics.avg_guesses:.2f} avg guesses)")
        else:
            print(f"    Could be more efficient ({metrics.avg_guesses:.2f} avg guesses)")

        if metrics.success_rate >= 95:
            print(f"    Very reliable ({metrics.success_rate:.1f}% success)")
        elif metrics.success_rate >= 85:
            print(f"    Reliable ({metrics.success_rate:.1f}% success)")
        else:
            print(f"    Reliability concerns ({metrics.success_rate:.1f}% success)")

        if metrics.failures:
            print(f"    Failed on {len(metrics.failures)} words: {', '.join(metrics.failures[:5])}")

        if metrics.guesses_per_game:
            distribution = Counter(metrics.guesses_per_game)
            max_guess = max(distribution)
            print("    Guess distribution:")
            for guess_count in range(1, max_guess + 1):
                attempts = distribution.get(guess_count, 0)
                if attempts:
                    label = "word" if attempts == 1 else "words"
                    print(
                        f"      • {guess_count} guess{'es' if guess_count > 1 else ''}: {attempts} {label}"
                    )
            unsolved = len(metrics.failures)
            if unsolved:
                label = "word" if unsolved == 1 else "words"
                print(f"      • Unsolved within limit: {unsolved} {label}")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    # Allow running directly for quick tests
    pytest.main([__file__, "-v", "-s"])


def _render_guess_distribution_table(results: Dict[str, PerformanceMetrics]) -> str:
    """Return an HTML table describing how many words required N guesses per strategy."""

    def describe(metrics: PerformanceMetrics) -> str:
        if not metrics.guesses_per_game:
            return "<em>No games recorded</em>"

        dist = Counter(metrics.guesses_per_game)
        max_guess = max(dist)
        parts: List[str] = []
        for guess_count in range(1, max_guess + 1):
            word_count = dist.get(guess_count, 0)
            if not word_count:
                continue
            label = "word" if word_count == 1 else "words"
            guess_label = "guess" if guess_count == 1 else "guesses"
            parts.append(f"{guess_count} {guess_label}: {word_count} {label}")

        unsolved = len(metrics.failures)
        if unsolved:
            label = "word" if unsolved == 1 else "words"
            parts.append(f"Unsolved within limit: {unsolved} {label}")

        return "<br>".join(parts)

    rows = [
        "<h2>Guess Distribution by Strategy</h2>",
        '<table border="1" cellpadding="8" cellspacing="0">',
    ]
    rows.append("<tr><th>Strategy</th><th>Distribution</th></tr>")
    for strategy, metrics in results.items():
        rows.append(f"<tr><td>{strategy}</td><td>{describe(metrics)}</td></tr>")
    rows.append("</table>")
    return "".join(rows)
