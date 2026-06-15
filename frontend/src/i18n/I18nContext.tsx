import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import type { Lang } from "./translations";
import { translations } from "./translations";

interface I18nContextValue {
  lang: Lang;
  setLang: (l: Lang) => void;
  t: typeof translations;
}

const I18nContext = createContext<I18nContextValue | null>(null);

const STORAGE_KEY = "academy_lang";

export function I18nProvider({ children }: { children: ReactNode }) {
  const [lang, setLangState] = useState<Lang>(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored === "ru" || stored === "en" || stored === "kz") return stored;
    return "ru";
  });

  function setLang(l: Lang) {
    setLangState(l);
    localStorage.setItem(STORAGE_KEY, l);
  }

  useEffect(() => {
    document.documentElement.lang = lang;
  }, [lang]);

  return (
    <I18nContext.Provider value={{ lang, setLang, t: translations }}>
      {children}
    </I18nContext.Provider>
  );
}

export function useI18n() {
  const ctx = useContext(I18nContext);
  if (!ctx) throw new Error("useI18n must be used inside I18nProvider");
  return ctx;
}

/** Helper: pick the correct language string from a translation node */
export function tx(
  node: { ru: string; en: string; kz: string },
  lang: Lang
): string {
  return node[lang];
}
