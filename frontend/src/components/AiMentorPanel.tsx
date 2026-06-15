import { useState } from "react";
import { Bot, Loader2, Send, Crown, Lock, Sparkles, MessageSquare } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { Link } from "react-router-dom";

interface Message {
  role: "mentor" | "review";
  text: string;
}

interface AiMentorPanelProps {
  onAsk: (errorMessage: string) => Promise<string>;
  disabled?: boolean;
  isCompleted?: boolean;
  onAskReview?: () => Promise<string>;
}

export function AiMentorPanel({ onAsk, disabled, isCompleted, onAskReview }: AiMentorPanelProps) {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState<"hint" | "review">("hint");
  const [messages, setMessages] = useState<Message[]>([]);
  const [reviewText, setReviewText] = useState<string | null>(null);
  
  const [loading, setLoading] = useState(false);
  const [errorContext, setErrorContext] = useState("");

  async function handleAsk() {
    setLoading(true);
    try {
      const hint = await onAsk(errorContext);
      setMessages((prev) => [...prev, { role: "mentor", text: hint }]);
    } catch (e) {
      const msg = e instanceof Error ? e.message : "Не удалось получить подсказку";
      setMessages((prev) => [...prev, { role: "mentor", text: msg }]);
    } finally {
      setLoading(false);
    }
  }

  async function handleGetReview() {
    if (!onAskReview) return;
    setLoading(true);
    try {
      const review = await onAskReview();
      setReviewText(review);
    } catch (e) {
      const msg = e instanceof Error ? e.message : "Не удалось получить код-ревью";
      setReviewText(msg);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col h-full min-h-[350px] rounded-xl border border-academy-border bg-academy-panel overflow-hidden">
      {/* Header and Tabs */}
      <div className="border-b border-academy-border bg-academy-bg/40">
        <div className="flex items-center gap-2 px-4 py-2.5 border-b border-academy-border/60">
          <Bot className="w-5 h-5 text-academy-accent" />
          <span className="font-semibold text-sm">ИИ-Помощник</span>
        </div>
        <div className="flex text-xs font-medium">
          <button
            type="button"
            onClick={() => setActiveTab("hint")}
            className={`flex-1 py-2 text-center border-b-2 transition-all ${
              activeTab === "hint"
                ? "border-academy-accent text-white bg-academy-panel"
                : "border-transparent text-academy-muted hover:text-white"
            }`}
          >
            Подсказки
          </button>
          <button
            type="button"
            onClick={() => setActiveTab("review")}
            className={`flex-1 py-2 text-center border-b-2 transition-all flex items-center justify-center gap-1 ${
              activeTab === "review"
                ? "border-academy-accent text-white bg-academy-panel"
                : "border-transparent text-academy-muted hover:text-white"
            }`}
          >
            {!user?.is_premium && <Crown className="w-3.5 h-3.5 text-amber-400 fill-amber-400 shrink-0" />}
            Код-ревью
            {isCompleted && <span className="w-1.5 h-1.5 rounded-full bg-academy-success shrink-0" />}
          </button>
        </div>
      </div>

      {/* Tab Contents */}
      <div className="flex-1 overflow-y-auto p-4 min-h-0">
        {activeTab === "hint" ? (
          <div className="space-y-3 h-full flex flex-col justify-between">
            <div className="space-y-3 overflow-y-auto flex-1 max-h-[260px] pr-1">
              {messages.length === 0 && (
                <p className="text-xs text-academy-muted leading-relaxed">
                  Не получается решить задачу? Нажмите кнопку ниже, чтобы ИИ-наставник дал подсказку наводящими вопросами по методу Сократа. Наставник никогда не пишет готовый код за вас.
                </p>
              )}
              {messages.map((m, i) => (
                <div key={i} className="text-xs bg-academy-bg rounded-xl p-3 border border-academy-border leading-relaxed whitespace-pre-wrap">
                  {m.text}
                </div>
              ))}
            </div>
          </div>
        ) : (
          /* Review Tab */
          <div className="h-full space-y-4">
            {!isCompleted ? (
              <div className="flex flex-col items-center justify-center text-center py-10 space-y-2">
                <Lock className="w-8 h-8 text-academy-muted" />
                <h4 className="font-semibold text-sm text-slate-200">Функция заблокирована</h4>
                <p className="text-xs text-academy-muted max-w-[200px]">
                  Пройдите этот уровень успешно, чтобы получить доступ к подробному ИИ-код-ревью решения.
                </p>
              </div>
            ) : !user?.is_premium ? (
              /* Completed but Free User */
              <div className="rounded-xl border border-amber-500/20 bg-amber-500/5 p-4 space-y-3 text-center">
                <div className="w-8 h-8 rounded-lg bg-amber-500/10 flex items-center justify-center text-amber-400 mx-auto">
                  <Crown className="w-4 h-4 fill-amber-400" />
                </div>
                <h4 className="font-semibold text-sm text-amber-300">Требуется подписка PRO</h4>
                <p className="text-[11px] text-academy-muted leading-relaxed">
                  ИИ-обзор и оценка оптимальности решения по времени, памяти и стилю написания кода доступны только с Premium PRO.
                </p>
                <Link
                  to="/billing"
                  className="block w-full py-2 text-center text-xs font-semibold rounded-lg text-academy-bg bg-amber-400 hover:bg-amber-500 transition-colors"
                >
                  Активировать PRO
                </Link>
              </div>
            ) : (
              /* Premium & Completed */
              <div className="space-y-3">
                {reviewText ? (
                  <div className="text-xs bg-academy-bg rounded-xl p-4 border border-academy-border leading-relaxed whitespace-pre-wrap">
                    <div className="flex items-center gap-1 text-[10px] font-bold text-amber-400 uppercase tracking-wider mb-2">
                      <Sparkles className="w-3.5 h-3.5" />
                      ИИ Анализ решения
                    </div>
                    {reviewText}
                  </div>
                ) : (
                  <div className="text-center py-8 space-y-3">
                    <MessageSquare className="w-8 h-8 text-academy-accent mx-auto" />
                    <p className="text-xs text-academy-muted max-w-[220px] mx-auto">
                      Вы успешно завершили уровень! Нажмите кнопку ниже, чтобы получить оценку вашего кода.
                    </p>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Bottom Actions */}
      <div className="p-3 border-t border-academy-border bg-academy-bg/20 space-y-2 shrink-0">
        {activeTab === "hint" ? (
          <>
            <input
              type="text"
              placeholder="Текст ошибки (необязательно)"
              value={errorContext}
              onChange={(e) => setErrorContext(e.target.value)}
              className="w-full px-3 py-1.5 text-xs rounded-lg bg-academy-bg border border-academy-border focus:outline-none focus:border-academy-accent"
            />
            <button
              type="button"
              disabled={disabled || loading}
              onClick={handleAsk}
              className="w-full flex items-center justify-center gap-2 py-2 rounded-lg bg-academy-accent hover:bg-blue-600 disabled:opacity-50 text-xs font-medium transition-colors"
            >
              {loading ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Send className="w-3.5 h-3.5" />}
              Спросить наставника
            </button>
          </>
        ) : (
          isCompleted && user?.is_premium && (
            <button
              type="button"
              disabled={loading}
              onClick={handleGetReview}
              className="w-full flex items-center justify-center gap-2 py-2 rounded-lg bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-600 hover:to-amber-700 text-white disabled:opacity-50 text-xs font-medium transition-all"
            >
              {loading ? (
                <Loader2 className="w-3.5 h-3.5 animate-spin" />
              ) : (
                <Crown className="w-3.5 h-3.5 fill-white" />
              )}
              {reviewText ? "Повторить ревью кода" : "Сделать код-ревью (PRO)"}
            </button>
          )
        )}
      </div>
    </div>
  );
}
