import React from "react";
import Link from "next/link";
import { BUTTON } from "@/constants/constants";
import { AlgorithmType } from "@/types/types";

interface GameControlsProps {
    onShowStats: () => void;
    onRunAgent?: () => void;
    isAgentRunning?: boolean;
    isGameOver?: boolean;
    selectedAlgorithm?: AlgorithmType;
    onAlgorithmChange?: (algorithm: AlgorithmType) => void;
}

export function GameControls({ 
    onShowStats, 
    onRunAgent, 
    isAgentRunning, 
    isGameOver,
    selectedAlgorithm = 'dfs',
    onAlgorithmChange 
}: GameControlsProps) {
    return (
        <div className="flex flex-col sm:flex-row gap-4 w-full max-w-md">
            {onRunAgent && (
                <div className="flex flex-col gap-2 flex-1">
                    {onAlgorithmChange && (
                        <select 
                            value={selectedAlgorithm}
                            onChange={(e) => onAlgorithmChange(e.target.value as AlgorithmType)}
                            disabled={isAgentRunning || isGameOver}
                            className="w-full px-4 py-2 rounded-lg border-2 border-gray-700 bg-gray-800 text-white disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none focus:border-blue-500"
                        >
                            <option value="dfs">DFS (Depth-First Search)</option>
                            <option value="hill-climbing">Hill Climbing</option>
                            <option value="simulated-annealing">Simulated Annealing</option>
                        </select>
                    )}
                    <button 
                        onClick={onRunAgent} 
                        disabled={isAgentRunning || isGameOver}
                        className={`${BUTTON.primary} disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center`}
                    >
                        <svg
                            className="w-4 h-4 mr-2"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
                            />
                        </svg>
                        {isAgentRunning ? "Agent Running..." : "🤖 Agent Solve"}
                    </button>
                </div>
            )}
            
            <Link href="/scores" className={`${BUTTON.secondary} flex-1 text-center flex items-center justify-center`}>
                <svg
                    className="w-4 h-4 mr-2"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                >
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                    />
                </svg>
                Score History
            </Link>

            <button onClick={onShowStats} className={`${BUTTON.accent} flex-1 flex items-center justify-center`}>
                <svg
                    className="w-4 h-4 mr-2"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                >
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                    />
                </svg>
                Statistics
            </button>
        </div>
    );
}
