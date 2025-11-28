import Link from "next/link";

interface GameActionsProps {
  onShowStats?: () => void;
}

export const GameActions = ({ onShowStats }: GameActionsProps) => {
  return (
    <div className="flex flex-wrap items-center justify-center gap-2 sm:gap-3">
      <Link
        href="/scores"
        className="px-3 py-2 text-sm font-medium text-neutral-700 bg-white border border-neutral-200 rounded-xl hover:bg-primary-50 hover:text-primary-600 hover:border-primary-300 transition-all flex items-center gap-1.5 whitespace-nowrap"
      >
        <img className="w-4 h-4" src="/assets/history.svg" alt="Score History" />
        Score History
      </Link>

      {onShowStats && (
        <button
          onClick={onShowStats}
          className="px-3 py-2 text-sm font-medium text-neutral-700 bg-white border border-neutral-200 rounded-xl hover:bg-accent-purple/10 hover:text-accent-purple hover:border-accent-purple/30 transition-all flex items-center gap-1.5 whitespace-nowrap"
        >
          <img className="w-4 h-4" src="/assets/analytics.svg" alt="Game Statistics" />
          Statistics
        </button>
      )}
    </div>
  );
};
