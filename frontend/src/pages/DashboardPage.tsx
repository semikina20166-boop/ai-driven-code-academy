import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Code2, Loader2, Play } from "lucide-react";
import { api } from "../api/client";
import type { ProgressSummary, Track } from "../api/types";
import { useI18n, tx } from "../i18n/I18nContext";

const LANG_COLORS: Record<string, string> = {
  python:     "from-yellow-500/20 to-yellow-600/5 border-yellow-500/30",
  csharp:     "from-purple-500/20 to-purple-600/5 border-purple-500/30",
  php:        "from-indigo-500/20 to-indigo-600/5 border-indigo-500/30",
  javascript: "from-amber-500/20 to-amber-600/5 border-amber-500/30",
  java:       "from-red-500/20 to-red-600/5 border-red-500/30",
};

export function DashboardPage() {
  const { lang, t } = useI18n();
  const [tracks, setTracks] = useState<Track[]>([]);
  const [progress, setProgress] = useState<ProgressSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [starting, setStarting] = useState<number | null>(null);

  useEffect(() => {
    Promise.all([api.get<Track[]>("/tracks"), api.get<ProgressSummary>("/progress/summary")])
      .then(([tr, p]) => { setTracks(tr); setProgress(p); })
      .finally(() => setLoading(false));
  }, []);

  async function handleStart(trackId: number) {
    setStarting(trackId);
    try { await api.post(`/tracks/${trackId}/start`); }
    finally { setStarting(null); }
  }

  if (loading) {
    return (
      <div className="flex justify-center py-20">
        <Loader2 className="w-10 h-10 animate-spin text-academy-accent" />
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-xl sm:text-2xl font-bold mb-1">{tx(t.dashboard.title, lang)}</h1>
      <p className="text-academy-muted mb-5 text-sm sm:text-base">{tx(t.dashboard.subtitle, lang)}</p>

      {progress && (
        <div className="mb-6 p-4 rounded-xl border border-academy-border bg-academy-panel">
          <div className="text-sm text-academy-muted mb-1">{tx(t.dashboard.overallProgress, lang)}</div>
          <div className="text-xl sm:text-2xl font-semibold">
            {progress.completed_levels} / {progress.total_levels}{" "}
            <span className="text-sm font-normal text-academy-muted">{tx(t.dashboard.levels, lang)}</span>
          </div>
          <div className="mt-2 h-2 rounded-full bg-academy-bg overflow-hidden">
            <div
              className="h-full bg-academy-accent transition-all"
              style={{ width: `${progress.total_levels ? (100 * progress.completed_levels) / progress.total_levels : 0}%` }}
            />
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {tracks.map((track) => {
          const code = track.language?.code ?? "python";
          const gradient = LANG_COLORS[code] ?? LANG_COLORS.python;
          const done = progress?.by_track[code] ?? 0;

          return (
            <article key={track.id} className={`rounded-xl border bg-gradient-to-br p-4 sm:p-5 flex flex-col ${gradient}`}>
              <div className="flex items-start justify-between mb-3">
                <Code2 className="w-8 h-8 text-academy-accent" />
                <span className="text-xs text-academy-muted">
                  {done} {tx(t.dashboard.completed, lang)}
                </span>
              </div>
              <h2 className="text-lg font-semibold mb-1">{track.language?.name ?? track.title}</h2>
              <p className="text-sm text-academy-muted flex-1 mb-4">
                {track.description ?? tx(t.dashboard.defaultDesc, lang)}
              </p>
              <div className="flex gap-2">
                <button
                  type="button"
                  onClick={() => handleStart(track.id)}
                  disabled={starting === track.id}
                  className="flex items-center gap-1 px-3 py-1.5 text-sm rounded-lg border border-academy-border hover:bg-academy-bg/50 transition-colors"
                >
                  {starting === track.id
                    ? <Loader2 className="w-4 h-4 animate-spin" />
                    : <Play className="w-4 h-4" />}
                  {tx(t.dashboard.start, lang)}
                </button>
                <Link
                  to={`/tracks/${track.id}`}
                  className="flex-1 text-center py-1.5 text-sm rounded-lg bg-academy-accent hover:bg-blue-600 font-medium transition-colors"
                >
                  {tx(t.dashboard.levelMap, lang)}
                </Link>
              </div>
            </article>
          );
        })}
      </div>
    </div>
  );
}
