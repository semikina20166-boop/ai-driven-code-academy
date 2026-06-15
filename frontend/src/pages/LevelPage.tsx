import { useCallback, useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { ArrowLeft, ArrowRight, Loader2, Play, Crown, ChevronDown, ChevronUp } from "lucide-react";
import { api, ApiError } from "../api/client";
import type { AiHintResponse, LevelDetail, RunCodeResult } from "../api/types";
import { AiMentorPanel } from "../components/AiMentorPanel";
import { CodeEditor } from "../components/CodeEditor";
import { OutputPanel } from "../components/OutputPanel";
import { useI18n, tx } from "../i18n/I18nContext";

export function LevelPage() {
  const { trackId, levelId } = useParams<{ trackId: string; levelId: string }>();
  const navigate = useNavigate();
  const { lang, t } = useI18n();

  const [level, setLevel] = useState<LevelDetail | null>(null);
  const [code, setCode] = useState("");
  const [output, setOutput] = useState("");
  const [passed, setPassed] = useState<boolean | null>(null);
  const [lastError, setLastError] = useState("");
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);
  const [errorStatus, setErrorStatus] = useState<number | null>(null);

  // Mobile: which panel is expanded
  const [mobilePanel, setMobilePanel] = useState<"task" | "editor" | "ai">("editor");

  function formatRunOutput(result: RunCodeResult): string {
    const parts: string[] = [];
    if (result.passed) parts.push(tx(t.level.allPassed, lang) + "\n");
    if (result.stderr) parts.push(result.stderr);
    if (result.stdout) parts.push(result.stdout);
    if (result.details?.length) parts.push(JSON.stringify(result.details, null, 2));
    return parts.join("\n") || tx(t.level.noOutput, lang);
  }

  useEffect(() => {
    const lid = Number(levelId);
    if (!lid) return;
    setLoading(true);
    setErrorStatus(null);
    api.get<LevelDetail>(`/levels/${lid}`)
      .then((l) => { setLevel(l); setCode(l.starter_code); })
      .catch((err) => {
        setLevel(null);
        if (err instanceof ApiError) setErrorStatus(err.status);
        else if (err && typeof err === "object" && "status" in err) setErrorStatus((err as { status: number }).status);
        else setErrorStatus(500);
      })
      .finally(() => setLoading(false));
  }, [levelId]);

  const handleRun = useCallback(async () => {
    if (!level) return;
    setRunning(true);
    setPassed(null);
    setMobilePanel("editor");
    try {
      const result = await api.post<RunCodeResult>("/levels/run", { level_id: level.id, code });
      setOutput(formatRunOutput(result));
      setPassed(result.passed);
      setLastError(result.stderr || JSON.stringify(result.details));
      if (result.passed) setLevel((prev) => (prev ? { ...prev, status: "completed" } : prev));
    } catch (e) {
      const msg = e instanceof Error ? e.message : tx(t.level.runError, lang);
      setOutput(msg);
      setPassed(false);
      setLastError(msg);
    } finally {
      setRunning(false);
    }
  }, [level, code, lang]);

  const handleHint = useCallback(async (errorMessage: string) => {
    if (!level) return "";
    const res = await api.post<AiHintResponse>("/ai/hint", {
      level_id: level.id, code, error_message: errorMessage || lastError,
    });
    return res.hint;
  }, [level, code, lastError]);

  const handleCodeReview = useCallback(async () => {
    if (!level) return "";
    const res = await api.post<{ review: string }>("/ai/review", { level_id: level.id, code });
    return res.review;
  }, [level, code]);

  if (loading) {
    return (
      <div className="flex justify-center py-20">
        <Loader2 className="w-10 h-10 animate-spin text-academy-accent" />
      </div>
    );
  }

  if (errorStatus === 402) {
    return (
      <div className="max-w-xl mx-auto py-10 sm:py-16 text-center space-y-6 px-4">
        <div className="w-16 h-16 rounded-2xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center mx-auto text-amber-400">
          <Crown className="w-8 h-8 fill-amber-400 animate-pulse" />
        </div>
        <div className="space-y-2">
          <h1 className="text-xl sm:text-2xl font-bold text-white">{tx(t.level.proTitle, lang)}</h1>
          <p className="text-sm text-academy-muted max-w-md mx-auto">{tx(t.level.proDesc, lang)}</p>
        </div>
        <div className="p-4 sm:p-5 rounded-2xl border border-academy-border bg-academy-panel max-w-sm mx-auto text-left space-y-3">
          <h3 className="text-sm font-semibold text-white">{tx(t.level.proFeatures, lang)}</h3>
          <ul className="text-xs space-y-2 text-slate-300">
            {[t.level.proF1, t.level.proF2, t.level.proF3, t.level.proF4].map((f, i) => (
              <li key={i} className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-amber-400 shrink-0" />
                {tx(f, lang)}
              </li>
            ))}
          </ul>
        </div>
        <div className="flex flex-col sm:flex-row justify-center gap-3">
          <Link to={`/tracks/${trackId}`} className="px-5 py-2.5 rounded-xl border border-academy-border hover:bg-academy-panel text-sm font-medium transition-colors">
            {tx(t.level.backToMap, lang)}
          </Link>
          <Link to="/billing" className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-500 hover:to-amber-600 text-academy-bg font-semibold text-sm shadow-lg transition-all">
            {tx(t.level.activatePro, lang)}
          </Link>
        </div>
      </div>
    );
  }

  if (!level) {
    return (
      <div className="text-center py-12 px-4">
        <p className="text-red-400 mb-4">{tx(t.level.levelNotFound, lang)}</p>
        <Link to={`/tracks/${trackId}`} className="text-academy-accent hover:underline">
          {tx(t.level.backToMap, lang)}
        </Link>
      </div>
    );
  }

  // ── Mobile accordion panel helper ──
  const PanelHeader = ({
    id, label,
  }: { id: "task" | "editor" | "ai"; label: string }) => (
    <button
      type="button"
      onClick={() => setMobilePanel(mobilePanel === id ? "editor" : id)}
      className="lg:hidden w-full flex items-center justify-between px-3 py-2 rounded-lg border border-academy-border bg-academy-panel text-sm font-medium mb-1"
    >
      {label}
      {mobilePanel === id
        ? <ChevronUp className="w-4 h-4 text-academy-muted" />
        : <ChevronDown className="w-4 h-4 text-academy-muted" />}
    </button>
  );

  return (
    <div className="flex flex-col">
      {/* ── Top bar ── */}
      <div className="flex items-center justify-between gap-2 mb-3 shrink-0">
        <Link to={`/tracks/${trackId}`} className="inline-flex items-center gap-1 text-sm text-academy-muted hover:text-white shrink-0">
          <ArrowLeft className="w-4 h-4" />
          <span className="hidden sm:inline">{tx(t.level.map, lang)}</span>
        </Link>
        <div className="text-center flex-1 min-w-0">
          <h1 className="font-semibold truncate text-sm sm:text-base">{level.title}</h1>
          <p className="text-xs text-academy-muted">{level.difficulty_name} · {tx(t.level.condition, lang)} {level.order_num}</p>
        </div>
        <button
          type="button"
          onClick={handleRun}
          disabled={running}
          className="flex items-center gap-1.5 px-3 sm:px-4 py-2 rounded-lg bg-academy-success hover:bg-green-600 font-medium text-sm shrink-0 transition-colors"
        >
          {running ? <Loader2 className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
          <span className="hidden sm:inline">{tx(t.level.run, lang)}</span>
        </button>
      </div>

      {/* ── Desktop layout (3 columns) ── */}
      <div className="hidden lg:grid lg:grid-cols-12 gap-4" style={{ height: "calc(100vh - 8rem)" }}>
        {/* Task */}
        <aside className="lg:col-span-3 overflow-y-auto rounded-xl border border-academy-border bg-academy-panel p-4">
          <h2 className="text-sm font-medium text-academy-muted mb-2">{tx(t.level.condition, lang)}</h2>
          <p className="text-sm leading-relaxed whitespace-pre-wrap">{level.task_text}</p>
          {level.allowed_concepts.length > 0 && (
            <div className="mt-4">
              <h3 className="text-xs text-academy-muted mb-2">{tx(t.level.allowedTerms, lang)}</h3>
              <div className="flex flex-wrap gap-1">
                {level.allowed_concepts.map((c) => (
                  <span key={c} className="text-xs px-2 py-0.5 rounded bg-academy-bg border border-academy-border">{c}</span>
                ))}
              </div>
            </div>
          )}
          {passed && (
            <button type="button" onClick={() => navigate(`/tracks/${trackId}`)}
              className="mt-6 w-full flex items-center justify-center gap-2 py-2 rounded-lg bg-academy-accent text-sm font-medium">
              {tx(t.level.nextLevel, lang)} <ArrowRight className="w-4 h-4" />
            </button>
          )}
        </aside>

        {/* Editor + Output */}
        <div className="lg:col-span-5 flex flex-col min-h-0 gap-4">
          <div className="flex-1 min-h-0">
            <CodeEditor value={code} onChange={setCode} language="python" />
          </div>
          <div className="h-40 shrink-0">
            <OutputPanel output={output} passed={passed} />
          </div>
        </div>

        {/* AI Mentor */}
        <div className="lg:col-span-4">
          <AiMentorPanel onAsk={handleHint} disabled={running} isCompleted={level.status === "completed"} onAskReview={handleCodeReview} />
        </div>
      </div>

      {/* ── Mobile layout (accordion) ── */}
      <div className="lg:hidden space-y-2">
        {/* Task accordion */}
        <PanelHeader id="task" label={tx(t.level.condition, lang)} />
        {mobilePanel === "task" && (
          <div className="rounded-xl border border-academy-border bg-academy-panel p-4">
            <p className="text-sm leading-relaxed whitespace-pre-wrap">{level.task_text}</p>
            {level.allowed_concepts.length > 0 && (
              <div className="mt-3">
                <h3 className="text-xs text-academy-muted mb-2">{tx(t.level.allowedTerms, lang)}</h3>
                <div className="flex flex-wrap gap-1">
                  {level.allowed_concepts.map((c) => (
                    <span key={c} className="text-xs px-2 py-0.5 rounded bg-academy-bg border border-academy-border">{c}</span>
                  ))}
                </div>
              </div>
            )}
            {passed && (
              <button type="button" onClick={() => navigate(`/tracks/${trackId}`)}
                className="mt-4 w-full flex items-center justify-center gap-2 py-2 rounded-lg bg-academy-accent text-sm font-medium">
                {tx(t.level.nextLevel, lang)} <ArrowRight className="w-4 h-4" />
              </button>
            )}
          </div>
        )}

        {/* Editor */}
        <PanelHeader id="editor" label={tx(t.level.editor, lang)} />
        {mobilePanel === "editor" && (
          <div className="space-y-2">
            <div className="h-64 sm:h-80 rounded-xl overflow-hidden border border-academy-border">
              <CodeEditor value={code} onChange={setCode} language="python" />
            </div>
            <div className="h-32">
              <OutputPanel output={output} passed={passed} />
            </div>
          </div>
        )}

        {/* AI Mentor */}
        <PanelHeader id="ai" label={tx(t.ai.title, lang)} />
        {mobilePanel === "ai" && (
          <div className="h-80">
            <AiMentorPanel onAsk={handleHint} disabled={running} isCompleted={level.status === "completed"} onAskReview={handleCodeReview} />
          </div>
        )}
      </div>
    </div>
  );
}
