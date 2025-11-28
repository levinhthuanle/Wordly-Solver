"use client";

import { useState } from "react";
import { GameBoard } from "@/components/GameBoard";
import { GameOverModal } from "@/components/GameOverModal";
import { GameHeader } from "@/components/GameHeader";
import StatsModal from "@/components/StatsModal";
import { BUTTON, LAYOUT } from "@/constants/constants";
import dynamic from "next/dynamic";
import { useGameController } from "@/hooks/useGameController";
import { AISuggestionPanel } from "@/components/AISuggestionPanel";
import { AttemptsCounter } from "@/components/AttemptsCounter";
import { useGameStore } from "@/stores/game-store";
import { useAISuggestions } from "@/hooks/useAISuggestions";
import { SugesstionResult } from "@/components/SugesstionResult";
import { AutoplayPanel } from "@/components/AutoplayPanel";
import { useAutoplay } from "@/hooks/useAutoplay";
import { ChartVisualizationPanel } from "@/components/ChartVisualizationPanel";

const OnscreenKeyboard = dynamic(
  () => import("@/components/keyboard/OnscreenKeyboard"),
  { ssr: false }
);

export default function WordlyMain() {
  const {
    showModal,
    setShowModal,
    handlePlayAgain,
    guesses,
    isWinner,
    answer,
  } = useGameController();

  const isGameOver = useGameStore((state) => state.isGameOver);
  const isKeyboardVisible = useGameStore((state) => state.isKeyboardVisible);
  const startNewGame = useGameStore((state) => state.startNewGame);
  const evaluations = useGameStore((state) => state.evaluations);

  const [showStats, setShowStats] = useState(false);

  const {
    suggestion,
    isLoading,
    error,
    selectedAlgorithm,
    setSelectedAlgorithm,
    getSuggestion,
    clearSuggestion,
  } = useAISuggestions();

  const autoplay = useAutoplay();

  const hasSuggestion = Boolean(suggestion) && !isLoading;

  const handleRetry = () => {
    clearSuggestion();
    autoplay.reset();
    startNewGame();
  };

  const aiPanelContent = (
    <div className="space-y-4">
      <AISuggestionPanel
        selectedAlgorithm={selectedAlgorithm}
        setSelectedAlgorithm={setSelectedAlgorithm}
        getSuggestion={getSuggestion}
        clearSuggestion={clearSuggestion}
        isLoading={isLoading}
        error={error}
        hasSuggestion={hasSuggestion}
      />
      {!error && (
        <SugesstionResult
          suggestion={hasSuggestion && suggestion ? suggestion : null}
          isLoading={isLoading}
        />
      )}
    </div>
  );

  return (
    <div className={`${LAYOUT.container} space-y-6`}>
      <div className="card">
        <GameHeader onShowStats={() => setShowStats(true)} />
      </div>

      <div className="grid gap-6 xl:grid-cols-[340px_minmax(0,1fr)_360px]">
        <section className="order-1 flex flex-col gap-6 xl:order-2">
          <div className="card-elevated flex flex-col items-center gap-5 p-6">
            <GameBoard />
            <div className="flex flex-col items-center gap-3 sm:flex-row sm:items-center sm:gap-4">
              <AttemptsCounter attempts={guesses.length} maxAttempts={6} />
              <button
                type="button"
                onClick={handleRetry}
                className={`${BUTTON.secondary} px-4 py-2 text-sm leading-none`}
              >
                Retry
              </button>
            </div>
          </div>

          {isKeyboardVisible && (
            <div className="card-elevated px-4 pb-6 pt-4">
              <OnscreenKeyboard />
            </div>
          )}
        </section>

        <aside className="order-2 flex flex-col gap-4 xl:order-1">
          {aiPanelContent}
        </aside>

        <aside className="order-3 flex flex-col gap-4 xl:order-3">
          <ChartVisualizationPanel guesses={guesses} evaluations={evaluations} />
          <AutoplayPanel autoplayState={autoplay} />
        </aside>
      </div>

      <GameOverModal
        isWinner={isWinner}
        wordToGuess={answer}
        numGuesses={guesses.length}
        onPlayAgain={handlePlayAgain}
        isOpen={showModal}
      />

      <StatsModal isOpen={showStats} onClose={() => setShowStats(false)} />
    </div>
  );
}
