import { memo, useEffect, useMemo, useState } from "react";
import { Chart } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  ChartOptions,
  ChartData,
  ChartDataset,
  BarController,
  LineController,
} from "chart.js";
import { LetterState } from "@/types/types";
import { getWordListSnapshot } from "@/utils/game-utils";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  BarController,
  LineController,
  Tooltip,
  Legend
);

const STATUS_ORDER: LetterState[] = ["correct", "present", "absent", "unused"];
const STATUS_COLOR: Record<LetterState, string> = {
  correct: "#16a34a",
  present: "#f59e0b",
  absent: "#6b7280",
  unused: "#a1a1aa",
};

const STATE_TO_DIGIT: Record<LetterState, string> = {
  correct: "2",
  present: "1",
  absent: "0",
  unused: "0",
};

interface ChartVisualizationPanelProps {
  guesses: string[];
  evaluations: LetterState[][];
}

const chartOptions: ChartOptions<"bar" | "line"> = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    mode: "index",
    intersect: false,
  },
  plugins: {
    legend: {
      display: true,
      position: "bottom",
      labels: {
        usePointStyle: true,
        pointStyle: "rectRounded",
      },
    },
    tooltip: {
      callbacks: {
        label: (context) => {
          const label = context.dataset.label || "";
          const value = context.parsed.y ?? 0;
          return `${label}: ${value}`;
        },
      },
    },
  },
  scales: {
    x: {
      stacked: true,
      grid: {
        display: false,
      },
    },
    y: {
      stacked: true,
      beginAtZero: true,
      ticks: {
        stepSize: 1,
        precision: 0,
      },
    },
    yCandidates: {
      position: "right",
      beginAtZero: true,
      grid: {
        drawOnChartArea: false,
      },
      title: {
        display: true,
        text: "Remaining candidates",
      },
    },
  },
};

const ChartVisualizationPanelComponent = ({
  guesses,
  evaluations,
}: ChartVisualizationPanelProps) => {
  const [candidateTrend, setCandidateTrend] = useState<number[]>([]);

  useEffect(() => {
    let isMounted = true;

    const computeCandidateTrend = async () => {
      if (!guesses.length) {
        if (isMounted) setCandidateTrend([]);
        return;
      }

      const wordList = await getWordListSnapshot();
      if (!isMounted) return;
      if (!wordList.length) {
        setCandidateTrend([]);
        return;
      }

      let candidates = wordList.map((word) => word.toUpperCase());
      const trend: number[] = [];

      for (let i = 0; i < guesses.length; i++) {
        const guess = guesses[i]?.toUpperCase();
        const evalRow = evaluations[i];

        if (!guess || !evalRow || evalRow.length !== guess.length) {
          trend.push(candidates.length);
          continue;
        }

        const pattern = evaluationToPattern(evalRow);
        candidates = filterCandidates(candidates, guess, pattern);
        trend.push(candidates.length);
      }

      if (isMounted) {
        setCandidateTrend(trend);
      }
    };

    computeCandidateTrend();
    return () => {
      isMounted = false;
    };
  }, [guesses, evaluations]);

  const { labels, datasets, hasData, latestRemaining } = useMemo(() => {
    const labels = guesses.map((guess, idx) => guess?.toUpperCase() || `Guess ${idx + 1}`);
    const counts = guesses.map((_, idx) => {
      const evalRow = evaluations[idx] ?? [];
      const base: Record<LetterState, number> = {
        correct: 0,
        present: 0,
        absent: 0,
        unused: 0,
      };

      evalRow.forEach((state) => {
        base[state] = (base[state] || 0) + 1;
      });

      return base;
    });

    const barDatasets: ChartDataset<"bar">[] = STATUS_ORDER.filter((status) => status !== "unused").map((status) => ({
      label: status.charAt(0).toUpperCase() + status.slice(1),
      data: counts.map((row) => row[status] ?? 0),
      backgroundColor: STATUS_COLOR[status],
      borderRadius: 4,
      order: 2,
    }));

    const lineData = guesses.map((_, idx) => candidateTrend[idx] ?? null);
    const lineDataset: ChartDataset<"line"> | null = lineData.some((value) => value !== null)
      ? {
          type: "line" as const,
          label: "Remaining Candidates",
          data: lineData,
          borderColor: "#3b82f6",
          backgroundColor: "#3b82f650",
          borderWidth: 2,
          tension: 0.35,
          yAxisID: "yCandidates",
          pointRadius: 4,
          pointHoverRadius: 6,
          spanGaps: true,
          order: 1,
        }
      : null;

    const datasets = lineDataset ? [...barDatasets, lineDataset] : barDatasets;
    const latestRemaining = candidateTrend.length
      ? candidateTrend[candidateTrend.length - 1]
      : null;

    return {
      labels,
      datasets,
      hasData: guesses.length > 0 && evaluations.length > 0,
      latestRemaining,
    };
  }, [guesses, evaluations, candidateTrend]);

  return (
    <div className="card-elevated flex flex-col gap-4 p-4">
      <div>
        <h2 className="text-lg font-semibold">Guess Feedback Overview</h2>
        <p className="text-sm text-muted-foreground">
          Track feedback quality and how many candidate words remain after each guess.
        </p>
        {hasData && latestRemaining !== null && (
          <p className="text-xs text-muted-foreground">
            Remaining candidates after last guess: <strong>{latestRemaining}</strong>
          </p>
        )}
      </div>
      {hasData ? (
        <div className="h-64">
          <Chart<"bar" | "line"> type="bar" data={{ labels, datasets } as ChartData<"bar" | "line">} options={chartOptions} />
        </div>
      ) : (
        <div className="rounded-md border border-dashed border-muted-foreground/40 p-4 text-sm text-muted-foreground">
          Submit at least one guess to see the visualization.
        </div>
      )}
    </div>
  );
};

export const ChartVisualizationPanel = memo(ChartVisualizationPanelComponent);

function evaluationToPattern(evals: LetterState[]): string {
  return evals.map((state) => STATE_TO_DIGIT[state] ?? "0").join("");
}

function filterCandidates(candidates: string[], guess: string, pattern: string): string[] {
  return candidates.filter((candidate) => getPattern(guess, candidate) === pattern);
}

function getPattern(guess: string, target: string): string {
  const guessChars = guess.toUpperCase().split("");
  const targetChars = target.toUpperCase().split("");
  const result = Array(guessChars.length).fill("0");
  const remainingCounts: Record<string, number> = {};

  for (let i = 0; i < targetChars.length; i++) {
    const ch = targetChars[i];
    remainingCounts[ch] = (remainingCounts[ch] ?? 0) + 1;
  }

  for (let i = 0; i < guessChars.length; i++) {
    if (guessChars[i] === targetChars[i]) {
      result[i] = "2";
      remainingCounts[guessChars[i]] -= 1;
    }
  }

  for (let i = 0; i < guessChars.length; i++) {
    if (result[i] === "2") continue;
    const ch = guessChars[i];
    const remaining = remainingCounts[ch] ?? 0;
    if (remaining > 0) {
      result[i] = "1";
      remainingCounts[ch] = remaining - 1;
    }
  }

  return result.join("");
}
