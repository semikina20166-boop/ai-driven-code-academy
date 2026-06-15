CREATE EXTENSION IF NOT EXISTS "pgcrypto";

DO $$ BEGIN
  CREATE TYPE progress_status AS ENUM ('locked', 'open', 'completed');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
  CREATE TYPE exam_type AS ENUM ('difficulty_block', 'selected_tracks', 'final');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

-- 1. ЯЗЫКИ ПРОГРАММИРОВАНИЯ
CREATE TABLE IF NOT EXISTS languages (
  id SERIAL PRIMARY KEY,
  code VARCHAR(16) UNIQUE NOT NULL,
  name VARCHAR(64) NOT NULL  -- Названия технологий (Python, Java) обычно не переводят
);

-- 2. СЛОЖНОСТЬ (Локализованная)
CREATE TABLE IF NOT EXISTS difficulties (
  id SERIAL PRIMARY KEY,
  code VARCHAR(16) UNIQUE NOT NULL,
  name_ru VARCHAR(32) NOT NULL,
  name_en VARCHAR(32) NOT NULL,
  name_kz VARCHAR(32) NOT NULL,
  sort_order SMALLINT NOT NULL DEFAULT 0
);

-- 3. ТРЕКИ (Локализованные)
CREATE TABLE IF NOT EXISTS tracks (
  id SERIAL PRIMARY KEY,
  language_id INT NOT NULL REFERENCES languages(id) ON DELETE CASCADE,
  title_ru VARCHAR(128) NOT NULL,
  title_en VARCHAR(128) NOT NULL,
  title_kz VARCHAR(128) NOT NULL,
  description_ru TEXT,
  description_en TEXT,
  description_kz TEXT,
  UNIQUE (language_id)
);

-- 4. УРОВНИ / ЗАДАЧИ (Локализованные)
CREATE TABLE IF NOT EXISTS levels (
  id SERIAL PRIMARY KEY,
  track_id INT NOT NULL REFERENCES tracks(id) ON DELETE CASCADE,
  difficulty_id INT NOT NULL REFERENCES difficulties(id) ON DELETE CASCADE,
  order_num SMALLINT NOT NULL CHECK (order_num BETWEEN 1 AND 5),
  title_ru VARCHAR(255) NOT NULL DEFAULT '',
  title_en VARCHAR(255) NOT NULL DEFAULT '',
  title_kz VARCHAR(255) NOT NULL DEFAULT '',
  task_text_ru TEXT NOT NULL,
  task_text_en TEXT NOT NULL,
  task_text_kz TEXT NOT NULL,
  starter_code TEXT NOT NULL,
  solution_tests JSONB NOT NULL,
  allowed_concepts TEXT[] DEFAULT '{}',
  theory_ru TEXT,
  theory_en TEXT,
  theory_kz TEXT,
  UNIQUE (track_id, difficulty_id, order_num)
);

-- 5. ПОЛЬЗОВАТЕЛИ
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  display_name VARCHAR(128),
  is_premium BOOLEAN DEFAULT FALSE,
  hints_used_today INT DEFAULT 0,
  last_hint_date DATE DEFAULT CURRENT_DATE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 6. ПРОГРЕСС
CREATE TABLE IF NOT EXISTS user_progress (
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  level_id INT NOT NULL REFERENCES levels(id) ON DELETE CASCADE,
  status progress_status NOT NULL DEFAULT 'locked',
  attempts INT NOT NULL DEFAULT 0,
  completed_at TIMESTAMPTZ,
  PRIMARY KEY (user_id, level_id)
);

-- 7. ЭКЗАМЕНЫ (Локализованные)
CREATE TABLE IF NOT EXISTS exams (
  id SERIAL PRIMARY KEY,
  exam_type exam_type NOT NULL,
  title_ru VARCHAR(255) NOT NULL,
  title_en VARCHAR(255) NOT NULL,
  title_kz VARCHAR(255) NOT NULL,
  description_ru TEXT,
  description_en TEXT,
  description_kz TEXT,
  pass_percent SMALLINT NOT NULL DEFAULT 70 CHECK (pass_percent BETWEEN 1 AND 100),
  time_limit_min INT,
  max_attempts SMALLINT NOT NULL DEFAULT 3
);

-- 8. СВЯЗЬ ЭКЗАМЕНОВ И БЛОКОВ СЛОЖНОСТИ
CREATE TABLE IF NOT EXISTS exam_difficulty_blocks (
  exam_id INT PRIMARY KEY REFERENCES exams(id) ON DELETE CASCADE,
  track_id INT NOT NULL REFERENCES tracks(id) ON DELETE CASCADE,
  difficulty_id INT NOT NULL REFERENCES difficulties(id) ON DELETE CASCADE,
  UNIQUE (track_id, difficulty_id)
);

-- 9. ВОПРОСЫ ЭКЗАМЕНОВ (Локализованные)
CREATE TABLE IF NOT EXISTS exam_questions (
  id SERIAL PRIMARY KEY,
  exam_id INT NOT NULL REFERENCES exams(id) ON DELETE CASCADE,
  order_num SMALLINT NOT NULL CHECK (order_num BETWEEN 1 AND 20),
  task_text_ru TEXT NOT NULL,
  task_text_en TEXT NOT NULL,
  task_text_kz TEXT NOT NULL,
  starter_code TEXT NOT NULL,
  tests JSONB NOT NULL,
  language_id INT REFERENCES languages(id) ON DELETE SET NULL,
  UNIQUE (exam_id, order_num)
);

-- ОСТАЛЬНЫЕ ТАБЛИЦЫ ОСТАЮТСЯ БЕЗ ИЗМЕНЕНИЙ (они хранят только логику, коды или ID)
CREATE TABLE IF NOT EXISTS user_selected_tracks_for_exam (
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  exam_id INT NOT NULL REFERENCES exams(id) ON DELETE CASCADE,
  track_ids INT[] NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (user_id, exam_id)
);

CREATE TABLE IF NOT EXISTS user_exam_attempts (
  id SERIAL PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  exam_id INT NOT NULL REFERENCES exams(id) ON DELETE CASCADE,
  score SMALLINT,
  passed BOOLEAN,
  started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  finished_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS user_exam_answers (
  id SERIAL PRIMARY KEY,
  attempt_id INT NOT NULL REFERENCES user_exam_attempts(id) ON DELETE CASCADE,
  question_id INT NOT NULL REFERENCES exam_questions(id) ON DELETE CASCADE,
  submitted_code TEXT NOT NULL,
  test_result JSONB,
  passed BOOLEAN NOT NULL DEFAULT false,
  submitted_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_levels_track_difficulty ON levels (track_id, difficulty_id);
CREATE INDEX IF NOT EXISTS idx_user_progress_user ON user_progress (user_id);
CREATE INDEX IF NOT EXISTS idx_user_exam_attempts_user ON user_exam_attempts (user_id, exam_id);