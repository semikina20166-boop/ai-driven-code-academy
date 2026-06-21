import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Library, BookOpen, Crown, Lock, ChevronRight, Play, Loader2, Code2, ArrowRight, Plus } from "lucide-react";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";
import { useI18n, tx } from "../i18n/I18nContext";
import { AddLectureModal } from "../components/admin/AdminModals";

interface LectureLevel {
  id: number;
  order_num: number;
  title: string;
  difficulty_code: string;
  difficulty_name: string;
  theory: string | null;
}

interface TrackLectures {
  track_id: number;
  language_code: string;
  language_name: string;
  levels: LectureLevel[];
}

export function LecturesPage() {
  const { user } = useAuth();
  const { lang, t } = useI18n();
  const [data, setData] = useState<TrackLectures[]>([]);
  const [loading, setLoading] = useState(true);

  const [selectedTrack, setSelectedTrack] = useState<TrackLectures | null>(null);
  const [selectedLevel, setSelectedLevel] = useState<LectureLevel | null>(null);
  // Mobile: show sidebar or content
  const [mobileView, setMobileView] = useState<"sidebar" | "content">("sidebar");
  const [isLectureOpen, setIsLectureOpen] = useState(false);

  const reload = () => {
    api
      .get<TrackLectures[]>("/lectures")
      .then((res) => {
        setData(res);
        if (res.length > 0) {
          setSelectedTrack(res[0]);
          if (res[0].levels.length > 0) setSelectedLevel(res[0].levels[0]);
        }
      })
      .catch((err) => console.error("Error loading lectures:", err))
      .finally(() => setLoading(false));
  };

  const difficultyLabel = (code: string) => {
    const key = code as keyof typeof t.lectures.difficulty;
    return t.lectures.difficulty[key] ? tx(t.lectures.difficulty[key], lang) : code;
  };

  useEffect(() => {
    reload();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center py-20">
        <Loader2 className="w-10 h-10 animate-spin text-academy-accent" />
      </div>
    );
  }

  const groupedLevels = selectedTrack
    ? ["easy", "medium", "hard"].map((diff) => ({
        code: diff,
        label: difficultyLabel(diff),
        items: selectedTrack.levels.filter((l) => l.difficulty_code === diff),
      }))
    : [];

  return (
    <div>
      {/* Mobile: view toggle */}
      <div className="lg:hidden flex gap-2 mb-3">
        <button
          onClick={() => setMobileView("sidebar")}
          className={`flex-1 py-2 rounded-lg text-sm font-medium border transition-all ${
            mobileView === "sidebar"
              ? "bg-academy-accent/10 border-academy-accent text-white"
              : "border-academy-border text-academy-muted"
          }`}
        >
          {tx(t.lectures.contents, lang)}
        </button>
        <button
          onClick={() => setMobileView("content")}
          className={`flex-1 py-2 rounded-lg text-sm font-medium border transition-all ${
            mobileView === "content"
              ? "bg-academy-accent/10 border-academy-accent text-white"
              : "border-academy-border text-academy-muted"
          }`}
        >
          {tx(t.lectures.theory, lang)}
        </button>
      </div>

      <div className="grid lg:grid-cols-12 gap-4 lg:gap-6" style={{ minHeight: "calc(100vh - 9rem)" }}>
        {/* Left Sidebar: Tracks & Levels Navigation */}
        <aside className={`lg:col-span-4 flex flex-col gap-4 min-h-0 ${mobileView === "content" ? "hidden lg:flex" : "flex"}`}>
          {/* Track / Language Select */}
          <div className="rounded-xl border border-academy-border bg-academy-panel p-3 shrink-0">
            <label className="block text-xs font-semibold text-academy-muted uppercase tracking-wider mb-2 px-1">
              {tx(t.lectures.selectTrack, lang)}
            </label>
            <div className="flex flex-wrap gap-1">
              {data.map((track) => {
                const active = selectedTrack?.track_id === track.track_id;
                return (
                  <button
                    key={track.track_id}
                    onClick={() => {
                      setSelectedTrack(track);
                      if (track.levels.length > 0) {
                        setSelectedLevel(track.levels[0]);
                      } else {
                        setSelectedLevel(null);
                      }
                    }}
                    className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all ${
                      active
                        ? "bg-academy-accent/15 border-academy-accent text-white shadow-md shadow-academy-accent/10"
                        : "bg-academy-bg/40 border-academy-border text-academy-muted hover:text-white hover:bg-academy-panel"
                    }`}
                  >
                    <Code2 className="w-3.5 h-3.5" />
                    {track.language_name}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Levels List */}
          <div className="flex-1 rounded-xl border border-academy-border bg-academy-panel p-4 overflow-y-auto space-y-5 min-h-0 max-h-[60vh] lg:max-h-none">
            <div className="flex items-center justify-between mb-1">
            <h3 className="text-xs font-bold text-academy-muted uppercase tracking-wider">
              {tx(t.lectures.contents, lang)}
            </h3>
            {user?.is_admin && selectedTrack && (
              <button
                onClick={() => setIsLectureOpen(true)}
                className="flex items-center gap-1 px-2 py-1 text-xs rounded-lg bg-academy-accent hover:bg-blue-600 font-medium transition-colors"
              >
                <Plus className="w-3 h-3" /> Добавить лекцию
              </button>
            )}
          </div>

            {groupedLevels.map((group) => {
              if (group.items.length === 0) return null;
              return (
                <div key={group.code} className="space-y-1.5">
                  <span className="text-[10px] font-bold text-academy-muted uppercase tracking-wider block mb-1">
                    {group.label}
                  </span>
                  <div className="space-y-1">
                    {group.items.map((level) => {
                      const active = selectedLevel?.id === level.id;
                      const isHard = level.difficulty_code === "hard";
                      const isLocked = isHard && !user?.is_premium;

                      return (
                        <button
                          key={level.id}
                          onClick={() => {
                            setSelectedLevel(level);
                            setMobileView("content"); // auto-switch on mobile
                          }}
                          className={`w-full flex items-center justify-between gap-2 p-2.5 rounded-lg text-left transition-all text-xs border ${
                            active
                              ? "bg-academy-accent/10 border-academy-accent/30 text-white font-medium"
                              : "bg-transparent border-transparent text-slate-300 hover:bg-academy-bg/40 hover:text-white"
                          }`}
                        >
                          <span className="truncate flex-1 flex items-center gap-1.5">
                            <span className="opacity-60 font-mono shrink-0">{tx(t.lectures.lectureNum, lang)} {level.order_num}:</span>
                            <span className="truncate">{level.title.split(" — ")[1] || level.title}</span>
                          </span>
                          {isLocked ? (
                            <Crown className="w-3.5 h-3.5 text-amber-400 fill-amber-400 shrink-0" />
                          ) : (
                            <ChevronRight className={`w-3.5 h-3.5 opacity-40 shrink-0 ${active ? "translate-x-0.5 opacity-80" : ""}`} />
                          )}
                        </button>
                      );
                    })}
                  </div>
                </div>
              );
            })}
          </div>
        </aside>

        {/* Right Content Pane: Theory Reader */}
        <main className={`lg:col-span-8 flex flex-col rounded-xl border border-academy-border bg-academy-panel overflow-hidden min-h-0 ${mobileView === "sidebar" ? "hidden lg:flex" : "flex"}`}>
          {selectedLevel ? (
            <div className="flex flex-col h-full min-h-0">
              {/* Header */}
              <div className="p-4 sm:p-5 border-b border-academy-border bg-academy-bg/20 flex flex-col sm:flex-row sm:items-center justify-between gap-3 shrink-0">
                <div>
                  <span className="text-[10px] font-bold text-academy-accent uppercase tracking-wider">
                    {selectedTrack?.language_name} / {difficultyLabel(selectedLevel.difficulty_code)}
                  </span>
                  <h2 className="text-base sm:text-lg font-bold text-white mt-0.5">
                    {selectedLevel.title.split(" — ")[1] || selectedLevel.title}
                  </h2>
                </div>

                {selectedLevel.theory ? (
                  <Link
                    to={`/tracks/${selectedTrack?.track_id}/levels/${selectedLevel.id}`}
                    className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-semibold text-white bg-academy-success hover:bg-green-600 transition-all shadow-md shadow-academy-success/10 shrink-0"
                  >
                    <Play className="w-3.5 h-3.5 fill-white" />
                    {tx(t.lectures.solveTask, lang)}
                  </Link>
                ) : (
                  <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[10px] font-bold text-amber-300 border border-amber-500/30 bg-amber-500/10 uppercase tracking-wider shrink-0">
                    <Crown className="w-3 h-3 fill-amber-300" />
                    PRO
                  </span>
                )}
              </div>

              {/* Theory Text */}
              <div className="flex-1 overflow-y-auto p-4 sm:p-6 min-h-0">
                {selectedLevel.theory ? (
                  <Markdown content={selectedLevel.theory} />
                ) : user?.is_premium ? (
                  <div className="flex items-center justify-center h-full text-academy-muted text-sm italic">
                    {tx(t.lectures.proLocked, lang) /* We can reuse a generic text or just say no theory */}
                    Теория для этого урока в разработке.
                  </div>
                ) : (
                  /* Premium Lock State */
                  <div className="max-w-md mx-auto text-center py-8 sm:py-12 space-y-6">
                    <div className="w-14 h-14 rounded-2xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center mx-auto text-amber-400 shadow-[0_0_20px_-3px_rgba(251,191,36,0.3)]">
                      <Crown className="w-7 h-7 fill-amber-400 animate-pulse" />
                    </div>
                    <div className="space-y-2">
                      <h3 className="text-lg font-bold text-white">{tx(t.lectures.proLocked, lang)}</h3>
                      <p className="text-xs text-academy-muted leading-relaxed">
                        {tx(t.lectures.proLockedDesc, lang)}
                      </p>
                    </div>
                    <div className="p-4 rounded-xl border border-academy-border bg-academy-bg/40 text-left space-y-2">
                      <span className="text-[10px] font-bold text-white uppercase tracking-wider block">
                        {tx(t.lectures.proGet, lang)}
                      </span>
                      <ul className="text-xs space-y-1.5 text-slate-300">
                        {[t.lectures.proF1, t.lectures.proF2, t.lectures.proF3].map((f, i) => (
                          <li key={i} className="flex items-center gap-2">
                            <span className="w-1 h-1 rounded-full bg-amber-400 shrink-0" />
                            {tx(f, lang)}
                          </li>
                        ))}
                      </ul>
                    </div>
                    <Link
                      to="/billing"
                      className="inline-flex items-center justify-center gap-1.5 px-6 py-2.5 rounded-xl bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-500 hover:to-amber-600 text-academy-bg text-sm font-semibold transition-all hover:scale-[1.01]"
                    >
                      {tx(t.lectures.activatePro, lang)}
                      <ArrowRight className="w-4 h-4" />
                    </Link>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center text-center p-8 h-full space-y-3">
              <Library className="w-12 h-12 text-academy-muted animate-pulse" />
              <h3 className="font-bold text-base text-slate-200">{tx(t.lectures.selectLecture, lang)}</h3>
              <p className="text-xs text-academy-muted max-w-xs">
                {tx(t.lectures.selectLectureDesc, lang)}
              </p>
            </div>
          )}
        </main>
      </div>

      {selectedTrack && (
        <AddLectureModal
          trackId={selectedTrack.track_id}
          isOpen={isLectureOpen}
          onClose={() => setIsLectureOpen(false)}
          onSuccess={() => { setIsLectureOpen(false); reload(); }}
        />
      )}
    </div>
  );
}

/* Custom Lightweight Markdown Parser */
function Markdown({ content }: { content: string }) {
  const parts = content.split(/(```[\s\S]*?```)/g);

  return (
    <div className="space-y-4 text-slate-300 leading-relaxed text-sm max-w-none">
      {parts.map((part, index) => {
        if (part.startsWith("```")) {
          const lines = part.split("\n");
          const lang = lines[0].replace("```", "").trim();
          const code = lines.slice(1, -1).join("\n");
          return (
            <div key={index} className="relative group my-4">
              <div className="absolute right-3 top-3 text-[10px] text-academy-muted font-bold uppercase select-none">
                {lang}
              </div>
              <pre className="p-4 rounded-xl border border-academy-border bg-academy-bg/85 overflow-x-auto font-mono text-xs text-emerald-400 leading-normal">
                <code>{code}</code>
              </pre>
            </div>
          );
        }

        const lines = part.split("\n");
        return (
          <div key={index} className="space-y-3">
            {lines.map((line, lIndex) => {
              const cleanLine = line.trim();
              if (!cleanLine) return null;

              if (cleanLine.startsWith("###")) {
                return (
                  <h4 key={lIndex} className="text-sm font-bold text-white mt-5 mb-2 flex items-center gap-1.5">
                    <BookOpen className="w-4 h-4 text-academy-accent shrink-0" />
                    {cleanLine.replace("###", "").trim()}
                  </h4>
                );
              }
              if (cleanLine.startsWith("##")) {
                return (
                  <h3 key={lIndex} className="text-base font-bold text-white mt-6 mb-3 border-b border-academy-border/30 pb-1.5">
                    {cleanLine.replace("##", "").trim()}
                  </h3>
                );
              }
              if (cleanLine.startsWith("#")) {
                return (
                  <h2 key={lIndex} className="text-lg font-bold text-white mt-8 mb-4 border-b border-academy-border/30 pb-2">
                    {cleanLine.replace("#", "").trim()}
                  </h2>
                );
              }

              if (cleanLine.startsWith("-") || cleanLine.startsWith("*")) {
                const listText = cleanLine.substring(1).trim();
                return (
                  <ul key={lIndex} className="list-disc pl-5 my-1.5 space-y-1">
                    <li>{parseInline(listText)}</li>
                  </ul>
                );
              }

              const numMatch = cleanLine.match(/^(\d+)\.\s(.*)/);
              if (numMatch) {
                const num = numMatch[1];
                const listText = numMatch[2];
                return (
                  <ol key={lIndex} className="list-decimal pl-5 my-1.5 space-y-1">
                    <li value={parseInt(num, 10)}>{parseInline(listText)}</li>
                  </ol>
                );
              }

              return <p key={lIndex} className="leading-relaxed">{parseInline(cleanLine)}</p>;
            })}
          </div>
        );
      })}
    </div>
  );
}

function parseInline(text: string) {
  const boldParts = text.split(/(\*\*.*?\*\*)/g);
  return boldParts.map((bPart, idx) => {
    if (bPart.startsWith("**") && bPart.endsWith("**")) {
      return (
        <strong key={idx} className="text-white font-bold">
          {bPart.slice(2, -2)}
        </strong>
      );
    }
    const codeParts = bPart.split(/(`.*?`)/g);
    return codeParts.map((cPart, cIdx) => {
      if (cPart.startsWith("`") && cPart.endsWith("`")) {
        return (
          <code
            key={cIdx}
            className="px-1.5 py-0.5 rounded bg-academy-bg border border-academy-border font-mono text-xs text-academy-accent"
          >
            {cPart.slice(1, -1)}
          </code>
        );
      }
      return cPart;
    });
  });
}
