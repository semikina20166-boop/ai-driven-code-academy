import json

LANGUAGES = [
    ("python", "Python"),
    ("csharp", "C#"),
    ("php", "PHP"),
    ("javascript", "JavaScript"),
    ("java", "Java")
]

DIFFICULTIES = [
    ("easy", "Начальный", "Beginner", "Бастапқы", 1),
    ("medium", "Средний", "Intermediate", "Орташа", 2),
    ("hard", "Продвинутый", "Advanced", "Жоғары", 3)
]

# We will define tasks for each difficulty level (1-5)
TASKS = {
    "easy": {
        1: {
            "name": "sum_two",
            "ru": "Напишите функцию sum_two(a, b), которая возвращает сумму двух чисел.",
            "en": "Write a function sum_two(a, b) that returns the sum of two numbers.",
            "kz": "Екі санның қосындысын қайтаратын sum_two(a, b) функциясын жазыңыз.",
            "concepts": ["переменная", "функция", "return"],
            "tests": {
                "python": {"function": "sum_two", "language": "python", "cases": [{"args": [1, 2], "expected": 3}, {"args": [-1, 5], "expected": 4}]},
                "javascript": {"function": "sumTwo", "language": "javascript", "cases": [{"args": [1, 2], "expected": 3}, {"args": [-1, 5], "expected": 4}]},
                "csharp": {"function": "SumTwo", "language": "csharp", "cases": [{"args": [1, 2], "expected": 3}, {"args": [-1, 5], "expected": 4}]},
                "java": {"function": "sumTwo", "language": "java", "cases": [{"args": [1, 2], "expected": 3}, {"args": [-1, 5], "expected": 4}]},
                "php": {"function": "sumTwo", "language": "php", "cases": [{"args": [1, 2], "expected": 3}, {"args": [-1, 5], "expected": 4}]}
            },
            "starter": {
                "python": "def sum_two(a, b):\n    pass\n",
                "javascript": "function sumTwo(a, b) {\n    \n}\n",
                "csharp": "public int SumTwo(int a, int b) {\n    return 0;\n}\n",
                "java": "public static int sumTwo(int a, int b) {\n    return 0;\n}\n",
                "php": "function sumTwo($a, $b) {\n    \n}\n"
            }
        },
        2: {
            "name": "is_even",
            "ru": "Напишите функцию is_even(n), которая возвращает true, если число чётное, и false в противном случае.",
            "en": "Write a function is_even(n) that returns true if the number is even, and false otherwise.",
            "kz": "Сан жұп болса true, әйтпесе false қайтаратын is_even(n) функциясын жазыңыз.",
            "concepts": ["условие", "оператор", "return"],
            "tests": {
                "python": {"function": "is_even", "language": "python", "cases": [{"args": [4], "expected": True}, {"args": [7], "expected": False}]},
                "javascript": {"function": "isEven", "language": "javascript", "cases": [{"args": [4], "expected": True}, {"args": [7], "expected": False}]},
                "csharp": {"function": "IsEven", "language": "csharp", "cases": [{"args": [4], "expected": True}, {"args": [7], "expected": False}]},
                "java": {"function": "isEven", "language": "java", "cases": [{"args": [4], "expected": True}, {"args": [7], "expected": False}]},
                "php": {"function": "isEven", "language": "php", "cases": [{"args": [4], "expected": True}, {"args": [7], "expected": False}]}
            },
            "starter": {
                "python": "def is_even(n):\n    pass\n",
                "javascript": "function isEven(n) {\n    \n}\n",
                "csharp": "public bool IsEven(int n) {\n    return false;\n}\n",
                "java": "public static boolean isEven(int n) {\n    return false;\n}\n",
                "php": "function isEven($n) {\n    \n}\n"
            }
        },
        3: {
            "name": "max_of_two",
            "ru": "Напишите функцию max_of_two(a, b), возвращающую наибольшее из двух чисел.",
            "en": "Write a function max_of_two(a, b) returning the largest of two numbers.",
            "kz": "Екі санның үлкенін қайтаратын max_of_two(a, b) функциясын жазыңыз.",
            "concepts": ["условие", "return"],
            "tests": {
                "python": {"function": "max_of_two", "language": "python", "cases": [{"args": [10, 20], "expected": 20}, {"args": [5, -5], "expected": 5}]},
                "javascript": {"function": "maxOfTwo", "language": "javascript", "cases": [{"args": [10, 20], "expected": 20}, {"args": [5, -5], "expected": 5}]},
                "csharp": {"function": "MaxOfTwo", "language": "csharp", "cases": [{"args": [10, 20], "expected": 20}, {"args": [5, -5], "expected": 5}]},
                "java": {"function": "maxOfTwo", "language": "java", "cases": [{"args": [10, 20], "expected": 20}, {"args": [5, -5], "expected": 5}]},
                "php": {"function": "maxOfTwo", "language": "php", "cases": [{"args": [10, 20], "expected": 20}, {"args": [5, -5], "expected": 5}]}
            },
            "starter": {
                "python": "def max_of_two(a, b):\n    pass\n",
                "javascript": "function maxOfTwo(a, b) {\n    \n}\n",
                "csharp": "public int MaxOfTwo(int a, int b) {\n    return 0;\n}\n",
                "java": "public static int maxOfTwo(int a, int b) {\n    return 0;\n}\n",
                "php": "function maxOfTwo($a, $b) {\n    \n}\n"
            }
        },
        4: {
            "name": "factorial",
            "ru": "Напишите функцию factorial(n) для вычисления факториала (n >= 0).",
            "en": "Write a function factorial(n) to calculate the factorial (n >= 0).",
            "kz": "Факториалды есептейтін factorial(n) функциясын жазыңыз (n >= 0).",
            "concepts": ["цикл", "рекурсия"],
            "tests": {
                "python": {"function": "factorial", "language": "python", "cases": [{"args": [0], "expected": 1}, {"args": [5], "expected": 120}]},
                "javascript": {"function": "factorial", "language": "javascript", "cases": [{"args": [0], "expected": 1}, {"args": [5], "expected": 120}]},
                "csharp": {"function": "Factorial", "language": "csharp", "cases": [{"args": [0], "expected": 1}, {"args": [5], "expected": 120}]},
                "java": {"function": "factorial", "language": "java", "cases": [{"args": [0], "expected": 1}, {"args": [5], "expected": 120}]},
                "php": {"function": "factorial", "language": "php", "cases": [{"args": [0], "expected": 1}, {"args": [5], "expected": 120}]}
            },
            "starter": {
                "python": "def factorial(n):\n    pass\n",
                "javascript": "function factorial(n) {\n    \n}\n",
                "csharp": "public int Factorial(int n) {\n    return 0;\n}\n",
                "java": "public static int factorial(int n) {\n    return 0;\n}\n",
                "php": "function factorial($n) {\n    \n}\n"
            }
        },
        5: {
            "name": "reverse_string",
            "ru": "Напишите функцию reverse_string(s), которая переворачивает строку.",
            "en": "Write a function reverse_string(s) that reverses a string.",
            "kz": "Жолды кері айналдыратын reverse_string(s) функциясын жазыңыз.",
            "concepts": ["строка", "цикл"],
            "tests": {
                "python": {"function": "reverse_string", "language": "python", "cases": [{"args": ["hello"], "expected": "olleh"}, {"args": [""], "expected": ""}]},
                "javascript": {"function": "reverseString", "language": "javascript", "cases": [{"args": ["hello"], "expected": "olleh"}, {"args": [""], "expected": ""}]},
                "csharp": {"function": "ReverseString", "language": "csharp", "cases": [{"args": ["hello"], "expected": "olleh"}, {"args": [""], "expected": ""}]},
                "java": {"function": "reverseString", "language": "java", "cases": [{"args": ["hello"], "expected": "olleh"}, {"args": [""], "expected": ""}]},
                "php": {"function": "reverseString", "language": "php", "cases": [{"args": ["hello"], "expected": "olleh"}, {"args": [""], "expected": ""}]}
            },
            "starter": {
                "python": "def reverse_string(s):\n    pass\n",
                "javascript": "function reverseString(s) {\n    \n}\n",
                "csharp": "public string ReverseString(string s) {\n    return \"\";\n}\n",
                "java": "public static String reverseString(String s) {\n    return \"\";\n}\n",
                "php": "function reverseString($s) {\n    \n}\n"
            }
        }
    },
    "medium": {
        1: {
            "name": "sum_list",
            "ru": "Напишите функцию sum_list(lst), которая возвращает сумму всех элементов списка/массива.",
            "en": "Write a function sum_list(lst) that returns the sum of all elements in a list/array.",
            "kz": "Тізімнің/массивтің барлық элементтерінің қосындысын қайтаратын sum_list(lst) функциясын жазыңыз.",
            "concepts": ["цикл", "список", "массив"],
            "tests": {
                "python": {"function": "sum_list", "language": "python", "cases": [{"args": [[1, 2, 3]], "expected": 6}, {"args": [[]], "expected": 0}]},
                "javascript": {"function": "sumList", "language": "javascript", "cases": [{"args": [[1, 2, 3]], "expected": 6}, {"args": [[]], "expected": 0}]},
                "csharp": {"function": "SumList", "language": "csharp", "cases": [{"args": [[1, 2, 3]], "expected": 6}, {"args": [[]], "expected": 0}]},
                "java": {"function": "sumList", "language": "java", "cases": [{"args": [[1, 2, 3]], "expected": 6}, {"args": [[]], "expected": 0}]},
                "php": {"function": "sumList", "language": "php", "cases": [{"args": [[1, 2, 3]], "expected": 6}, {"args": [[]], "expected": 0}]}
            },
            "starter": {
                "python": "def sum_list(lst):\n    pass\n",
                "javascript": "function sumList(lst) {\n    \n}\n",
                "csharp": "public int SumList(int[] lst) {\n    return 0;\n}\n",
                "java": "public static int sumList(int[] lst) {\n    return 0;\n}\n",
                "php": "function sumList($lst) {\n    \n}\n"
            }
        },
        2: {
            "name": "count_vowels",
            "ru": "Напишите функцию count_vowels(s), возвращающую количество гласных букв (a, e, i, o, u) в строке без учета регистра.",
            "en": "Write a function count_vowels(s) returning the number of vowels (a, e, i, o, u) in a string case-insensitively.",
            "kz": "Жолдағы дауысты дыбыстардың (a, e, i, o, u) санын регистрге қарамастан қайтаратын count_vowels(s) функциясын жазыңыз.",
            "concepts": ["строка", "цикл", "условие"],
            "tests": {
                "python": {"function": "count_vowels", "language": "python", "cases": [{"args": ["hello"], "expected": 2}, {"args": ["APPLE"], "expected": 2}]},
                "javascript": {"function": "countVowels", "language": "javascript", "cases": [{"args": ["hello"], "expected": 2}, {"args": ["APPLE"], "expected": 2}]},
                "csharp": {"function": "CountVowels", "language": "csharp", "cases": [{"args": ["hello"], "expected": 2}, {"args": ["APPLE"], "expected": 2}]},
                "java": {"function": "countVowels", "language": "java", "cases": [{"args": ["hello"], "expected": 2}, {"args": ["APPLE"], "expected": 2}]},
                "php": {"function": "countVowels", "language": "php", "cases": [{"args": ["hello"], "expected": 2}, {"args": ["APPLE"], "expected": 2}]}
            },
            "starter": {
                "python": "def count_vowels(s):\n    pass\n",
                "javascript": "function countVowels(s) {\n    \n}\n",
                "csharp": "public int CountVowels(string s) {\n    return 0;\n}\n",
                "java": "public static int countVowels(String s) {\n    return 0;\n}\n",
                "php": "function countVowels($s) {\n    \n}\n"
            }
        },
        3: {
            "name": "fizzbuzz",
            "ru": "Напишите функцию fizzbuzz(n), возвращающую 'FizzBuzz' если n делится на 15, 'Fizz' если на 3, 'Buzz' если на 5, иначе строку n.",
            "en": "Write fizzbuzz(n) returning 'FizzBuzz' if n is divisible by 15, 'Fizz' if by 3, 'Buzz' if by 5, else string of n.",
            "kz": "Егер n 15-ке бөлінсе 'FizzBuzz', 3-ке бөлінсе 'Fizz', 5-ке бөлінсе 'Buzz', әйтпесе n жолын қайтаратын fizzbuzz(n) функциясын жазыңыз.",
            "concepts": ["условие", "оператор"],
            "tests": {
                "python": {"function": "fizzbuzz", "language": "python", "cases": [{"args": [15], "expected": "FizzBuzz"}, {"args": [3], "expected": "Fizz"}, {"args": [5], "expected": "Buzz"}, {"args": [7], "expected": "7"}]},
                "javascript": {"function": "fizzbuzz", "language": "javascript", "cases": [{"args": [15], "expected": "FizzBuzz"}, {"args": [3], "expected": "Fizz"}, {"args": [5], "expected": "Buzz"}, {"args": [7], "expected": "7"}]},
                "csharp": {"function": "Fizzbuzz", "language": "csharp", "cases": [{"args": [15], "expected": "FizzBuzz"}, {"args": [3], "expected": "Fizz"}, {"args": [5], "expected": "Buzz"}, {"args": [7], "expected": "7"}]},
                "java": {"function": "fizzbuzz", "language": "java", "cases": [{"args": [15], "expected": "FizzBuzz"}, {"args": [3], "expected": "Fizz"}, {"args": [5], "expected": "Buzz"}, {"args": [7], "expected": "7"}]},
                "php": {"function": "fizzbuzz", "language": "php", "cases": [{"args": [15], "expected": "FizzBuzz"}, {"args": [3], "expected": "Fizz"}, {"args": [5], "expected": "Buzz"}, {"args": [7], "expected": "7"}]}
            },
            "starter": {
                "python": "def fizzbuzz(n):\n    pass\n",
                "javascript": "function fizzbuzz(n) {\n    \n}\n",
                "csharp": "public string Fizzbuzz(int n) {\n    return \"\";\n}\n",
                "java": "public static String fizzbuzz(int n) {\n    return \"\";\n}\n",
                "php": "function fizzbuzz($n) {\n    \n}\n"
            }
        },
        4: {
            "name": "is_palindrome",
            "ru": "Напишите функцию is_palindrome(s), проверяющую, является ли строка палиндромом (читается одинаково слева направо и справа налево).",
            "en": "Write a function is_palindrome(s) checking if a string is a palindrome.",
            "kz": "Жолдың палиндром екенін тексеретін is_palindrome(s) функциясын жазыңыз.",
            "concepts": ["строка", "срез"],
            "tests": {
                "python": {"function": "is_palindrome", "language": "python", "cases": [{"args": ["racecar"], "expected": True}, {"args": ["hello"], "expected": False}]},
                "javascript": {"function": "isPalindrome", "language": "javascript", "cases": [{"args": ["racecar"], "expected": True}, {"args": ["hello"], "expected": False}]},
                "csharp": {"function": "IsPalindrome", "language": "csharp", "cases": [{"args": ["racecar"], "expected": True}, {"args": ["hello"], "expected": False}]},
                "java": {"function": "isPalindrome", "language": "java", "cases": [{"args": ["racecar"], "expected": True}, {"args": ["hello"], "expected": False}]},
                "php": {"function": "isPalindrome", "language": "php", "cases": [{"args": ["racecar"], "expected": True}, {"args": ["hello"], "expected": False}]}
            },
            "starter": {
                "python": "def is_palindrome(s):\n    pass\n",
                "javascript": "function isPalindrome(s) {\n    \n}\n",
                "csharp": "public bool IsPalindrome(string s) {\n    return false;\n}\n",
                "java": "public static boolean isPalindrome(String s) {\n    return false;\n}\n",
                "php": "function isPalindrome($s) {\n    \n}\n"
            }
        },
        5: {
            "name": "binary_search",
            "ru": "Напишите функцию binary_search(arr, target), реализующую бинарный поиск. Возвращает индекс элемента или -1.",
            "en": "Write a function binary_search(arr, target) implementing binary search. Returns index or -1.",
            "kz": "Бинарлық іздеуді жүзеге асыратын binary_search(arr, target) функциясын жазыңыз. Индексті немесе -1 қайтарады.",
            "concepts": ["алгоритм", "массив", "цикл"],
            "tests": {
                "python": {"function": "binary_search", "language": "python", "cases": [{"args": [[1, 2, 3, 4, 5], 4], "expected": 3}, {"args": [[1, 2, 3, 4, 5], 6], "expected": -1}]},
                "javascript": {"function": "binarySearch", "language": "javascript", "cases": [{"args": [[1, 2, 3, 4, 5], 4], "expected": 3}, {"args": [[1, 2, 3, 4, 5], 6], "expected": -1}]},
                "csharp": {"function": "BinarySearch", "language": "csharp", "cases": [{"args": [[1, 2, 3, 4, 5], 4], "expected": 3}, {"args": [[1, 2, 3, 4, 5], 6], "expected": -1}]},
                "java": {"function": "binarySearch", "language": "java", "cases": [{"args": [[1, 2, 3, 4, 5], 4], "expected": 3}, {"args": [[1, 2, 3, 4, 5], 6], "expected": -1}]},
                "php": {"function": "binarySearch", "language": "php", "cases": [{"args": [[1, 2, 3, 4, 5], 4], "expected": 3}, {"args": [[1, 2, 3, 4, 5], 6], "expected": -1}]}
            },
            "starter": {
                "python": "def binary_search(arr, target):\n    pass\n",
                "javascript": "function binarySearch(arr, target) {\n    \n}\n",
                "csharp": "public int BinarySearch(int[] arr, int target) {\n    return -1;\n}\n",
                "java": "public static int binarySearch(int[] arr, int target) {\n    return -1;\n}\n",
                "php": "function binarySearch($arr, $target) {\n    \n}\n"
            }
        }
    },
    "hard": {
        1: {
            "name": "fibonacci",
            "ru": "Напишите функцию fibonacci(n), возвращающую n-ое число Фибоначчи (0-ое = 0, 1-ое = 1).",
            "en": "Write a function fibonacci(n) returning the n-th Fibonacci number (0-th = 0, 1-st = 1).",
            "kz": "n-ші Фибоначчи санын қайтаратын fibonacci(n) функциясын жазыңыз.",
            "concepts": ["рекурсия", "цикл", "алгоритм"],
            "tests": {
                "python": {"function": "fibonacci", "language": "python", "cases": [{"args": [0], "expected": 0}, {"args": [6], "expected": 8}]},
                "javascript": {"function": "fibonacci", "language": "javascript", "cases": [{"args": [0], "expected": 0}, {"args": [6], "expected": 8}]},
                "csharp": {"function": "Fibonacci", "language": "csharp", "cases": [{"args": [0], "expected": 0}, {"args": [6], "expected": 8}]},
                "java": {"function": "fibonacci", "language": "java", "cases": [{"args": [0], "expected": 0}, {"args": [6], "expected": 8}]},
                "php": {"function": "fibonacci", "language": "php", "cases": [{"args": [0], "expected": 0}, {"args": [6], "expected": 8}]}
            },
            "starter": {
                "python": "def fibonacci(n):\n    pass\n",
                "javascript": "function fibonacci(n) {\n    \n}\n",
                "csharp": "public int Fibonacci(int n) {\n    return 0;\n}\n",
                "java": "public static int fibonacci(int n) {\n    return 0;\n}\n",
                "php": "function fibonacci($n) {\n    \n}\n"
            }
        },
        2: {
            "name": "unique_elements",
            "ru": "Напишите функцию unique_elements(lst), возвращающую новый массив только с уникальными элементами.",
            "en": "Write a function unique_elements(lst) returning a new array with only unique elements.",
            "kz": "Тек бірегей элементтері бар жаңа массивті қайтаратын unique_elements(lst) функциясын жазыңыз.",
            "concepts": ["массив", "set", "хэш"],
            "tests": {
                "python": {"function": "unique_elements", "language": "python", "cases": [{"args": [[1, 2, 2, 3]], "expected": [1, 2, 3]}, {"args": [[1, 1, 1]], "expected": [1]}]},
                "javascript": {"function": "uniqueElements", "language": "javascript", "cases": [{"args": [[1, 2, 2, 3]], "expected": [1, 2, 3]}, {"args": [[1, 1, 1]], "expected": [1]}]},
                "csharp": {"function": "UniqueElements", "language": "csharp", "cases": [{"args": [[1, 2, 2, 3]], "expected": [1, 2, 3]}, {"args": [[1, 1, 1]], "expected": [1]}]},
                "java": {"function": "uniqueElements", "language": "java", "cases": [{"args": [[1, 2, 2, 3]], "expected": [1, 2, 3]}, {"args": [[1, 1, 1]], "expected": [1]}]},
                "php": {"function": "uniqueElements", "language": "php", "cases": [{"args": [[1, 2, 2, 3]], "expected": [1, 2, 3]}, {"args": [[1, 1, 1]], "expected": [1]}]}
            },
            "starter": {
                "python": "def unique_elements(lst):\n    pass\n",
                "javascript": "function uniqueElements(lst) {\n    \n}\n",
                "csharp": "public int[] UniqueElements(int[] lst) {\n    return new int[0];\n}\n",
                "java": "public static int[] uniqueElements(int[] lst) {\n    return new int[0];\n}\n",
                "php": "function uniqueElements($lst) {\n    \n}\n"
            }
        },
        3: {
            "name": "merge_sorted",
            "ru": "Напишите функцию merge_sorted(a, b), сливающую два отсортированных массива в один отсортированный.",
            "en": "Write a function merge_sorted(a, b) merging two sorted arrays into one sorted array.",
            "kz": "Екі сұрыпталған массивті бір сұрыпталған массивке біріктіретін merge_sorted(a, b) функциясын жазыңыз.",
            "concepts": ["массив", "сортировка", "алгоритм"],
            "tests": {
                "python": {"function": "merge_sorted", "language": "python", "cases": [{"args": [[1, 3], [2, 4]], "expected": [1, 2, 3, 4]}]},
                "javascript": {"function": "mergeSorted", "language": "javascript", "cases": [{"args": [[1, 3], [2, 4]], "expected": [1, 2, 3, 4]}]},
                "csharp": {"function": "MergeSorted", "language": "csharp", "cases": [{"args": [[1, 3], [2, 4]], "expected": [1, 2, 3, 4]}]},
                "java": {"function": "mergeSorted", "language": "java", "cases": [{"args": [[1, 3], [2, 4]], "expected": [1, 2, 3, 4]}]},
                "php": {"function": "mergeSorted", "language": "php", "cases": [{"args": [[1, 3], [2, 4]], "expected": [1, 2, 3, 4]}]}
            },
            "starter": {
                "python": "def merge_sorted(a, b):\n    pass\n",
                "javascript": "function mergeSorted(a, b) {\n    \n}\n",
                "csharp": "public int[] MergeSorted(int[] a, int[] b) {\n    return new int[0];\n}\n",
                "java": "public static int[] mergeSorted(int[] a, int[] b) {\n    return new int[0];\n}\n",
                "php": "function mergeSorted($a, $b) {\n    \n}\n"
            }
        },
        4: {
            "name": "bubble_sort",
            "ru": "Напишите функцию bubble_sort(lst), сортирующую массив пузырьком.",
            "en": "Write a function bubble_sort(lst) that sorts an array using bubble sort.",
            "kz": "Массивті көпіршік әдісімен сұрыптайтын bubble_sort(lst) функциясын жазыңыз.",
            "concepts": ["массив", "сортировка", "вложенный цикл"],
            "tests": {
                "python": {"function": "bubble_sort", "language": "python", "cases": [{"args": [[3, 1, 2]], "expected": [1, 2, 3]}]},
                "javascript": {"function": "bubbleSort", "language": "javascript", "cases": [{"args": [[3, 1, 2]], "expected": [1, 2, 3]}]},
                "csharp": {"function": "BubbleSort", "language": "csharp", "cases": [{"args": [[3, 1, 2]], "expected": [1, 2, 3]}]},
                "java": {"function": "bubbleSort", "language": "java", "cases": [{"args": [[3, 1, 2]], "expected": [1, 2, 3]}]},
                "php": {"function": "bubbleSort", "language": "php", "cases": [{"args": [[3, 1, 2]], "expected": [1, 2, 3]}]}
            },
            "starter": {
                "python": "def bubble_sort(lst):\n    pass\n",
                "javascript": "function bubbleSort(lst) {\n    \n}\n",
                "csharp": "public int[] BubbleSort(int[] lst) {\n    return lst;\n}\n",
                "java": "public static int[] bubbleSort(int[] lst) {\n    return lst;\n}\n",
                "php": "function bubbleSort($lst) {\n    \n}\n"
            }
        },
        5: {
            "name": "matrix_sum",
            "ru": "Напишите функцию matrix_sum(matrix), возвращающую сумму всех элементов двумерного массива.",
            "en": "Write a function matrix_sum(matrix) returning the sum of all elements in a 2D array.",
            "kz": "Екі өлшемді массивтің барлық элементтерінің қосындысын қайтаратын matrix_sum(matrix) функциясын жазыңыз.",
            "concepts": ["массив", "матрица", "вложенный цикл"],
            "tests": {
                "python": {"function": "matrix_sum", "language": "python", "cases": [{"args": [[[1, 2], [3, 4]]], "expected": 10}, {"args": [[[]]], "expected": 0}]},
                "javascript": {"function": "matrixSum", "language": "javascript", "cases": [{"args": [[[1, 2], [3, 4]]], "expected": 10}, {"args": [[[]]], "expected": 0}]},
                "csharp": {"function": "MatrixSum", "language": "csharp", "cases": [{"args": [[[1, 2], [3, 4]]], "expected": 10}, {"args": [[[]]], "expected": 0}]},
                "java": {"function": "matrixSum", "language": "java", "cases": [{"args": [[[1, 2], [3, 4]]], "expected": 10}, {"args": [[[]]], "expected": 0}]},
                "php": {"function": "matrixSum", "language": "php", "cases": [{"args": [[[1, 2], [3, 4]]], "expected": 10}, {"args": [[[]]], "expected": 0}]}
            },
            "starter": {
                "python": "def matrix_sum(matrix):\n    pass\n",
                "javascript": "function matrixSum(matrix) {\n    \n}\n",
                "csharp": "public int MatrixSum(int[][] matrix) {\n    return 0;\n}\n",
                "java": "public static int matrixSum(int[][] matrix) {\n    return 0;\n}\n",
                "php": "function matrixSum($matrix) {\n    \n}\n"
            }
        }
    }
}


sql_lines = []
sql_lines.append("-- =============================================")
sql_lines.append("-- ПОЛНОЕ НАПОЛНЕНИЕ БАЗЫ ДАННЫХ (РЕАЛЬНЫЕ ЗАДАНИЯ)")
sql_lines.append("-- =============================================")
sql_lines.append("")

sql_lines.append("INSERT INTO languages (code, name) VALUES")
sql_lines.append("  ('python', 'Python'),")
sql_lines.append("  ('csharp', 'C#'),")
sql_lines.append("  ('php', 'PHP'),")
sql_lines.append("  ('javascript', 'JavaScript'),")
sql_lines.append("  ('java', 'Java')")
sql_lines.append("ON CONFLICT (code) DO NOTHING;")
sql_lines.append("")

sql_lines.append("INSERT INTO difficulties (code, name_ru, name_en, name_kz, sort_order) VALUES")
sql_lines.append("  ('easy', 'Начальный', 'Beginner', 'Бастапқы', 1),")
sql_lines.append("  ('medium', 'Средний', 'Intermediate', 'Орташа', 2),")
sql_lines.append("  ('hard', 'Продвинутый', 'Advanced', 'Жоғары', 3)")
sql_lines.append("ON CONFLICT (code) DO NOTHING;")
sql_lines.append("")

sql_lines.append("INSERT INTO tracks (language_id, title_ru, title_en, title_kz, description_ru, description_en, description_kz)")
sql_lines.append("SELECT l.id, l.name || ' — трек', l.name || ' — Track', l.name || ' — трегі',")
sql_lines.append("  'Обучающий трек по языку ' || l.name, 'Learning track for ' || l.name, l.name || ' тілі бойынша оқыту трегі'")
sql_lines.append("FROM languages l")
sql_lines.append("WHERE NOT EXISTS (SELECT 1 FROM tracks t WHERE t.language_id = l.id);")
sql_lines.append("")

def escape_sql_string(s):
    if s is None:
        return "NULL"
    return "'" + s.replace("'", "''") + "'"

def get_track_id_sql(lang_code):
    return f"(SELECT t.id FROM tracks t JOIN languages l ON t.language_id = l.id WHERE l.code = '{lang_code}')"

def get_diff_id_sql(diff_code):
    return f"(SELECT id FROM difficulties WHERE code = '{diff_code}')"

for lang_code, lang_name in LANGUAGES:
    for diff_code, diff_ru, diff_en, diff_kz, _ in DIFFICULTIES:
        for order_num in range(1, 6):
            task = TASKS[diff_code][order_num]
            
            title_ru = escape_sql_string(f"{lang_name} / {diff_ru} — уровень {order_num}")
            title_en = escape_sql_string(f"{lang_name} / {diff_en} — Level {order_num}")
            title_kz = escape_sql_string(f"{lang_name} / {diff_kz} — деңгей {order_num}")
            
            task_ru = escape_sql_string(task["ru"])
            task_en = escape_sql_string(task["en"])
            task_kz = escape_sql_string(task["kz"])
            
            starter = escape_sql_string(task["starter"][lang_code])
            tests = escape_sql_string(json.dumps(task["tests"][lang_code]))
            
            concepts_array = "ARRAY[" + ", ".join("'" + c + "'" for c in task["concepts"]) + "]::text[]"
            
            sql = f"""
INSERT INTO levels (
  track_id, difficulty_id, order_num, 
  title_ru, title_en, title_kz, 
  task_text_ru, task_text_en, task_text_kz, 
  starter_code, solution_tests, allowed_concepts
)
VALUES (
  {get_track_id_sql(lang_code)}, {get_diff_id_sql(diff_code)}, {order_num},
  {title_ru}, {title_en}, {title_kz},
  {task_ru}, {task_en}, {task_kz},
  {starter}, {tests}::jsonb, {concepts_array}
)
ON CONFLICT (track_id, difficulty_id, order_num) DO UPDATE SET
  title_ru=EXCLUDED.title_ru, title_en=EXCLUDED.title_en, title_kz=EXCLUDED.title_kz,
  task_text_ru=EXCLUDED.task_text_ru, task_text_en=EXCLUDED.task_text_en, task_text_kz=EXCLUDED.task_text_kz,
  starter_code=EXCLUDED.starter_code, solution_tests=EXCLUDED.solution_tests, allowed_concepts=EXCLUDED.allowed_concepts;
"""
            sql_lines.append(sql.strip())

sql_lines.append("")
sql_lines.append("-- =============================================")
sql_lines.append("-- ЭКЗАМЕНЫ")
sql_lines.append("-- =============================================")
sql_lines.append("")

sql_lines.append("""
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
""")

sql_lines.append("""
INSERT INTO exam_difficulty_blocks (exam_id, track_id, difficulty_id)
SELECT e.id, tr.id, d.id
FROM tracks tr
JOIN languages l ON l.id = tr.language_id
CROSS JOIN difficulties d
JOIN exams e ON e.title_ru = l.name || ' — экзамен: ' || d.name_ru
WHERE e.exam_type = 'difficulty_block'
ON CONFLICT DO NOTHING;
""")

sql_lines.append("DELETE FROM exam_questions;")

EXAM_QUESTIONS = {
    "easy": {
        1: {
            "ru": "Экзамен: напишите функцию is_odd(n), которая возвращает true если число нечетное.",
            "en": "Exam: write a function is_odd(n) that returns true if the number is odd.",
            "kz": "Емтихан: сан тақ болса true қайтаратын is_odd(n) функциясын жазыңыз.",
            "name": "is_odd",
            "tests": {
                "python": {"function": "is_odd", "language": "python", "cases": [{"args": [3], "expected": True}, {"args": [4], "expected": False}]},
                "javascript": {"function": "isOdd", "language": "javascript", "cases": [{"args": [3], "expected": True}, {"args": [4], "expected": False}]},
                "csharp": {"function": "IsOdd", "language": "csharp", "cases": [{"args": [3], "expected": True}, {"args": [4], "expected": False}]},
                "java": {"function": "isOdd", "language": "java", "cases": [{"args": [3], "expected": True}, {"args": [4], "expected": False}]},
                "php": {"function": "isOdd", "language": "php", "cases": [{"args": [3], "expected": True}, {"args": [4], "expected": False}]}
            },
            "starter": {
                "python": "def is_odd(n):\n    pass\n",
                "javascript": "function isOdd(n) {\n    \n}\n",
                "csharp": "public bool IsOdd(int n) {\n    return false;\n}\n",
                "java": "public static boolean isOdd(int n) {\n    return false;\n}\n",
                "php": "function isOdd($n) {\n    \n}\n"
            }
        },
        2: {
            "ru": "Экзамен: функция mult_two(a, b), возвращающая произведение чисел.",
            "en": "Exam: mult_two(a, b) function returning the product of two numbers.",
            "kz": "Емтихан: сандардың көбейтіндісін қайтаратын mult_two(a, b) функциясы.",
            "name": "mult_two",
            "tests": {
                "python": {"function": "mult_two", "language": "python", "cases": [{"args": [3, 4], "expected": 12}]},
                "javascript": {"function": "multTwo", "language": "javascript", "cases": [{"args": [3, 4], "expected": 12}]},
                "csharp": {"function": "MultTwo", "language": "csharp", "cases": [{"args": [3, 4], "expected": 12}]},
                "java": {"function": "multTwo", "language": "java", "cases": [{"args": [3, 4], "expected": 12}]},
                "php": {"function": "multTwo", "language": "php", "cases": [{"args": [3, 4], "expected": 12}]}
            },
            "starter": {
                "python": "def mult_two(a, b):\n    pass\n",
                "javascript": "function multTwo(a, b) {\n    \n}\n",
                "csharp": "public int MultTwo(int a, int b) {\n    return 0;\n}\n",
                "java": "public static int multTwo(int a, int b) {\n    return 0;\n}\n",
                "php": "function multTwo($a, $b) {\n    \n}\n"
            }
        },
        3: {
            "ru": "Экзамен: вернуть 'positive' если число > 0, иначе 'non-positive'. Функция check_pos(n).",
            "en": "Exam: return 'positive' if n > 0, else 'non-positive'. check_pos(n).",
            "kz": "Емтихан: n > 0 болса 'positive', әйтпесе 'non-positive' қайтару. check_pos(n).",
            "name": "check_pos",
            "tests": {
                "python": {"function": "check_pos", "language": "python", "cases": [{"args": [1], "expected": "positive"}, {"args": [0], "expected": "non-positive"}]},
                "javascript": {"function": "checkPos", "language": "javascript", "cases": [{"args": [1], "expected": "positive"}, {"args": [0], "expected": "non-positive"}]},
                "csharp": {"function": "CheckPos", "language": "csharp", "cases": [{"args": [1], "expected": "positive"}, {"args": [0], "expected": "non-positive"}]},
                "java": {"function": "checkPos", "language": "java", "cases": [{"args": [1], "expected": "positive"}, {"args": [0], "expected": "non-positive"}]},
                "php": {"function": "checkPos", "language": "php", "cases": [{"args": [1], "expected": "positive"}, {"args": [0], "expected": "non-positive"}]}
            },
            "starter": {
                "python": "def check_pos(n):\n    pass\n",
                "javascript": "function checkPos(n) {\n    \n}\n",
                "csharp": "public string CheckPos(int n) {\n    return \"\";\n}\n",
                "java": "public static String checkPos(int n) {\n    return \"\";\n}\n",
                "php": "function checkPos($n) {\n    \n}\n"
            }
        }
    },
    "medium": {
        1: {
            "ru": "Экзамен: функция min_in_list(lst), возвращающая минимальный элемент в массиве.",
            "en": "Exam: min_in_list(lst) returning the minimum element in an array.",
            "kz": "Емтихан: массивтегі минималды элементті қайтаратын min_in_list(lst).",
            "name": "min_in_list",
            "tests": {
                "python": {"function": "min_in_list", "language": "python", "cases": [{"args": [[3, 1, 2]], "expected": 1}]},
                "javascript": {"function": "minInList", "language": "javascript", "cases": [{"args": [[3, 1, 2]], "expected": 1}]},
                "csharp": {"function": "MinInList", "language": "csharp", "cases": [{"args": [[3, 1, 2]], "expected": 1}]},
                "java": {"function": "minInList", "language": "java", "cases": [{"args": [[3, 1, 2]], "expected": 1}]},
                "php": {"function": "minInList", "language": "php", "cases": [{"args": [[3, 1, 2]], "expected": 1}]}
            },
            "starter": {
                "python": "def min_in_list(lst):\n    pass\n",
                "javascript": "function minInList(lst) {\n    \n}\n",
                "csharp": "public int MinInList(int[] lst) {\n    return 0;\n}\n",
                "java": "public static int minInList(int[] lst) {\n    return 0;\n}\n",
                "php": "function minInList($lst) {\n    \n}\n"
            }
        },
        2: {
            "ru": "Экзамен: функция reverse_array(arr), переворачивающая массив.",
            "en": "Exam: reverse_array(arr) reversing an array.",
            "kz": "Емтихан: массивті кері айналдыратын reverse_array(arr).",
            "name": "reverse_array",
            "tests": {
                "python": {"function": "reverse_array", "language": "python", "cases": [{"args": [[1, 2, 3]], "expected": [3, 2, 1]}]},
                "javascript": {"function": "reverseArray", "language": "javascript", "cases": [{"args": [[1, 2, 3]], "expected": [3, 2, 1]}]},
                "csharp": {"function": "ReverseArray", "language": "csharp", "cases": [{"args": [[1, 2, 3]], "expected": [3, 2, 1]}]},
                "java": {"function": "reverseArray", "language": "java", "cases": [{"args": [[1, 2, 3]], "expected": [3, 2, 1]}]},
                "php": {"function": "reverseArray", "language": "php", "cases": [{"args": [[1, 2, 3]], "expected": [3, 2, 1]}]}
            },
            "starter": {
                "python": "def reverse_array(arr):\n    pass\n",
                "javascript": "function reverseArray(arr) {\n    \n}\n",
                "csharp": "public int[] ReverseArray(int[] arr) {\n    return new int[0];\n}\n",
                "java": "public static int[] reverseArray(int[] arr) {\n    return new int[0];\n}\n",
                "php": "function reverseArray($arr) {\n    \n}\n"
            }
        },
        3: {
            "ru": "Экзамен: функция replace_spaces(s), заменяющая пробелы на подчеркивания.",
            "en": "Exam: replace_spaces(s) replacing spaces with underscores.",
            "kz": "Емтихан: бос орындарды астын сызумен ауыстыратын replace_spaces(s).",
            "name": "replace_spaces",
            "tests": {
                "python": {"function": "replace_spaces", "language": "python", "cases": [{"args": ["a b c"], "expected": "a_b_c"}]},
                "javascript": {"function": "replaceSpaces", "language": "javascript", "cases": [{"args": ["a b c"], "expected": "a_b_c"}]},
                "csharp": {"function": "ReplaceSpaces", "language": "csharp", "cases": [{"args": ["a b c"], "expected": "a_b_c"}]},
                "java": {"function": "replaceSpaces", "language": "java", "cases": [{"args": ["a b c"], "expected": "a_b_c"}]},
                "php": {"function": "replaceSpaces", "language": "php", "cases": [{"args": ["a b c"], "expected": "a_b_c"}]}
            },
            "starter": {
                "python": "def replace_spaces(s):\n    pass\n",
                "javascript": "function replaceSpaces(s) {\n    \n}\n",
                "csharp": "public string ReplaceSpaces(string s) {\n    return \"\";\n}\n",
                "java": "public static String replaceSpaces(String s) {\n    return \"\";\n}\n",
                "php": "function replaceSpaces($s) {\n    \n}\n"
            }
        }
    },
    "hard": {
        1: {
            "ru": "Экзамен: функция find_duplicates(lst), возвращающая элементы, которые встречаются более одного раза.",
            "en": "Exam: find_duplicates(lst) returning elements that appear more than once.",
            "kz": "Емтихан: бірнеше рет кездесетін элементтерді қайтаратын find_duplicates(lst).",
            "name": "find_duplicates",
            "tests": {
                "python": {"function": "find_duplicates", "language": "python", "cases": [{"args": [[1, 2, 2, 3, 1]], "expected": [1, 2]}]},
                "javascript": {"function": "findDuplicates", "language": "javascript", "cases": [{"args": [[1, 2, 2, 3, 1]], "expected": [1, 2]}]},
                "csharp": {"function": "FindDuplicates", "language": "csharp", "cases": [{"args": [[1, 2, 2, 3, 1]], "expected": [1, 2]}]},
                "java": {"function": "findDuplicates", "language": "java", "cases": [{"args": [[1, 2, 2, 3, 1]], "expected": [1, 2]}]},
                "php": {"function": "findDuplicates", "language": "php", "cases": [{"args": [[1, 2, 2, 3, 1]], "expected": [1, 2]}]}
            },
            "starter": {
                "python": "def find_duplicates(lst):\n    pass\n",
                "javascript": "function findDuplicates(lst) {\n    \n}\n",
                "csharp": "public int[] FindDuplicates(int[] lst) {\n    return new int[0];\n}\n",
                "java": "public static int[] findDuplicates(int[] lst) {\n    return new int[0];\n}\n",
                "php": "function findDuplicates($lst) {\n    \n}\n"
            }
        },
        2: {
            "ru": "Экзамен: функция is_prime(n), возвращающая true если число простое.",
            "en": "Exam: is_prime(n) returning true if the number is prime.",
            "kz": "Емтихан: сан жай болса true қайтаратын is_prime(n).",
            "name": "is_prime",
            "tests": {
                "python": {"function": "is_prime", "language": "python", "cases": [{"args": [7], "expected": True}, {"args": [10], "expected": False}]},
                "javascript": {"function": "isPrime", "language": "javascript", "cases": [{"args": [7], "expected": True}, {"args": [10], "expected": False}]},
                "csharp": {"function": "IsPrime", "language": "csharp", "cases": [{"args": [7], "expected": True}, {"args": [10], "expected": False}]},
                "java": {"function": "isPrime", "language": "java", "cases": [{"args": [7], "expected": True}, {"args": [10], "expected": False}]},
                "php": {"function": "isPrime", "language": "php", "cases": [{"args": [7], "expected": True}, {"args": [10], "expected": False}]}
            },
            "starter": {
                "python": "def is_prime(n):\n    pass\n",
                "javascript": "function isPrime(n) {\n    \n}\n",
                "csharp": "public bool IsPrime(int n) {\n    return false;\n}\n",
                "java": "public static boolean isPrime(int n) {\n    return false;\n}\n",
                "php": "function isPrime($n) {\n    \n}\n"
            }
        },
        3: {
            "ru": "Экзамен: функция second_largest(lst), возвращающая второе по величине число.",
            "en": "Exam: second_largest(lst) returning the second largest number.",
            "kz": "Емтихан: екінші ең үлкен санды қайтаратын second_largest(lst).",
            "name": "second_largest",
            "tests": {
                "python": {"function": "second_largest", "language": "python", "cases": [{"args": [[1, 5, 3, 4]], "expected": 4}]},
                "javascript": {"function": "secondLargest", "language": "javascript", "cases": [{"args": [[1, 5, 3, 4]], "expected": 4}]},
                "csharp": {"function": "SecondLargest", "language": "csharp", "cases": [{"args": [[1, 5, 3, 4]], "expected": 4}]},
                "java": {"function": "secondLargest", "language": "java", "cases": [{"args": [[1, 5, 3, 4]], "expected": 4}]},
                "php": {"function": "secondLargest", "language": "php", "cases": [{"args": [[1, 5, 3, 4]], "expected": 4}]}
            },
            "starter": {
                "python": "def second_largest(lst):\n    pass\n",
                "javascript": "function secondLargest(lst) {\n    \n}\n",
                "csharp": "public int SecondLargest(int[] lst) {\n    return 0;\n}\n",
                "java": "public static int secondLargest(int[] lst) {\n    return 0;\n}\n",
                "php": "function secondLargest($lst) {\n    \n}\n"
            }
        }
    }
}

for lang_code, lang_name in LANGUAGES:
    for diff_code, diff_ru, diff_en, diff_kz, _ in DIFFICULTIES:
        for order_num in range(1, 4):
            task = EXAM_QUESTIONS[diff_code][order_num]
            
            task_ru = escape_sql_string(task["ru"])
            task_en = escape_sql_string(task["en"])
            task_kz = escape_sql_string(task["kz"])
            
            starter = escape_sql_string(task["starter"][lang_code])
            tests = escape_sql_string(json.dumps(task["tests"][lang_code]))
            
            sql = f"""
INSERT INTO exam_questions (exam_id, order_num, task_text_ru, task_text_en, task_text_kz, starter_code, tests, language_id)
SELECT e.id, {order_num}, {task_ru}, {task_en}, {task_kz}, {starter}, {tests}::jsonb, (SELECT id FROM languages WHERE code = '{lang_code}')
FROM exams e
JOIN exam_difficulty_blocks edb ON edb.exam_id = e.id
JOIN tracks tr ON tr.id = edb.track_id
JOIN languages l ON l.id = tr.language_id
WHERE e.exam_type = 'difficulty_block' AND l.code = '{lang_code}' AND edb.difficulty_id = {get_diff_id_sql(diff_code)}
ON CONFLICT DO NOTHING;
"""
            sql_lines.append(sql.strip())


sql_lines.append("""
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
""")

with open("c:/Users/semik/OneDrive/Desktop/Диплом/ai-academy-backend-v2/database/seed.sql", "w", encoding="utf-8") as f:
    f.write("\n".join(sql_lines))
    f.write("\n")

print("Generated seed.sql successfully.")
