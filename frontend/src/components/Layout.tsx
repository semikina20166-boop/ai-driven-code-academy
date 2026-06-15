import { useState } from "react";
import { Link, NavLink, Outlet } from "react-router-dom";
import {
  BookOpen, GraduationCap, LayoutDashboard, LogOut,
  Crown, User as UserIcon, Library, Menu, X,
} from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { useI18n, tx } from "../i18n/I18nContext";
import { LangSwitcher } from "./LangSwitcher";

export function Layout() {
  const { user, logout } = useAuth();
  const { lang, t } = useI18n();
  const [mobileOpen, setMobileOpen] = useState(false);

  const navClass = ({ isActive }: { isActive: boolean }) =>
    `flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
      isActive
        ? "bg-academy-accent/10 text-academy-accent border border-academy-accent/20"
        : "text-academy-muted hover:bg-academy-panel hover:text-white"
    }`;

  const navLinks = [
    { to: "/",         end: true,  icon: <LayoutDashboard className="w-4 h-4" />, label: tx(t.nav.tracks,   lang) },
    { to: "/lectures", end: false, icon: <Library className="w-4 h-4" />,         label: tx(t.nav.lectures, lang) },
    { to: "/exams",    end: false, icon: <BookOpen className="w-4 h-4" />,         label: tx(t.nav.exams,    lang) },
    { to: "/profile",  end: false, icon: <UserIcon className="w-4 h-4" />,         label: tx(t.nav.profile,  lang) },
  ];

  return (
    <div className="min-h-screen flex flex-col bg-academy-bg text-slate-100 font-sans">
      {/* ── Header ─────────────────────────────────────────── */}
      <header className="border-b border-academy-border bg-academy-bg/85 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between gap-2">

          {/* Logo */}
          <Link to="/" className="flex items-center gap-2 font-bold text-xl tracking-tight group shrink-0">
            <GraduationCap className="w-8 h-8 text-academy-accent group-hover:scale-110 transition-transform" />
            <span className="bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent hidden sm:inline">
              AI Academy
            </span>
          </Link>

          {/* Desktop nav */}
          <nav className="hidden md:flex items-center gap-1.5 flex-1 justify-center">
            {navLinks.map((l) => (
              <NavLink key={l.to} to={l.to} end={l.end} className={navClass}>
                {l.icon}
                {l.label}
              </NavLink>
            ))}
          </nav>

          {/* Right side */}
          <div className="flex items-center gap-2">
            {/* Lang switcher — hidden on tiny screens, compact on mobile */}
            <div className="hidden sm:flex">
              <LangSwitcher />
            </div>
            <div className="flex sm:hidden">
              <LangSwitcher compact />
            </div>

            {user && (
              <div className="hidden sm:flex items-center gap-2">
                {user.is_premium ? (
                  <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold text-amber-300 border border-amber-500/30 bg-amber-500/10">
                    <Crown className="w-3.5 h-3.5 fill-amber-300 animate-pulse" />
                    <span>PRO</span>
                  </div>
                ) : (
                  <Link
                    to="/billing"
                    className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold text-white bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-600 hover:to-amber-700 shadow-md transition-all"
                  >
                    {tx(t.nav.activatePro, lang)}
                  </Link>
                )}
                <span className="text-slate-400 hidden lg:inline font-medium text-sm truncate max-w-[140px]">
                  {user.display_name || user.email}
                </span>
              </div>
            )}

            {/* Logout — desktop */}
            <button
              type="button"
              onClick={logout}
              className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-academy-border bg-academy-panel/40 hover:bg-academy-panel hover:text-white transition-colors text-sm"
            >
              <LogOut className="w-4 h-4 text-rose-400" />
              <span className="hidden md:inline">{tx(t.nav.logout, lang)}</span>
            </button>

            {/* Hamburger — mobile */}
            <button
              type="button"
              onClick={() => setMobileOpen(!mobileOpen)}
              className="md:hidden p-2 rounded-lg border border-academy-border bg-academy-panel/40 hover:bg-academy-panel"
            >
              {mobileOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>

        {/* Mobile menu */}
        {mobileOpen && (
          <div className="md:hidden border-t border-academy-border bg-academy-bg/95 backdrop-blur-md px-4 py-3 space-y-1">
            {navLinks.map((l) => (
              <NavLink
                key={l.to}
                to={l.to}
                end={l.end}
                className={navClass}
                onClick={() => setMobileOpen(false)}
              >
                {l.icon}
                {l.label}
              </NavLink>
            ))}

            {user && !user.is_premium && (
              <Link
                to="/billing"
                onClick={() => setMobileOpen(false)}
                className="flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-semibold text-amber-300 border border-amber-500/30 bg-amber-500/10"
              >
                <Crown className="w-4 h-4" />
                {tx(t.nav.activatePro, lang)}
              </Link>
            )}

            <button
              type="button"
              onClick={() => { logout(); setMobileOpen(false); }}
              className="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm text-rose-400 hover:bg-academy-panel"
            >
              <LogOut className="w-4 h-4" />
              {tx(t.nav.logout, lang)}
            </button>
          </div>
        )}
      </header>

      {/* ── Page content ───────────────────────────────────── */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-3 sm:px-4 py-4 sm:py-6">
        <Outlet />
      </main>
    </div>
  );
}
