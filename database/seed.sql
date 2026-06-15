-- Наполнение языков
INSERT INTO languages (code, name) VALUES
  ('python', 'Python'),
  ('csharp', 'C#'),
  ('php', 'PHP'),
  ('javascript', 'JavaScript'),
  ('java', 'Java')
ON CONFLICT (code) DO NOTHING;

-- Наполнение локализованных сложностей
INSERT INTO difficulties (code, name_ru, name_en, name_kz, sort_order) VALUES
  ('easy', 'Начальный', 'Easy', 'Бастапқы', 1),
  ('medium', 'Средний', 'Medium', 'Орташа', 2),
  ('hard', 'Продвинутый', 'Hard', 'Жоғары', 3)
ON CONFLICT (code) DO NOTHING;

-- Наполнение локализованных треков
INSERT INTO tracks (language_id, title_ru, title_en, title_kz, description_ru, description_en, description_kz)
SELECT 
  l.id, 
  l.name || ' — трек', 
  l.name || ' — Track', 
  l.name || ' — трегі',
  'Обучающий трек по языку ' || l.name,
  'Learning track for ' || l.name,
  ' ' || l.name || ' тілі бойынша оқыту трегі'
FROM languages l
WHERE NOT EXISTS (SELECT 1 FROM tracks t WHERE t.language_id = l.id);

-- Автогенерация 75 уровней на 3-х языках
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
SELECT
  tr.id,
  d.id,
  n.n,
  -- Заголовки
  l.name || ' / ' || d.name_ru || ' — уровень ' || n.n,
  l.name || ' / ' || d.name_en || ' — Level ' || n.n,
  l.name || ' / ' || d.name_kz || ' — деңгей ' || n.n,
  -- Условие задачи (Для Python Easy 1 — полный перевод, для остальных — шаблоны)
  CASE
    WHEN l.code = 'python' AND d.code = 'easy' AND n.n = 1 THEN 'Напишите функцию sum_two(a, b), которая возвращает сумму двух чисел.'
    ELSE 'Задача ' || n.n || ' (' || l.name || ', ' || d.name_ru || '). Реализуйте функцию solve() согласно условию наставника.'
  END,
  CASE
    WHEN l.code = 'python' AND d.code = 'easy' AND n.n = 1 THEN 'Write a function sum_two(a, b) that returns the sum of two numbers.'
    ELSE 'Task ' || n.n || ' (' || l.name || ', ' || d.name_en || '). Implement the solve() function as requested by your mentor.'
  END,
  CASE
    WHEN l.code = 'python' AND d.code = 'easy' AND n.n = 1 THEN 'Екі санның қосындысын қайтаратын sum_two(a, b) функциясын жазыңыз.'
    ELSE 'Тапсырма ' || n.n || ' (' || l.name || ', ' || d.name_kz || '). Тәлімгердің шарты бойынша solve() функциясын іске асырыңыз.'
  END,
  -- Стартовый код
  CASE
    WHEN l.code = 'python' AND d.code = 'easy' AND n.n = 1 THEN E'def sum_two(a, b):\n    # ваш код / your code / сіздің кодыңыз\n    pass\n'
    ELSE E'def solve():\n    # ваш код / your code / сіздің кодыңыз\n    pass\n'
  END,
  -- Тесты
  CASE
    WHEN l.code = 'python' AND d.code = 'easy' AND n.n = 1 THEN '{"function": "sum_two", "language": "python", "cases": [{"args": [1, 2], "expected": 3}, {"args": [-1, 5], "expected": 4}]}'::jsonb
    ELSE '{"function": "solve", "language": "python", "cases": [{"args": [], "expected": null}]}'::jsonb
  END,
  -- Разрешенные концепции
  CASE
    WHEN d.code = 'easy' THEN ARRAY['переменная', 'функция', 'return']
    WHEN d.code = 'medium' THEN ARRAY['цикл', 'условие', 'список']
    ELSE ARRAY['класс', 'исключение', 'алгоритм']
  END
FROM tracks tr
JOIN languages l ON l.id = tr.language_id
CROSS JOIN difficulties d
CROSS JOIN generate_series(1, 5) AS n(n)
WHERE NOT EXISTS (
  SELECT 1 FROM levels lv
  WHERE lv.track_id = tr.id AND lv.difficulty_id = d.id AND lv.order_num = n.n
);

-- Генерация блочных экзаменов (15 штук)
INSERT INTO exams (exam_type, title_ru, title_en, title_kz, description_ru, description_en, description_kz, pass_percent, time_limit_min, max_attempts)
SELECT
  'difficulty_block'::exam_type,
  l.name || ' — экзамен: ' || d.name_ru,
  l.name || ' — Exam: ' || d.name_en,
  l.name || ' — емтихан: ' || d.name_kz,
  'Проверка знаний после 5 уровней сложности «' || d.name_ru || '»',
  'Knowledge test after 5 levels of difficulty "' || d.name_en || '"',
  '«' || d.name_kz || '» күрделілігінің 5 деңгейінен кейін білімді тексеру',
  70, 30, 3
FROM tracks tr
JOIN languages l ON l.id = tr.language_id
CROSS JOIN difficulties d
WHERE NOT EXISTS (
  SELECT 1 FROM exams e
  WHERE e.title_ru = l.name || ' — экзамен: ' || d.name_ru AND e.exam_type = 'difficulty_block'
);

-- Связка с таблицей блоков
INSERT INTO exam_difficulty_blocks (exam_id, track_id, difficulty_id)
SELECT e.id, tr.id, d.id
FROM tracks tr
JOIN languages l ON l.id = tr.language_id
CROSS JOIN difficulties d
JOIN exams e ON e.title_ru = l.name || ' — экзамен: ' || d.name_ru
WHERE e.exam_type = 'difficulty_block'
ON CONFLICT DO NOTHING;

-- Вопросы к экзаменам (по 3 на каждый)
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT
  e.id,
  q.n,
  'Экзаменационный вопрос ' || q.n || ' для «' || e.title_ru || '».',
  'Exam question ' || q.n || ' for "' || e.title_en || '".',
  '«' || e.title_kz || '» үшін ' || q.n || '-емтихан сұрағы.',
  E'def exam_answer():\n    pass\n',
  '{"function": "exam_answer", "language": "python", "cases": [{"args": [], "expected": null}]}'::jsonb,
  tr.language_id
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
CROSS JOIN generate_series(1, 3) AS q(n)
WHERE e.exam_type = 'difficulty_block'
  AND NOT EXISTS (
    SELECT 1 FROM exam_questions eq WHERE eq.exam_id = e.id AND eq.order_num = q.n
  );

-- Итоговый экзамен
INSERT INTO exams (exam_type, title_ru, title_en, title_kz, description_ru, description_en, description_kz, pass_percent, time_limit_min, max_attempts)
SELECT 
  'final'::exam_type, 
  'Итоговый экзамен', 'Final Exam', 'Қорытынды емтихан',
  'Обобщённая проверка по всем трекам', 'Comprehensive test across all tracks', 'Барлық тректер бойынша жалпылама тексеру',
  75, 60, 2
WHERE NOT EXISTS (SELECT 1 FROM exams WHERE exam_type = 'final');

-- Экзамен по выбору
INSERT INTO exams (exam_type, title_ru, title_en, title_kz, description_ru, description_en, description_kz, pass_percent, time_limit_min, max_attempts)
SELECT 
  'selected_tracks'::exam_type, 
  'Экзамен по выбранным курсам', 'Exam on Selected Courses', 'Таңдалған курстар бойынша емтихан',
  'Пользователь выбирает один или несколько треков', 'The user selects one or more tracks', 'Пайдаланушы бір немесе бірнеше тректерді таңдайды',
  70, 45, 3
WHERE NOT EXISTS (SELECT 1 FROM exams WHERE exam_type = 'selected_tracks');

-- Вопрос к экзамену по выбору
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests)
SELECT 
  e.id, 1,
  'Смешанный вопрос по выбранным курсам: реализуйте функцию mixed_task().',
  'Mixed question for selected courses: implement the mixed_task() function.',
  'Таңдалған курстар бойынша аралас сұрақ: mixed_task() функциясын іске асырыңыз.',
  E'def mixed_task():\n    pass\n',
  '{"function": "mixed_task", "language": "python", "cases": [{"args": [], "expected": null}]}'::jsonb
FROM exams e
WHERE e.exam_type = 'selected_tracks'
  AND NOT EXISTS (SELECT 1 FROM exam_questions eq WHERE eq.exam_id = e.id);