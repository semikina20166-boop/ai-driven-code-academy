SOLUTIONS = {
    "easy": {
        "1": {
            "python": "def sum_two(a, b):\n    return a + b",
            "javascript": "function sumTwo(a, b) {\n    return a + b;\n}",
            "csharp": "public int SumTwo(int a, int b) {\n    return a + b;\n}",
            "java": "public static int sumTwo(int a, int b) {\n    return a + b;\n}",
            "php": "function sumTwo($a, $b) {\n    return $a + $b;\n}"
        },
        "2": {
            "python": "def is_even(n):\n    return n % 2 == 0",
            "javascript": "function isEven(n) {\n    return n % 2 === 0;\n}",
            "csharp": "public bool IsEven(int n) {\n    return n % 2 == 0;\n}",
            "java": "public static boolean isEven(int n) {\n    return n % 2 == 0;\n}",
            "php": "function isEven($n) {\n    return $n % 2 == 0;\n}"
        },
        "3": {
            "python": "def max_of_two(a, b):\n    if a > b:\n        return a\n    return b",
            "javascript": "function maxOfTwo(a, b) {\n    if (a > b) return a;\n    return b;\n}",
            "csharp": "public int MaxOfTwo(int a, int b) {\n    if (a > b) return a;\n    return b;\n}",
            "java": "public static int maxOfTwo(int a, int b) {\n    if (a > b) return a;\n    return b;\n}",
            "php": "function maxOfTwo($a, $b) {\n    if ($a > $b) return $a;\n    return $b;\n}"
        },
        "4": {
            "python": "def factorial(n):\n    result = 1\n    for i in range(1, n + 1):\n        result *= i\n    return result",
            "javascript": "function factorial(n) {\n    let result = 1;\n    for (let i = 1; i <= n; i++) {\n        result *= i;\n    }\n    return result;\n}",
            "csharp": "public int Factorial(int n) {\n    int result = 1;\n    for (int i = 1; i <= n; i++) {\n        result *= i;\n    }\n    return result;\n}",
            "java": "public static int factorial(int n) {\n    int result = 1;\n    for (int i = 1; i <= n; i++) {\n        result *= i;\n    }\n    return result;\n}",
            "php": "function factorial($n) {\n    $result = 1;\n    for ($i = 1; $i <= $n; $i++) {\n        $result *= $i;\n    }\n    return $result;\n}"
        },
        "5": {
            "python": "def reverse_string(s):\n    return s[::-1]",
            "javascript": "function reverseString(s) {\n    return s.split('').reverse().join('');\n}",
            "csharp": "public string ReverseString(string s) {\n    char[] arr = s.ToCharArray();\n    Array.Reverse(arr);\n    return new string(arr);\n}",
            "java": "public static String reverseString(String s) {\n    return new StringBuilder(s).reverse().toString();\n}",
            "php": "function reverseString($s) {\n    return strrev($s);\n}"
        }
    },
    "medium": {
        "1": {
            "python": "def sum_list(lst):\n    total = 0\n    for num in lst:\n        total += num\n    return total",
            "javascript": "function sumList(lst) {\n    let total = 0;\n    for (let num of lst) {\n        total += num;\n    }\n    return total;\n}",
            "csharp": "public int SumList(int[] lst) {\n    int total = 0;\n    foreach (int num in lst) {\n        total += num;\n    }\n    return total;\n}",
            "java": "public static int sumList(int[] lst) {\n    int total = 0;\n    for (int num : lst) {\n        total += num;\n    }\n    return total;\n}",
            "php": "function sumList($lst) {\n    $total = 0;\n    foreach ($lst as $num) {\n        $total += $num;\n    }\n    return $total;\n}"
        },
        "2": {
            "python": "def count_vowels(s):\n    count = 0\n    for char in s.lower():\n        if char in 'aeiou':\n            count += 1\n    return count",
            "javascript": "function countVowels(s) {\n    let count = 0;\n    for (let char of s.toLowerCase()) {\n        if ('aeiou'.includes(char)) count++;\n    }\n    return count;\n}",
            "csharp": "public int CountVowels(string s) {\n    int count = 0;\n    foreach (char c in s.ToLower()) {\n        if (\"aeiou\".Contains(c)) count++;\n    }\n    return count;\n}",
            "java": "public static int countVowels(String s) {\n    int count = 0;\n    for (char c : s.toLowerCase().toCharArray()) {\n        if (\"aeiou\".indexOf(c) != -1) count++;\n    }\n    return count;\n}",
            "php": "function countVowels($s) {\n    $count = 0;\n    $s = strtolower($s);\n    for ($i = 0; $i < strlen($s); $i++) {\n        if (strpos('aeiou', $s[$i]) !== false) $count++;\n    }\n    return $count;\n}"
        },
        "3": {
            "python": "def fizzbuzz(n):\n    if n % 15 == 0:\n        return 'FizzBuzz'\n    elif n % 3 == 0:\n        return 'Fizz'\n    elif n % 5 == 0:\n        return 'Buzz'\n    return str(n)",
            "javascript": "function fizzbuzz(n) {\n    if (n % 15 === 0) return 'FizzBuzz';\n    if (n % 3 === 0) return 'Fizz';\n    if (n % 5 === 0) return 'Buzz';\n    return String(n);\n}",
            "csharp": "public string Fizzbuzz(int n) {\n    if (n % 15 == 0) return \"FizzBuzz\";\n    if (n % 3 == 0) return \"Fizz\";\n    if (n % 5 == 0) return \"Buzz\";\n    return n.ToString();\n}",
            "java": "public static String fizzbuzz(int n) {\n    if (n % 15 == 0) return \"FizzBuzz\";\n    if (n % 3 == 0) return \"Fizz\";\n    if (n % 5 == 0) return \"Buzz\";\n    return String.valueOf(n);\n}",
            "php": "function fizzbuzz($n) {\n    if ($n % 15 == 0) return 'FizzBuzz';\n    if ($n % 3 == 0) return 'Fizz';\n    if ($n % 5 == 0) return 'Buzz';\n    return (string)$n;\n}"
        },
        "4": {
            "python": "def is_palindrome(s):\n    return s == s[::-1]",
            "javascript": "function isPalindrome(s) {\n    return s === s.split('').reverse().join('');\n}",
            "csharp": "public bool IsPalindrome(string s) {\n    char[] arr = s.ToCharArray();\n    Array.Reverse(arr);\n    return s == new string(arr);\n}",
            "java": "public static boolean isPalindrome(String s) {\n    return s.equals(new StringBuilder(s).reverse().toString());\n}",
            "php": "function isPalindrome($s) {\n    return $s === strrev($s);\n}"
        },
        "5": {
            "python": "def binary_search(arr, target):\n    left, right = 0, len(arr) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1",
            "javascript": "function binarySearch(arr, target) {\n    let left = 0, right = arr.length - 1;\n    while (left <= right) {\n        let mid = Math.floor((left + right) / 2);\n        if (arr[mid] === target) return mid;\n        if (arr[mid] < target) left = mid + 1;\n        else right = mid - 1;\n    }\n    return -1;\n}",
            "csharp": "public int BinarySearch(int[] arr, int target) {\n    int left = 0, right = arr.Length - 1;\n    while (left <= right) {\n        int mid = left + (right - left) / 2;\n        if (arr[mid] == target) return mid;\n        if (arr[mid] < target) left = mid + 1;\n        else right = mid - 1;\n    }\n    return -1;\n}",
            "java": "public static int binarySearch(int[] arr, int target) {\n    int left = 0, right = arr.length - 1;\n    while (left <= right) {\n        int mid = left + (right - left) / 2;\n        if (arr[mid] == target) return mid;\n        if (arr[mid] < target) left = mid + 1;\n        else right = mid - 1;\n    }\n    return -1;\n}",
            "php": "function binarySearch($arr, $target) {\n    $left = 0;\n    $right = count($arr) - 1;\n    while ($left <= $right) {\n        $mid = (int)(($left + $right) / 2);\n        if ($arr[$mid] == $target) return $mid;\n        if ($arr[$mid] < $target) $left = $mid + 1;\n        else $right = $mid - 1;\n    }\n    return -1;\n}"
        }
    },
    "hard": {
        "1": {
            "python": "def fibonacci(n):\n    if n <= 1:\n        return n\n    a, b = 0, 1\n    for _ in range(2, n + 1):\n        a, b = b, a + b\n    return b",
            "javascript": "function fibonacci(n) {\n    if (n <= 1) return n;\n    let a = 0, b = 1;\n    for (let i = 2; i <= n; i++) {\n        let temp = a + b;\n        a = b;\n        b = temp;\n    }\n    return b;\n}",
            "csharp": "public int Fibonacci(int n) {\n    if (n <= 1) return n;\n    int a = 0, b = 1;\n    for (int i = 2; i <= n; i++) {\n        int temp = a + b;\n        a = b;\n        b = temp;\n    }\n    return b;\n}",
            "java": "public static int fibonacci(int n) {\n    if (n <= 1) return n;\n    int a = 0, b = 1;\n    for (int i = 2; i <= n; i++) {\n        int temp = a + b;\n        a = b;\n        b = temp;\n    }\n    return b;\n}",
            "php": "function fibonacci($n) {\n    if ($n <= 1) return $n;\n    $a = 0; $b = 1;\n    for ($i = 2; $i <= $n; $i++) {\n        $temp = $a + $b;\n        $a = $b;\n        $b = $temp;\n    }\n    return $b;\n}"
        },
        "2": {
            "python": "def unique_elements(lst):\n    return list(set(lst))",
            "javascript": "function uniqueElements(lst) {\n    return [...new Set(lst)];\n}",
            "csharp": "public int[] UniqueElements(int[] lst) {\n    return lst.Distinct().ToArray();\n}",
            "java": "public static int[] uniqueElements(int[] lst) {\n    return java.util.Arrays.stream(lst).distinct().toArray();\n}",
            "php": "function uniqueElements($lst) {\n    return array_values(array_unique($lst));\n}"
        },
        "3": {
            "python": "def merge_sorted(a, b):\n    i, j, result = 0, 0, []\n    while i < len(a) and j < len(b):\n        if a[i] < b[j]:\n            result.append(a[i])\n            i += 1\n        else:\n            result.append(b[j])\n            j += 1\n    result.extend(a[i:])\n    result.extend(b[j:])\n    return result",
            "javascript": "function mergeSorted(a, b) {\n    let i = 0, j = 0, result = [];\n    while (i < a.length && j < b.length) {\n        if (a[i] < b[j]) result.push(a[i++]);\n        else result.push(b[j++]);\n    }\n    while (i < a.length) result.push(a[i++]);\n    while (j < b.length) result.push(b[j++]);\n    return result;\n}",
            "csharp": "public int[] MergeSorted(int[] a, int[] b) {\n    int[] result = new int[a.Length + b.Length];\n    int i = 0, j = 0, k = 0;\n    while (i < a.Length && j < b.Length) {\n        if (a[i] < b[j]) result[k++] = a[i++];\n        else result[k++] = b[j++];\n    }\n    while (i < a.Length) result[k++] = a[i++];\n    while (j < b.Length) result[k++] = b[j++];\n    return result;\n}",
            "java": "public static int[] mergeSorted(int[] a, int[] b) {\n    int[] result = new int[a.length + b.length];\n    int i = 0, j = 0, k = 0;\n    while (i < a.length && j < b.length) {\n        if (a[i] < b[j]) result[k++] = a[i++];\n        else result[k++] = b[j++];\n    }\n    while (i < a.length) result[k++] = a[i++];\n    while (j < b.length) result[k++] = b[j++];\n    return result;\n}",
            "php": "function mergeSorted($a, $b) {\n    $result = [];\n    $i = 0; $j = 0;\n    while ($i < count($a) && $j < count($b)) {\n        if ($a[$i] < $b[$j]) $result[] = $a[$i++];\n        else $result[] = $b[$j++];\n    }\n    while ($i < count($a)) $result[] = $a[$i++];\n    while ($j < count($b)) $result[] = $b[$j++];\n    return $result;\n}"
        },
        "4": {
            "python": "def bubble_sort(lst):\n    n = len(lst)\n    for i in range(n):\n        for j in range(0, n-i-1):\n            if lst[j] > lst[j+1]:\n                lst[j], lst[j+1] = lst[j+1], lst[j]\n    return lst",
            "javascript": "function bubbleSort(lst) {\n    let len = lst.length;\n    for (let i = 0; i < len; i++) {\n        for (let j = 0; j < len - i - 1; j++) {\n            if (lst[j] > lst[j + 1]) {\n                let temp = lst[j];\n                lst[j] = lst[j + 1];\n                lst[j + 1] = temp;\n            }\n        }\n    }\n    return lst;\n}",
            "csharp": "public int[] BubbleSort(int[] lst) {\n    int len = lst.Length;\n    for (int i = 0; i < len; i++) {\n        for (int j = 0; j < len - i - 1; j++) {\n            if (lst[j] > lst[j + 1]) {\n                int temp = lst[j];\n                lst[j] = lst[j + 1];\n                lst[j + 1] = temp;\n            }\n        }\n    }\n    return lst;\n}",
            "java": "public static int[] bubbleSort(int[] lst) {\n    int len = lst.length;\n    for (int i = 0; i < len; i++) {\n        for (int j = 0; j < len - i - 1; j++) {\n            if (lst[j] > lst[j + 1]) {\n                int temp = lst[j];\n                lst[j] = lst[j + 1];\n                lst[j + 1] = temp;\n            }\n        }\n    }\n    return lst;\n}",
            "php": "function bubbleSort($lst) {\n    $len = count($lst);\n    for ($i = 0; $i < $len; $i++) {\n        for ($j = 0; $j < $len - $i - 1; $j++) {\n            if ($lst[$j] > $lst[$j + 1]) {\n                $temp = $lst[$j];\n                $lst[$j] = $lst[$j + 1];\n                $lst[$j + 1] = $temp;\n            }\n        }\n    }\n    return $lst;\n}"
        },
        "5": {
            "python": "def matrix_sum(matrix):\n    total = 0\n    for row in matrix:\n        for num in row:\n            total += num\n    return total",
            "javascript": "function matrixSum(matrix) {\n    let total = 0;\n    for (let row of matrix) {\n        for (let num of row) {\n            total += num;\n        }\n    }\n    return total;\n}",
            "csharp": "public int MatrixSum(int[][] matrix) {\n    int total = 0;\n    foreach (int[] row in matrix) {\n        foreach (int num in row) {\n            total += num;\n        }\n    }\n    return total;\n}",
            "java": "public static int matrixSum(int[][] matrix) {\n    int total = 0;\n    for (int[] row : matrix) {\n        for (int num : row) {\n            total += num;\n        }\n    }\n    return total;\n}",
            "php": "function matrixSum($matrix) {\n    $total = 0;\n    foreach ($matrix as $row) {\n        foreach ($row as $num) {\n            $total += $num;\n        }\n    }\n    return $total;\n}"
        }
    }
}

import asyncio
import os
import sys
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

database_url = "postgresql+asyncpg://postgres:postgres@localhost:5432/ai_academy"
if os.path.exists(".env"):
    with open(".env", "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("DATABASE_URL="):
                database_url = line.strip().split("DATABASE_URL=")[1].strip()

# Красивые лекции для всех задач
LECTURES = {
    "easy": {
        1: {
            "title": "Сумма двух чисел",
            "goal": "Научиться создавать простые функции и понимать, как они работают.",
            "intro": "Функция — это именованный блок кода, который выполняет определённое действие и возвращает результат.\nПредставь, что функция — это кухонный комбайн:\n- Ты даёшь ему ингредиенты (аргументы)\n- Он что-то с ними делает\n- Выдаёт готовый результат (через `return`)",
            "rules": "- Слово `def` / `function` — обязательно\n- После названия обязательно ставятся скобки `()`\n- Тело функции пишется с отступом (или в фигурных скобках `{}`)",
            "tips": "Имя функции должно быть говорящим (что она делает).\nНе забывай `return`, иначе функция вернет пустоту (`None` или `undefined`)."
        },
        2: {
            "title": "Проверка на четность",
            "goal": "Научиться использовать условные конструкции `if/else` и оператор остатка от деления.",
            "intro": "Условные конструкции позволяют программе принимать решения.\nПредставь, что это фейсконтроль на входе:\n- **Если (if)** число делится на 2 без остатка ➡️ оно четное (возвращаем True).\n- **Иначе (else)** ➡️ оно нечетное (возвращаем False).",
            "rules": "- Оператор `%` возвращает остаток от деления (например, `5 % 2` даст `1`).\n- Для проверки равенства используется двойное равно `==`.\n- Блоки внутри условий всегда пишутся с отступом.",
            "tips": "Эту функцию часто можно записать в одну строку: `return n % 2 == 0;`"
        },
        3: {
            "title": "Наибольшее из двух чисел",
            "goal": "Закрепить работу с `if/else` и операторами сравнения.",
            "intro": "Мы можем сравнивать числа, используя операторы `>` (больше), `<` (меньше) и `==` (равно).\nПрограмма посмотрит на оба числа и выберет то, которое перевешивает на весах.",
            "rules": "- Сначала проверяем `if a > b`.\n- Если условие не выполнилось, значит `b` больше или они равны, и мы можем использовать `else`.",
            "tips": "В большинстве языков программирования есть встроенная функция (например, `Math.max(a, b)` или `max(a, b)`), но здесь важно написать логику вручную!"
        },
        4: {
            "title": "Вычисление факториала",
            "goal": "Познакомиться с циклами и/или рекурсией для многократного повторения действий.",
            "intro": "Факториал числа `n` (обозначается как `n!`) — это произведение всех чисел от 1 до `n`.\nНапример, `5! = 1 * 2 * 3 * 4 * 5 = 120`.\nФакториал нуля всегда равен 1.",
            "rules": "- Заведи переменную-копилку (например, `result = 1`).\n- Используй цикл, чтобы умножать эту копилку на каждое число от 1 до `n`.\n- После цикла верни `result`.",
            "tips": "Будь осторожен: если `n = 0`, цикл не должен выполняться, и функция сразу должна вернуть 1."
        },
        5: {
            "title": "Переворот строки",
            "goal": "Научиться работать со строками и обходить их с конца в начало.",
            "intro": "Строка — это как массив символов. Мы можем прочитать ее задом наперед.\nЕсли на вход поступает 'cat', мы должны вернуть 'tac'.",
            "rules": "- Создай пустую строку `reversed = ''`.\n- Пройдись циклом по исходной строке с конца.\n- Приклеивай каждый символ к новой строке.",
            "tips": "Во многих языках есть встроенные методы переворота (например, `split('').reverse().join('')` в JS или срез `[::-1]` в Python), но постарайся решить задачу через цикл."
        }
    },
    "medium": {
        1: {
            "title": "Сумма элементов массива",
            "goal": "Понять, как перебирать элементы массива/списка с помощью цикла.",
            "intro": "Массив (`list` или `array`) — это коробка, в которой лежит много значений (например, `[10, 20, 30]`).\nЦикл — это конвейер, который берет из массива по одному числу за раз.",
            "rules": "- Заведи 'копилку' `total = 0`.\n- Используй цикл (`for` или `foreach`), чтобы пройти по всем элементам.\n- Прибавляй каждый элемент к копилке.",
            "tips": "Не забывай, что `return total` должен находиться **вне** цикла, чтобы вернуть результат только после сложения всех чисел."
        },
        2: {
            "title": "Подсчет гласных букв",
            "goal": "Объединить работу со строками, массивами и условиями.",
            "intro": "Нам нужно проанализировать текст и посчитать, сколько раз в нем встречаются буквы `a, e, i, o, u`.\nДля этого нам понадобится счетчик и проверка каждого символа.",
            "rules": "- Приведи строку к нижнему регистру, чтобы не зависеть от больших/маленьких букв.\n- Создай счетчик `count = 0`.\n- Пройдись по строке циклом и проверяй, есть ли символ в списке гласных.",
            "tips": "Проверять можно так: `char in 'aeiou'` (Python) или `'aeiou'.includes(char)` (JavaScript)."
        },
        3: {
            "title": "Классическая задача FizzBuzz",
            "goal": "Научиться правильно выстраивать порядок условий (if / else if).",
            "intro": "FizzBuzz — самая популярная задача на собеседованиях для новичков.\nПравила игры:\n- Кратность 15 -> 'FizzBuzz'\n- Кратность 3 -> 'Fizz'\n- Кратность 5 -> 'Buzz'\n- Иначе -> само число в виде строки.",
            "rules": "- Порядок проверок **очень важен**!\n- Сначала всегда проверяй деление на 15 (и на 3, и на 5 одновременно), иначе условие `n % 3 == 0` перехватит число 15 и выдаст 'Fizz' вместо 'FizzBuzz'.",
            "tips": "Для проверки кратности используй остаток от деления: `n % 3 == 0`."
        },
        4: {
            "title": "Проверка на палиндром",
            "goal": "Научиться сравнивать строки и находить симметрию.",
            "intro": "Палиндром — это слово, которое читается одинаково в обоих направлениях (например, 'racecar' или 'казак').",
            "rules": "- Получи перевернутую копию строки.\n- Сравни исходную строку с перевернутой.\n- Верни результат сравнения (True или False).",
            "tips": "Вспомни лекцию про переворот строки. Эту задачу можно решить, просто вызвав ту же логику переворота!"
        },
        5: {
            "title": "Бинарный поиск",
            "goal": "Познакомиться с алгоритмами быстрого поиска (O(log n)).",
            "intro": "Бинарный поиск работает как поиск слова в словаре:\nТы открываешь книгу посередине. Если нужное слово по алфавиту раньше — ищешь в левой половине, если позже — в правой.\nРаботает **только** на отсортированных массивах!",
            "rules": "- Заведи два указателя: `left = 0` и `right = длина_массива - 1`.\n- Пока `left <= right`, находи середину `mid`.\n- Сравнивай элемент посередине с искомым числом и сдвигай нужный указатель.",
            "tips": "Формула середины: `mid = (left + right) // 2` (для Python) или `Math.floor((left + right) / 2)` (для JS)."
        }
    },
    "hard": {
        1: {
            "title": "Числа Фибоначчи",
            "goal": "Разобраться с динамическим программированием или рекурсией.",
            "intro": "Последовательность Фибоначчи — это ряд чисел, где каждое следующее число равно сумме двух предыдущих: 0, 1, 1, 2, 3, 5, 8, 13...\n0-е число = 0, 1-е = 1.",
            "rules": "- Рекурсивный подход: `F(n) = F(n-1) + F(n-2)`.\n- Циклический подход (через переменные `a` и `b`) работает гораздо быстрее, так как не вычисляет одно и то же по много раз.",
            "tips": "Для больших `n` обычная рекурсия зависнет. Старайся использовать цикл `for` и обновлять две переменные."
        },
        2: {
            "title": "Уникальные элементы",
            "goal": "Изучить структуры данных, исключающие дубликаты (Множества / Sets).",
            "intro": "Часто в данных бывают повторения. Наша задача — убрать все дубликаты и оставить только уникальные значения.",
            "rules": "- Самый быстрый способ — использовать структуру `Set` (множество), которая автоматически удаляет дубли.\n- Второй способ — создать новый пустой массив и добавлять в него элементы, предварительно проверяя, нет ли их уже там.",
            "tips": "Приведение массива к Set и обратно к массиву — классический паттерн во многих языках (например, `list(set(arr))` в Python или `Array.from(new Set(arr))` в JS)."
        },
        3: {
            "title": "Слияние отсортированных массивов",
            "goal": "Освоить алгоритм слияния (Merge), являющийся основой Merge Sort.",
            "intro": "У нас есть два массива, которые уже отсортированы по возрастанию.\nНужно объединить их в один так, чтобы результат тоже был отсортирован, как застежка-молния.",
            "rules": "- Используй два указателя (`i` для первого массива, `j` для второго).\n- Сравнивай элементы `a[i]` и `b[j]`.\n- Меньший элемент добавляй в новый массив и двигай его указатель вперед.\n- В конце добавь оставшиеся элементы из массивов.",
            "tips": "Не используй встроенную сортировку `concat().sort()` — это работает медленнее (O(N log N)), тогда как метод двух указателей делает это за один проход O(N)."
        },
        4: {
            "title": "Сортировка пузырьком (Bubble Sort)",
            "goal": "Написать свой первый алгоритм сортировки и понять вложенные циклы.",
            "intro": "Пузырьковая сортировка сравнивает соседние элементы и меняет их местами, если левый больше правого.\nСамые большие числа 'всплывают' в конец массива, словно пузырьки воздуха в воде.",
            "rules": "- Понадобятся два цикла: внешний и внутренний.\n- Внутренний цикл идет по массиву и меняет элементы `arr[j]` и `arr[j+1]` местами.\n- Внешний цикл повторяет этот процесс, пока весь массив не отсортируется.",
            "tips": "Для обмена значений в Python можно использовать синтаксис `a, b = b, a`. В других языках понадобится временная переменная `temp`."
        },
        5: {
            "title": "Сумма двумерного массива (Матрицы)",
            "goal": "Научиться работать с матрицами (массивами внутри массивов).",
            "intro": "Матрица — это таблица со строками и столбцами.\nВ коде это выглядит как массив, в котором каждый элемент — тоже массив.\nПример: `[[1, 2], [3, 4]]`.",
            "rules": "- Тебе понадобится вложенный цикл (один цикл `for` внутри другого).\n- Внешний цикл перебирает строки `row`.\n- Внутренний цикл перебирает числа `num` внутри каждой строки.\n- Прибавляй каждое число к общей `total` сумме.",
            "tips": "Относись к матрице как к коробке с коробками. Сначала открываем большую коробку, потом по очереди маленькие."
        }
    }
}

async def main():
    engine = create_async_engine(database_url, echo=False)
    print("Populating beautiful lectures for all levels...")
    
    async with engine.begin() as conn:
        # Получаем данные
        result = await conn.execute(text("SELECT t.id, l.code, l.name FROM tracks t JOIN languages l ON l.id = t.language_id"))
        tracks = result.all()
        
        result = await conn.execute(text("SELECT id, code, name_ru FROM difficulties"))
        diffs = {row.code: (row.id, row.name_ru) for row in result.all()}
        
        result = await conn.execute(text("SELECT track_id, difficulty_id, order_num, starter_code FROM levels"))
        levels_data = {(row.track_id, row.difficulty_id, row.order_num): row.starter_code for row in result.all()}
        
        count = 0
        for track in tracks:
            track_id, lang_code, lang_name = track
            for diff_code, (diff_id, diff_name_ru) in diffs.items():
                for order_num, lec in LECTURES[diff_code].items():
                    title = f"{lang_name} / {diff_name_ru} — {lec['title']}"
                    
                    # Извлекаем starter_code (чтобы показать пример правильного синтаксиса, или хотя бы заготовку)
                    starter = levels_data.get((track_id, diff_id, order_num), "")
                    
                    theory_md = (
                        f"✅ **Лекция для урока:** «{lec['title']}»\n\n"
                        f"🎯 **Цель урока**\n{lec['goal']}\n\n"
                        f"**Что это такое?**\n{lec['intro']}\n\n"
                        f"**Важные правила:**\n{lec['rules']}\n\n"
                        f"**💡 Лайфхак / Совет:**\n{lec['tips']}\n\n"
                        f"✅ **Пример решения на {lang_name}:**\n"
                        f"```{lang_code}\n"
                        f"{SOLUTIONS[diff_code][str(order_num)].get(lang_code, starter.strip())}\n"
                        f"```\n"
                    )
                    
                    await conn.execute(text(
                        "UPDATE levels "
                        "SET title = :title, title_ru = :title, title_en = :title, title_kz = :title, "
                        "theory = :theory, theory_ru = :theory, theory_en = :theory, theory_kz = :theory "
                        "WHERE track_id = :track_id AND difficulty_id = :difficulty_id AND order_num = :order_num"
                    ), {
                        "title": title,
                        "theory": theory_md,
                        "track_id": track_id,
                        "difficulty_id": diff_id,
                        "order_num": order_num
                    })
                    
                    # Update English text (if possible, but requested ru)
                    # For theory, we'll set the main theory to theory_ru in case the DB only uses `theory`
                    # In generate_seed we saw task_text_ru, task_text_en, etc. Wait, the DB column for theory might be `theory` or `theory_ru`.
                    
                    # Just attempt to update 'theory' column as well if it exists
                    try:
                        await conn.execute(text(
                            "UPDATE levels "
                            "SET theory = :theory "
                            "WHERE track_id = :track_id AND difficulty_id = :difficulty_id AND order_num = :order_num"
                        ), {
                            "theory": theory_md,
                            "track_id": track_id,
                            "difficulty_id": diff_id,
                            "order_num": order_num
                        })
                    except Exception as e:
                        pass # if 'theory' column doesn't exist but 'theory_ru' does

                    count += 1
        
        print(f"Successfully updated {count} beautiful lectures!")

if __name__ == "__main__":
    asyncio.run(main())
