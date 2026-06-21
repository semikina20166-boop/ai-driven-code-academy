import React, { useState } from "react";
import { X, Loader2 } from "lucide-react";
import { api } from "../../api/client";
import type { Language, Track } from "../../api/types";
import { useI18n } from "../../i18n/I18nContext";

function ModalBase({ title, isOpen, onClose, children }: { title: string, isOpen: boolean, onClose: () => void, children: React.ReactNode }) {
  if (!isOpen) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 overflow-y-auto">
      <div className="bg-academy-panel border border-academy-border rounded-xl w-full max-w-lg p-6 relative">
        <button onClick={onClose} className="absolute top-4 right-4 text-academy-muted hover:text-white">
          <X className="w-5 h-5" />
        </button>
        <h2 className="text-xl font-bold mb-4">{title}</h2>
        {children}
      </div>
    </div>
  );
}

export function AddLanguageModal({ isOpen, onClose, onSuccess }: { isOpen: boolean, onClose: () => void, onSuccess?: () => void }) {
  const [code, setCode] = useState("");
  const [name, setName] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.post("/languages", { code, name });
      onSuccess?.();
      onClose();
    } catch (e: any) {
      alert("Error: " + e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ModalBase title="Добавить язык" isOpen={isOpen} onClose={onClose}>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <div>
          <label className="block text-sm mb-1">Код (напр. 'go', 'rust')</label>
          <input type="text" className="w-full bg-academy-bg border border-academy-border rounded p-2 text-white" value={code} onChange={(e) => setCode(e.target.value)} required />
        </div>
        <div>
          <label className="block text-sm mb-1">Название (напр. 'Go', 'Rust')</label>
          <input type="text" className="w-full bg-academy-bg border border-academy-border rounded p-2 text-white" value={name} onChange={(e) => setName(e.target.value)} required />
        </div>
        <button type="submit" disabled={loading} className="mt-4 bg-academy-accent hover:bg-blue-600 text-white p-2 rounded flex justify-center items-center">
          {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Добавить язык"}
        </button>
      </form>
    </ModalBase>
  );
}

export function AddCourseModal({ isOpen, onClose, onSuccess }: { isOpen: boolean, onClose: () => void, onSuccess?: () => void }) {
  const [langId, setLangId] = useState(1);
  const [title, setTitle] = useState("");
  const [desc, setDesc] = useState("");
  const [loading, setLoading] = useState(false);
  const [languages, setLanguages] = React.useState<Language[]>([]);

  React.useEffect(() => {
    if (isOpen) {
      Promise.all([
        api.get<Language[]>("/languages"),
        api.get<Track[]>("/tracks")
      ]).then(([langs, tracks]) => {
        const usedLangIds = new Set(tracks.map((t) => t.language_id));
        const availableLangs = langs.filter((l) => !usedLangIds.has(l.id));
        setLanguages(availableLangs);
        if (availableLangs.length > 0) setLangId(availableLangs[0].id);
      }).catch(console.error);
    }
  }, [isOpen]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.post("/tracks", {
        language_id: langId,
        title_ru: title,
        description_ru: desc,
      });
      onSuccess?.();
      onClose();
    } catch (e: any) {
      alert("Error: " + e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ModalBase title="Добавить курс (Трек)" isOpen={isOpen} onClose={onClose}>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <div>
          <label className="block text-sm mb-1">Язык</label>
          <select className="w-full bg-academy-bg border border-academy-border rounded p-2 text-white" value={langId} onChange={(e) => setLangId(Number(e.target.value))}>
            {languages.length === 0 && <option disabled>Все языки уже добавлены</option>}
            {languages.map((l) => (
              <option key={l.id} value={l.id}>{l.name} (ID: {l.id})</option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-sm mb-1">Название (RU)</label>
          <input type="text" className="w-full bg-academy-bg border border-academy-border rounded p-2 text-white" value={title} onChange={(e) => setTitle(e.target.value)} required />
        </div>
        <div>
          <label className="block text-sm mb-1">Описание (RU)</label>
          <textarea className="w-full bg-academy-bg border border-academy-border rounded p-2 text-white" value={desc} onChange={(e) => setDesc(e.target.value)} />
        </div>
        <button type="submit" disabled={loading} className="mt-4 bg-academy-accent hover:bg-blue-600 text-white p-2 rounded flex justify-center items-center">
          {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Создать курс"}
        </button>
      </form>
    </ModalBase>
  );
}

export function AddLectureModal({ trackId, isOpen, onClose, onSuccess }: { trackId: number, isOpen: boolean, onClose: () => void, onSuccess?: () => void }) {
  const [title, setTitle] = useState("");
  const [theory, setTheory] = useState("");
  const [diffId, setDiffId] = useState(1);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.post(`/levels/track/${trackId}`, {
        difficulty_id: diffId,
        title_ru: title,
        theory_ru: theory,
      });
      onSuccess?.();
      onClose();
    } catch (e: any) {
      alert("Error: " + e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ModalBase title="Добавить лекцию" isOpen={isOpen} onClose={onClose}>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <div>
          <label className="block text-sm mb-1">Название (RU)</label>
          <input type="text" className="w-full bg-academy-bg border border-academy-border rounded p-2 text-white" value={title} onChange={(e) => setTitle(e.target.value)} required />
        </div>
        <div>
          <label className="block text-sm mb-1">Difficulty ID (1=Easy, 2=Medium, 3=Hard)</label>
          <input type="number" className="w-full bg-academy-bg border border-academy-border rounded p-2 text-white" value={diffId} onChange={(e) => setDiffId(Number(e.target.value))} required />
        </div>
        <div>
          <label className="block text-sm mb-1">Теория (RU - Markdown)</label>
          <textarea rows={5} className="w-full bg-academy-bg border border-academy-border rounded p-2 text-white font-mono text-sm" value={theory} onChange={(e) => setTheory(e.target.value)} />
        </div>
        <button type="submit" disabled={loading} className="mt-4 bg-academy-accent hover:bg-blue-600 text-white p-2 rounded flex justify-center items-center">
          {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Создать лекцию"}
        </button>
      </form>
    </ModalBase>
  );
}

export function AddTaskModal({ trackId, isOpen, onClose, onSuccess }: { trackId: number, isOpen: boolean, onClose: () => void, onSuccess?: () => void }) {
  const [title, setTitle] = useState("");
  const [taskText, setTaskText] = useState("");
  const [starterCode, setStarterCode] = useState("");
  const [testsStr, setTestsStr] = useState("[]");
  const [diffId, setDiffId] = useState(1);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    let parsedTests = [];
    try {
      parsedTests = JSON.parse(testsStr);
    } catch {
      alert("Invalid JSON format for tests");
      setLoading(false);
      return;
    }

    try {
      await api.post(`/levels/track/${trackId}`, {
        difficulty_id: diffId,
        title_ru: title,
        task_text_ru: taskText,
        starter_code: starterCode,
        solution_tests: { cases: parsedTests },
      });
      onSuccess?.();
      onClose();
    } catch (e: any) {
      alert("Error: " + e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ModalBase title="Добавить задание" isOpen={isOpen} onClose={onClose}>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4 max-h-[70vh] overflow-y-auto p-1">
        <div>
          <label className="block text-sm mb-1">Название (RU)</label>
          <input type="text" className="w-full bg-academy-bg border border-academy-border rounded p-2 text-white" value={title} onChange={(e) => setTitle(e.target.value)} required />
        </div>
        <div>
          <label className="block text-sm mb-1">Difficulty ID (1=Easy, 2=Medium, 3=Hard)</label>
          <input type="number" className="w-full bg-academy-bg border border-academy-border rounded p-2 text-white" value={diffId} onChange={(e) => setDiffId(Number(e.target.value))} required />
        </div>
        <div>
          <label className="block text-sm mb-1">Текст задания (RU)</label>
          <textarea className="w-full bg-academy-bg border border-academy-border rounded p-2 text-white" value={taskText} onChange={(e) => setTaskText(e.target.value)} required />
        </div>
        <div>
          <label className="block text-sm mb-1">Стартовый код</label>
          <textarea className="w-full bg-academy-bg border border-academy-border rounded p-2 text-white font-mono text-sm" value={starterCode} onChange={(e) => setStarterCode(e.target.value)} />
        </div>
        <div>
          <label className="block text-sm mb-1">Тесты (JSON array: [{'{'}"input": "...", "expected_output": "..."{'}'}])</label>
          <textarea rows={3} className="w-full bg-academy-bg border border-academy-border rounded p-2 text-white font-mono text-sm" value={testsStr} onChange={(e) => setTestsStr(e.target.value)} />
        </div>
        <button type="submit" disabled={loading} className="mt-4 bg-academy-accent hover:bg-blue-600 text-white p-2 rounded flex justify-center items-center">
          {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Создать задание"}
        </button>
      </form>
    </ModalBase>
  );
}

export function AddExamModal({ trackId, isOpen, onClose, onSuccess }: { trackId: number, isOpen: boolean, onClose: () => void, onSuccess?: () => void }) {
  const [title, setTitle] = useState("");
  const [desc, setDesc] = useState("");
  const [examType, setExamType] = useState("difficulty_block");
  const [diffId, setDiffId] = useState(1);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.post(`/exams`, {
        exam_type: examType,
        title_ru: title,
        description_ru: desc,
        track_ids: [trackId],
        difficulty_id: examType === "difficulty_block" ? diffId : null,
      });
      onSuccess?.();
      onClose();
    } catch (e: any) {
      alert("Error: " + e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ModalBase title="Добавить экзамен" isOpen={isOpen} onClose={onClose}>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <div>
          <label className="block text-sm mb-1">Название (RU)</label>
          <input type="text" className="w-full bg-academy-bg border border-academy-border rounded p-2 text-white" value={title} onChange={(e) => setTitle(e.target.value)} required />
        </div>
        <div>
          <label className="block text-sm mb-1">Описание (RU)</label>
          <textarea className="w-full bg-academy-bg border border-academy-border rounded p-2 text-white" value={desc} onChange={(e) => setDesc(e.target.value)} />
        </div>
        <div>
          <label className="block text-sm mb-1">Тип экзамена</label>
          <select className="w-full bg-academy-bg border border-academy-border rounded p-2 text-white" value={examType} onChange={(e) => setExamType(e.target.value)}>
            <option value="difficulty_block">Блок сложности (difficulty_block)</option>
            <option value="selected_tracks">Выбранные треки (selected_tracks)</option>
            <option value="final">Финальный (final)</option>
          </select>
        </div>
        {examType === "difficulty_block" && (
          <div>
            <label className="block text-sm mb-1">Difficulty ID (1=Easy, 2=Medium, 3=Hard)</label>
            <input type="number" className="w-full bg-academy-bg border border-academy-border rounded p-2 text-white" value={diffId} onChange={(e) => setDiffId(Number(e.target.value))} required />
          </div>
        )}
        <button type="submit" disabled={loading} className="mt-4 bg-academy-accent hover:bg-blue-600 text-white p-2 rounded flex justify-center items-center">
          {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Создать экзамен"}
        </button>
      </form>
    </ModalBase>
  );
}

export function AddExamQuestionModal({ examId, isOpen, onClose, onSuccess }: { examId: number, isOpen: boolean, onClose: () => void, onSuccess?: () => void }) {
  const [taskText, setTaskText] = useState("");
  const [starterCode, setStarterCode] = useState("");
  const [testsStr, setTestsStr] = useState('[{"input": "", "expected_output": ""}]');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    let parsedTests: object[] = [];
    try {
      parsedTests = JSON.parse(testsStr);
    } catch {
      alert("Неверный формат JSON для тестов");
      setLoading(false);
      return;
    }

    try {
      await api.post(`/exams/${examId}/questions`, {
        task_text_ru: taskText,
        starter_code: starterCode,
        tests: { cases: parsedTests },
      });
      onSuccess?.();
      onClose();
      setTaskText("");
      setStarterCode("");
      setTestsStr('[{"input": "", "expected_output": ""}]');
    } catch (e: any) {
      alert("Error: " + e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ModalBase title="Добавить вопрос к экзамену" isOpen={isOpen} onClose={onClose}>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4 max-h-[70vh] overflow-y-auto p-1">
        <div>
          <label className="block text-sm mb-1">Текст задания (RU)</label>
          <textarea rows={4} className="w-full bg-academy-bg border border-academy-border rounded p-2 text-white" value={taskText} onChange={(e) => setTaskText(e.target.value)} required />
        </div>
        <div>
          <label className="block text-sm mb-1">Стартовый код</label>
          <textarea rows={5} className="w-full bg-academy-bg border border-academy-border rounded p-2 text-white font-mono text-sm" value={starterCode} onChange={(e) => setStarterCode(e.target.value)} />
        </div>
        <div>
          <label className="block text-sm mb-1">{'Тесты (JSON array: [{"input": "...", "expected_output": "..."}])'}</label>
          <textarea rows={3} className="w-full bg-academy-bg border border-academy-border rounded p-2 text-white font-mono text-sm" value={testsStr} onChange={(e) => setTestsStr(e.target.value)} />
        </div>
        <button type="submit" disabled={loading} className="mt-4 bg-purple-600 hover:bg-purple-700 text-white p-2 rounded flex justify-center items-center">
          {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Добавить вопрос"}
        </button>
      </form>
    </ModalBase>
  );
}
