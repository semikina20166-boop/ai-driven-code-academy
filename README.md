# AI-Driven Code Academy — Backend & Database

Интерактивный тренажёр для изучения языков программирования (дипломный проект).

> **Быстрый старт:** пошаговая инструкция запуска и проверки — [STARTUP.md](STARTUP.md)

## Запуск за 3 шага

```powershell
# 1. БД: выполнить database/schema.sql и database/seed.sql в pgAdmin

# 2. Backend (терминал 1)
cd backend
.\.venv\Scripts\Activate.ps1   # или создайте venv — см. STARTUP.md
uvicorn app.main:app --reload --port 8000

# 3. Frontend (терминал 2)
cd frontend
npm run dev
```

Откройте http://localhost:5173 — в `.env` backend должно быть `AI_PROVIDER=builtin`.

## Структура

```text
ai-academy-backend-v2/
├── database/
│   ├── schema.sql    # схема PostgreSQL
│   └── seed.sql      # 75 уровней, экзамены
├── backend/
│   ├── app/          # FastAPI
│   ├── requirements.txt
│   └── .env.example
├── ai-model/         # обучение своего ИИ-наставника (LoRA)
│   ├── data/
│   ├── scripts/
│   └── README.md
├── frontend/         # React + Vite + Tailwind + Monaco
│   ├── src/
│   └── package.json
└── README.md
```

## 1. PostgreSQL (pgAdmin)

1. Установите PostgreSQL и pgAdmin 4.
2. Создайте базу: **Databases → Create → Database** → имя `ai_academy`.
3. Откройте **Query Tool** на базе `ai_academy`.
4. Выполните по порядку:
   - `database/schema.sql`
   - `database/seed.sql`
5. Проверка:

```sql
SELECT COUNT(*) FROM levels;   -- 75
SELECT COUNT(*) FROM exams WHERE exam_type = 'difficulty_block';  -- 15
```

## 2. Backend (FastAPI)

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
# отредактируйте DATABASE_URL и SECRET_KEY в .env
uvicorn app.main:app --reload --port 8000
```

- Swagger: http://localhost:8000/docs  
- Health: http://localhost:8000/health  

## 3. Быстрый тест API

1. `POST /auth/register` — `{ "email": "test@example.com", "password": "123456" }`
2. Скопируйте `access_token`, в Swagger нажмите **Authorize** → `Bearer <token>`
3. `GET /tracks` — список треков
4. `POST /tracks/1/start` — открыть первый уровень Python
5. `GET /levels/track/1/map` — карта уровней
6. `GET /levels/{id}` — условие задачи
7. `POST /levels/run` — `{ "level_id": 1, "code": "def sum_two(a, b):\n    return a + b" }` (для первого Python easy)

## Переменные окружения (.env)

| Переменная | Описание |
|------------|----------|
| `DATABASE_URL` | `postgresql+asyncpg://user:pass@localhost:5432/ai_academy` |
| `SECRET_KEY` | секрет для JWT |
| `AI_PROVIDER` | `builtin` — встроенный наставник (по умолчанию); `remote` — обученная модель |
| `AI_BASE_URL` | URL API модели при `remote`, напр. `http://localhost:8001/v1` |
| `AI_MODEL` | имя модели при `remote`, напр. `ai-academy-mentor` |
| `AI_API_KEY` | ключ API (для локального сервера можно оставить пустым) |
| `AI_TIMEOUT_SEC` | таймаут ответа ИИ в секундах (по умолчанию 60) |

## 5. Свой ИИ-наставник (обучение модели)

По умолчанию работает **встроенный** наставник (`AI_PROVIDER=builtin`) — ничего дополнительно ставить не нужно.

Чтобы обучить **свою** модель под проект:

```powershell
cd ai-model
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/build_dataset.py
python scripts/train_lora.py
python scripts/serve.py
```

Затем в `backend/.env`: `AI_PROVIDER=remote`, `AI_BASE_URL=http://localhost:8001/v1`, `AI_MODEL=ai-academy-mentor`.

Подробности: [ai-model/README.md](ai-model/README.md)

## Экзамены

| Тип | Условие доступа |
|-----|-----------------|
| `difficulty_block` | Все 5 уровней блока (трек + сложность) пройдены |
| `selected_tracks` | ≥ 5 пройденных уровней всего |
| `final` | ≥ 30 пройденных уровней |

Эндпоинты: `GET /exams/available`, `POST /exams/{id}/start`, `POST /exams/attempt/{id}/submit`, `POST /exams/attempt/{id}/finish`.

## 4. Frontend (React)

```powershell
cd frontend
npm install
npm run dev
```

Откройте http://localhost:5173 — регистрация, треки, карта уровней, редактор Monaco, консоль, AI-наставник, экзамены.

Запросы к API проксируются: `/api` → `http://localhost:8000` (см. `frontend/vite.config.ts`).

Перед запуском фронтенда должен работать backend на порту 8000.

## Стек

- **Frontend:** React 18, Vite, Tailwind CSS, Lucide React, Monaco Editor
- **Backend:** FastAPI, SQLAlchemy 2 (async), JWT
- **DB:** PostgreSQL
- **Проверка кода:** Python subprocess (демо); для продакшена — Docker
- **ИИ:** встроенный наставник + LoRA fine-tuning (Qwen2.5-0.5B), метод Сократа, русский язык
"# ai-driven-code-academy" 
