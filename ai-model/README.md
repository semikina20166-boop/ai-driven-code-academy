# ИИ-наставник AI-Driven Code Academy

Модуль для создания **собственной** модели-наставника под этот проект.

> Полная инструкция запуска всего приложения: [STARTUP.md](../STARTUP.md)

## Два режима работы

| Режим | Когда использовать |
|-------|-------------------|
| `builtin` (по умолчанию) | Сразу — встроенный наставник в backend, GPU не нужен |
| `remote` | После обучения — LoRA-модель через локальный API |

## Датасет: задача + код + ошибка + подсказка

Примеры лежат в `data/training_examples.json` — **43 сценария**:

- Python: начальный / средний / продвинутый
- JavaScript, Java, C#, PHP
- экзаменационный режим (краткие подсказки)

Формат одной записи:

```json
{
  "task_text": "Напишите функцию sum_two(a, b)...",
  "user_code": "def sum_two(a, b):\n    pass\n",
  "error": "тесты не пройдены: получено None",
  "hint": "В теле функции остался pass...",
  "level_title": "Python / Начальный — уровень 1",
  "difficulty_name": "Начальный",
  "allowed_concepts": ["переменная", "функция", "return"]
}
```

Дополнительные примеры вручную — в `data/seed_examples.jsonl`.

## Быстрый старт (без обучения)

В `backend/.env`:

```env
AI_PROVIDER=builtin
```

Перезапустите backend — наставник работает сразу.

## Обучение своей модели

### 1. Окружение

```powershell
cd ai-model
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Рекомендуется GPU NVIDIA 6+ ГБ VRAM.

### 2. Сборка датасета

```powershell
python scripts/build_dataset.py
```

Создаёт `data/train.jsonl` (~46 примеров из JSON + seed).

### 3. Обучение (LoRA)

```powershell
python scripts/train_lora.py
```

Результат: `output/ai-academy-mentor/`

### 4. Запуск inference-сервера

```powershell
python scripts/serve.py
```

- Health: http://localhost:8001/health
- API: http://localhost:8001/v1/chat/completions

### 5. Подключение к backend

В `backend/.env`:

```env
AI_PROVIDER=remote
AI_BASE_URL=http://localhost:8001/v1
AI_MODEL=ai-academy-mentor
```

Перезапустите backend и проверьте наставника на уровне 1.

## Как проверить, что всё работает

| Что проверяем | Как |
|---------------|-----|
| Встроенный наставник | `AI_PROVIDER=builtin`, POST `/ai/hint` в Swagger |
| Датасет | `python scripts/build_dataset.py` → «Сохранено N примеров» |
| Сервер модели | http://localhost:8001/health → `{"status":"ok"}` |
| Обученная модель | `AI_PROVIDER=remote` + serve.py + кнопка в UI |

## Структура

```text
ai-model/
├── data/
│   ├── system_prompt.txt
│   ├── training_examples.json   # основной набор (редактируйте здесь)
│   ├── seed_examples.jsonl      # доп. примеры
│   └── train.jsonl              # генерируется build_dataset.py
├── scripts/
│   ├── build_dataset.py
│   ├── train_lora.py
│   └── serve.py
├── output/                      # обученная модель (в .gitignore)
└── requirements.txt
```

## Для диплома

1. **builtin** — rule-based наставник, работает без GPU.
2. **Датасет** — 40+ примеров в стиле Сократа под задачи платформы.
3. **LoRA fine-tuning** — дообучение Qwen2.5-0.5B под домен проекта.
4. **Интеграция** — OpenAI-совместимый API в общий backend.
