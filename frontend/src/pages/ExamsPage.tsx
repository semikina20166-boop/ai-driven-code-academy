import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { BookOpen, Clock, Loader2, Lock, Unlock, Crown, CheckCircle2, Plus } from "lucide-react";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";
import { useI18n, tx } from "../i18n/I18nContext";
import type { Exam, Track } from "../api/types";
import { AddExamQuestionModal } from "../components/admin/AdminModals";

export function ExamsPage() {
  const { user } = useAuth();
  const { lang, t } = useI18n();
  const [exams, setExams] = useState<Exam[]>([]);
  const [tracks, setTracks] = useState<Track[]>([]);
  const [selectedTrackIds, setSelectedTrackIds] = useState<number[]>([]);
  const [loading, setLoading] = useState(true);
  const [addQuestionExamId, setAddQuestionExamId] = useState<number | null>(null);

  const isPremium = user?.is_premium;

  useEffect(() => {
    Promise.all([api.get<Exam[]>("/exams/available"), api.get<Track[]>("/tracks")]).then(([e, tr]) => {
      setExams(e);
      setTracks(tr);
      setSelectedTrackIds(tr.slice(0, 2).map((x) => x.id));
    }).finally(() => setLoading(false));
  }, []);

  async function registerSelectedTracks(examId: number) {
    await api.post("/exams/selected-tracks/register", {
      exam_id: examId,
      track_ids: selectedTrackIds,
    });
    alert(tx(t.exams.savedAlert, lang));
  }

  if (loading) {
    return (
      <div className="flex justify-center py-20">
        <Loader2 className="w-10 h-10 animate-spin text-academy-accent" />
      </div>
    );
  }

  const selectedExam = exams.find((e) => e.exam_type === "selected_tracks");

  const getTypeLabel = (type: string) => {
    const key = type as keyof typeof t.exams.types;
    return t.exams.types[key] ? tx(t.exams.types[key], lang) : type;
  };

  return (
    <div>
      <h1 className="text-xl sm:text-2xl font-bold mb-2 flex items-center gap-2">
        <BookOpen className="w-6 h-6 sm:w-7 sm:h-7 text-academy-accent" />
        {tx(t.exams.title, lang)}
      </h1>
      <p className="text-academy-muted mb-6 sm:mb-8 text-sm sm:text-base">
        {tx(t.exams.subtitle, lang)}
      </p>

      {selectedExam && isPremium && (
        <div className="mb-6 sm:mb-8 p-4 rounded-xl border border-academy-border bg-academy-panel">
          <h2 className="font-medium mb-3">{tx(t.exams.selectedTracks, lang)}</h2>
          <div className="flex flex-wrap gap-2 mb-3">
            {tracks.map((tr) => (
              <label key={tr.id} className="flex items-center gap-2 text-sm cursor-pointer">
                <input
                  type="checkbox"
                  checked={selectedTrackIds.includes(tr.id)}
                  onChange={(e) => {
                    setSelectedTrackIds((prev) =>
                      e.target.checked ? [...prev, tr.id] : prev.filter((id) => id !== tr.id),
                    );
                  }}
                  className="rounded"
                />
                {tr.language?.name}
              </label>
            ))}
          </div>
          <button
            type="button"
            onClick={() => registerSelectedTracks(selectedExam.id)}
            className="text-sm px-3 py-1.5 rounded-lg border border-academy-border hover:bg-academy-bg"
          >
            {tx(t.exams.saveSelection, lang)}
          </button>
        </div>
      )}

      <div className="grid gap-4">
        {exams.map((exam) => {
          const isSelectedTracksExam = exam.exam_type === "selected_tracks";
          const isExamPremiumLocked = isSelectedTracksExam && !isPremium;

          return (
            <article
              key={exam.id}
              className={`p-4 sm:p-5 rounded-xl border flex flex-col sm:flex-row sm:items-center gap-4 ${
                isExamPremiumLocked
                  ? "border-amber-500/20 bg-gradient-to-r from-amber-500/5 to-academy-panel"
                  : exam.available
                  ? "border-academy-accent/40 bg-academy-panel"
                  : "border-academy-border bg-academy-panel/50 opacity-80"
              }`}
            >
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <div className="text-xs text-academy-muted">{getTypeLabel(exam.exam_type)}</div>
                  {isSelectedTracksExam && (
                    <span className="flex items-center gap-0.5 text-[9px] font-bold px-1.5 py-0.5 rounded-full text-amber-300 bg-amber-500/10 border border-amber-500/30">
                      <Crown className="w-2.5 h-2.5 fill-amber-300" />
                      PRO
                    </span>
                  )}
                </div>
                <h2 className="font-semibold text-slate-100">{exam.title}</h2>
                {exam.description && <p className="text-sm text-academy-muted mt-1">{exam.description}</p>}
                <div className="flex flex-wrap gap-3 sm:gap-4 mt-2 text-xs text-academy-muted">
                  <span>{tx(t.exams.passPercentOf, lang)} {exam.pass_percent}%</span>
                  {exam.time_limit_min && (
                    <span className="flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      {exam.time_limit_min} {tx(t.exams.minutesShort, lang)}
                    </span>
                  )}
                  {exam.passed && exam.best_score != null && (
                    <span className="text-academy-success">
                      {tx(t.exams.scoreResult, lang)} {exam.best_score}%
                    </span>
                  )}
                </div>
              </div>

              {isExamPremiumLocked ? (
                <Link
                  to="/billing"
                  className="flex items-center justify-center gap-1.5 px-4 py-2 rounded-lg bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-500 hover:to-amber-600 text-academy-bg text-sm font-semibold shrink-0 w-full sm:w-auto"
                >
                  <Crown className="w-4 h-4 fill-academy-bg" />
                  {tx(t.exams.activatePro, lang)}
                </Link>
              ) : exam.passed ? (
                <span className="flex items-center justify-center gap-2 px-4 py-2 rounded-lg border border-academy-success/40 bg-academy-success/10 text-academy-success text-sm font-medium shrink-0 w-full sm:w-auto">
                  <CheckCircle2 className="w-4 h-4" />
                  {tx(t.exams.completed, lang)}
                </span>
              ) : exam.available ? (
                <Link
                  to={`/exams/${exam.id}/session`}
                  className="flex items-center justify-center gap-2 px-4 py-2 rounded-lg bg-academy-accent hover:bg-blue-600 text-sm font-medium shrink-0 w-full sm:w-auto"
                >
                  <Unlock className="w-4 h-4" />
                  {tx(t.exams.startShort, lang)}
                </Link>
              ) : (
                <span className="flex items-center gap-2 text-sm text-academy-muted shrink-0">
                  <Lock className="w-4 h-4" />
                  {tx(t.exams.locked, lang)}
                </span>
              )}
              {user?.is_admin && (
                <button
                  onClick={() => setAddQuestionExamId(exam.id)}
                  className="flex items-center gap-1 px-3 py-1.5 text-xs rounded-lg bg-purple-600 hover:bg-purple-700 font-medium transition-colors shrink-0"
                >
                  <Plus className="w-3.5 h-3.5" /> Добавить вопрос
                </button>
              )}
            </article>
          );
        })}
      </div>

      {addQuestionExamId !== null && (
        <AddExamQuestionModal
          examId={addQuestionExamId}
          isOpen={true}
          onClose={() => setAddQuestionExamId(null)}
          onSuccess={() => setAddQuestionExamId(null)}
        />
      )}
    </div>
  );
}
