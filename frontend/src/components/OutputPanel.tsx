import { Terminal } from "lucide-react";

interface OutputPanelProps {
  output: string;
  passed?: boolean | null;
}

export function OutputPanel({ output, passed }: OutputPanelProps) {
  return (
    <div className="flex flex-col h-full min-h-[160px] rounded-lg border border-academy-border bg-[#0d1117] overflow-hidden">
      <div className="flex items-center gap-2 px-3 py-2 border-b border-academy-border bg-academy-panel text-sm">
        <Terminal className="w-4 h-4 text-academy-muted" />
        <span>Консоль</span>
        {passed === true && (
          <span className="ml-auto text-xs text-academy-success font-medium">Тесты пройдены</span>
        )}
        {passed === false && (
          <span className="ml-auto text-xs text-red-400 font-medium">Ошибка</span>
        )}
      </div>
      <pre className="flex-1 p-3 text-sm font-mono text-green-400/90 overflow-auto whitespace-pre-wrap">
        {output || "Запустите код, чтобы увидеть результат…"}
      </pre>
    </div>
  );
}
