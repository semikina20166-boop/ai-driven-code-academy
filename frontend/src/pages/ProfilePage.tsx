import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Crown, Award, Sparkles, Loader2, User as UserIcon, Calendar, CheckSquare } from "lucide-react";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";
import { useI18n, tx } from "../i18n/I18nContext";
import type { ProgressSummary, Track } from "../api/types";

export function ProfilePage() {
  const { user } = useAuth();
  const { lang, t } = useI18n();
  const [progress, setProgress] = useState<ProgressSummary | null>(null);
  const [tracks, setTracks] = useState<Track[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      api.get<ProgressSummary>("/progress/summary"),
      api.get<Track[]>("/tracks"),
    ])
      .then(([p, tr]) => {
        setProgress(p);
        setTracks(tr);
      })
      .catch((err) => console.error("Error loading profile stats:", err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center py-20">
        <Loader2 className="w-10 h-10 animate-spin text-academy-accent" />
      </div>
    );
  }

  const overallPercent = progress && progress.total_levels
    ? Math.round((progress.completed_levels / progress.total_levels) * 100)
    : 0;

  return (
    <div className="max-w-4xl mx-auto space-y-6 sm:space-y-8">
      {/* Profile Header Card */}
      <div className="rounded-2xl border border-academy-border bg-academy-panel p-5 sm:p-8 flex flex-col sm:flex-row items-center gap-4 sm:gap-6 relative overflow-hidden">
        {user?.is_premium && (
          <div className="absolute top-0 right-0 w-32 h-32 bg-amber-500/5 rounded-bl-full pointer-events-none" />
        )}

        {/* Avatar Placeholder */}
        <div className="w-16 h-16 sm:w-20 sm:h-20 rounded-2xl bg-academy-bg border border-academy-border flex items-center justify-center shrink-0">
          <UserIcon className="w-8 h-8 sm:w-10 sm:h-10 text-academy-accent" />
        </div>

        {/* User Info */}
        <div className="flex-1 text-center sm:text-left space-y-1 min-w-0">
          <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-white truncate">
            {user?.display_name || tx(t.profile.defaultName, lang)}
          </h1>
          <p className="text-academy-muted text-sm truncate">{user?.email}</p>
          <div className="flex flex-wrap items-center justify-center sm:justify-start gap-3 sm:gap-4 mt-2 text-xs text-academy-muted">
            <span className="flex items-center gap-1">
              <Calendar className="w-3.5 h-3.5" />
              {tx(t.profile.memberSince, lang)}
            </span>
          </div>
        </div>

        {/* Subscription Badge/Button */}
        <div className="shrink-0">
          {user?.is_premium ? (
            <div className="flex flex-col items-center sm:items-end gap-1">
              <div className="flex items-center gap-1.5 px-4 py-2 rounded-xl text-sm font-bold text-amber-300 border border-amber-500/30 bg-amber-500/10 shadow-[0_0_20px_-3px_rgba(251,191,36,0.25)]">
                <Crown className="w-4 h-4 fill-amber-300" />
                <span>Premium PRO</span>
              </div>
              <Link
                to="/billing"
                className="text-xs text-academy-muted hover:text-white underline mt-1.5 transition-colors"
              >
                {tx(t.profile.manageSubscription, lang)}
              </Link>
            </div>
          ) : (
            <div className="flex flex-col items-center sm:items-end gap-1">
              <span className="text-xs text-academy-muted mb-1">{tx(t.profile.basicAccount, lang)}</span>
              <Link
                to="/billing"
                className="flex items-center gap-1.5 px-4 py-2 rounded-xl text-sm font-semibold text-white bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-600 hover:to-amber-700 shadow-md shadow-amber-500/10 hover:shadow-lg transition-all"
              >
                <Sparkles className="w-4 h-4" />
                {tx(t.profile.buyPro, lang)}
              </Link>
            </div>
          )}
        </div>
      </div>

      <div className="grid md:grid-cols-12 gap-4 sm:gap-6">
        {/* Left Column: Progress Info */}
        <div className="md:col-span-8 space-y-6">
          {/* Progress Card */}
          <div className="rounded-2xl border border-academy-border bg-academy-panel p-5 sm:p-6 space-y-6">
            <h2 className="text-lg font-bold flex items-center gap-2">
              <Award className="w-5 h-5 text-academy-accent" />
              {tx(t.profile.yourProgress, lang)}
            </h2>

            {progress && (
              <div className="space-y-4">
                <div className="flex justify-between text-sm font-medium">
                  <span className="text-academy-muted">{tx(t.profile.completedOf, lang)}</span>
                  <span className="text-white">{progress.completed_levels} {tx(t.profile.outOf, lang)} {progress.total_levels} ({overallPercent}%)</span>
                </div>
                <div className="h-3 rounded-full bg-academy-bg overflow-hidden border border-academy-border">
                  <div
                    className="h-full bg-gradient-to-r from-academy-accent to-indigo-500 transition-all duration-500"
                    style={{ width: `${overallPercent}%` }}
                  />
                </div>
              </div>
            )}

            {/* Track Progress Breakdown */}
            <div className="pt-4 border-t border-academy-border space-y-4">
              <h3 className="text-sm font-semibold text-academy-muted uppercase tracking-wider">
                {tx(t.profile.byLanguage, lang)}
              </h3>

              <div className="grid sm:grid-cols-2 gap-4">
                {tracks.map((track) => {
                  const code = track.language?.code ?? "python";
                  const completed = progress?.by_track[code] ?? 0;
                  const total = 15;
                  const percent = Math.round((completed / total) * 100);

                  return (
                    <div
                      key={track.id}
                      className="p-4 rounded-xl border border-academy-border bg-academy-bg/40 space-y-2.5"
                    >
                      <div className="flex justify-between items-center">
                        <span className="text-sm font-bold text-white capitalize">{track.language?.name ?? track.title}</span>
                        <span className="text-xs text-academy-muted">{completed} / {total}</span>
                      </div>
                      <div className="h-1.5 rounded-full bg-academy-panel overflow-hidden">
                        <div
                          className="h-full bg-academy-accent"
                          style={{ width: `${percent}%` }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Premium Promo or Premium Info */}
        <div className="md:col-span-4">
          {!user?.is_premium ? (
            <div className="rounded-2xl border border-amber-500/20 bg-gradient-to-b from-amber-500/5 to-academy-panel p-5 sm:p-6 space-y-4 shadow-[0_4px_20px_-5px_rgba(251,191,36,0.1)]">
              <div className="w-10 h-10 rounded-xl bg-amber-500/10 flex items-center justify-center text-amber-400">
                <Crown className="w-5 h-5 fill-amber-400" />
              </div>
              <h3 className="font-bold text-white">{tx(t.profile.unlockPremium, lang)}</h3>
              <p className="text-xs text-academy-muted leading-relaxed">
                {tx(t.profile.premiumDesc, lang)}
              </p>
              <Link
                to="/billing"
                className="block w-full py-2.5 text-center text-xs font-semibold rounded-lg text-academy-bg bg-amber-400 hover:bg-amber-500 transition-colors shadow-lg shadow-amber-500/10"
              >
                {tx(t.profile.learnMorePro, lang)}
              </Link>
            </div>
          ) : (
            <div className="rounded-2xl border border-academy-border bg-academy-panel p-5 sm:p-6 space-y-4">
              <div className="w-10 h-10 rounded-xl bg-academy-bg border border-academy-border flex items-center justify-center text-amber-400">
                <Crown className="w-5 h-5 fill-amber-400" />
              </div>
              <h3 className="font-bold text-white">{tx(t.profile.proActive, lang)}</h3>
              <ul className="text-xs space-y-2 text-slate-300">
                {[t.profile.proF1, t.profile.proF2, t.profile.proF3, t.profile.proF4].map((f, i) => (
                  <li key={i} className="flex items-center gap-1.5">
                    <CheckSquare className="w-3.5 h-3.5 text-academy-success shrink-0" />
                    {tx(f, lang)}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
