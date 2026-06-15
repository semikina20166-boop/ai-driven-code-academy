import asyncio
import os
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

# Read DATABASE_URL from .env manually if needed
database_url = "postgresql+asyncpg://postgres:postgres@localhost:5432/ai_academy"
if os.path.exists(".env"):
    with open(".env", "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("DATABASE_URL="):
                database_url = line.strip().split("DATABASE_URL=")[1].strip()

# Syllabus mapping
TOPICS = {
    "easy": {
        1: {
            "title_ru": "Введение в переменные и функции",
            "desc": "Знакомство с синтаксисом создания переменных, базовыми типами данных и объявлением функций, возвращающих значения.",
            "code_templates": {
                "python": "def sum_two(a, b):\n    # Переменные создаются динамически\n    result = a + b\n    return result",
                "javascript": "function sumTwo(a, b) {\n    // Переменные объявляются через let/const\n    const result = a + b;\n    return result;\n}",
                "csharp": "public int SumTwo(int a, int b) {\n    // Статическая типизация данных\n    int result = a + b;\n    return result;\n}",
                "java": "public static int sumTwo(int a, int b) {\n    // Переменная типа int внутри метода\n    int result = a + b;\n    return result;\n}",
                "php": "function sumTwo($a, $b) {\n    // Переменные начинаются со знака $\n    $result = $a + $b;\n    return $result;\n}"
            }
        },
        2: {
            "title_ru": "Условные операторы и логика",
            "desc": "Изучение ветвления кода с использованием конструкций if, else if / elif и логических операций для принятия решений.",
            "code_templates": {
                "python": "def check_number(num):\n    if num > 0:\n        return 'Положительное'\n    elif num < 0:\n        return 'Отрицательное'\n    else:\n        return 'Ноль'",
                "javascript": "function checkNumber(num) {\n    if (num > 0) {\n        return 'Положительное';\n    } else if (num < 0) {\n        return 'Отрицательное';\n    } else {\n        return 'Ноль';\n    }\n}",
                "csharp": "public string CheckNumber(int num) {\n    if (num > 0) {\n        return \"Положительное\";\n    }\n    else if (num < 0) {\n        return \"Отрицательное\";\n    }\n    else {\n        return \"Ноль\";\n    }\n}",
                "java": "public static String checkNumber(int num) {\n    if (num > 0) {\n        return \"Положительное\";\n    } else if (num < 0) {\n        return \"Отрицательное\";\n    } else {\n        return \"Ноль\";\n    }\n}",
                "php": "function checkNumber($num) {\n    if ($num > 0) {\n        return 'Положительное';\n    } elseif ($num < 0) {\n        return 'Отрицательное';\n    } else {\n        return 'Ноль';\n    }\n}"
            }
        },
        3: {
            "title_ru": "Циклы и итерации",
            "desc": "Управление повторяющимися действиями с помощью циклов for и while. Понятие счетчика и условия выхода из цикла.",
            "code_templates": {
                "python": "def sum_up_to(n):\n    total = 0\n    for i in range(1, n + 1):\n        total += i\n    return total",
                "javascript": "function sumUpTo(n) {\n    let total = 0;\n    for (let i = 1; i <= n; i++) {\n        total += i;\n    }\n    return total;\n}",
                "csharp": "public int SumUpTo(int n) {\n    int total = 0;\n    for (int i = 1; i <= n; i++) {\n        total += i;\n    }\n    return total;\n}",
                "java": "public static int sumUpTo(int n) {\n    int total = 0;\n    for (int i = 1; i <= n; i++) {\n        total += i;\n    }\n    return total;\n}",
                "php": "function sumUpTo($n) {\n    $total = 0;\n    for ($i = 1; $i <= $n; $i++) {\n        $total += $i;\n    }\n    return $total;\n}"
            }
        },
        4: {
            "title_ru": "Вложенные конструкции",
            "desc": "Комбинирование циклов внутри циклов, ветвления внутри итераторов. Решение задач двумерного обхода.",
            "code_templates": {
                "python": "def draw_rectangle(w, h):\n    result = ''\n    for i in range(h):\n        for j in range(w):\n            result += '*'\n        result += '\\n'\n    return result",
                "javascript": "function drawRectangle(w, h) {\n    let result = '';\n    for (let i = 0; i < h; i++) {\n        for (let j = 0; j < w; j++) {\n            result += '*';\n        }\n        result += '\\n';\n    }\n    return result;\n}",
                "csharp": "public string DrawRectangle(int w, int h) {\n    string result = \"\";\n    for (int i = 0; i < h; i++) {\n        for (int j = 0; j < w; j++) {\n            result += \"*\";\n        }\n        result += \"\\n\";\n    }\n    return result;\n}",
                "java": "public static String drawRectangle(int w, int h) {\n    StringBuilder result = new StringBuilder();\n    for (int i = 0; i < h; i++) {\n        for (int j = 0; j < w; j++) {\n            result.append(\"*\");\n        }\n        result.append(\"\\n\");\n    }\n    return result.toString();\n}",
                "php": "function drawRectangle($w, $h) {\n    $result = '';\n    for ($i = 0; $i < $h; $i++) {\n        for ($j = 0; $j < $w; $j++) {\n            $result .= '*';\n        }\n        $result .= \"\\n\";\n    }\n    return $result;\n}"
            }
        },
        5: {
            "title_ru": "Массивы и списки",
            "desc": "Работа со структурами линейных последовательностей. Добавление, удаление, обход элементов массива по индексу.",
            "code_templates": {
                "python": "def filter_even(lst):\n    # Использование генератора списков в Python\n    return [x for x in lst if x % 2 == 0]",
                "javascript": "function filterEven(arr) {\n    // Встроенный метод .filter()\n    return arr.filter(x => x % 2 === 0);\n}",
                "csharp": "public int[] FilterEven(int[] arr) {\n    // Использование System.Linq\n    return arr.Where(x => x % 2 == 0).ToArray();\n}",
                "java": "public static int[] filterEven(int[] arr) {\n    // Фильтрация через Java Stream API\n    return Arrays.stream(arr).filter(x -> x % 2 == 0).toArray();\n}",
                "php": "function filterEven($arr) {\n    // Фильтрация массива в PHP\n    return array_values(array_filter($arr, function($x) {\n        return $x % 2 == 0;\n    }));\n}"
            }
        }
    },
    "medium": {
        1: {
            "title_ru": "Словари и хэш-таблицы",
            "desc": "Хранение данных в формате Ключ-Значение. Быстрый поиск и обновление пар значений по уникальным ключам.",
            "code_templates": {
                "python": "def count_occurrences(lst):\n    counts = {}\n    for item in lst:\n        counts[item] = counts.get(item, 0) + 1\n    return counts",
                "javascript": "function countOccurrences(arr) {\n    const counts = {};\n    for (const item of arr) {\n        counts[item] = (counts[item] || 0) + 1;\n    }\n    return counts;\n}",
                "csharp": "public Dictionary<string, int> CountOccurrences(string[] arr) {\n    var counts = new Dictionary<string, int>();\n    foreach (var item in arr) {\n        if (counts.ContainsKey(item)) counts[item]++;\n        else counts[item] = 1;\n    }\n    return counts;\n}",
                "java": "public static HashMap<String, Integer> countOccurrences(String[] arr) {\n    HashMap<String, Integer> counts = new HashMap<>();\n    for (String item : arr) {\n        counts.put(item, counts.getOrDefault(item, 0) + 1);\n    }\n    return counts;\n}",
                "php": "function countOccurrences($arr) {\n    $counts = [];\n    foreach ($arr as $item) {\n        $counts[$item] = ($counts[$item] ?? 0) + 1;\n    }\n    return $counts;\n}"
            }
        },
        2: {
            "title_ru": "Алгоритмы сортировки и поиска",
            "desc": "Алгоритмические подходы к упорядочиванию данных. Разбор сортировки пузырьком (Bubble Sort) и бинарного поиска.",
            "code_templates": {
                "python": "def bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n-i-1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n    return arr",
                "javascript": "function bubbleSort(arr) {\n    let len = arr.length;\n    for (let i = 0; i < len; i++) {\n        for (let j = 0; j < len - i - 1; j++) {\n            if (arr[j] > arr[j + 1]) {\n                let temp = arr[j];\n                arr[j] = arr[j + 1];\n                arr[j + 1] = temp;\n            }\n        }\n    }\n    return arr;\n}",
                "csharp": "public int[] BubbleSort(int[] arr) {\n    int n = arr.Length;\n    for (int i = 0; i < n; i++) {\n        for (int j = 0; j < n - i - 1; j++) {\n            if (arr[j] > arr[j + 1]) {\n                int temp = arr[j];\n                arr[j] = arr[j + 1];\n                arr[j + 1] = temp;\n            }\n        }\n    }\n    return arr;\n}",
                "java": "public static int[] bubbleSort(int[] arr) {\n    int n = arr.length;\n    for (int i = 0; i < n; i++) {\n        for (int j = 0; j < n - i - 1; j++) {\n            if (arr[j] > arr[j + 1]) {\n                int temp = arr[j];\n                arr[j] = arr[j + 1];\n                arr[j + 1] = temp;\n            }\n        }\n    }\n    return arr;\n}",
                "php": "function bubbleSort($arr) {\n    $n = count($arr);\n    for ($i = 0; $i < $n; $i++) {\n        for ($j = 0; $j < $n - $i - 1; $j++) {\n            if ($arr[$j] > $arr[$j + 1]) {\n                $temp = $arr[$j];\n                $arr[$j] = $arr[$j + 1];\n                $arr[$j + 1] = $temp;\n            }\n        }\n    }\n    return $arr;\n}"
            }
        },
        3: {
            "title_ru": "Методы обработки строк",
            "desc": "Работа со строковыми типами данных. Срезы, конкатенация, поиск подстроки, замена символов и регулярные выражения.",
            "code_templates": {
                "python": "def reverse_string(s):\n    # Быстрый срез строки в Python\n    return s[::-1]",
                "javascript": "function reverseString(s) {\n    // Разбиваем строку, переворачиваем массив и склеиваем\n    return s.split('').reverse().join('');\n}",
                "csharp": "public string ReverseString(string s) {\n    char[] arr = s.ToCharArray();\n    Array.Reverse(arr);\n    return new string(arr);\n}",
                "java": "public static String reverseString(String s) {\n    return new StringBuilder(s).reverse().toString();\n}",
                "php": "function reverseString($s) {\n    // Встроенная функция в PHP\n    return strrev($s);\n}"
            }
        },
        4: {
            "title_ru": "Исключения и обработка ошибок",
            "desc": "Управление стабильностью программы. Перехват критических ошибок времени выполнения с помощью блоков try-catch-finally.",
            "code_templates": {
                "python": "def safe_divide(a, b):\n    try:\n        return a / b\n    except ZeroDivisionError:\n        return 'Деление на ноль заблокировано'",
                "javascript": "function safeDivide(a, b) {\n    try {\n        if (b === 0) throw new Error('Zero division');\n        return a / b;\n    } catch (e) {\n        return 'Деление на ноль заблокировано';\n    }\n}",
                "csharp": "public double SafeDivide(double a, double b) {\n    try {\n        if (b == 0) throw new DivideByZeroException();\n        return a / b;\n    }\n    catch (DivideByZeroException) {\n        return 0; // или обработка\n    }\n}",
                "java": "public static double safeDivide(double a, double b) {\n    try {\n        if (b == 0) throw new ArithmeticException(\"Zero division\");\n        return a / b;\n    } catch (ArithmeticException e) {\n        return 0;\n    }\n}",
                "php": "function safeDivide($a, $b) {\n    try {\n        if ($b == 0) throw new Exception('Zero division');\n        return $a / $b;\n    } catch (Exception $e) {\n        return 'Деление на ноль заблокировано';\n    }\n}"
            }
        },
        5: {
            "title_ru": "Рекурсивные алгоритмы",
            "desc": "Концепция вызова функции из самой себя. Базовый случай рекурсии и рекурсивный шаг на примере чисел Фибоначчи и факториала.",
            "code_templates": {
                "python": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)",
                "javascript": "function factorial(n) {\n    if (n <= 1) return 1;\n    return n * factorial(n - 1);\n}",
                "csharp": "public int Factorial(int n) {\n    if (n <= 1) return 1;\n    return n * Factorial(n - 1);\n}",
                "java": "public static int factorial(int n) {\n    if (n <= 1) return 1;\n    return n * factorial(n - 1);\n}",
                "php": "function factorial($n) {\n    if ($n <= 1) return 1;\n    return $n * factorial($n - 1);\n}"
            }
        }
    },
    "hard": {
        1: {
            "title_ru": "ООП: Классы и свойства",
            "desc": "Конструирование собственных сложных типов данных. Инкапсуляция переменных состояния внутри класса с помощью геттеров и сеттеров.",
            "code_templates": {
                "python": "class User:\n    def __init__(self, name):\n        self._name = name  # Защищенное свойство\n\n    @property\n    def name(self):\n        return self._name",
                "javascript": "class User {\n    constructor(name) {\n        this._name = name;\n    }\n    get name() {\n        return this._name;\n    }\n}",
                "csharp": "public class User {\n    public string Name { get; private set; }\n    public User(string name) {\n        Name = name;\n    }\n}",
                "java": "public class User {\n    private String name;\n    public User(String name) { this.name = name; }\n    public String getName() { return name; }\n}",
                "php": "class User {\n    private $name;\n    public function __construct($name) {\n        $this->name = $name;\n    }\n    public function getName() {\n        return $this->name;\n    }\n}"
            }
        },
        2: {
            "title_ru": "ООП: Наследование и полиморфизм",
            "desc": "Переиспользование кода родительских классов. Переопределение абстрактных методов в дочерних классах (полиморфизм поведения).",
            "code_templates": {
                "python": "class Animal:\n    def speak(self): pass\n\nclass Dog(Animal):\n    def speak(self):\n        return 'Гав!'",
                "javascript": "class Animal {\n    speak() { return ''; }\n}\nclass Dog extends Animal {\n    speak() { return 'Гав!'; }\n}",
                "csharp": "public abstract class Animal {\n    public abstract string Speak();\n}\npublic class Dog : Animal {\n    public override string Speak() => \"Гав!\";\n}",
                "java": "abstract class Animal {\n    abstract String speak();\n}\nclass Dog extends Animal {\n    String speak() { return \"Гав!\"; }\n}",
                "php": "abstract class Animal {\n    abstract public function speak();\n}\nclass Dog extends Animal {\n    public function speak() {\n        return 'Гав!';\n    }\n}"
            }
        },
        3: {
            "title_ru": "Потоки и асинхронность",
            "desc": "Выполнение неблокирующих фоновых операций. Использование планировщиков, задач (Promise / Task) и сопрограмм.",
            "code_templates": {
                "python": "import asyncio\nasync def fetch_data():\n    await asyncio.sleep(1)\n    return 'данные загружены'",
                "javascript": "async function fetchData() {\n    await new Promise(r => setTimeout(r, 1000));\n    return 'данные загружены';\n}",
                "csharp": "public async Task<string> FetchDataAsync() {\n    await Task.Delay(1000);\n    return \"данные загружены\";\n}",
                "java": "public static CompletableFuture<String> fetchData() {\n    return CompletableFuture.supplyAsync(() -> {\n        try { Thread.sleep(1000); } catch(Exception e) {} \n        return \"данные загружены\";\n    });\n}",
                "php": "// В классическом PHP асинхронность реализуется через ReactPHP или Swoole\n// Пример эмуляции многопоточного Curl\n$mh = curl_multi_init();"
            }
        },
        4: {
            "title_ru": "Замыкания и функции высшего порядка",
            "desc": "Передача функций как объектов первого класса. Сохранение лексического окружения контекста внутри возвращаемой функции.",
            "code_templates": {
                "python": "def make_multiplier(x):\n    def multiplier(y):\n        return x * y\n    return multiplier",
                "javascript": "function makeMultiplier(x) {\n    return function(y) {\n        return x * y;\n    };\n}",
                "csharp": "public Func<int, int> MakeMultiplier(int x) {\n    return (y) => x * y;\n}",
                "java": "public static Function<Integer, Integer> makeMultiplier(int x) {\n    return (y) -> x * y;\n}",
                "php": "function makeMultiplier($x) {\n    return function($y) use ($x) {\n        return $x * $y;\n    };\n}"
            }
        },
        5: {
            "title_ru": "Big O: Оценка сложности",
            "desc": "Теоретические основы оценки алгоритмической эффективности. Сравнение константной O(1), линейной O(N) и квадратичной O(N^2) сложностей по времени.",
            "code_templates": {
                "python": "# O(1) - Время выполнения не зависит от размера данных\ndef get_first(lst):\n    return lst[0] if lst else None",
                "javascript": "// O(1) - Константная сложность\nfunction getFirst(arr) {\n    return arr.length > 0 ? arr[0] : null;\n}",
                "csharp": "// O(1) - Поиск по индексу массива\npublic int? GetFirst(int[] arr) {\n    return arr.Length > 0 ? (int?)arr[0] : null;\n}",
                "java": "// O(1) - Доступ к первому элементу массива\npublic static Integer getFirst(int[] arr) {\n    return arr.length > 0 ? arr[0] : null;\n}",
                "php": "// O(1) - Выборка первого элемента массива\nfunction getFirst($arr) {\n    return count($arr) > 0 ? $arr[0] : null;\n}"
            }
        }
    }
}

async def main():
    engine = create_async_engine(database_url, echo=False)
    print(f"Connecting to database to seed 75 rich level lectures...")
    
    async with engine.begin() as conn:
        # Fetch tracks and map to language code
        result = await conn.execute(text(
            "SELECT t.id, l.code, l.name FROM tracks t JOIN languages l ON l.id = t.language_id"
        ))
        tracks = result.all()
        
        # Fetch difficulties and map to code
        result = await conn.execute(text("SELECT id, code, name_ru FROM difficulties"))
        diffs = {row.code: (row.id, row.name_ru) for row in result.all()}
        
        count = 0
        for track in tracks:
            track_id, lang_code, lang_name = track
            for diff_code, (diff_id, diff_name_ru) in diffs.items():
                for order_num, topic in TOPICS[diff_code].items():
                    title = f"{lang_name} / {diff_name_ru} — {topic['title_ru']}"
                    
                    # Code example
                    code_ex = topic["code_templates"].get(lang_code, "")
                    
                    theory_md = (
                        f"## 📖 Лекция: {topic['title_ru']}\n\n"
                        f"{topic['desc']}\n\n"
                        f"Понимание этой концепции критически важно для дальнейшего прохождения трека по языку **{lang_name}**.\n\n"
                        f"### ⚙️ Пример синтаксиса на {lang_name}:\n"
                        f"``` {lang_code}\n"
                        f"{code_ex}\n"
                        f"```\n\n"
                        f"### 💡 Практические рекомендации:\n"
                        f"1. Пишите читаемый и хорошо структурированный код.\n"
                        f"2. Обращайте внимание на отступы и скобки, специфичные для {lang_name}.\n"
                        f"3. Используйте правильные наименования переменных (camelCase, snake_case и т.д.).\n\n"
                        f"После детального изучения теории перейдите к написанию кода для закрепления материала."
                    )
                    
                    # Update level title and theory
                    await conn.execute(text(
                        "UPDATE levels "
                        "SET title = :title, theory = :theory "
                        "WHERE track_id = :track_id AND difficulty_id = :difficulty_id AND order_num = :order_num"
                    ), {
                        "title": title,
                        "theory": theory_md,
                        "track_id": track_id,
                        "difficulty_id": diff_id,
                        "order_num": order_num
                    })
                    count += 1
        
        print(f"Successfully populated {count} levels with rich customized theory.")

if __name__ == "__main__":
    asyncio.run(main())
