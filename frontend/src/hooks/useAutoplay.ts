"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { solverAPI } from "@/utils/api-utils";
import type {
  AutoplayRequestPayload,
  AutoplayResponse,
  AutoplayStep,
} from "@/types/types";

const STEP_INTERVAL_MS = 1400;

type AutoplayStatus = "idle" | "requesting" | "playing" | "completed";

type UseAutoplayResult = {
  session: AutoplayResponse | null;
  status: AutoplayStatus;
  error: string | null;
  activeStepIndex: number;
  isRequesting: boolean;
  isPlaying: boolean;
  runAutoplay: (payload: AutoplayRequestPayload) => Promise<void>;
  replay: () => void;
  stop: () => void;
  reset: () => void;
};

export function useAutoplay(stepInterval: number = STEP_INTERVAL_MS): UseAutoplayResult {
  const [session, setSession] = useState<AutoplayResponse | null>(null);
  const [status, setStatus] = useState<AutoplayStatus>("idle");
  const [error, setError] = useState<string | null>(null);
  const [activeStepIndex, setActiveStepIndex] = useState(-1);

  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const stepsRef = useRef<AutoplayStep[]>([]);

  const clearPlayback = useCallback(() => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }
  }, []);

  const finishPlayback = useCallback(() => {
    clearPlayback();
    setStatus("completed");
  }, [clearPlayback]);

  const schedulePlayback = useCallback(
    (startIndex: number) => {
      const steps = stepsRef.current;
      if (!steps.length) {
        setActiveStepIndex(-1);
        finishPlayback();
        return;
      }

      let nextIndex = Math.max(0, startIndex);

      const runStep = () => {
        setActiveStepIndex(nextIndex);
        if (nextIndex >= steps.length - 1) {
          timeoutRef.current = setTimeout(() => {
            finishPlayback();
          }, stepInterval);
          return;
        }

        nextIndex += 1;
        timeoutRef.current = setTimeout(runStep, stepInterval);
      };

      clearPlayback();
      timeoutRef.current = setTimeout(runStep, 0);
    },
    [clearPlayback, finishPlayback, stepInterval]
  );

  const runAutoplay = useCallback(
    async (payload: AutoplayRequestPayload) => {
      clearPlayback();
      setStatus("requesting");
      setError(null);
      setActiveStepIndex(-1);

      try {
        const sanitizedPayload = {
          ...payload,
          answer: payload.answer?.trim().toUpperCase() || undefined,
        };
        const response = await solverAPI.runAutoplay(sanitizedPayload);
        setSession(response);
        stepsRef.current = response.steps;

        if (response.steps.length === 0) {
          setStatus("completed");
          return;
        }

        setStatus("playing");
        schedulePlayback(0);
      } catch (err) {
        console.error("Autoplay error:", err);
        setSession(null);
        stepsRef.current = [];
        setStatus("idle");
        const message = err instanceof Error ? err.message : "Failed to run autoplay";
        setError(message);
      }
    },
    [clearPlayback, schedulePlayback]
  );

  const replay = useCallback(() => {
    if (!session || !session.steps.length) {
      return;
    }
    setActiveStepIndex(-1);
    setStatus("playing");
    stepsRef.current = session.steps;
    schedulePlayback(0);
  }, [schedulePlayback, session]);

  const stop = useCallback(() => {
    if (status === "idle" || status === "completed") {
      return;
    }
    clearPlayback();
    setStatus("idle");
    setActiveStepIndex(-1);
  }, [clearPlayback, status]);

  const reset = useCallback(() => {
    clearPlayback();
    setSession(null);
    setStatus("idle");
    setError(null);
    setActiveStepIndex(-1);
    stepsRef.current = [];
  }, [clearPlayback]);

  useEffect(() => {
    return () => {
      clearPlayback();
    };
  }, [clearPlayback]);

  return {
    session,
    status,
    error,
    activeStepIndex,
    isRequesting: status === "requesting",
    isPlaying: status === "playing",
    runAutoplay,
    replay,
    stop,
    reset,
  };
}
