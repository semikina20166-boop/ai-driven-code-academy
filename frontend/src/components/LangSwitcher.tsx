import { useI18n } from "../i18n/I18nContext";
import type { Lang } from "../i18n/translations";

const FLAGS: Record<Lang, string> = { ru: "🇷🇺", en: "🇬🇧", kz: "🇰🇿" };
const LABELS: Record<Lang, string> = { ru: "RU", en: "EN", kz: "KZ" };
const ALL_LANGS: Lang[] = ["ru", "en", "kz"];

interface Props {
  compact?: boolean;
}

export function LangSwitcher({ compact = false }: Props) {
  const { lang, setLang } = useI18n();

  return (
    <div className="flex items-center gap-1">
      {ALL_LANGS.map((l) => (
        <button
          key={l}
          onClick={() => setLang(l)}
          title={l.toUpperCase()}
          className={`flex items-center gap-1 px-2 py-1 rounded-md text-xs font-semibold transition-all
            ${lang === l
              ? "bg-academy-accent text-white shadow-sm"
              : "text-academy-muted hover:bg-academy-panel hover:text-white"
            }`}
        >
          <span>{FLAGS[l]}</span>
          {!compact && <span>{LABELS[l]}</span>}
        </button>
      ))}
    </div>
  );
}
