"use client";

import { AutoplayStep } from "@/types/types";
import { FC } from "react";

interface AutoplayTranscriptModalProps {
  isOpen: boolean;
  onClose: () => void;
  steps: AutoplayStep[];
  answer: string;
  attempts: number;
  solved: boolean;
}

const FEEDBACK_COLORS: Record<string, string> = {
  "2": "bg-emerald-500",
  "1": "bg-amber-400",
  "0": "bg-neutral-300",
};

const FEEDBACK_BOX_STYLES: Record<string, string> = {
  "2": "bg-emerald-500 text-white",
  "1": "bg-amber-400 text-white",
  "0": "bg-neutral-300 text-neutral-700",
};

export const AutoplayTranscriptModal: FC<AutoplayTranscriptModalProps> = ({
  isOpen,
  onClose,
  steps,
  answer,
  attempts,
  solved,
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center bg-black/50 p-4">
      <div className="relative flex w-full max-w-3xl flex-col rounded-3xl bg-white p-6 shadow-strong">
        <button
          type="button"
          aria-label="Close transcript"
          onClick={onClose}
          className="absolute right-4 top-4 rounded-full border border-neutral-200 bg-white px-3 py-1 text-sm font-semibold text-neutral-600 hover:bg-neutral-50"
        >
          Close
        </button>

        <header className="space-y-2 pr-16">
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-primary-500">
            Autoplay transcript
          </p>
          <h2 className="text-2xl font-semibold text-neutral-900">{answer}</h2>
          <p className="text-sm text-neutral-600">
            {solved
              ? `Solved automatically in ${attempts} ${attempts === 1 ? "guess" : "guesses"}.`
              : "The solver ran out of attempts."}
          </p>
        </header>

        <div className="mt-4 max-h-[60vh] space-y-3 overflow-y-auto pr-1">
          {steps.map((step, index) => (
            <TranscriptStepCard key={`${step.guess}-${index}`} step={step} index={index} />
          ))}
        </div>
      </div>
    </div>
  );
};

const TranscriptStepCard = ({
  step,
  index,
}: {
  step: AutoplayStep;
  index: number;
}) => (
  <article className="rounded-2xl border border-neutral-200 bg-white px-4 py-3">
    <header className="flex items-center justify-between text-xs font-semibold uppercase tracking-[0.2em] text-neutral-500">
      <span>Guess {index + 1}</span>
      <span className="rounded-full border border-neutral-200 px-3 py-1 text-[0.65rem] font-medium normal-case tracking-widest text-neutral-600">
        {step.remaining_candidates} left
      </span>
    </header>

    <GuessLettersRow guess={step.guess} feedback={step.feedback} />

    <div className="mt-3 flex items-center gap-2 text-xs text-neutral-500">
      <span className="font-semibold uppercase tracking-[0.2em]">Feedback</span>
      <FeedbackRow feedback={step.feedback} />
    </div>

    {step.thoughts && step.thoughts.length > 0 && (
      <details className="mt-3 rounded-2xl border border-neutral-100 bg-neutral-50/70 px-3 py-2 text-xs text-neutral-600">
        <summary className="cursor-pointer text-neutral-700">Agent thoughts</summary>
        <ul className="mt-2 space-y-1">
          {step.thoughts.map((thought, idx) => (
            <li key={`${thought.message}-${idx}`}>
              {thought.message}
              {typeof thought.score === "number" && (
                <span className="text-neutral-500"> · score {thought.score.toFixed(2)}</span>
              )}
            </li>
          ))}
        </ul>
      </details>
    )}
  </article>
);

const FeedbackRow = ({ feedback }: { feedback: string }) => (
  <span className="flex gap-1">
    {feedback.split("").map((state, index) => (
      <span
        key={`${state}-${index}`}
        className={`h-4 w-4 rounded ${FEEDBACK_COLORS[state] ?? "bg-neutral-200"}`}
      />
    ))}
  </span>
);

const GuessLettersRow = ({ guess, feedback }: { guess: string; feedback: string }) => {
  const letters = guess.split("");
  const states = feedback.split("");
  return (
    <div className="mt-3 grid grid-cols-5 gap-1">
      {letters.map((letter, index) => (
        <span
          key={`${letter}-${index}`}
          className={`flex h-10 items-center justify-center rounded-lg text-base font-semibold uppercase tracking-[0.3em] ${
            FEEDBACK_BOX_STYLES[states[index]] ?? "bg-neutral-200 text-neutral-700"
          }`}
        >
          {letter}
        </span>
      ))}
    </div>
  );
};
