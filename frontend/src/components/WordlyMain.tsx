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
import { GameActions } from "@/components/GameActions";
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

  return (
    <div className={LAYOUT.container}>
      {/* Elegant header card */}
      <div className="card">
        <GameHeader onShowStats={() => setShowStats(true)} />
      </div>

      {/* Container: Relative positioning is key here so children can be absolute */}
      <div className="relative h-[calc(100vh-64px)] w-full overflow-hidden bg-gray-50">
        
        {/* FLOATING PANEL (Left) */}
        {/* absolute: Takes it out of flow. 
            left-4 top-4 bottom-4: Pins it to the left with a "floating" gap. 
            z-20: Ensures it sits above the background. */}
        <div className="absolute left-4 top-4 bottom-4 bg-white/95 backdrop-blur-sm rounded-2xl shadow-2xl border border-white/20 overflow-hidden z-20 hidden xl:block">
          {/* Scrollable internal container */}
          <div className="h-full overflow-y-auto p-4 space-y-4">
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
        </div>

        {/* CENTER COLUMN: Main Game Area */}
        {/* w-full h-full: Takes up the WHOLE screen space.
            items-center: Centers the board perfectly in the middle of the viewport. */}
        <main className="w-full h-full flex flex-col items-center justify-center relative z-10">
          
          {/* 1. The Board Area */}
          <div className="flex-1 flex flex-col items-center justify-center min-h-0 w-full p-4">
            <div className="card-elevated p-6 bg-white rounded-xl shadow-sm border border-gray-100 flex flex-col items-center">
              <GameBoard />
              <div className="mt-4">
                <AttemptsCounter attempts={guesses.length} maxAttempts={6} />
              </div>
            </div>
          </div>

          {/* 2. The Keyboard Area */}
          {isKeyboardVisible && (
            <div className="w-full max-w-lg shrink-0 px-4 pb-6">
              <OnscreenKeyboard />
            </div>
          )}

        </main>
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
