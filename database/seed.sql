-- =============================================
-- ПОЛНОЕ НАПОЛНЕНИЕ БАЗЫ ДАННЫХ (РЕАЛЬНЫЕ ЗАДАНИЯ)
-- =============================================

INSERT INTO languages (code, name) VALUES
  ('python', 'Python'),
  ('csharp', 'C#'),
  ('php', 'PHP'),
  ('javascript', 'JavaScript'),
  ('java', 'Java')
ON CONFLICT (code) DO NOTHING;

INSERT INTO difficulties (code, name_ru, name_en, name_kz, sort_order) VALUES
  ('easy', 'Начальный', 'Beginner', 'Бастапқы', 1),
  ('medium', 'Средний', 'Intermediate', 'Орташа', 2),
  ('hard', 'Продвинутый', 'Advanced', 'Жоғары', 3)
ON CONFLICT (code) DO NOTHING;

INSERT INTO tracks (language_id, title_ru, title_en, title_kz, description_ru, description_en, description_kz)
SELECT l.id, l.name || ' — трек', l.name || ' — Track', l.name || ' — трегі',
  'Обучающий трек по языку ' || l.name, 'Learning track for ' || l.name, l.name || ' тілі бойынша оқыту трегі'
FROM languages l
WHERE NOT EXISTS (SELECT 1 FROM tracks t WHERE t.language_id = l.id);

INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'python'), (SELECT id FROM difficulties WHERE code = 'easy'), 1,
  'Python / Начальный — уровень 1', 'Python / Beginner — Level 1', 'Python / Бастапқы — деңгей 1',
  'Напишите функцию sum_two(a, b), которая возвращает сумму двух чисел.', 'Write a function sum_two(a, b) that returns the sum of two numbers.', 'Екі санның қосындысын қайтаратын sum_two(a, b) функциясын жазыңыз.',
  'def sum_two(a, b):
    pass
', '{"function": "sum_two", "language": "python", "cases": [{"args": [1, 2], "expected": 3}, {"args": [-1, 5], "expected": 4}]}'::jsonb, ARRAY['переменная', 'функция', 'return']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'python'), (SELECT id FROM difficulties WHERE code = 'easy'), 2,
  'Python / Начальный — уровень 2', 'Python / Beginner — Level 2', 'Python / Бастапқы — деңгей 2',
  'Напишите функцию is_even(n), которая возвращает true, если число чётное, и false в противном случае.', 'Write a function is_even(n) that returns true if the number is even, and false otherwise.', 'Сан жұп болса true, әйтпесе false қайтаратын is_even(n) функциясын жазыңыз.',
  'def is_even(n):
    pass
', '{"function": "is_even", "language": "python", "cases": [{"args": [4], "expected": true}, {"args": [7], "expected": false}]}'::jsonb, ARRAY['условие', 'оператор', 'return']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'python'), (SELECT id FROM difficulties WHERE code = 'easy'), 3,
  'Python / Начальный — уровень 3', 'Python / Beginner — Level 3', 'Python / Бастапқы — деңгей 3',
  'Напишите функцию max_of_two(a, b), возвращающую наибольшее из двух чисел.', 'Write a function max_of_two(a, b) returning the largest of two numbers.', 'Екі санның үлкенін қайтаратын max_of_two(a, b) функциясын жазыңыз.',
  'def max_of_two(a, b):
    pass
', '{"function": "max_of_two", "language": "python", "cases": [{"args": [10, 20], "expected": 20}, {"args": [5, -5], "expected": 5}]}'::jsonb, ARRAY['условие', 'return']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'python'), (SELECT id FROM difficulties WHERE code = 'easy'), 4,
  'Python / Начальный — уровень 4', 'Python / Beginner — Level 4', 'Python / Бастапқы — деңгей 4',
  'Напишите функцию factorial(n) для вычисления факториала (n >= 0).', 'Write a function factorial(n) to calculate the factorial (n >= 0).', 'Факториалды есептейтін factorial(n) функциясын жазыңыз (n >= 0).',
  'def factorial(n):
    pass
', '{"function": "factorial", "language": "python", "cases": [{"args": [0], "expected": 1}, {"args": [5], "expected": 120}]}'::jsonb, ARRAY['цикл', 'рекурсия']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'python'), (SELECT id FROM difficulties WHERE code = 'easy'), 5,
  'Python / Начальный — уровень 5', 'Python / Beginner — Level 5', 'Python / Бастапқы — деңгей 5',
  'Напишите функцию reverse_string(s), которая переворачивает строку.', 'Write a function reverse_string(s) that reverses a string.', 'Жолды кері айналдыратын reverse_string(s) функциясын жазыңыз.',
  'def reverse_string(s):
    pass
', '{"function": "reverse_string", "language": "python", "cases": [{"args": ["hello"], "expected": "olleh"}, {"args": [""], "expected": ""}]}'::jsonb, ARRAY['строка', 'цикл']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'python'), (SELECT id FROM difficulties WHERE code = 'medium'), 1,
  'Python / Средний — уровень 1', 'Python / Intermediate — Level 1', 'Python / Орташа — деңгей 1',
  'Напишите функцию sum_list(lst), которая возвращает сумму всех элементов списка/массива.', 'Write a function sum_list(lst) that returns the sum of all elements in a list/array.', 'Тізімнің/массивтің барлық элементтерінің қосындысын қайтаратын sum_list(lst) функциясын жазыңыз.',
  'def sum_list(lst):
    pass
', '{"function": "sum_list", "language": "python", "cases": [{"args": [[1, 2, 3]], "expected": 6}, {"args": [[]], "expected": 0}]}'::jsonb, ARRAY['цикл', 'список', 'массив']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'python'), (SELECT id FROM difficulties WHERE code = 'medium'), 2,
  'Python / Средний — уровень 2', 'Python / Intermediate — Level 2', 'Python / Орташа — деңгей 2',
  'Напишите функцию count_vowels(s), возвращающую количество гласных букв (a, e, i, o, u) в строке без учета регистра.', 'Write a function count_vowels(s) returning the number of vowels (a, e, i, o, u) in a string case-insensitively.', 'Жолдағы дауысты дыбыстардың (a, e, i, o, u) санын регистрге қарамастан қайтаратын count_vowels(s) функциясын жазыңыз.',
  'def count_vowels(s):
    pass
', '{"function": "count_vowels", "language": "python", "cases": [{"args": ["hello"], "expected": 2}, {"args": ["APPLE"], "expected": 2}]}'::jsonb, ARRAY['строка', 'цикл', 'условие']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'python'), (SELECT id FROM difficulties WHERE code = 'medium'), 3,
  'Python / Средний — уровень 3', 'Python / Intermediate — Level 3', 'Python / Орташа — деңгей 3',
  'Напишите функцию fizzbuzz(n), возвращающую ''FizzBuzz'' если n делится на 15, ''Fizz'' если на 3, ''Buzz'' если на 5, иначе строку n.', 'Write fizzbuzz(n) returning ''FizzBuzz'' if n is divisible by 15, ''Fizz'' if by 3, ''Buzz'' if by 5, else string of n.', 'Егер n 15-ке бөлінсе ''FizzBuzz'', 3-ке бөлінсе ''Fizz'', 5-ке бөлінсе ''Buzz'', әйтпесе n жолын қайтаратын fizzbuzz(n) функциясын жазыңыз.',
  'def fizzbuzz(n):
    pass
', '{"function": "fizzbuzz", "language": "python", "cases": [{"args": [15], "expected": "FizzBuzz"}, {"args": [3], "expected": "Fizz"}, {"args": [5], "expected": "Buzz"}, {"args": [7], "expected": "7"}]}'::jsonb, ARRAY['условие', 'оператор']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'python'), (SELECT id FROM difficulties WHERE code = 'medium'), 4,
  'Python / Средний — уровень 4', 'Python / Intermediate — Level 4', 'Python / Орташа — деңгей 4',
  'Напишите функцию is_palindrome(s), проверяющую, является ли строка палиндромом (читается одинаково слева направо и справа налево).', 'Write a function is_palindrome(s) checking if a string is a palindrome.', 'Жолдың палиндром екенін тексеретін is_palindrome(s) функциясын жазыңыз.',
  'def is_palindrome(s):
    pass
', '{"function": "is_palindrome", "language": "python", "cases": [{"args": ["racecar"], "expected": true}, {"args": ["hello"], "expected": false}]}'::jsonb, ARRAY['строка', 'срез']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'python'), (SELECT id FROM difficulties WHERE code = 'medium'), 5,
  'Python / Средний — уровень 5', 'Python / Intermediate — Level 5', 'Python / Орташа — деңгей 5',
  'Напишите функцию binary_search(arr, target), реализующую бинарный поиск. Возвращает индекс элемента или -1.', 'Write a function binary_search(arr, target) implementing binary search. Returns index or -1.', 'Бинарлық іздеуді жүзеге асыратын binary_search(arr, target) функциясын жазыңыз. Индексті немесе -1 қайтарады.',
  'def binary_search(arr, target):
    pass
', '{"function": "binary_search", "language": "python", "cases": [{"args": [[1, 2, 3, 4, 5], 4], "expected": 3}, {"args": [[1, 2, 3, 4, 5], 6], "expected": -1}]}'::jsonb, ARRAY['алгоритм', 'массив', 'цикл']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'python'), (SELECT id FROM difficulties WHERE code = 'hard'), 1,
  'Python / Продвинутый — уровень 1', 'Python / Advanced — Level 1', 'Python / Жоғары — деңгей 1',
  'Напишите функцию fibonacci(n), возвращающую n-ое число Фибоначчи (0-ое = 0, 1-ое = 1).', 'Write a function fibonacci(n) returning the n-th Fibonacci number (0-th = 0, 1-st = 1).', 'n-ші Фибоначчи санын қайтаратын fibonacci(n) функциясын жазыңыз.',
  'def fibonacci(n):
    pass
', '{"function": "fibonacci", "language": "python", "cases": [{"args": [0], "expected": 0}, {"args": [6], "expected": 8}]}'::jsonb, ARRAY['рекурсия', 'цикл', 'алгоритм']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'python'), (SELECT id FROM difficulties WHERE code = 'hard'), 2,
  'Python / Продвинутый — уровень 2', 'Python / Advanced — Level 2', 'Python / Жоғары — деңгей 2',
  'Напишите функцию unique_elements(lst), возвращающую новый массив только с уникальными элементами.', 'Write a function unique_elements(lst) returning a new array with only unique elements.', 'Тек бірегей элементтері бар жаңа массивті қайтаратын unique_elements(lst) функциясын жазыңыз.',
  'def unique_elements(lst):
    pass
', '{"function": "unique_elements", "language": "python", "cases": [{"args": [[1, 2, 2, 3]], "expected": [1, 2, 3]}, {"args": [[1, 1, 1]], "expected": [1]}]}'::jsonb, ARRAY['массив', 'set', 'хэш']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'python'), (SELECT id FROM difficulties WHERE code = 'hard'), 3,
  'Python / Продвинутый — уровень 3', 'Python / Advanced — Level 3', 'Python / Жоғары — деңгей 3',
  'Напишите функцию merge_sorted(a, b), сливающую два отсортированных массива в один отсортированный.', 'Write a function merge_sorted(a, b) merging two sorted arrays into one sorted array.', 'Екі сұрыпталған массивті бір сұрыпталған массивке біріктіретін merge_sorted(a, b) функциясын жазыңыз.',
  'def merge_sorted(a, b):
    pass
', '{"function": "merge_sorted", "language": "python", "cases": [{"args": [[1, 3], [2, 4]], "expected": [1, 2, 3, 4]}]}'::jsonb, ARRAY['массив', 'сортировка', 'алгоритм']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'python'), (SELECT id FROM difficulties WHERE code = 'hard'), 4,
  'Python / Продвинутый — уровень 4', 'Python / Advanced — Level 4', 'Python / Жоғары — деңгей 4',
  'Напишите функцию bubble_sort(lst), сортирующую массив пузырьком.', 'Write a function bubble_sort(lst) that sorts an array using bubble sort.', 'Массивті көпіршік әдісімен сұрыптайтын bubble_sort(lst) функциясын жазыңыз.',
  'def bubble_sort(lst):
    pass
', '{"function": "bubble_sort", "language": "python", "cases": [{"args": [[3, 1, 2]], "expected": [1, 2, 3]}]}'::jsonb, ARRAY['массив', 'сортировка', 'вложенный цикл']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'python'), (SELECT id FROM difficulties WHERE code = 'hard'), 5,
  'Python / Продвинутый — уровень 5', 'Python / Advanced — Level 5', 'Python / Жоғары — деңгей 5',
  'Напишите функцию matrix_sum(matrix), возвращающую сумму всех элементов двумерного массива.', 'Write a function matrix_sum(matrix) returning the sum of all elements in a 2D array.', 'Екі өлшемді массивтің барлық элементтерінің қосындысын қайтаратын matrix_sum(matrix) функциясын жазыңыз.',
  'def matrix_sum(matrix):
    pass
', '{"function": "matrix_sum", "language": "python", "cases": [{"args": [[[1, 2], [3, 4]]], "expected": 10}, {"args": [[[]]], "expected": 0}]}'::jsonb, ARRAY['массив', 'матрица', 'вложенный цикл']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'csharp'), (SELECT id FROM difficulties WHERE code = 'easy'), 1,
  'C# / Начальный — уровень 1', 'C# / Beginner — Level 1', 'C# / Бастапқы — деңгей 1',
  'Напишите функцию sum_two(a, b), которая возвращает сумму двух чисел.', 'Write a function sum_two(a, b) that returns the sum of two numbers.', 'Екі санның қосындысын қайтаратын sum_two(a, b) функциясын жазыңыз.',
  'public int SumTwo(int a, int b) {
    return 0;
}
', '{"function": "SumTwo", "language": "csharp", "cases": [{"args": [1, 2], "expected": 3}, {"args": [-1, 5], "expected": 4}]}'::jsonb, ARRAY['переменная', 'функция', 'return']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'csharp'), (SELECT id FROM difficulties WHERE code = 'easy'), 2,
  'C# / Начальный — уровень 2', 'C# / Beginner — Level 2', 'C# / Бастапқы — деңгей 2',
  'Напишите функцию is_even(n), которая возвращает true, если число чётное, и false в противном случае.', 'Write a function is_even(n) that returns true if the number is even, and false otherwise.', 'Сан жұп болса true, әйтпесе false қайтаратын is_even(n) функциясын жазыңыз.',
  'public bool IsEven(int n) {
    return false;
}
', '{"function": "IsEven", "language": "csharp", "cases": [{"args": [4], "expected": true}, {"args": [7], "expected": false}]}'::jsonb, ARRAY['условие', 'оператор', 'return']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'csharp'), (SELECT id FROM difficulties WHERE code = 'easy'), 3,
  'C# / Начальный — уровень 3', 'C# / Beginner — Level 3', 'C# / Бастапқы — деңгей 3',
  'Напишите функцию max_of_two(a, b), возвращающую наибольшее из двух чисел.', 'Write a function max_of_two(a, b) returning the largest of two numbers.', 'Екі санның үлкенін қайтаратын max_of_two(a, b) функциясын жазыңыз.',
  'public int MaxOfTwo(int a, int b) {
    return 0;
}
', '{"function": "MaxOfTwo", "language": "csharp", "cases": [{"args": [10, 20], "expected": 20}, {"args": [5, -5], "expected": 5}]}'::jsonb, ARRAY['условие', 'return']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'csharp'), (SELECT id FROM difficulties WHERE code = 'easy'), 4,
  'C# / Начальный — уровень 4', 'C# / Beginner — Level 4', 'C# / Бастапқы — деңгей 4',
  'Напишите функцию factorial(n) для вычисления факториала (n >= 0).', 'Write a function factorial(n) to calculate the factorial (n >= 0).', 'Факториалды есептейтін factorial(n) функциясын жазыңыз (n >= 0).',
  'public int Factorial(int n) {
    return 0;
}
', '{"function": "Factorial", "language": "csharp", "cases": [{"args": [0], "expected": 1}, {"args": [5], "expected": 120}]}'::jsonb, ARRAY['цикл', 'рекурсия']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'csharp'), (SELECT id FROM difficulties WHERE code = 'easy'), 5,
  'C# / Начальный — уровень 5', 'C# / Beginner — Level 5', 'C# / Бастапқы — деңгей 5',
  'Напишите функцию reverse_string(s), которая переворачивает строку.', 'Write a function reverse_string(s) that reverses a string.', 'Жолды кері айналдыратын reverse_string(s) функциясын жазыңыз.',
  'public string ReverseString(string s) {
    return "";
}
', '{"function": "ReverseString", "language": "csharp", "cases": [{"args": ["hello"], "expected": "olleh"}, {"args": [""], "expected": ""}]}'::jsonb, ARRAY['строка', 'цикл']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'csharp'), (SELECT id FROM difficulties WHERE code = 'medium'), 1,
  'C# / Средний — уровень 1', 'C# / Intermediate — Level 1', 'C# / Орташа — деңгей 1',
  'Напишите функцию sum_list(lst), которая возвращает сумму всех элементов списка/массива.', 'Write a function sum_list(lst) that returns the sum of all elements in a list/array.', 'Тізімнің/массивтің барлық элементтерінің қосындысын қайтаратын sum_list(lst) функциясын жазыңыз.',
  'public int SumList(int[] lst) {
    return 0;
}
', '{"function": "SumList", "language": "csharp", "cases": [{"args": [[1, 2, 3]], "expected": 6}, {"args": [[]], "expected": 0}]}'::jsonb, ARRAY['цикл', 'список', 'массив']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'csharp'), (SELECT id FROM difficulties WHERE code = 'medium'), 2,
  'C# / Средний — уровень 2', 'C# / Intermediate — Level 2', 'C# / Орташа — деңгей 2',
  'Напишите функцию count_vowels(s), возвращающую количество гласных букв (a, e, i, o, u) в строке без учета регистра.', 'Write a function count_vowels(s) returning the number of vowels (a, e, i, o, u) in a string case-insensitively.', 'Жолдағы дауысты дыбыстардың (a, e, i, o, u) санын регистрге қарамастан қайтаратын count_vowels(s) функциясын жазыңыз.',
  'public int CountVowels(string s) {
    return 0;
}
', '{"function": "CountVowels", "language": "csharp", "cases": [{"args": ["hello"], "expected": 2}, {"args": ["APPLE"], "expected": 2}]}'::jsonb, ARRAY['строка', 'цикл', 'условие']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'csharp'), (SELECT id FROM difficulties WHERE code = 'medium'), 3,
  'C# / Средний — уровень 3', 'C# / Intermediate — Level 3', 'C# / Орташа — деңгей 3',
  'Напишите функцию fizzbuzz(n), возвращающую ''FizzBuzz'' если n делится на 15, ''Fizz'' если на 3, ''Buzz'' если на 5, иначе строку n.', 'Write fizzbuzz(n) returning ''FizzBuzz'' if n is divisible by 15, ''Fizz'' if by 3, ''Buzz'' if by 5, else string of n.', 'Егер n 15-ке бөлінсе ''FizzBuzz'', 3-ке бөлінсе ''Fizz'', 5-ке бөлінсе ''Buzz'', әйтпесе n жолын қайтаратын fizzbuzz(n) функциясын жазыңыз.',
  'public string Fizzbuzz(int n) {
    return "";
}
', '{"function": "Fizzbuzz", "language": "csharp", "cases": [{"args": [15], "expected": "FizzBuzz"}, {"args": [3], "expected": "Fizz"}, {"args": [5], "expected": "Buzz"}, {"args": [7], "expected": "7"}]}'::jsonb, ARRAY['условие', 'оператор']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'csharp'), (SELECT id FROM difficulties WHERE code = 'medium'), 4,
  'C# / Средний — уровень 4', 'C# / Intermediate — Level 4', 'C# / Орташа — деңгей 4',
  'Напишите функцию is_palindrome(s), проверяющую, является ли строка палиндромом (читается одинаково слева направо и справа налево).', 'Write a function is_palindrome(s) checking if a string is a palindrome.', 'Жолдың палиндром екенін тексеретін is_palindrome(s) функциясын жазыңыз.',
  'public bool IsPalindrome(string s) {
    return false;
}
', '{"function": "IsPalindrome", "language": "csharp", "cases": [{"args": ["racecar"], "expected": true}, {"args": ["hello"], "expected": false}]}'::jsonb, ARRAY['строка', 'срез']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'csharp'), (SELECT id FROM difficulties WHERE code = 'medium'), 5,
  'C# / Средний — уровень 5', 'C# / Intermediate — Level 5', 'C# / Орташа — деңгей 5',
  'Напишите функцию binary_search(arr, target), реализующую бинарный поиск. Возвращает индекс элемента или -1.', 'Write a function binary_search(arr, target) implementing binary search. Returns index or -1.', 'Бинарлық іздеуді жүзеге асыратын binary_search(arr, target) функциясын жазыңыз. Индексті немесе -1 қайтарады.',
  'public int BinarySearch(int[] arr, int target) {
    return -1;
}
', '{"function": "BinarySearch", "language": "csharp", "cases": [{"args": [[1, 2, 3, 4, 5], 4], "expected": 3}, {"args": [[1, 2, 3, 4, 5], 6], "expected": -1}]}'::jsonb, ARRAY['алгоритм', 'массив', 'цикл']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'csharp'), (SELECT id FROM difficulties WHERE code = 'hard'), 1,
  'C# / Продвинутый — уровень 1', 'C# / Advanced — Level 1', 'C# / Жоғары — деңгей 1',
  'Напишите функцию fibonacci(n), возвращающую n-ое число Фибоначчи (0-ое = 0, 1-ое = 1).', 'Write a function fibonacci(n) returning the n-th Fibonacci number (0-th = 0, 1-st = 1).', 'n-ші Фибоначчи санын қайтаратын fibonacci(n) функциясын жазыңыз.',
  'public int Fibonacci(int n) {
    return 0;
}
', '{"function": "Fibonacci", "language": "csharp", "cases": [{"args": [0], "expected": 0}, {"args": [6], "expected": 8}]}'::jsonb, ARRAY['рекурсия', 'цикл', 'алгоритм']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'csharp'), (SELECT id FROM difficulties WHERE code = 'hard'), 2,
  'C# / Продвинутый — уровень 2', 'C# / Advanced — Level 2', 'C# / Жоғары — деңгей 2',
  'Напишите функцию unique_elements(lst), возвращающую новый массив только с уникальными элементами.', 'Write a function unique_elements(lst) returning a new array with only unique elements.', 'Тек бірегей элементтері бар жаңа массивті қайтаратын unique_elements(lst) функциясын жазыңыз.',
  'public int[] UniqueElements(int[] lst) {
    return new int[0];
}
', '{"function": "UniqueElements", "language": "csharp", "cases": [{"args": [[1, 2, 2, 3]], "expected": [1, 2, 3]}, {"args": [[1, 1, 1]], "expected": [1]}]}'::jsonb, ARRAY['массив', 'set', 'хэш']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'csharp'), (SELECT id FROM difficulties WHERE code = 'hard'), 3,
  'C# / Продвинутый — уровень 3', 'C# / Advanced — Level 3', 'C# / Жоғары — деңгей 3',
  'Напишите функцию merge_sorted(a, b), сливающую два отсортированных массива в один отсортированный.', 'Write a function merge_sorted(a, b) merging two sorted arrays into one sorted array.', 'Екі сұрыпталған массивті бір сұрыпталған массивке біріктіретін merge_sorted(a, b) функциясын жазыңыз.',
  'public int[] MergeSorted(int[] a, int[] b) {
    return new int[0];
}
', '{"function": "MergeSorted", "language": "csharp", "cases": [{"args": [[1, 3], [2, 4]], "expected": [1, 2, 3, 4]}]}'::jsonb, ARRAY['массив', 'сортировка', 'алгоритм']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'csharp'), (SELECT id FROM difficulties WHERE code = 'hard'), 4,
  'C# / Продвинутый — уровень 4', 'C# / Advanced — Level 4', 'C# / Жоғары — деңгей 4',
  'Напишите функцию bubble_sort(lst), сортирующую массив пузырьком.', 'Write a function bubble_sort(lst) that sorts an array using bubble sort.', 'Массивті көпіршік әдісімен сұрыптайтын bubble_sort(lst) функциясын жазыңыз.',
  'public int[] BubbleSort(int[] lst) {
    return lst;
}
', '{"function": "BubbleSort", "language": "csharp", "cases": [{"args": [[3, 1, 2]], "expected": [1, 2, 3]}]}'::jsonb, ARRAY['массив', 'сортировка', 'вложенный цикл']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'csharp'), (SELECT id FROM difficulties WHERE code = 'hard'), 5,
  'C# / Продвинутый — уровень 5', 'C# / Advanced — Level 5', 'C# / Жоғары — деңгей 5',
  'Напишите функцию matrix_sum(matrix), возвращающую сумму всех элементов двумерного массива.', 'Write a function matrix_sum(matrix) returning the sum of all elements in a 2D array.', 'Екі өлшемді массивтің барлық элементтерінің қосындысын қайтаратын matrix_sum(matrix) функциясын жазыңыз.',
  'public int MatrixSum(int[][] matrix) {
    return 0;
}
', '{"function": "MatrixSum", "language": "csharp", "cases": [{"args": [[[1, 2], [3, 4]]], "expected": 10}, {"args": [[[]]], "expected": 0}]}'::jsonb, ARRAY['массив', 'матрица', 'вложенный цикл']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'php'), (SELECT id FROM difficulties WHERE code = 'easy'), 1,
  'PHP / Начальный — уровень 1', 'PHP / Beginner — Level 1', 'PHP / Бастапқы — деңгей 1',
  'Напишите функцию sum_two(a, b), которая возвращает сумму двух чисел.', 'Write a function sum_two(a, b) that returns the sum of two numbers.', 'Екі санның қосындысын қайтаратын sum_two(a, b) функциясын жазыңыз.',
  'function sumTwo($a, $b) {
    
}
', '{"function": "sumTwo", "language": "php", "cases": [{"args": [1, 2], "expected": 3}, {"args": [-1, 5], "expected": 4}]}'::jsonb, ARRAY['переменная', 'функция', 'return']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'php'), (SELECT id FROM difficulties WHERE code = 'easy'), 2,
  'PHP / Начальный — уровень 2', 'PHP / Beginner — Level 2', 'PHP / Бастапқы — деңгей 2',
  'Напишите функцию is_even(n), которая возвращает true, если число чётное, и false в противном случае.', 'Write a function is_even(n) that returns true if the number is even, and false otherwise.', 'Сан жұп болса true, әйтпесе false қайтаратын is_even(n) функциясын жазыңыз.',
  'function isEven($n) {
    
}
', '{"function": "isEven", "language": "php", "cases": [{"args": [4], "expected": true}, {"args": [7], "expected": false}]}'::jsonb, ARRAY['условие', 'оператор', 'return']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'php'), (SELECT id FROM difficulties WHERE code = 'easy'), 3,
  'PHP / Начальный — уровень 3', 'PHP / Beginner — Level 3', 'PHP / Бастапқы — деңгей 3',
  'Напишите функцию max_of_two(a, b), возвращающую наибольшее из двух чисел.', 'Write a function max_of_two(a, b) returning the largest of two numbers.', 'Екі санның үлкенін қайтаратын max_of_two(a, b) функциясын жазыңыз.',
  'function maxOfTwo($a, $b) {
    
}
', '{"function": "maxOfTwo", "language": "php", "cases": [{"args": [10, 20], "expected": 20}, {"args": [5, -5], "expected": 5}]}'::jsonb, ARRAY['условие', 'return']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'php'), (SELECT id FROM difficulties WHERE code = 'easy'), 4,
  'PHP / Начальный — уровень 4', 'PHP / Beginner — Level 4', 'PHP / Бастапқы — деңгей 4',
  'Напишите функцию factorial(n) для вычисления факториала (n >= 0).', 'Write a function factorial(n) to calculate the factorial (n >= 0).', 'Факториалды есептейтін factorial(n) функциясын жазыңыз (n >= 0).',
  'function factorial($n) {
    
}
', '{"function": "factorial", "language": "php", "cases": [{"args": [0], "expected": 1}, {"args": [5], "expected": 120}]}'::jsonb, ARRAY['цикл', 'рекурсия']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'php'), (SELECT id FROM difficulties WHERE code = 'easy'), 5,
  'PHP / Начальный — уровень 5', 'PHP / Beginner — Level 5', 'PHP / Бастапқы — деңгей 5',
  'Напишите функцию reverse_string(s), которая переворачивает строку.', 'Write a function reverse_string(s) that reverses a string.', 'Жолды кері айналдыратын reverse_string(s) функциясын жазыңыз.',
  'function reverseString($s) {
    
}
', '{"function": "reverseString", "language": "php", "cases": [{"args": ["hello"], "expected": "olleh"}, {"args": [""], "expected": ""}]}'::jsonb, ARRAY['строка', 'цикл']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'php'), (SELECT id FROM difficulties WHERE code = 'medium'), 1,
  'PHP / Средний — уровень 1', 'PHP / Intermediate — Level 1', 'PHP / Орташа — деңгей 1',
  'Напишите функцию sum_list(lst), которая возвращает сумму всех элементов списка/массива.', 'Write a function sum_list(lst) that returns the sum of all elements in a list/array.', 'Тізімнің/массивтің барлық элементтерінің қосындысын қайтаратын sum_list(lst) функциясын жазыңыз.',
  'function sumList($lst) {
    
}
', '{"function": "sumList", "language": "php", "cases": [{"args": [[1, 2, 3]], "expected": 6}, {"args": [[]], "expected": 0}]}'::jsonb, ARRAY['цикл', 'список', 'массив']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'php'), (SELECT id FROM difficulties WHERE code = 'medium'), 2,
  'PHP / Средний — уровень 2', 'PHP / Intermediate — Level 2', 'PHP / Орташа — деңгей 2',
  'Напишите функцию count_vowels(s), возвращающую количество гласных букв (a, e, i, o, u) в строке без учета регистра.', 'Write a function count_vowels(s) returning the number of vowels (a, e, i, o, u) in a string case-insensitively.', 'Жолдағы дауысты дыбыстардың (a, e, i, o, u) санын регистрге қарамастан қайтаратын count_vowels(s) функциясын жазыңыз.',
  'function countVowels($s) {
    
}
', '{"function": "countVowels", "language": "php", "cases": [{"args": ["hello"], "expected": 2}, {"args": ["APPLE"], "expected": 2}]}'::jsonb, ARRAY['строка', 'цикл', 'условие']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'php'), (SELECT id FROM difficulties WHERE code = 'medium'), 3,
  'PHP / Средний — уровень 3', 'PHP / Intermediate — Level 3', 'PHP / Орташа — деңгей 3',
  'Напишите функцию fizzbuzz(n), возвращающую ''FizzBuzz'' если n делится на 15, ''Fizz'' если на 3, ''Buzz'' если на 5, иначе строку n.', 'Write fizzbuzz(n) returning ''FizzBuzz'' if n is divisible by 15, ''Fizz'' if by 3, ''Buzz'' if by 5, else string of n.', 'Егер n 15-ке бөлінсе ''FizzBuzz'', 3-ке бөлінсе ''Fizz'', 5-ке бөлінсе ''Buzz'', әйтпесе n жолын қайтаратын fizzbuzz(n) функциясын жазыңыз.',
  'function fizzbuzz($n) {
    
}
', '{"function": "fizzbuzz", "language": "php", "cases": [{"args": [15], "expected": "FizzBuzz"}, {"args": [3], "expected": "Fizz"}, {"args": [5], "expected": "Buzz"}, {"args": [7], "expected": "7"}]}'::jsonb, ARRAY['условие', 'оператор']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'php'), (SELECT id FROM difficulties WHERE code = 'medium'), 4,
  'PHP / Средний — уровень 4', 'PHP / Intermediate — Level 4', 'PHP / Орташа — деңгей 4',
  'Напишите функцию is_palindrome(s), проверяющую, является ли строка палиндромом (читается одинаково слева направо и справа налево).', 'Write a function is_palindrome(s) checking if a string is a palindrome.', 'Жолдың палиндром екенін тексеретін is_palindrome(s) функциясын жазыңыз.',
  'function isPalindrome($s) {
    
}
', '{"function": "isPalindrome", "language": "php", "cases": [{"args": ["racecar"], "expected": true}, {"args": ["hello"], "expected": false}]}'::jsonb, ARRAY['строка', 'срез']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'php'), (SELECT id FROM difficulties WHERE code = 'medium'), 5,
  'PHP / Средний — уровень 5', 'PHP / Intermediate — Level 5', 'PHP / Орташа — деңгей 5',
  'Напишите функцию binary_search(arr, target), реализующую бинарный поиск. Возвращает индекс элемента или -1.', 'Write a function binary_search(arr, target) implementing binary search. Returns index or -1.', 'Бинарлық іздеуді жүзеге асыратын binary_search(arr, target) функциясын жазыңыз. Индексті немесе -1 қайтарады.',
  'function binarySearch($arr, $target) {
    
}
', '{"function": "binarySearch", "language": "php", "cases": [{"args": [[1, 2, 3, 4, 5], 4], "expected": 3}, {"args": [[1, 2, 3, 4, 5], 6], "expected": -1}]}'::jsonb, ARRAY['алгоритм', 'массив', 'цикл']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'php'), (SELECT id FROM difficulties WHERE code = 'hard'), 1,
  'PHP / Продвинутый — уровень 1', 'PHP / Advanced — Level 1', 'PHP / Жоғары — деңгей 1',
  'Напишите функцию fibonacci(n), возвращающую n-ое число Фибоначчи (0-ое = 0, 1-ое = 1).', 'Write a function fibonacci(n) returning the n-th Fibonacci number (0-th = 0, 1-st = 1).', 'n-ші Фибоначчи санын қайтаратын fibonacci(n) функциясын жазыңыз.',
  'function fibonacci($n) {
    
}
', '{"function": "fibonacci", "language": "php", "cases": [{"args": [0], "expected": 0}, {"args": [6], "expected": 8}]}'::jsonb, ARRAY['рекурсия', 'цикл', 'алгоритм']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'php'), (SELECT id FROM difficulties WHERE code = 'hard'), 2,
  'PHP / Продвинутый — уровень 2', 'PHP / Advanced — Level 2', 'PHP / Жоғары — деңгей 2',
  'Напишите функцию unique_elements(lst), возвращающую новый массив только с уникальными элементами.', 'Write a function unique_elements(lst) returning a new array with only unique elements.', 'Тек бірегей элементтері бар жаңа массивті қайтаратын unique_elements(lst) функциясын жазыңыз.',
  'function uniqueElements($lst) {
    
}
', '{"function": "uniqueElements", "language": "php", "cases": [{"args": [[1, 2, 2, 3]], "expected": [1, 2, 3]}, {"args": [[1, 1, 1]], "expected": [1]}]}'::jsonb, ARRAY['массив', 'set', 'хэш']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'php'), (SELECT id FROM difficulties WHERE code = 'hard'), 3,
  'PHP / Продвинутый — уровень 3', 'PHP / Advanced — Level 3', 'PHP / Жоғары — деңгей 3',
  'Напишите функцию merge_sorted(a, b), сливающую два отсортированных массива в один отсортированный.', 'Write a function merge_sorted(a, b) merging two sorted arrays into one sorted array.', 'Екі сұрыпталған массивті бір сұрыпталған массивке біріктіретін merge_sorted(a, b) функциясын жазыңыз.',
  'function mergeSorted($a, $b) {
    
}
', '{"function": "mergeSorted", "language": "php", "cases": [{"args": [[1, 3], [2, 4]], "expected": [1, 2, 3, 4]}]}'::jsonb, ARRAY['массив', 'сортировка', 'алгоритм']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'php'), (SELECT id FROM difficulties WHERE code = 'hard'), 4,
  'PHP / Продвинутый — уровень 4', 'PHP / Advanced — Level 4', 'PHP / Жоғары — деңгей 4',
  'Напишите функцию bubble_sort(lst), сортирующую массив пузырьком.', 'Write a function bubble_sort(lst) that sorts an array using bubble sort.', 'Массивті көпіршік әдісімен сұрыптайтын bubble_sort(lst) функциясын жазыңыз.',
  'function bubbleSort($lst) {
    
}
', '{"function": "bubbleSort", "language": "php", "cases": [{"args": [[3, 1, 2]], "expected": [1, 2, 3]}]}'::jsonb, ARRAY['массив', 'сортировка', 'вложенный цикл']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'php'), (SELECT id FROM difficulties WHERE code = 'hard'), 5,
  'PHP / Продвинутый — уровень 5', 'PHP / Advanced — Level 5', 'PHP / Жоғары — деңгей 5',
  'Напишите функцию matrix_sum(matrix), возвращающую сумму всех элементов двумерного массива.', 'Write a function matrix_sum(matrix) returning the sum of all elements in a 2D array.', 'Екі өлшемді массивтің барлық элементтерінің қосындысын қайтаратын matrix_sum(matrix) функциясын жазыңыз.',
  'function matrixSum($matrix) {
    
}
', '{"function": "matrixSum", "language": "php", "cases": [{"args": [[[1, 2], [3, 4]]], "expected": 10}, {"args": [[[]]], "expected": 0}]}'::jsonb, ARRAY['массив', 'матрица', 'вложенный цикл']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'javascript'), (SELECT id FROM difficulties WHERE code = 'easy'), 1,
  'JavaScript / Начальный — уровень 1', 'JavaScript / Beginner — Level 1', 'JavaScript / Бастапқы — деңгей 1',
  'Напишите функцию sum_two(a, b), которая возвращает сумму двух чисел.', 'Write a function sum_two(a, b) that returns the sum of two numbers.', 'Екі санның қосындысын қайтаратын sum_two(a, b) функциясын жазыңыз.',
  'function sumTwo(a, b) {
    
}
', '{"function": "sumTwo", "language": "javascript", "cases": [{"args": [1, 2], "expected": 3}, {"args": [-1, 5], "expected": 4}]}'::jsonb, ARRAY['переменная', 'функция', 'return']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'javascript'), (SELECT id FROM difficulties WHERE code = 'easy'), 2,
  'JavaScript / Начальный — уровень 2', 'JavaScript / Beginner — Level 2', 'JavaScript / Бастапқы — деңгей 2',
  'Напишите функцию is_even(n), которая возвращает true, если число чётное, и false в противном случае.', 'Write a function is_even(n) that returns true if the number is even, and false otherwise.', 'Сан жұп болса true, әйтпесе false қайтаратын is_even(n) функциясын жазыңыз.',
  'function isEven(n) {
    
}
', '{"function": "isEven", "language": "javascript", "cases": [{"args": [4], "expected": true}, {"args": [7], "expected": false}]}'::jsonb, ARRAY['условие', 'оператор', 'return']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'javascript'), (SELECT id FROM difficulties WHERE code = 'easy'), 3,
  'JavaScript / Начальный — уровень 3', 'JavaScript / Beginner — Level 3', 'JavaScript / Бастапқы — деңгей 3',
  'Напишите функцию max_of_two(a, b), возвращающую наибольшее из двух чисел.', 'Write a function max_of_two(a, b) returning the largest of two numbers.', 'Екі санның үлкенін қайтаратын max_of_two(a, b) функциясын жазыңыз.',
  'function maxOfTwo(a, b) {
    
}
', '{"function": "maxOfTwo", "language": "javascript", "cases": [{"args": [10, 20], "expected": 20}, {"args": [5, -5], "expected": 5}]}'::jsonb, ARRAY['условие', 'return']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'javascript'), (SELECT id FROM difficulties WHERE code = 'easy'), 4,
  'JavaScript / Начальный — уровень 4', 'JavaScript / Beginner — Level 4', 'JavaScript / Бастапқы — деңгей 4',
  'Напишите функцию factorial(n) для вычисления факториала (n >= 0).', 'Write a function factorial(n) to calculate the factorial (n >= 0).', 'Факториалды есептейтін factorial(n) функциясын жазыңыз (n >= 0).',
  'function factorial(n) {
    
}
', '{"function": "factorial", "language": "javascript", "cases": [{"args": [0], "expected": 1}, {"args": [5], "expected": 120}]}'::jsonb, ARRAY['цикл', 'рекурсия']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'javascript'), (SELECT id FROM difficulties WHERE code = 'easy'), 5,
  'JavaScript / Начальный — уровень 5', 'JavaScript / Beginner — Level 5', 'JavaScript / Бастапқы — деңгей 5',
  'Напишите функцию reverse_string(s), которая переворачивает строку.', 'Write a function reverse_string(s) that reverses a string.', 'Жолды кері айналдыратын reverse_string(s) функциясын жазыңыз.',
  'function reverseString(s) {
    
}
', '{"function": "reverseString", "language": "javascript", "cases": [{"args": ["hello"], "expected": "olleh"}, {"args": [""], "expected": ""}]}'::jsonb, ARRAY['строка', 'цикл']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'javascript'), (SELECT id FROM difficulties WHERE code = 'medium'), 1,
  'JavaScript / Средний — уровень 1', 'JavaScript / Intermediate — Level 1', 'JavaScript / Орташа — деңгей 1',
  'Напишите функцию sum_list(lst), которая возвращает сумму всех элементов списка/массива.', 'Write a function sum_list(lst) that returns the sum of all elements in a list/array.', 'Тізімнің/массивтің барлық элементтерінің қосындысын қайтаратын sum_list(lst) функциясын жазыңыз.',
  'function sumList(lst) {
    
}
', '{"function": "sumList", "language": "javascript", "cases": [{"args": [[1, 2, 3]], "expected": 6}, {"args": [[]], "expected": 0}]}'::jsonb, ARRAY['цикл', 'список', 'массив']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'javascript'), (SELECT id FROM difficulties WHERE code = 'medium'), 2,
  'JavaScript / Средний — уровень 2', 'JavaScript / Intermediate — Level 2', 'JavaScript / Орташа — деңгей 2',
  'Напишите функцию count_vowels(s), возвращающую количество гласных букв (a, e, i, o, u) в строке без учета регистра.', 'Write a function count_vowels(s) returning the number of vowels (a, e, i, o, u) in a string case-insensitively.', 'Жолдағы дауысты дыбыстардың (a, e, i, o, u) санын регистрге қарамастан қайтаратын count_vowels(s) функциясын жазыңыз.',
  'function countVowels(s) {
    
}
', '{"function": "countVowels", "language": "javascript", "cases": [{"args": ["hello"], "expected": 2}, {"args": ["APPLE"], "expected": 2}]}'::jsonb, ARRAY['строка', 'цикл', 'условие']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'javascript'), (SELECT id FROM difficulties WHERE code = 'medium'), 3,
  'JavaScript / Средний — уровень 3', 'JavaScript / Intermediate — Level 3', 'JavaScript / Орташа — деңгей 3',
  'Напишите функцию fizzbuzz(n), возвращающую ''FizzBuzz'' если n делится на 15, ''Fizz'' если на 3, ''Buzz'' если на 5, иначе строку n.', 'Write fizzbuzz(n) returning ''FizzBuzz'' if n is divisible by 15, ''Fizz'' if by 3, ''Buzz'' if by 5, else string of n.', 'Егер n 15-ке бөлінсе ''FizzBuzz'', 3-ке бөлінсе ''Fizz'', 5-ке бөлінсе ''Buzz'', әйтпесе n жолын қайтаратын fizzbuzz(n) функциясын жазыңыз.',
  'function fizzbuzz(n) {
    
}
', '{"function": "fizzbuzz", "language": "javascript", "cases": [{"args": [15], "expected": "FizzBuzz"}, {"args": [3], "expected": "Fizz"}, {"args": [5], "expected": "Buzz"}, {"args": [7], "expected": "7"}]}'::jsonb, ARRAY['условие', 'оператор']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'javascript'), (SELECT id FROM difficulties WHERE code = 'medium'), 4,
  'JavaScript / Средний — уровень 4', 'JavaScript / Intermediate — Level 4', 'JavaScript / Орташа — деңгей 4',
  'Напишите функцию is_palindrome(s), проверяющую, является ли строка палиндромом (читается одинаково слева направо и справа налево).', 'Write a function is_palindrome(s) checking if a string is a palindrome.', 'Жолдың палиндром екенін тексеретін is_palindrome(s) функциясын жазыңыз.',
  'function isPalindrome(s) {
    
}
', '{"function": "isPalindrome", "language": "javascript", "cases": [{"args": ["racecar"], "expected": true}, {"args": ["hello"], "expected": false}]}'::jsonb, ARRAY['строка', 'срез']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'javascript'), (SELECT id FROM difficulties WHERE code = 'medium'), 5,
  'JavaScript / Средний — уровень 5', 'JavaScript / Intermediate — Level 5', 'JavaScript / Орташа — деңгей 5',
  'Напишите функцию binary_search(arr, target), реализующую бинарный поиск. Возвращает индекс элемента или -1.', 'Write a function binary_search(arr, target) implementing binary search. Returns index or -1.', 'Бинарлық іздеуді жүзеге асыратын binary_search(arr, target) функциясын жазыңыз. Индексті немесе -1 қайтарады.',
  'function binarySearch(arr, target) {
    
}
', '{"function": "binarySearch", "language": "javascript", "cases": [{"args": [[1, 2, 3, 4, 5], 4], "expected": 3}, {"args": [[1, 2, 3, 4, 5], 6], "expected": -1}]}'::jsonb, ARRAY['алгоритм', 'массив', 'цикл']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'javascript'), (SELECT id FROM difficulties WHERE code = 'hard'), 1,
  'JavaScript / Продвинутый — уровень 1', 'JavaScript / Advanced — Level 1', 'JavaScript / Жоғары — деңгей 1',
  'Напишите функцию fibonacci(n), возвращающую n-ое число Фибоначчи (0-ое = 0, 1-ое = 1).', 'Write a function fibonacci(n) returning the n-th Fibonacci number (0-th = 0, 1-st = 1).', 'n-ші Фибоначчи санын қайтаратын fibonacci(n) функциясын жазыңыз.',
  'function fibonacci(n) {
    
}
', '{"function": "fibonacci", "language": "javascript", "cases": [{"args": [0], "expected": 0}, {"args": [6], "expected": 8}]}'::jsonb, ARRAY['рекурсия', 'цикл', 'алгоритм']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'javascript'), (SELECT id FROM difficulties WHERE code = 'hard'), 2,
  'JavaScript / Продвинутый — уровень 2', 'JavaScript / Advanced — Level 2', 'JavaScript / Жоғары — деңгей 2',
  'Напишите функцию unique_elements(lst), возвращающую новый массив только с уникальными элементами.', 'Write a function unique_elements(lst) returning a new array with only unique elements.', 'Тек бірегей элементтері бар жаңа массивті қайтаратын unique_elements(lst) функциясын жазыңыз.',
  'function uniqueElements(lst) {
    
}
', '{"function": "uniqueElements", "language": "javascript", "cases": [{"args": [[1, 2, 2, 3]], "expected": [1, 2, 3]}, {"args": [[1, 1, 1]], "expected": [1]}]}'::jsonb, ARRAY['массив', 'set', 'хэш']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'javascript'), (SELECT id FROM difficulties WHERE code = 'hard'), 3,
  'JavaScript / Продвинутый — уровень 3', 'JavaScript / Advanced — Level 3', 'JavaScript / Жоғары — деңгей 3',
  'Напишите функцию merge_sorted(a, b), сливающую два отсортированных массива в один отсортированный.', 'Write a function merge_sorted(a, b) merging two sorted arrays into one sorted array.', 'Екі сұрыпталған массивті бір сұрыпталған массивке біріктіретін merge_sorted(a, b) функциясын жазыңыз.',
  'function mergeSorted(a, b) {
    
}
', '{"function": "mergeSorted", "language": "javascript", "cases": [{"args": [[1, 3], [2, 4]], "expected": [1, 2, 3, 4]}]}'::jsonb, ARRAY['массив', 'сортировка', 'алгоритм']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'javascript'), (SELECT id FROM difficulties WHERE code = 'hard'), 4,
  'JavaScript / Продвинутый — уровень 4', 'JavaScript / Advanced — Level 4', 'JavaScript / Жоғары — деңгей 4',
  'Напишите функцию bubble_sort(lst), сортирующую массив пузырьком.', 'Write a function bubble_sort(lst) that sorts an array using bubble sort.', 'Массивті көпіршік әдісімен сұрыптайтын bubble_sort(lst) функциясын жазыңыз.',
  'function bubbleSort(lst) {
    
}
', '{"function": "bubbleSort", "language": "javascript", "cases": [{"args": [[3, 1, 2]], "expected": [1, 2, 3]}]}'::jsonb, ARRAY['массив', 'сортировка', 'вложенный цикл']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'javascript'), (SELECT id FROM difficulties WHERE code = 'hard'), 5,
  'JavaScript / Продвинутый — уровень 5', 'JavaScript / Advanced — Level 5', 'JavaScript / Жоғары — деңгей 5',
  'Напишите функцию matrix_sum(matrix), возвращающую сумму всех элементов двумерного массива.', 'Write a function matrix_sum(matrix) returning the sum of all elements in a 2D array.', 'Екі өлшемді массивтің барлық элементтерінің қосындысын қайтаратын matrix_sum(matrix) функциясын жазыңыз.',
  'function matrixSum(matrix) {
    
}
', '{"function": "matrixSum", "language": "javascript", "cases": [{"args": [[[1, 2], [3, 4]]], "expected": 10}, {"args": [[[]]], "expected": 0}]}'::jsonb, ARRAY['массив', 'матрица', 'вложенный цикл']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'java'), (SELECT id FROM difficulties WHERE code = 'easy'), 1,
  'Java / Начальный — уровень 1', 'Java / Beginner — Level 1', 'Java / Бастапқы — деңгей 1',
  'Напишите функцию sum_two(a, b), которая возвращает сумму двух чисел.', 'Write a function sum_two(a, b) that returns the sum of two numbers.', 'Екі санның қосындысын қайтаратын sum_two(a, b) функциясын жазыңыз.',
  'public static int sumTwo(int a, int b) {
    return 0;
}
', '{"function": "sumTwo", "language": "java", "cases": [{"args": [1, 2], "expected": 3}, {"args": [-1, 5], "expected": 4}]}'::jsonb, ARRAY['переменная', 'функция', 'return']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'java'), (SELECT id FROM difficulties WHERE code = 'easy'), 2,
  'Java / Начальный — уровень 2', 'Java / Beginner — Level 2', 'Java / Бастапқы — деңгей 2',
  'Напишите функцию is_even(n), которая возвращает true, если число чётное, и false в противном случае.', 'Write a function is_even(n) that returns true if the number is even, and false otherwise.', 'Сан жұп болса true, әйтпесе false қайтаратын is_even(n) функциясын жазыңыз.',
  'public static boolean isEven(int n) {
    return false;
}
', '{"function": "isEven", "language": "java", "cases": [{"args": [4], "expected": true}, {"args": [7], "expected": false}]}'::jsonb, ARRAY['условие', 'оператор', 'return']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'java'), (SELECT id FROM difficulties WHERE code = 'easy'), 3,
  'Java / Начальный — уровень 3', 'Java / Beginner — Level 3', 'Java / Бастапқы — деңгей 3',
  'Напишите функцию max_of_two(a, b), возвращающую наибольшее из двух чисел.', 'Write a function max_of_two(a, b) returning the largest of two numbers.', 'Екі санның үлкенін қайтаратын max_of_two(a, b) функциясын жазыңыз.',
  'public static int maxOfTwo(int a, int b) {
    return 0;
}
', '{"function": "maxOfTwo", "language": "java", "cases": [{"args": [10, 20], "expected": 20}, {"args": [5, -5], "expected": 5}]}'::jsonb, ARRAY['условие', 'return']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'java'), (SELECT id FROM difficulties WHERE code = 'easy'), 4,
  'Java / Начальный — уровень 4', 'Java / Beginner — Level 4', 'Java / Бастапқы — деңгей 4',
  'Напишите функцию factorial(n) для вычисления факториала (n >= 0).', 'Write a function factorial(n) to calculate the factorial (n >= 0).', 'Факториалды есептейтін factorial(n) функциясын жазыңыз (n >= 0).',
  'public static int factorial(int n) {
    return 0;
}
', '{"function": "factorial", "language": "java", "cases": [{"args": [0], "expected": 1}, {"args": [5], "expected": 120}]}'::jsonb, ARRAY['цикл', 'рекурсия']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'java'), (SELECT id FROM difficulties WHERE code = 'easy'), 5,
  'Java / Начальный — уровень 5', 'Java / Beginner — Level 5', 'Java / Бастапқы — деңгей 5',
  'Напишите функцию reverse_string(s), которая переворачивает строку.', 'Write a function reverse_string(s) that reverses a string.', 'Жолды кері айналдыратын reverse_string(s) функциясын жазыңыз.',
  'public static String reverseString(String s) {
    return "";
}
', '{"function": "reverseString", "language": "java", "cases": [{"args": ["hello"], "expected": "olleh"}, {"args": [""], "expected": ""}]}'::jsonb, ARRAY['строка', 'цикл']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'java'), (SELECT id FROM difficulties WHERE code = 'medium'), 1,
  'Java / Средний — уровень 1', 'Java / Intermediate — Level 1', 'Java / Орташа — деңгей 1',
  'Напишите функцию sum_list(lst), которая возвращает сумму всех элементов списка/массива.', 'Write a function sum_list(lst) that returns the sum of all elements in a list/array.', 'Тізімнің/массивтің барлық элементтерінің қосындысын қайтаратын sum_list(lst) функциясын жазыңыз.',
  'public static int sumList(int[] lst) {
    return 0;
}
', '{"function": "sumList", "language": "java", "cases": [{"args": [[1, 2, 3]], "expected": 6}, {"args": [[]], "expected": 0}]}'::jsonb, ARRAY['цикл', 'список', 'массив']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'java'), (SELECT id FROM difficulties WHERE code = 'medium'), 2,
  'Java / Средний — уровень 2', 'Java / Intermediate — Level 2', 'Java / Орташа — деңгей 2',
  'Напишите функцию count_vowels(s), возвращающую количество гласных букв (a, e, i, o, u) в строке без учета регистра.', 'Write a function count_vowels(s) returning the number of vowels (a, e, i, o, u) in a string case-insensitively.', 'Жолдағы дауысты дыбыстардың (a, e, i, o, u) санын регистрге қарамастан қайтаратын count_vowels(s) функциясын жазыңыз.',
  'public static int countVowels(String s) {
    return 0;
}
', '{"function": "countVowels", "language": "java", "cases": [{"args": ["hello"], "expected": 2}, {"args": ["APPLE"], "expected": 2}]}'::jsonb, ARRAY['строка', 'цикл', 'условие']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'java'), (SELECT id FROM difficulties WHERE code = 'medium'), 3,
  'Java / Средний — уровень 3', 'Java / Intermediate — Level 3', 'Java / Орташа — деңгей 3',
  'Напишите функцию fizzbuzz(n), возвращающую ''FizzBuzz'' если n делится на 15, ''Fizz'' если на 3, ''Buzz'' если на 5, иначе строку n.', 'Write fizzbuzz(n) returning ''FizzBuzz'' if n is divisible by 15, ''Fizz'' if by 3, ''Buzz'' if by 5, else string of n.', 'Егер n 15-ке бөлінсе ''FizzBuzz'', 3-ке бөлінсе ''Fizz'', 5-ке бөлінсе ''Buzz'', әйтпесе n жолын қайтаратын fizzbuzz(n) функциясын жазыңыз.',
  'public static String fizzbuzz(int n) {
    return "";
}
', '{"function": "fizzbuzz", "language": "java", "cases": [{"args": [15], "expected": "FizzBuzz"}, {"args": [3], "expected": "Fizz"}, {"args": [5], "expected": "Buzz"}, {"args": [7], "expected": "7"}]}'::jsonb, ARRAY['условие', 'оператор']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'java'), (SELECT id FROM difficulties WHERE code = 'medium'), 4,
  'Java / Средний — уровень 4', 'Java / Intermediate — Level 4', 'Java / Орташа — деңгей 4',
  'Напишите функцию is_palindrome(s), проверяющую, является ли строка палиндромом (читается одинаково слева направо и справа налево).', 'Write a function is_palindrome(s) checking if a string is a palindrome.', 'Жолдың палиндром екенін тексеретін is_palindrome(s) функциясын жазыңыз.',
  'public static boolean isPalindrome(String s) {
    return false;
}
', '{"function": "isPalindrome", "language": "java", "cases": [{"args": ["racecar"], "expected": true}, {"args": ["hello"], "expected": false}]}'::jsonb, ARRAY['строка', 'срез']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'java'), (SELECT id FROM difficulties WHERE code = 'medium'), 5,
  'Java / Средний — уровень 5', 'Java / Intermediate — Level 5', 'Java / Орташа — деңгей 5',
  'Напишите функцию binary_search(arr, target), реализующую бинарный поиск. Возвращает индекс элемента или -1.', 'Write a function binary_search(arr, target) implementing binary search. Returns index or -1.', 'Бинарлық іздеуді жүзеге асыратын binary_search(arr, target) функциясын жазыңыз. Индексті немесе -1 қайтарады.',
  'public static int binarySearch(int[] arr, int target) {
    return -1;
}
', '{"function": "binarySearch", "language": "java", "cases": [{"args": [[1, 2, 3, 4, 5], 4], "expected": 3}, {"args": [[1, 2, 3, 4, 5], 6], "expected": -1}]}'::jsonb, ARRAY['алгоритм', 'массив', 'цикл']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'java'), (SELECT id FROM difficulties WHERE code = 'hard'), 1,
  'Java / Продвинутый — уровень 1', 'Java / Advanced — Level 1', 'Java / Жоғары — деңгей 1',
  'Напишите функцию fibonacci(n), возвращающую n-ое число Фибоначчи (0-ое = 0, 1-ое = 1).', 'Write a function fibonacci(n) returning the n-th Fibonacci number (0-th = 0, 1-st = 1).', 'n-ші Фибоначчи санын қайтаратын fibonacci(n) функциясын жазыңыз.',
  'public static int fibonacci(int n) {
    return 0;
}
', '{"function": "fibonacci", "language": "java", "cases": [{"args": [0], "expected": 0}, {"args": [6], "expected": 8}]}'::jsonb, ARRAY['рекурсия', 'цикл', 'алгоритм']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'java'), (SELECT id FROM difficulties WHERE code = 'hard'), 2,
  'Java / Продвинутый — уровень 2', 'Java / Advanced — Level 2', 'Java / Жоғары — деңгей 2',
  'Напишите функцию unique_elements(lst), возвращающую новый массив только с уникальными элементами.', 'Write a function unique_elements(lst) returning a new array with only unique elements.', 'Тек бірегей элементтері бар жаңа массивті қайтаратын unique_elements(lst) функциясын жазыңыз.',
  'public static int[] uniqueElements(int[] lst) {
    return new int[0];
}
', '{"function": "uniqueElements", "language": "java", "cases": [{"args": [[1, 2, 2, 3]], "expected": [1, 2, 3]}, {"args": [[1, 1, 1]], "expected": [1]}]}'::jsonb, ARRAY['массив', 'set', 'хэш']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'java'), (SELECT id FROM difficulties WHERE code = 'hard'), 3,
  'Java / Продвинутый — уровень 3', 'Java / Advanced — Level 3', 'Java / Жоғары — деңгей 3',
  'Напишите функцию merge_sorted(a, b), сливающую два отсортированных массива в один отсортированный.', 'Write a function merge_sorted(a, b) merging two sorted arrays into one sorted array.', 'Екі сұрыпталған массивті бір сұрыпталған массивке біріктіретін merge_sorted(a, b) функциясын жазыңыз.',
  'public static int[] mergeSorted(int[] a, int[] b) {
    return new int[0];
}
', '{"function": "mergeSorted", "language": "java", "cases": [{"args": [[1, 3], [2, 4]], "expected": [1, 2, 3, 4]}]}'::jsonb, ARRAY['массив', 'сортировка', 'алгоритм']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'java'), (SELECT id FROM difficulties WHERE code = 'hard'), 4,
  'Java / Продвинутый — уровень 4', 'Java / Advanced — Level 4', 'Java / Жоғары — деңгей 4',
  'Напишите функцию bubble_sort(lst), сортирующую массив пузырьком.', 'Write a function bubble_sort(lst) that sorts an array using bubble sort.', 'Массивті көпіршік әдісімен сұрыптайтын bubble_sort(lst) функциясын жазыңыз.',
  'public static int[] bubbleSort(int[] lst) {
    return lst;
}
', '{"function": "bubbleSort", "language": "java", "cases": [{"args": [[3, 1, 2]], "expected": [1, 2, 3]}]}'::jsonb, ARRAY['массив', 'сортировка', 'вложенный цикл']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  (SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = 'java'), (SELECT id FROM difficulties WHERE code = 'hard'), 5,
  'Java / Продвинутый — уровень 5', 'Java / Advanced — Level 5', 'Java / Жоғары — деңгей 5',
  'Напишите функцию matrix_sum(matrix), возвращающую сумму всех элементов двумерного массива.', 'Write a function matrix_sum(matrix) returning the sum of all elements in a 2D array.', 'Екі өлшемді массивтің барлық элементтерінің қосындысын қайтаратын matrix_sum(matrix) функциясын жазыңыз.',
  'public static int matrixSum(int[][] matrix) {
    return 0;
}
', '{"function": "matrixSum", "language": "java", "cases": [{"args": [[[1, 2], [3, 4]]], "expected": 10}, {"args": [[[]]], "expected": 0}]}'::jsonb, ARRAY['массив', 'матрица', 'вложенный цикл']::text[]
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;

-- =============================================
-- ЭКЗАМЕНЫ
-- =============================================


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
ON CONFLICT DO NOTHING;


INSERT INTO exam_difficulty_blocks (exam_id, track_id, difficulty_id)
SELECT e.id, tr.id, d.id
FROM tracks tr
JOIN languages l ON l.id = tr.language_id
CROSS JOIN difficulties d
JOIN exams e ON e.title_ru = l.name || ' — экзамен: ' || d.name_ru
WHERE e.exam_type = 'difficulty_block'
ON CONFLICT DO NOTHING;

DELETE FROM exam_questions;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 1, 'Экзамен: напишите функцию is_odd(n), которая возвращает true если число нечетное.', 'Exam: write a function is_odd(n) that returns true if the number is odd.', 'Емтихан: сан тақ болса true қайтаратын is_odd(n) функциясын жазыңыз.', 'def is_odd(n):
    pass
', '{"function": "is_odd", "language": "python", "cases": [{"args": [3], "expected": true}, {"args": [4], "expected": false}]}'::jsonb, (SELECT id FROM languages WHERE code = 'python')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'python' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'easy')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 2, 'Экзамен: функция mult_two(a, b), возвращающая произведение чисел.', 'Exam: mult_two(a, b) function returning the product of two numbers.', 'Емтихан: сандардың көбейтіндісін қайтаратын mult_two(a, b) функциясы.', 'def mult_two(a, b):
    pass
', '{"function": "mult_two", "language": "python", "cases": [{"args": [3, 4], "expected": 12}]}'::jsonb, (SELECT id FROM languages WHERE code = 'python')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'python' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'easy')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 3, 'Экзамен: вернуть ''positive'' если число > 0, иначе ''non-positive''. Функция check_pos(n).', 'Exam: return ''positive'' if n > 0, else ''non-positive''. check_pos(n).', 'Емтихан: n > 0 болса ''positive'', әйтпесе ''non-positive'' қайтару. check_pos(n).', 'def check_pos(n):
    pass
', '{"function": "check_pos", "language": "python", "cases": [{"args": [1], "expected": "positive"}, {"args": [0], "expected": "non-positive"}]}'::jsonb, (SELECT id FROM languages WHERE code = 'python')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'python' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'easy')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 1, 'Экзамен: функция min_in_list(lst), возвращающая минимальный элемент в массиве.', 'Exam: min_in_list(lst) returning the minimum element in an array.', 'Емтихан: массивтегі минималды элементті қайтаратын min_in_list(lst).', 'def min_in_list(lst):
    pass
', '{"function": "min_in_list", "language": "python", "cases": [{"args": [[3, 1, 2]], "expected": 1}]}'::jsonb, (SELECT id FROM languages WHERE code = 'python')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'python' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'medium')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 2, 'Экзамен: функция reverse_array(arr), переворачивающая массив.', 'Exam: reverse_array(arr) reversing an array.', 'Емтихан: массивті кері айналдыратын reverse_array(arr).', 'def reverse_array(arr):
    pass
', '{"function": "reverse_array", "language": "python", "cases": [{"args": [[1, 2, 3]], "expected": [3, 2, 1]}]}'::jsonb, (SELECT id FROM languages WHERE code = 'python')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'python' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'medium')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 3, 'Экзамен: функция replace_spaces(s), заменяющая пробелы на подчеркивания.', 'Exam: replace_spaces(s) replacing spaces with underscores.', 'Емтихан: бос орындарды астын сызумен ауыстыратын replace_spaces(s).', 'def replace_spaces(s):
    pass
', '{"function": "replace_spaces", "language": "python", "cases": [{"args": ["a b c"], "expected": "a_b_c"}]}'::jsonb, (SELECT id FROM languages WHERE code = 'python')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'python' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'medium')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 1, 'Экзамен: функция find_duplicates(lst), возвращающая элементы, которые встречаются более одного раза.', 'Exam: find_duplicates(lst) returning elements that appear more than once.', 'Емтихан: бірнеше рет кездесетін элементтерді қайтаратын find_duplicates(lst).', 'def find_duplicates(lst):
    pass
', '{"function": "find_duplicates", "language": "python", "cases": [{"args": [[1, 2, 2, 3, 1]], "expected": [1, 2]}]}'::jsonb, (SELECT id FROM languages WHERE code = 'python')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'python' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'hard')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 2, 'Экзамен: функция is_prime(n), возвращающая true если число простое.', 'Exam: is_prime(n) returning true if the number is prime.', 'Емтихан: сан жай болса true қайтаратын is_prime(n).', 'def is_prime(n):
    pass
', '{"function": "is_prime", "language": "python", "cases": [{"args": [7], "expected": true}, {"args": [10], "expected": false}]}'::jsonb, (SELECT id FROM languages WHERE code = 'python')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'python' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'hard')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 3, 'Экзамен: функция second_largest(lst), возвращающая второе по величине число.', 'Exam: second_largest(lst) returning the second largest number.', 'Емтихан: екінші ең үлкен санды қайтаратын second_largest(lst).', 'def second_largest(lst):
    pass
', '{"function": "second_largest", "language": "python", "cases": [{"args": [[1, 5, 3, 4]], "expected": 4}]}'::jsonb, (SELECT id FROM languages WHERE code = 'python')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'python' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'hard')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 1, 'Экзамен: напишите функцию is_odd(n), которая возвращает true если число нечетное.', 'Exam: write a function is_odd(n) that returns true if the number is odd.', 'Емтихан: сан тақ болса true қайтаратын is_odd(n) функциясын жазыңыз.', 'public bool IsOdd(int n) {
    return false;
}
', '{"function": "IsOdd", "language": "csharp", "cases": [{"args": [3], "expected": true}, {"args": [4], "expected": false}]}'::jsonb, (SELECT id FROM languages WHERE code = 'csharp')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'csharp' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'easy')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 2, 'Экзамен: функция mult_two(a, b), возвращающая произведение чисел.', 'Exam: mult_two(a, b) function returning the product of two numbers.', 'Емтихан: сандардың көбейтіндісін қайтаратын mult_two(a, b) функциясы.', 'public int MultTwo(int a, int b) {
    return 0;
}
', '{"function": "MultTwo", "language": "csharp", "cases": [{"args": [3, 4], "expected": 12}]}'::jsonb, (SELECT id FROM languages WHERE code = 'csharp')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'csharp' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'easy')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 3, 'Экзамен: вернуть ''positive'' если число > 0, иначе ''non-positive''. Функция check_pos(n).', 'Exam: return ''positive'' if n > 0, else ''non-positive''. check_pos(n).', 'Емтихан: n > 0 болса ''positive'', әйтпесе ''non-positive'' қайтару. check_pos(n).', 'public string CheckPos(int n) {
    return "";
}
', '{"function": "CheckPos", "language": "csharp", "cases": [{"args": [1], "expected": "positive"}, {"args": [0], "expected": "non-positive"}]}'::jsonb, (SELECT id FROM languages WHERE code = 'csharp')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'csharp' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'easy')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 1, 'Экзамен: функция min_in_list(lst), возвращающая минимальный элемент в массиве.', 'Exam: min_in_list(lst) returning the minimum element in an array.', 'Емтихан: массивтегі минималды элементті қайтаратын min_in_list(lst).', 'public int MinInList(int[] lst) {
    return 0;
}
', '{"function": "MinInList", "language": "csharp", "cases": [{"args": [[3, 1, 2]], "expected": 1}]}'::jsonb, (SELECT id FROM languages WHERE code = 'csharp')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'csharp' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'medium')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 2, 'Экзамен: функция reverse_array(arr), переворачивающая массив.', 'Exam: reverse_array(arr) reversing an array.', 'Емтихан: массивті кері айналдыратын reverse_array(arr).', 'public int[] ReverseArray(int[] arr) {
    return new int[0];
}
', '{"function": "ReverseArray", "language": "csharp", "cases": [{"args": [[1, 2, 3]], "expected": [3, 2, 1]}]}'::jsonb, (SELECT id FROM languages WHERE code = 'csharp')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'csharp' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'medium')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 3, 'Экзамен: функция replace_spaces(s), заменяющая пробелы на подчеркивания.', 'Exam: replace_spaces(s) replacing spaces with underscores.', 'Емтихан: бос орындарды астын сызумен ауыстыратын replace_spaces(s).', 'public string ReplaceSpaces(string s) {
    return "";
}
', '{"function": "ReplaceSpaces", "language": "csharp", "cases": [{"args": ["a b c"], "expected": "a_b_c"}]}'::jsonb, (SELECT id FROM languages WHERE code = 'csharp')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'csharp' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'medium')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 1, 'Экзамен: функция find_duplicates(lst), возвращающая элементы, которые встречаются более одного раза.', 'Exam: find_duplicates(lst) returning elements that appear more than once.', 'Емтихан: бірнеше рет кездесетін элементтерді қайтаратын find_duplicates(lst).', 'public int[] FindDuplicates(int[] lst) {
    return new int[0];
}
', '{"function": "FindDuplicates", "language": "csharp", "cases": [{"args": [[1, 2, 2, 3, 1]], "expected": [1, 2]}]}'::jsonb, (SELECT id FROM languages WHERE code = 'csharp')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'csharp' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'hard')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 2, 'Экзамен: функция is_prime(n), возвращающая true если число простое.', 'Exam: is_prime(n) returning true if the number is prime.', 'Емтихан: сан жай болса true қайтаратын is_prime(n).', 'public bool IsPrime(int n) {
    return false;
}
', '{"function": "IsPrime", "language": "csharp", "cases": [{"args": [7], "expected": true}, {"args": [10], "expected": false}]}'::jsonb, (SELECT id FROM languages WHERE code = 'csharp')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'csharp' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'hard')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 3, 'Экзамен: функция second_largest(lst), возвращающая второе по величине число.', 'Exam: second_largest(lst) returning the second largest number.', 'Емтихан: екінші ең үлкен санды қайтаратын second_largest(lst).', 'public int SecondLargest(int[] lst) {
    return 0;
}
', '{"function": "SecondLargest", "language": "csharp", "cases": [{"args": [[1, 5, 3, 4]], "expected": 4}]}'::jsonb, (SELECT id FROM languages WHERE code = 'csharp')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'csharp' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'hard')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 1, 'Экзамен: напишите функцию is_odd(n), которая возвращает true если число нечетное.', 'Exam: write a function is_odd(n) that returns true if the number is odd.', 'Емтихан: сан тақ болса true қайтаратын is_odd(n) функциясын жазыңыз.', 'function isOdd($n) {
    
}
', '{"function": "isOdd", "language": "php", "cases": [{"args": [3], "expected": true}, {"args": [4], "expected": false}]}'::jsonb, (SELECT id FROM languages WHERE code = 'php')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'php' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'easy')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 2, 'Экзамен: функция mult_two(a, b), возвращающая произведение чисел.', 'Exam: mult_two(a, b) function returning the product of two numbers.', 'Емтихан: сандардың көбейтіндісін қайтаратын mult_two(a, b) функциясы.', 'function multTwo($a, $b) {
    
}
', '{"function": "multTwo", "language": "php", "cases": [{"args": [3, 4], "expected": 12}]}'::jsonb, (SELECT id FROM languages WHERE code = 'php')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'php' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'easy')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 3, 'Экзамен: вернуть ''positive'' если число > 0, иначе ''non-positive''. Функция check_pos(n).', 'Exam: return ''positive'' if n > 0, else ''non-positive''. check_pos(n).', 'Емтихан: n > 0 болса ''positive'', әйтпесе ''non-positive'' қайтару. check_pos(n).', 'function checkPos($n) {
    
}
', '{"function": "checkPos", "language": "php", "cases": [{"args": [1], "expected": "positive"}, {"args": [0], "expected": "non-positive"}]}'::jsonb, (SELECT id FROM languages WHERE code = 'php')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'php' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'easy')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 1, 'Экзамен: функция min_in_list(lst), возвращающая минимальный элемент в массиве.', 'Exam: min_in_list(lst) returning the minimum element in an array.', 'Емтихан: массивтегі минималды элементті қайтаратын min_in_list(lst).', 'function minInList($lst) {
    
}
', '{"function": "minInList", "language": "php", "cases": [{"args": [[3, 1, 2]], "expected": 1}]}'::jsonb, (SELECT id FROM languages WHERE code = 'php')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'php' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'medium')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 2, 'Экзамен: функция reverse_array(arr), переворачивающая массив.', 'Exam: reverse_array(arr) reversing an array.', 'Емтихан: массивті кері айналдыратын reverse_array(arr).', 'function reverseArray($arr) {
    
}
', '{"function": "reverseArray", "language": "php", "cases": [{"args": [[1, 2, 3]], "expected": [3, 2, 1]}]}'::jsonb, (SELECT id FROM languages WHERE code = 'php')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'php' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'medium')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 3, 'Экзамен: функция replace_spaces(s), заменяющая пробелы на подчеркивания.', 'Exam: replace_spaces(s) replacing spaces with underscores.', 'Емтихан: бос орындарды астын сызумен ауыстыратын replace_spaces(s).', 'function replaceSpaces($s) {
    
}
', '{"function": "replaceSpaces", "language": "php", "cases": [{"args": ["a b c"], "expected": "a_b_c"}]}'::jsonb, (SELECT id FROM languages WHERE code = 'php')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'php' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'medium')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 1, 'Экзамен: функция find_duplicates(lst), возвращающая элементы, которые встречаются более одного раза.', 'Exam: find_duplicates(lst) returning elements that appear more than once.', 'Емтихан: бірнеше рет кездесетін элементтерді қайтаратын find_duplicates(lst).', 'function findDuplicates($lst) {
    
}
', '{"function": "findDuplicates", "language": "php", "cases": [{"args": [[1, 2, 2, 3, 1]], "expected": [1, 2]}]}'::jsonb, (SELECT id FROM languages WHERE code = 'php')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'php' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'hard')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 2, 'Экзамен: функция is_prime(n), возвращающая true если число простое.', 'Exam: is_prime(n) returning true if the number is prime.', 'Емтихан: сан жай болса true қайтаратын is_prime(n).', 'function isPrime($n) {
    
}
', '{"function": "isPrime", "language": "php", "cases": [{"args": [7], "expected": true}, {"args": [10], "expected": false}]}'::jsonb, (SELECT id FROM languages WHERE code = 'php')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'php' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'hard')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 3, 'Экзамен: функция second_largest(lst), возвращающая второе по величине число.', 'Exam: second_largest(lst) returning the second largest number.', 'Емтихан: екінші ең үлкен санды қайтаратын second_largest(lst).', 'function secondLargest($lst) {
    
}
', '{"function": "secondLargest", "language": "php", "cases": [{"args": [[1, 5, 3, 4]], "expected": 4}]}'::jsonb, (SELECT id FROM languages WHERE code = 'php')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'php' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'hard')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 1, 'Экзамен: напишите функцию is_odd(n), которая возвращает true если число нечетное.', 'Exam: write a function is_odd(n) that returns true if the number is odd.', 'Емтихан: сан тақ болса true қайтаратын is_odd(n) функциясын жазыңыз.', 'function isOdd(n) {
    
}
', '{"function": "isOdd", "language": "javascript", "cases": [{"args": [3], "expected": true}, {"args": [4], "expected": false}]}'::jsonb, (SELECT id FROM languages WHERE code = 'javascript')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'javascript' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'easy')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 2, 'Экзамен: функция mult_two(a, b), возвращающая произведение чисел.', 'Exam: mult_two(a, b) function returning the product of two numbers.', 'Емтихан: сандардың көбейтіндісін қайтаратын mult_two(a, b) функциясы.', 'function multTwo(a, b) {
    
}
', '{"function": "multTwo", "language": "javascript", "cases": [{"args": [3, 4], "expected": 12}]}'::jsonb, (SELECT id FROM languages WHERE code = 'javascript')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'javascript' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'easy')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 3, 'Экзамен: вернуть ''positive'' если число > 0, иначе ''non-positive''. Функция check_pos(n).', 'Exam: return ''positive'' if n > 0, else ''non-positive''. check_pos(n).', 'Емтихан: n > 0 болса ''positive'', әйтпесе ''non-positive'' қайтару. check_pos(n).', 'function checkPos(n) {
    
}
', '{"function": "checkPos", "language": "javascript", "cases": [{"args": [1], "expected": "positive"}, {"args": [0], "expected": "non-positive"}]}'::jsonb, (SELECT id FROM languages WHERE code = 'javascript')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'javascript' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'easy')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 1, 'Экзамен: функция min_in_list(lst), возвращающая минимальный элемент в массиве.', 'Exam: min_in_list(lst) returning the minimum element in an array.', 'Емтихан: массивтегі минималды элементті қайтаратын min_in_list(lst).', 'function minInList(lst) {
    
}
', '{"function": "minInList", "language": "javascript", "cases": [{"args": [[3, 1, 2]], "expected": 1}]}'::jsonb, (SELECT id FROM languages WHERE code = 'javascript')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'javascript' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'medium')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 2, 'Экзамен: функция reverse_array(arr), переворачивающая массив.', 'Exam: reverse_array(arr) reversing an array.', 'Емтихан: массивті кері айналдыратын reverse_array(arr).', 'function reverseArray(arr) {
    
}
', '{"function": "reverseArray", "language": "javascript", "cases": [{"args": [[1, 2, 3]], "expected": [3, 2, 1]}]}'::jsonb, (SELECT id FROM languages WHERE code = 'javascript')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'javascript' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'medium')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 3, 'Экзамен: функция replace_spaces(s), заменяющая пробелы на подчеркивания.', 'Exam: replace_spaces(s) replacing spaces with underscores.', 'Емтихан: бос орындарды астын сызумен ауыстыратын replace_spaces(s).', 'function replaceSpaces(s) {
    
}
', '{"function": "replaceSpaces", "language": "javascript", "cases": [{"args": ["a b c"], "expected": "a_b_c"}]}'::jsonb, (SELECT id FROM languages WHERE code = 'javascript')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'javascript' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'medium')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 1, 'Экзамен: функция find_duplicates(lst), возвращающая элементы, которые встречаются более одного раза.', 'Exam: find_duplicates(lst) returning elements that appear more than once.', 'Емтихан: бірнеше рет кездесетін элементтерді қайтаратын find_duplicates(lst).', 'function findDuplicates(lst) {
    
}
', '{"function": "findDuplicates", "language": "javascript", "cases": [{"args": [[1, 2, 2, 3, 1]], "expected": [1, 2]}]}'::jsonb, (SELECT id FROM languages WHERE code = 'javascript')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'javascript' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'hard')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 2, 'Экзамен: функция is_prime(n), возвращающая true если число простое.', 'Exam: is_prime(n) returning true if the number is prime.', 'Емтихан: сан жай болса true қайтаратын is_prime(n).', 'function isPrime(n) {
    
}
', '{"function": "isPrime", "language": "javascript", "cases": [{"args": [7], "expected": true}, {"args": [10], "expected": false}]}'::jsonb, (SELECT id FROM languages WHERE code = 'javascript')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'javascript' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'hard')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 3, 'Экзамен: функция second_largest(lst), возвращающая второе по величине число.', 'Exam: second_largest(lst) returning the second largest number.', 'Емтихан: екінші ең үлкен санды қайтаратын second_largest(lst).', 'function secondLargest(lst) {
    
}
', '{"function": "secondLargest", "language": "javascript", "cases": [{"args": [[1, 5, 3, 4]], "expected": 4}]}'::jsonb, (SELECT id FROM languages WHERE code = 'javascript')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'javascript' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'hard')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 1, 'Экзамен: напишите функцию is_odd(n), которая возвращает true если число нечетное.', 'Exam: write a function is_odd(n) that returns true if the number is odd.', 'Емтихан: сан тақ болса true қайтаратын is_odd(n) функциясын жазыңыз.', 'public static boolean isOdd(int n) {
    return false;
}
', '{"function": "isOdd", "language": "java", "cases": [{"args": [3], "expected": true}, {"args": [4], "expected": false}]}'::jsonb, (SELECT id FROM languages WHERE code = 'java')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'java' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'easy')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 2, 'Экзамен: функция mult_two(a, b), возвращающая произведение чисел.', 'Exam: mult_two(a, b) function returning the product of two numbers.', 'Емтихан: сандардың көбейтіндісін қайтаратын mult_two(a, b) функциясы.', 'public static int multTwo(int a, int b) {
    return 0;
}
', '{"function": "multTwo", "language": "java", "cases": [{"args": [3, 4], "expected": 12}]}'::jsonb, (SELECT id FROM languages WHERE code = 'java')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'java' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'easy')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 3, 'Экзамен: вернуть ''positive'' если число > 0, иначе ''non-positive''. Функция check_pos(n).', 'Exam: return ''positive'' if n > 0, else ''non-positive''. check_pos(n).', 'Емтихан: n > 0 болса ''positive'', әйтпесе ''non-positive'' қайтару. check_pos(n).', 'public static String checkPos(int n) {
    return "";
}
', '{"function": "checkPos", "language": "java", "cases": [{"args": [1], "expected": "positive"}, {"args": [0], "expected": "non-positive"}]}'::jsonb, (SELECT id FROM languages WHERE code = 'java')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'java' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'easy')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 1, 'Экзамен: функция min_in_list(lst), возвращающая минимальный элемент в массиве.', 'Exam: min_in_list(lst) returning the minimum element in an array.', 'Емтихан: массивтегі минималды элементті қайтаратын min_in_list(lst).', 'public static int minInList(int[] lst) {
    return 0;
}
', '{"function": "minInList", "language": "java", "cases": [{"args": [[3, 1, 2]], "expected": 1}]}'::jsonb, (SELECT id FROM languages WHERE code = 'java')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'java' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'medium')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 2, 'Экзамен: функция reverse_array(arr), переворачивающая массив.', 'Exam: reverse_array(arr) reversing an array.', 'Емтихан: массивті кері айналдыратын reverse_array(arr).', 'public static int[] reverseArray(int[] arr) {
    return new int[0];
}
', '{"function": "reverseArray", "language": "java", "cases": [{"args": [[1, 2, 3]], "expected": [3, 2, 1]}]}'::jsonb, (SELECT id FROM languages WHERE code = 'java')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'java' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'medium')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 3, 'Экзамен: функция replace_spaces(s), заменяющая пробелы на подчеркивания.', 'Exam: replace_spaces(s) replacing spaces with underscores.', 'Емтихан: бос орындарды астын сызумен ауыстыратын replace_spaces(s).', 'public static String replaceSpaces(String s) {
    return "";
}
', '{"function": "replaceSpaces", "language": "java", "cases": [{"args": ["a b c"], "expected": "a_b_c"}]}'::jsonb, (SELECT id FROM languages WHERE code = 'java')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'java' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'medium')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 1, 'Экзамен: функция find_duplicates(lst), возвращающая элементы, которые встречаются более одного раза.', 'Exam: find_duplicates(lst) returning elements that appear more than once.', 'Емтихан: бірнеше рет кездесетін элементтерді қайтаратын find_duplicates(lst).', 'public static int[] findDuplicates(int[] lst) {
    return new int[0];
}
', '{"function": "findDuplicates", "language": "java", "cases": [{"args": [[1, 2, 2, 3, 1]], "expected": [1, 2]}]}'::jsonb, (SELECT id FROM languages WHERE code = 'java')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'java' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'hard')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 2, 'Экзамен: функция is_prime(n), возвращающая true если число простое.', 'Exam: is_prime(n) returning true if the number is prime.', 'Емтихан: сан жай болса true қайтаратын is_prime(n).', 'public static boolean isPrime(int n) {
    return false;
}
', '{"function": "isPrime", "language": "java", "cases": [{"args": [7], "expected": true}, {"args": [10], "expected": false}]}'::jsonb, (SELECT id FROM languages WHERE code = 'java')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'java' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'hard')
ON CONFLICT DO NOTHING;
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, 3, 'Экзамен: функция second_largest(lst), возвращающая второе по величине число.', 'Exam: second_largest(lst) returning the second largest number.', 'Емтихан: екінші ең үлкен санды қайтаратын second_largest(lst).', 'public static int secondLargest(int[] lst) {
    return 0;
}
', '{"function": "secondLargest", "language": "java", "cases": [{"args": [[1, 5, 3, 4]], "expected": 4}]}'::jsonb, (SELECT id FROM languages WHERE code = 'java')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = 'java' AND edb.difficulty_id = (SELECT id FROM difficulties WHERE code = 'hard')
ON CONFLICT DO NOTHING;

-- Итоговый экзамен
INSERT INTO exams (exam_type, title_ru, title_en, title_kz, description_ru, description_en, description_kz, pass_percent, time_limit_min, max_attempts)
SELECT 'final'::exam_type, 'Итоговый экзамен', 'Final Exam', 'Қорытынды емтихан',
       'Обобщённая проверка по всем трекам', 'Comprehensive test across all tracks', 'Барлық тректер бойынша жалпылама тексеру',
       75, 60, 2
WHERE NOT EXISTS (SELECT 1 FROM exams WHERE exam_type = 'final');

-- Экзамен по выбранным трекам
INSERT INTO exams (exam_type, title_ru, title_en, title_kz, description_ru, description_en, description_kz, pass_percent, time_limit_min, max_attempts)
SELECT 'selected_tracks'::exam_type, 'Экзамен по выбранным курсам', 'Exam on Selected Courses', 'Таңдалған курстар бойынша емтихан',
       'Пользователь выбирает один или несколько треков', 'The user selects one or more tracks', 'Пайдаланушы бір немесе бірнеше тректерді таңдайды',
       70, 45, 3
WHERE NOT EXISTS (SELECT 1 FROM exams WHERE exam_type = 'selected_tracks');

