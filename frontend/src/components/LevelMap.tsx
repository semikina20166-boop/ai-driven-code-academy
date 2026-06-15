import { Link } from "react-router-dom";
import { CheckCircle2, Circle, Lock, Crown } from "lucide-react";
import type { LevelMapItem } from "../api/types";
import { useAuth } from "../context/AuthContext";

const DIFFICULTY_ORDER = ["easy", "medium", "hard"];
const DIFFICULTY_LABELS: Record<string, string> = {
  easy: "Начальный",
  medium: "Средний",
  hard: "Продвинутый",
};

interface LevelMapProps {
  trackId: number;
  levels: LevelMapItem[];
}

export function LevelMap({ trackId, levels }: LevelMapProps) {
  const grouped = DIFFICULTY_ORDER.map((code) => ({
    code,
    label: DIFFICULTY_LABELS[code] ?? code,
    items: levels.filter((l) => l.difficulty_code === code).sort((a, b) => a.order_num - b.order_num),
  }));

  return (
    <div className="space-y-8">
      {grouped.map((group) => (
        <section key={group.code}>
          <h3 className="text-sm font-medium text-academy-muted uppercase tracking-wider mb-4">
            {group.label}
          </h3>
          <div className="flex flex-wrap gap-3">
            {group.items.map((level) => (
              <LevelNode key={level.id} trackId={trackId} level={level} />
            ))}
          </div>
        </section>
      ))}
    </div>
  );
}

function LevelNode({ trackId, level }: { trackId: number; level: LevelMapItem }) {
  const { user } = useAuth();
  const isPremium = user?.is_premium;
  const isHard = level.difficulty_code === "hard";
  const isPremiumLocked = isHard && !isPremium;

  const locked = level.status === "locked";
  const completed = level.status === "completed";

  const content = (
    <>
      {isPremiumLocked ? (
        <div className="relative shrink-0 flex items-center justify-center w-8 h-8 rounded-full border border-amber-500/30 bg-amber-500/10 text-amber-400">
          <Crown className="w-4 h-4 fill-amber-400" />
        </div>
      ) : (
        <StatusIcon status={level.status} />
      )}
      <div className="text-left min-w-0 flex-1">
        <div className="flex items-center justify-between gap-1.5">
          <div className="text-xs text-academy-muted">Уровень {level.order_num}</div>
          {isHard && (
            <span className={`text-[9px] font-bold px-1.5 py-0.5 rounded-full ${isPremiumLocked ? 'text-amber-300 bg-amber-500/10 border border-amber-500/30' : 'text-academy-accent bg-academy-accent/10 border border-academy-accent/20'}`}>
              PRO
            </span>
          )}
        </div>
        <div className="font-medium truncate text-sm text-slate-100">{level.title}</div>
      </div>
    </>
  );

  const base =
    "flex items-center gap-3 p-4 rounded-xl border min-w-[200px] max-w-[280px] transition-all";

  if (isPremiumLocked) {
    return (
      <Link
        to="/billing"
        className={`${base} border-amber-500/20 bg-academy-panel hover:border-amber-500 hover:shadow-lg hover:shadow-amber-500/10`}
      >
        {content}
      </Link>
    );
  }

  if (locked) {
    return (
      <div className={`${base} border-academy-border bg-academy-panel/50 opacity-60 cursor-not-allowed`}>
        {content}
      </div>
    );
  }

  return (
    <Link
      to={`/tracks/${trackId}/levels/${level.id}`}
      className={`${base} border-academy-border bg-academy-panel hover:border-academy-accent hover:shadow-lg hover:shadow-blue-500/10 ${
        completed ? "border-academy-success/40" : "border-academy-accent/30"
      }`}
    >
      {content}
    </Link>
  );
}

function StatusIcon({ status }: { status: string }) {
  if (status === "completed") {
    return <CheckCircle2 className="w-8 h-8 text-academy-success shrink-0" />;
  }
  if (status === "open") {
    return <Circle className="w-8 h-8 text-academy-accent shrink-0" />;
  }
  return <Lock className="w-8 h-8 text-academy-muted shrink-0" />;
}
