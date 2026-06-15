import json
import os
import subprocess
import tempfile
from typing import Any

from app.config import settings


def run_python_tests(user_code: str, tests: dict) -> dict[str, Any]:
    """
    tests format:
    {
      "function": "sum_two",
      "language": "python",
      "cases": [{"args": [1, 2], "expected": 3}]
    }
    """
    cases_json = json.dumps(tests.get("cases", []))
    fn_name = json.dumps(tests.get("function", ""))

    wrapper = f'''import json
import traceback

{user_code}

def _run_tests():
    cases = {cases_json}
    fn_name = {fn_name}
    fn = globals().get(fn_name)
    if not callable(fn):
        return {{
            "passed": False,
            "stdout": "",
            "stderr": f"Функция {{fn_name}} не найдена или не вызывается",
            "details": [],
        }}
    details = []
    for i, case in enumerate(cases):
        try:
            got = fn(*case.get("args", []))
            expected = case.get("expected")
            ok = got == expected
            details.append({{"case": i, "ok": ok, "got": repr(got), "expected": repr(expected)}})
        except Exception as exc:
            details.append({{"case": i, "ok": False, "error": str(exc)}})
    passed = all(d.get("ok") for d in details) if details else False
    return {{"passed": passed, "stdout": "", "stderr": "", "details": details}}

if __name__ == "__main__":
    print(json.dumps(_run_tests()))
'''

    path = ""
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as fh:
            fh.write(wrapper)
            path = fh.name

        proc = subprocess.run(
            ["python", path],
            capture_output=True,
            text=True,
            timeout=settings.code_runner_timeout_sec,
        )
        if proc.returncode != 0:
            return {
                "passed": False,
                "stdout": proc.stdout,
                "stderr": proc.stderr or "Ошибка выполнения",
                "details": [],
            }
        line = (proc.stdout or "").strip().splitlines()
        if not line:
            return {"passed": False, "stdout": "", "stderr": "Пустой ответ", "details": []}
        return json.loads(line[-1])
    except subprocess.TimeoutExpired:
        return {"passed": False, "stdout": "", "stderr": "Превышено время выполнения", "details": []}
    except json.JSONDecodeError:
        return {"passed": False, "stdout": "", "stderr": "Не удалось разобрать результат тестов", "details": []}
    finally:
        if path and os.path.exists(path):
            os.unlink(path)


def run_tests_for_language(user_code: str, tests: dict) -> dict[str, Any]:
    language = (tests.get("language") or "python").lower()
    if language == "python":
        return run_python_tests(user_code, tests)
    return {
        "passed": False,
        "stdout": "",
        "stderr": f"Язык «{language}» пока поддерживается только для демо (Python).",
        "details": [],
    }
