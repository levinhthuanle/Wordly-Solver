"use client";

import { useState } from "react";
import { GameBoard } from "@/components/GameBoard";
import { GameOverModal } from "@/components/GameOverModal";
import { GameHeader } from "@/components/GameHeader";
import StatsModal from "@/components/StatsModal";
import { LAYOUT } from "@/constants/constants";
import dynamic from "next/dynamic";
import { useGameController } from "@/hooks/useGameController";
import { AISuggestionPanel } from "@/components/AISuggestionPanel";
import { AttemptsCounter } from "@/components/AttemptsCounter";
import { useGameStore } from "@/stores/game-store";
import { useAISuggestions } from "@/hooks/useAISuggestions";
import { SugesstionResult } from "@/components/SugesstionResult";

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

  const hasSuggestion = Boolean(suggestion) && !isLoading;

  const panelContent = (
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

      <div className="grid gap-6 xl:grid-cols-[380px_minmax(0,1fr)]">
        <aside className="hidden xl:flex flex-col">
          {panelContent}
        </aside>

        <section className="flex flex-col gap-6">
          <div className="card-elevated flex flex-col items-center gap-4 p-6">
            <GameBoard />
            <AttemptsCounter attempts={guesses.length} maxAttempts={6} />
          </div>

          {isKeyboardVisible && (
            <div className="card-elevated px-4 pb-6 pt-4">
              <OnscreenKeyboard />
            </div>
          )}
        </section>
      </div>

      <div className="space-y-4 xl:hidden">
        {panelContent}
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
