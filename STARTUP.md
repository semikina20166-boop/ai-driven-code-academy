# Как запустить приложение

Пошаговая инструкция для Windows (PowerShell).

## Что нужно установить

| Компонент | Зачем |
|-----------|--------|
| PostgreSQL + pgAdmin | база данных |
| Python 3.10+ | backend и ai-model |
| Node.js 18+ | frontend |

---

## Шаг 1. База данных (один раз)

1. Создайте базу `ai_academy` в pgAdmin.
2. В **Query Tool** выполните по порядку:
   - `database/schema.sql`
   - `database/seed.sql`
3. Проверка:

```sql
SELECT COUNT(*) FROM levels;  -- должно быть 75
```

---

## Шаг 2. Backend (терминал 1)

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Отредактируйте `backend/.env` — минимум:

```env
DATABASE_URL=postgresql+asyncpg://postgres:ВАШ_ПАРОЛЬ@localhost:5432/ai_academy
SECRET_KEY=любая-длинная-случайная-строка
AI_PROVIDER=builtin
```

Запуск:

```powershell
uvicorn app.main:app --reload --port 8000
```

Проверка: откройте http://localhost:8000/health — должно быть `{"status":"ok"}`.

---

## Шаг 3. Frontend (терминал 2)

```powershell
cd frontend
npm install
npm run dev
```

Откройте http://localhost:5173

> Backend на порту **8000** должен быть уже запущен.

---

## Шаг 4. Проверка ИИ-наставника в браузере

1. Зарегистрируйтесь на http://localhost:5173
2. Выберите трек **Python** → начните курс
3. Откройте **уровень 1** (sum_two)
4. В редакторе оставьте код с ошибкой, например:

```python
def sum_two(a, b):
    pass
```

5. Нажмите **Запустить** — тест не пройдёт
6. В панели **AI-наставник** нажмите **Спросить наставника**
7. Должна появиться подсказка на русском (без готового решения)

---

## Шаг 5. Проверка через Swagger (без фронтенда)

1. http://localhost:8000/docs
2. `POST /auth/register` → `{ "email": "test@test.com", "password": "123456" }`
3. **Authorize** → `Bearer <access_token>`
4. `POST /tracks/1/start`
5. `POST /ai/hint`:

```json
{
  "level_id": 1,
  "code": "def sum_two(a, b):\n    pass",
  "error_message": "тесты не пройдены: получено None"
}
```

В ответе поле `hint` — подсказка наставника.

---

## (Опционально) Обучение своей модели

Только если нужна **обученная** LLM вместо встроенного наставника.

### Терминал 3 — сборка датасета

```powershell
cd ai-model
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/build_dataset.py
```

Создаст `ai-model/data/train.jsonl` (~46 примеров).

### Терминал 3 — обучение (нужен GPU, долго)

```powershell
python scripts/train_lora.py
```

Результат: `ai-model/output/ai-academy-mentor/`

### Терминал 4 — сервер модели

```powershell
cd ai-model
.\.venv\Scripts\Activate.ps1
python scripts/serve.py
```

Проверка: http://localhost:8001/health

### Переключение backend на модель

В `backend/.env`:

```env
AI_PROVIDER=remote
AI_BASE_URL=http://localhost:8001/v1
AI_MODEL=ai-academy-mentor
```

Перезапустите backend (терминал 1).

---

## Сводка: какие терминалы держать открытыми

| Режим | Терминал 1 | Терминал 2 | Терминал 3 |
|-------|------------|------------|------------|
| **Обычная работа** | `uvicorn` (backend) | `npm run dev` (frontend) | — |
| **С обученной моделью** | `uvicorn` (backend) | `npm run dev` (frontend) | `python scripts/serve.py` |

---

## Частые проблемы

| Проблема | Решение |
|----------|---------|
| `503 База данных недоступна` | Запустите PostgreSQL, проверьте `DATABASE_URL` в `.env` |
| Фронтенд не видит API | Backend должен работать на порту 8000 |
| «Internal Server Error» при регистрации | Остановите backend (Ctrl+C), выполните `pip install -r requirements.txt`, снова `uvicorn app.main:app --reload --port 8000` |
| «ИИ-наставник не настроен» | Установите `AI_PROVIDER=builtin` в `backend/.env` |
| Модель не отвечает (remote) | Сначала запустите `python scripts/serve.py` |
| `train_lora.py` очень долго | Нормально на CPU; нужен GPU NVIDIA |

---

## Файлы проекта — что за что отвечает

```text
database/schema.sql      — создать таблицы
database/seed.sql        — 75 уровней и экзамены
backend/app/main.py      — точка входа API
backend/.env             — настройки (БД, ИИ)
frontend/src/            — интерфейс
ai-model/data/training_examples.json  — примеры для обучения
ai-model/scripts/build_dataset.py     — собрать train.jsonl
ai-model/scripts/train_lora.py        — обучить модель
ai-model/scripts/serve.py             — запустить модель
```
