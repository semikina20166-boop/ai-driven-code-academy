import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Crown, Check, AlertTriangle, CreditCard, Loader2, Sparkles, ArrowLeft, ShieldCheck } from "lucide-react";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";
import { useI18n, tx } from "../i18n/I18nContext";

export function BillingPage() {
  const { user, refreshUser } = useAuth();
  const navigate = useNavigate();
  const { lang, t } = useI18n();
  const [loading, setLoading] = useState(false);
  const [showPayModal, setShowPayModal] = useState(false);
  const [paymentStep, setPaymentStep] = useState<"form" | "processing" | "success">("form");
  const [showCancelModal, setShowCancelModal] = useState(false);

  // Form state
  const [cardNumber, setCardNumber] = useState("4400 1234 5678 9010");
  const [cardExpiry, setCardExpiry] = useState("12/28");
  const [cardCvc, setCardCvc] = useState("999");

  async function handleUpgrade() {
    setPaymentStep("processing");
    await new Promise((resolve) => setTimeout(resolve, 2000));
    try {
      await api.post("/auth/upgrade");
      await refreshUser();
      setPaymentStep("success");
    } catch (err) {
      alert(err instanceof Error ? err.message : tx(t.billing.upgradeFailed, lang));
      setPaymentStep("form");
      setShowPayModal(false);
    }
  }

  async function handleDowngrade() {
    setLoading(true);
    try {
      await api.post("/auth/downgrade");
      await refreshUser();
      setShowCancelModal(false);
    } catch (err) {
      alert(err instanceof Error ? err.message : tx(t.billing.downgradeError, lang));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-4xl mx-auto py-4 sm:py-6 px-2 sm:px-0">
      <button
        onClick={() => navigate(-1)}
        className="inline-flex items-center gap-1.5 text-sm text-academy-muted hover:text-white mb-6 transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        {tx(t.billing.back, lang)}
      </button>

      <div className="text-center mb-8 sm:mb-10">
        <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
          {tx(t.billing.title, lang)}
        </h1>
        <p className="mt-3 text-sm sm:text-lg text-academy-muted max-w-2xl mx-auto">
          {tx(t.billing.subtitle, lang)}
        </p>
      </div>

      <div className="grid sm:grid-cols-2 gap-6 sm:gap-8 items-stretch max-w-3xl mx-auto">
        {/* Free Plan */}
        <div className="rounded-2xl border border-academy-border bg-academy-panel/40 p-6 sm:p-8 flex flex-col justify-between relative overflow-hidden">
          <div>
            <h2 className="text-xl font-bold">{tx(t.billing.freeTitle, lang)}</h2>
            <p className="mt-2 text-sm text-academy-muted">{tx(t.billing.freeDesc, lang)}</p>
            <div className="mt-4 flex items-baseline">
              <span className="text-4xl font-extrabold text-white">0 ₽</span>
              <span className="ml-1 text-sm text-academy-muted">{tx(t.billing.forever, lang)}</span>
            </div>

            <ul className="mt-8 space-y-4">
              <li className="flex items-start gap-3 text-sm">
                <Check className="w-5 h-5 text-academy-success shrink-0 mt-0.5" />
                <span className="text-slate-300">{tx(t.billing.freeF1, lang)}</span>
              </li>
              <li className="flex items-start gap-3 text-sm">
                <Check className="w-5 h-5 text-academy-success shrink-0 mt-0.5" />
                <span className="text-slate-300">{tx(t.billing.freeF2, lang)}</span>
              </li>
              <li className="flex items-start gap-3 text-sm">
                <Check className="w-5 h-5 text-academy-success shrink-0 mt-0.5" />
                <span className="text-slate-300">{tx(t.billing.freeF3, lang)}</span>
              </li>
              <li className="flex items-start gap-3 text-sm opacity-50">
                <span className="w-5 h-5 text-red-400 font-bold shrink-0 text-center select-none">×</span>
                <span className="text-slate-400">{tx(t.billing.freeX1, lang)}</span>
              </li>
              <li className="flex items-start gap-3 text-sm opacity-50">
                <span className="w-5 h-5 text-red-400 font-bold shrink-0 text-center select-none">×</span>
                <span className="text-slate-400">{tx(t.billing.freeX2, lang)}</span>
              </li>
            </ul>
          </div>

          <div className="mt-8">
            {!user?.is_premium ? (
              <div className="w-full py-3 text-center text-sm font-medium rounded-xl border border-academy-border text-academy-muted bg-academy-bg/25">
                {tx(t.billing.currentPlan, lang)}
              </div>
            ) : (
              <button
                onClick={() => setShowCancelModal(true)}
                className="w-full py-3 text-center text-sm font-medium rounded-xl border border-red-500/20 hover:border-red-500/40 text-red-400 hover:bg-red-500/5 transition-all"
              >
                {tx(t.billing.returnToBasic, lang)}
              </button>
            )}
          </div>
        </div>

        {/* Premium PRO Plan */}
        <div className="rounded-2xl border border-amber-500/30 bg-gradient-to-b from-amber-500/10 via-academy-panel to-academy-panel p-6 sm:p-8 flex flex-col justify-between relative overflow-hidden shadow-[0_0_40px_-15px_rgba(251,191,36,0.3)] animate-pulse-glow">
          <div className="absolute top-4 right-4 flex items-center gap-1 px-2.5 py-1 rounded-full text-[10px] font-bold text-amber-300 border border-amber-500/30 bg-amber-500/10 uppercase tracking-wider">
            <Sparkles className="w-3 h-3 fill-amber-300" />
            {tx(t.billing.recommended, lang)}
          </div>

          <div>
            <div className="flex items-center gap-2">
              <Crown className="w-6 h-6 text-amber-400 fill-amber-400" />
              <h2 className="text-xl font-bold text-amber-400">Premium PRO access</h2>
            </div>
            <p className="mt-2 text-sm text-academy-muted">{tx(t.billing.proDesc, lang)}</p>
            <div className="mt-4 flex items-baseline">
              <span className="text-4xl font-extrabold text-white">499 ₽</span>
              <span className="ml-1 text-sm text-academy-muted">{tx(t.billing.perMonth, lang)}</span>
            </div>

            <ul className="mt-8 space-y-4">
              {[t.billing.proF1, t.billing.proF2, t.billing.proF3, t.billing.proF4, t.billing.proF5].map((f, i) => (
                <li key={i} className="flex items-start gap-3 text-sm">
                  <Check className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
                  <span className="text-slate-100 font-medium">{tx(f, lang)}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="mt-8">
            {user?.is_premium ? (
              <div className="w-full py-3 text-center text-sm font-semibold rounded-xl border border-amber-500/20 text-amber-300 bg-amber-500/10">
                {tx(t.billing.planActive, lang)}
              </div>
            ) : (
              <button
                onClick={() => {
                  setPaymentStep("form");
                  setShowPayModal(true);
                }}
                className="w-full py-3 text-center text-sm font-semibold rounded-xl text-academy-bg bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-500 hover:to-amber-600 shadow-lg shadow-amber-500/20 hover:shadow-xl hover:shadow-amber-500/30 active:scale-[0.98] transition-all"
              >
                {tx(t.billing.activate, lang)}
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Simulated Checkout Modal */}
      {showPayModal && (
        <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div className="w-full max-w-md bg-academy-panel border border-academy-border rounded-2xl p-6 shadow-2xl relative">
            {paymentStep === "form" && (
              <>
                <h3 className="text-lg font-bold flex items-center gap-2 mb-4">
                  <CreditCard className="w-5 h-5 text-academy-accent" />
                  {tx(t.billing.checkoutTitle, lang)}
                </h3>
                <p className="text-sm text-academy-muted mb-6">
                  {tx(t.billing.checkoutNote, lang)}
                </p>
                <div className="space-y-4 mb-6">
                  <div>
                    <label className="block text-xs font-semibold text-academy-muted uppercase tracking-wider mb-1">
                      {tx(t.billing.cardNumber, lang)}
                    </label>
                    <input
                      type="text"
                      value={cardNumber}
                      onChange={(e) => setCardNumber(e.target.value)}
                      className="w-full px-3 py-2 text-sm rounded-lg bg-academy-bg border border-academy-border focus:border-academy-accent outline-none"
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-xs font-semibold text-academy-muted uppercase tracking-wider mb-1">
                        {tx(t.billing.expiry, lang)}
                      </label>
                      <input
                        type="text"
                        value={cardExpiry}
                        onChange={(e) => setCardExpiry(e.target.value)}
                        className="w-full px-3 py-2 text-sm rounded-lg bg-academy-bg border border-academy-border focus:border-academy-accent outline-none"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-semibold text-academy-muted uppercase tracking-wider mb-1">
                        CVC/CVV
                      </label>
                      <input
                        type="password"
                        value={cardCvc}
                        onChange={(e) => setCardCvc(e.target.value)}
                        className="w-full px-3 py-2 text-sm rounded-lg bg-academy-bg border border-academy-border focus:border-academy-accent outline-none"
                      />
                    </div>
                  </div>
                </div>
                <div className="flex gap-3">
                  <button
                    onClick={() => setShowPayModal(false)}
                    className="flex-1 py-2 rounded-lg border border-academy-border hover:bg-academy-bg transition-colors text-sm font-medium"
                  >
                    {tx(t.billing.cancel, lang)}
                  </button>
                  <button
                    onClick={handleUpgrade}
                    className="flex-1 py-2 rounded-lg bg-academy-accent hover:bg-blue-600 text-sm font-medium transition-colors"
                  >
                    {tx(t.billing.pay, lang)}
                  </button>
                </div>
              </>
            )}

            {paymentStep === "processing" && (
              <div className="flex flex-col items-center justify-center py-10">
                <Loader2 className="w-12 h-12 animate-spin text-academy-accent mb-4" />
                <h3 className="font-bold text-lg">{tx(t.billing.processing, lang)}</h3>
                <p className="text-sm text-academy-muted mt-1">{tx(t.billing.pleaseWait, lang)}</p>
              </div>
            )}

            {paymentStep === "success" && (
              <div className="flex flex-col items-center justify-center text-center py-6">
                <div className="w-16 h-16 rounded-full bg-amber-500/10 border border-amber-500/30 flex items-center justify-center mb-4 text-amber-400">
                  <Crown className="w-8 h-8 fill-amber-400" />
                </div>
                <h3 className="text-xl font-bold text-amber-300">{tx(t.billing.successTitle, lang)}</h3>
                <p className="text-sm text-academy-muted mt-2 max-w-sm">
                  {tx(t.billing.successDesc, lang)}
                </p>
                <button
                  onClick={() => {
                    setShowPayModal(false);
                    navigate(-1);
                  }}
                  className="mt-6 px-6 py-2 rounded-lg bg-academy-accent hover:bg-blue-600 text-sm font-medium transition-colors"
                >
                  {tx(t.billing.startLearning, lang)}
                </button>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Cancel Subscription Confirmation Modal */}
      {showCancelModal && (
        <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div className="w-full max-w-md bg-academy-panel border border-academy-border rounded-2xl p-6 shadow-2xl relative">
            <h3 className="text-lg font-bold flex items-center gap-2 mb-3 text-red-400">
              <AlertTriangle className="w-5 h-5 shrink-0" />
              {tx(t.billing.cancelTitle, lang)}
            </h3>
            <p className="text-sm text-slate-300 leading-relaxed mb-6">
              {tx(t.billing.cancelDesc, lang)}
            </p>
            <div className="flex gap-3">
              <button
                disabled={loading}
                onClick={() => setShowCancelModal(false)}
                className="flex-1 py-2 rounded-lg border border-academy-border hover:bg-academy-bg transition-colors text-sm font-medium disabled:opacity-50"
              >
                {tx(t.billing.keepPro, lang)}
              </button>
              <button
                disabled={loading}
                onClick={handleDowngrade}
                className="flex-1 py-2 rounded-lg bg-red-600 hover:bg-red-700 text-white text-sm font-medium transition-colors disabled:opacity-50 flex items-center justify-center gap-1.5"
              >
                {loading && <Loader2 className="w-4 h-4 animate-spin" />}
                {tx(t.billing.confirmCancel, lang)}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
