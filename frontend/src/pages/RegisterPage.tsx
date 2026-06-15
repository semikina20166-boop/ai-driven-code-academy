import { FormEvent, useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import { GraduationCap, Loader2 } from "lucide-react";
import { ApiError } from "../api/client";
import { useAuth } from "../context/AuthContext";
import { useI18n, tx } from "../i18n/I18nContext";
import { LangSwitcher } from "../components/LangSwitcher";

export function RegisterPage() {
  const { register, user } = useAuth();
  const { lang, t } = useI18n();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  if (user) return <Navigate to="/" replace />;

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await register(email, password, displayName || undefined);
      navigate("/");
    } catch (err) {
      setError(err instanceof ApiError ? err.message : tx(t.register.error, lang));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4 bg-gradient-to-br from-academy-bg via-[#121a28] to-academy-bg">
      {/* Lang switcher */}
      <div className="absolute top-4 right-4">
        <LangSwitcher />
      </div>

      <div className="w-full max-w-md rounded-2xl border border-academy-border bg-academy-panel p-6 sm:p-8 shadow-xl">
        <div className="flex items-center justify-center gap-2 mb-6">
          <GraduationCap className="w-10 h-10 text-academy-accent" />
          <h1 className="text-2xl font-bold">{tx(t.register.title, lang)}</h1>
        </div>
        <form onSubmit={handleSubmit} className="space-y-4">
          <label className="block text-sm">
            <span className="text-academy-muted">{tx(t.register.name, lang)}</span>
            <input
              type="text"
              value={displayName}
              onChange={(e) => setDisplayName(e.target.value)}
              className="mt-1 w-full px-3 py-2 rounded-lg bg-academy-bg border border-academy-border focus:border-academy-accent outline-none text-base"
            />
          </label>
          <label className="block text-sm">
            <span className="text-academy-muted">{tx(t.register.email, lang)}</span>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="mt-1 w-full px-3 py-2 rounded-lg bg-academy-bg border border-academy-border focus:border-academy-accent outline-none text-base"
            />
          </label>
          <label className="block text-sm">
            <span className="text-academy-muted">{tx(t.register.password, lang)}</span>
            <input
              type="password"
              required
              minLength={6}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-1 w-full px-3 py-2 rounded-lg bg-academy-bg border border-academy-border focus:border-academy-accent outline-none text-base"
            />
          </label>
          {error && <p className="text-sm text-red-400">{error}</p>}
          <button
            type="submit"
            disabled={loading}
            className="w-full py-2.5 rounded-lg bg-academy-accent hover:bg-blue-600 font-medium flex items-center justify-center gap-2 transition-colors"
          >
            {loading && <Loader2 className="w-4 h-4 animate-spin" />}
            {tx(t.register.submit, lang)}
          </button>
        </form>
        <p className="mt-4 text-center text-sm text-academy-muted">
          {tx(t.register.hasAccount, lang)}{" "}
          <Link to="/login" className="text-academy-accent hover:underline">
            {tx(t.register.signIn, lang)}
          </Link>
        </p>
      </div>
    </div>
  );
}
