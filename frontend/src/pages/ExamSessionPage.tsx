import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { ArrowLeft, CheckCircle, Loader2, Play } from "lucide-react";
import { api } from "../api/client";
import type { RunCodeResult, StartExamResponse } from "../api/types";
import { CodeEditor } from "../components/CodeEditor";
import { OutputPanel } from "../components/OutputPanel";
import { useI18n, tx } from "../i18n/I18nContext";

export function ExamSessionPage() {
  const { examId } = useParams<{ examId: string }>();
  const { lang, t } = useI18n();
  const id = Number(examId);
  const [session, setSession] = useState<StartExamResponse | null>(null);
  const [activeQ, setActiveQ] = useState(0);
  const [code, setCode] = useState("");
  const [output, setOutput] = useState("");
  const [passed, setPassed] = useState<boolean | null>(null);
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);
  const [finished, setFinished] = useState<{ score: number; passed: boolean } | null>(null);

  useEffect(() => {
    if (!id) return;
    api
      .post<StartExamResponse>(`/exams/${id}/start`)
      .then((s) => {
        setSession(s);
        if (s.questions[0]) setCode(s.questions[0].starter_code);
      })
      .finally(() => setLoading(false));
  }, [id]);

  const question = session?.questions[activeQ];

  async function handleSubmit() {
    if (!session || !question) return;
    setRunning(true);
    try {
      const result = await api.post<RunCodeResult>(
        `/exams/attempt/${session.attempt_id}/submit`,
        { question_id: question.id, code },
      );
      setOutput(
        result.passed
          ? tx(t.examSession.answerAccepted, lang)
          : [result.stderr, JSON.stringify(result.details, null, 2)].filter(Boolean).join("\n"),
      );
      setPassed(result.passed);
    } catch (e) {
      setOutput(e instanceof Error ? e.message : tx(t.examSession.submitError, lang));
      setPassed(false);
    } finally {
      setRunning(false);
    }
  }

  async function handleFinish() {
    if (!session) return;
    const res = await api.post<{ score: number; passed: boolean }>(
      `/exams/attempt/${session.attempt_id}/finish`,
    );
    setFinished(res);
  }

  function goToQuestion(index: number) {
    const q = session?.questions[index];
    if (!q) return;
    setActiveQ(index);
    setCode(q.starter_code);
    setOutput("");
    setPassed(null);
  }

  if (loading) {
    return (
      <div className="flex justify-center py-20">
        <Loader2 className="w-10 h-10 animate-spin text-academy-accent" />
      </div>
    );
  }

  if (!session || !question) {
    return (
      <div className="text-center py-12">
        <p className="text-red-400">{tx(t.examSession.startFailed, lang)}</p>
        <Link to="/exams" className="text-academy-accent mt-4 inline-block">
          {tx(t.examSession.back, lang)}
        </Link>
      </div>
    );
  }

  if (finished) {
    return (
      <div className="max-w-md mx-auto text-center py-16 px-4">
        <CheckCircle
          className={`w-16 h-16 mx-auto mb-4 ${finished.passed ? "text-academy-success" : "text-academy-warn"}`}
        />
        <h1 className="text-2xl font-bold mb-2">
          {finished.passed ? tx(t.examSession.passed, lang) : tx(t.examSession.failed, lang)}
        </h1>
        <p className="text-academy-muted mb-6">
          {tx(t.examSession.score, lang)} {finished.score}%
        </p>
        <Link to="/exams" className="text-academy-accent hover:underline">
          {tx(t.examSession.backToExams, lang)}
        </Link>
      </div>
    );
  }

  return (
    <div className="flex flex-col" style={{ minHeight: "calc(100vh - 5.5rem)" }}>
      <div className="flex items-center justify-between mb-4 gap-2 flex-wrap">
        <Link to="/exams" className="inline-flex items-center gap-1 text-sm text-academy-muted hover:text-white">
          <ArrowLeft className="w-4 h-4" />
          <span className="hidden sm:inline">{tx(t.exams.title, lang)}</span>
        </Link>
        <span className="text-sm text-academy-muted">
          {tx(t.examSession.question, lang)} {activeQ + 1} / {session.questions.length}
        </span>
        <button
          type="button"
          onClick={handleFinish}
          className="text-sm px-3 py-1.5 rounded-lg border border-academy-border hover:bg-academy-panel"
        >
          {tx(t.examSession.finish, lang)}
        </button>
      </div>

      <div className="flex gap-2 mb-4 overflow-x-auto pb-1">
        {session.questions.map((q, i) => (
          <button
            key={q.id}
            type="button"
            onClick={() => goToQuestion(i)}
            className={`shrink-0 w-9 h-9 rounded-lg text-sm font-medium ${
              i === activeQ ? "bg-academy-accent" : "bg-academy-panel border border-academy-border"
            }`}
          >
            {q.order_num}
          </button>
        ))}
      </div>

      <div className="grid lg:grid-cols-2 gap-4 flex-1 min-h-0">
        <div className="rounded-xl border border-academy-border bg-academy-panel p-4 overflow-y-auto max-h-64 lg:max-h-none">
          <p className="text-sm whitespace-pre-wrap">{question.task_text}</p>
        </div>
        <div className="flex flex-col gap-4 min-h-0">
          <div className="flex-1 min-h-[200px] sm:min-h-[250px]">
            <CodeEditor value={code} onChange={setCode} />
          </div>
          <div className="h-32">
            <OutputPanel output={output} passed={passed} />
          </div>
          <button
            type="button"
            onClick={handleSubmit}
            disabled={running}
            className="flex items-center justify-center gap-2 py-2.5 rounded-lg bg-academy-accent font-medium"
          >
            {running ? <Loader2 className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
            {tx(t.examSession.submit, lang)}
          </button>
        </div>
      </div>
    </div>
  );
}
