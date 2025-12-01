"use client";

import { useEffect, useMemo, useState } from "react";
import { BUTTON } from "@/constants/constants";
import { useAutoplay } from "@/hooks/useAutoplay";
import type { SolverStrategy } from "@/types/types";
import { useGameStore } from "@/stores/game-store";
import { AutoplayTranscriptModal } from "@/components/AutoplayTranscriptModal";

const STRATEGIES: { value: SolverStrategy; label: string }[] = [
  { value: "entropy", label: "Entropy" },
  { value: "better_entropy", label: "Better Entropy" },
  { value: "frequency", label: "Frequency" },
  { value: "random", label: "Random" },
  { value: "k_beam", label: "K-Beam" },
];

type AutoplayPanelProps = {
  autoplayState: ReturnType<typeof useAutoplay>;
};

export function AutoplayPanel({ autoplayState }: AutoplayPanelProps) {
  const [strategy, setStrategy] = useState<SolverStrategy>("better_entropy");
  const [maxAttempts, setMaxAttempts] = useState(6);
  const [allowRepeats, setAllowRepeats] = useState(false);
  const [answerInput, setAnswerInput] = useState("");
  const [isTranscriptOpen, setTranscriptOpen] = useState(false);

  const {
    session,
    status,
    error,
    activeStepIndex,
    isRequesting,
    isPlaying,
    runAutoplay,
    replay,
    stop,
    reset,
  } = autoplayState;

  const currentAnswer = useGameStore((state) => state.answer);
  const syncAutoplayProgress = useGameStore((state) => state.syncAutoplayProgress);
  const stopAutoplayMode = useGameStore((state) => state.stopAutoplayMode);

  const hasTranscript = Boolean(session?.steps?.length);
  const isBusy = isRequesting || isPlaying;

  const statusLabel = useMemo(() => {
    switch (status) {
      case "requesting":
        return "Setting up";
      case "playing":
        return "Replaying";
      case "completed":
        return session?.solved ? "Solved run" : "Run complete";
      default:
        return "Ready";
    }
  }, [session?.solved, status]);

  const totalSteps = session?.steps?.length ?? 0;

  const progressLabel = useMemo(() => {
    if (!totalSteps) {
      return "0 / 0";
    }
    const current = activeStepIndex < 0 ? 0 : Math.min(activeStepIndex + 1, totalSteps);
    return `${current} / ${totalSteps}`;
  }, [activeStepIndex, totalSteps]);

  const handleAttemptsChange = (value: string) => {
    const parsed = Number(value);
    if (Number.isNaN(parsed)) {
      return;
    }
    const clamped = Math.max(1, Math.min(10, parsed));
    setMaxAttempts(clamped);
  };

  const handleRun = () => {
    const fallbackAnswer = answerInput.trim() || currentAnswer || undefined;
    runAutoplay({
      strategy,
      max_attempts: maxAttempts,
      allow_repeats: allowRepeats,
      answer: fallbackAnswer,
    });
  };

  const canReplay = hasTranscript && !isBusy;

  useEffect(() => {
    if (status === "requesting") {
      setTranscriptOpen(false);
    }
  }, [status]);

  useEffect(() => {
    if (!session) {
      if (status !== "requesting") {
        stopAutoplayMode();
      }
      return;
    }

    syncAutoplayProgress({
      answer: session.answer,
      steps: session.steps,
      uptoIndex: activeStepIndex,
    });

    if (status !== "playing") {
      stopAutoplayMode();
    }
  }, [
    session,
    activeStepIndex,
    status,
    syncAutoplayProgress,
    stopAutoplayMode,
  ]);

  if (isTranscriptOpen && session?.steps?.length) {
    return (
      <AutoplayTranscriptModal
        isOpen
        onClose={() => setTranscriptOpen(false)}
        steps={session.steps}
        answer={session.answer}
        attempts={session.attempts_used}
        solved={session.solved}
      />
    );
  }

  return (
    <section className="rounded-2xl bg-white/85 p-6 shadow-soft ring-1 ring-neutral-200/70 backdrop-blur">
      <header className="space-y-1">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-primary-500">
          Autoplay Lab
        </p>
        <h2 className="text-xl font-semibold text-neutral-900">Watch the agent play</h2>
        <p className="text-sm text-neutral-500">
          Spin up a fully automated run and watch each reasoning step unfold.
        </p>
      </header>

      <div className="mt-5 grid gap-4 md:grid-cols-2">
        <label className="text-xs font-semibold uppercase text-neutral-500">
          Strategy
          <select
            value={strategy}
            onChange={(event) => setStrategy(event.target.value as SolverStrategy)}
            disabled={isBusy}
            className="mt-2 w-full rounded-xl border border-neutral-200 bg-white px-3 py-2 text-sm font-semibold text-neutral-800 shadow-soft focus:outline-none focus:ring-2 focus:ring-primary-100 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {STRATEGIES.map(({ value, label }) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </select>
        </label>

        <label className="text-xs font-semibold uppercase text-neutral-500">
          Max attempts
          <input
            type="number"
            min={1}
            max={10}
            value={maxAttempts}
            onChange={(event) => handleAttemptsChange(event.target.value)}
            disabled={isBusy}
            className="mt-2 w-full rounded-xl border border-neutral-200 bg-white px-3 py-2 text-sm font-semibold text-neutral-800 shadow-soft focus:outline-none focus:ring-2 focus:ring-primary-100 disabled:cursor-not-allowed disabled:opacity-60"
          />
        </label>

        <label className="md:col-span-2 text-xs font-semibold uppercase text-neutral-500">
          Custom answer (optional)
          <input
            type="text"
            maxLength={5}
            placeholder="Leave blank for random"
            value={answerInput}
            onChange={(event) => setAnswerInput(event.target.value.toUpperCase())}
            disabled={isBusy}
            className="mt-2 w-full rounded-xl border border-neutral-200 bg-white px-3 py-2 text-sm font-semibold text-neutral-800 shadow-soft focus:outline-none focus:ring-2 focus:ring-primary-100 disabled:cursor-not-allowed disabled:opacity-60"
          />
        </label>

        <label className="md:col-span-2 flex items-center gap-3 rounded-2xl border border-neutral-200 bg-neutral-50/70 px-4 py-3 text-sm font-medium text-neutral-700">
          <input
            type="checkbox"
            checked={allowRepeats}
            onChange={(event) => setAllowRepeats(event.target.checked)}
            disabled={isBusy}
            className="h-4 w-4 rounded border-neutral-300 text-primary-600 focus:ring-primary-200"
          />
          Allow repeated letters
        </label>
      </div>

      {error && (
        <div className="mt-4 rounded-2xl border border-red-100 bg-red-50/80 px-4 py-3 text-sm text-red-700">
          {error}
        </div>
      )}

      <div className="mt-4 flex gap-3">
        <button
          onClick={handleRun}
          disabled={isBusy}
          className={`${BUTTON.secondary} flex-1 text-sm`}
        >
          {isRequesting ? "Running..." : "Start"}
        </button>
        <button
          onClick={replay}
          disabled={!canReplay}
          className={`${BUTTON.secondary} text-sm`}
        >
          Replay
        </button>
        <button
          onClick={stop}
          disabled={!isBusy}
          className={`${BUTTON.secondary} text-sm`}
        >
          Stop
        </button>
      </div>

      <StatusStrip
        statusLabel={statusLabel}
        progressLabel={progressLabel}
        solved={session?.solved ?? null}
      />

      {session && (
        <>
          <OutcomeSummary
            answer={session.answer}
            attempts={session.attempts_used}
            solved={session.solved}
          />
          <div className="mt-3">
            {session.steps.length > 0 ? (
              <button
                type="button"
                onClick={() => setTranscriptOpen(true)}
                className="w-full rounded-2xl border border-neutral-200 px-4 py-3 text-sm font-semibold text-neutral-700 hover:bg-neutral-50"
              >
                View solver transcript
              </button>
            ) : (
              <p className="rounded-2xl border border-dashed border-neutral-200 bg-neutral-50/80 px-4 py-3 text-sm text-neutral-500">
                Transcript becomes available after the solver makes at least one guess.
              </p>
            )}
          </div>
        </>
      )}
    </section>
  );
}

function StatusStrip({
  statusLabel,
  progressLabel,
  solved,
}: {
  statusLabel: string;
  progressLabel: string;
  solved: boolean | null;
}) {
  const badgeClass = solved == null
    ? "bg-neutral-100 text-neutral-600"
    : solved
      ? "bg-emerald-50 text-emerald-700"
      : "bg-amber-50 text-amber-700";

  const badgeLabel = solved == null ? "Idle" : solved ? "Solved" : "Unsolved";

  return (
    <div className="mt-4 flex items-center justify-between rounded-2xl border border-neutral-100 bg-neutral-50/60 px-4 py-3 text-sm text-neutral-700">
      <div className="flex flex-col">
        <span className="text-xs font-semibold uppercase tracking-[0.2em] text-neutral-500">
          Status
        </span>
        <span className="font-medium text-neutral-800">{statusLabel}</span>
      </div>
      <div className="flex items-center gap-3">
        <span className="text-xs font-semibold uppercase tracking-[0.2em] text-neutral-500">
          Steps
        </span>
        <span className="font-mono text-sm text-neutral-900">{progressLabel}</span>
        <span className={`rounded-full px-3 py-1 text-xs font-semibold ${badgeClass}`}>
          {badgeLabel}
        </span>
      </div>
    </div>
  );
}

function OutcomeSummary({
  answer,
  attempts,
  solved,
}: {
  answer: string;
  attempts: number;
  solved: boolean;
}) {
  return (
    <div className="mt-4 rounded-2xl border border-neutral-100 bg-gradient-to-br from-white to-neutral-50 px-5 py-4 text-sm text-neutral-700">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-neutral-500">
            Answer
          </p>
          <p className="text-2xl font-semibold tracking-[0.3em] text-neutral-900">{answer}</p>
        </div>
        <div className="text-right">
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-neutral-500">
            Attempts Used
          </p>
          <p className="text-lg font-semibold text-neutral-900">{attempts}</p>
          <p className={`text-xs font-medium ${solved ? "text-emerald-600" : "text-amber-600"}`}>
            {solved ? "Solved automatically" : "Solver stalled"}
          </p>
        </div>
      </div>
    </div>
  );
}

