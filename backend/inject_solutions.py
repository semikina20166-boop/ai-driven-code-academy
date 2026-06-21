import json

SOLUTIONS = {
    "easy": {
        1: {
            "python": "def sum_two(a, b):\n    return a + b",
            "javascript": "function sumTwo(a, b) {\n    return a + b;\n}",
            "csharp": "public int SumTwo(int a, int b) {\n    return a + b;\n}",
            "java": "public static int sumTwo(int a, int b) {\n    return a + b;\n}",
            "php": "function sumTwo($a, $b) {\n    return $a + $b;\n}"
        },
        2: {
            "python": "def is_even(n):\n    return n % 2 == 0",
            "javascript": "function isEven(n) {\n    return n % 2 === 0;\n}",
            "csharp": "public bool IsEven(int n) {\n    return n % 2 == 0;\n}",
            "java": "public static boolean isEven(int n) {\n    return n % 2 == 0;\n}",
            "php": "function isEven($n) {\n    return $n % 2 == 0;\n}"
        },
        3: {
            "python": "def max_of_two(a, b):\n    if a > b:\n        return a\n    return b",
            "javascript": "function maxOfTwo(a, b) {\n    if (a > b) return a;\n    return b;\n}",
            "csharp": "public int MaxOfTwo(int a, int b) {\n    if (a > b) return a;\n    return b;\n}",
            "java": "public static int maxOfTwo(int a, int b) {\n    if (a > b) return a;\n    return b;\n}",
            "php": "function maxOfTwo($a, $b) {\n    if ($a > $b) return $a;\n    return $b;\n}"
        },
        4: {
            "python": "def factorial(n):\n    result = 1\n    for i in range(1, n + 1):\n        result *= i\n    return result",
            "javascript": "function factorial(n) {\n    let result = 1;\n    for (let i = 1; i <= n; i++) {\n        result *= i;\n    }\n    return result;\n}",
            "csharp": "public int Factorial(int n) {\n    int result = 1;\n    for (int i = 1; i <= n; i++) {\n        result *= i;\n    }\n    return result;\n}",
            "java": "public static int factorial(int n) {\n    int result = 1;\n    for (int i = 1; i <= n; i++) {\n        result *= i;\n    }\n    return result;\n}",
            "php": "function factorial($n) {\n    $result = 1;\n    for ($i = 1; $i <= $n; $i++) {\n        $result *= $i;\n    }\n    return $result;\n}"
        },
        5: {
            "python": "def reverse_string(s):\n    return s[::-1]",
            "javascript": "function reverseString(s) {\n    return s.split('').reverse().join('');\n}",
            "csharp": "public string ReverseString(string s) {\n    char[] arr = s.ToCharArray();\n    Array.Reverse(arr);\n    return new string(arr);\n}",
            "java": "public static String reverseString(String s) {\n    return new StringBuilder(s).reverse().toString();\n}",
            "php": "function reverseString($s) {\n    return strrev($s);\n}"
        }
    },
    "medium": {
        1: {
            "python": "def sum_list(lst):\n    total = 0\n    for num in lst:\n        total += num\n    return total",
            "javascript": "function sumList(lst) {\n    let total = 0;\n    for (let num of lst) {\n        total += num;\n    }\n    return total;\n}",
            "csharp": "public int SumList(int[] lst) {\n    int total = 0;\n    foreach (int num in lst) {\n        total += num;\n    }\n    return total;\n}",
            "java": "public static int sumList(int[] lst) {\n    int total = 0;\n    for (int num : lst) {\n        total += num;\n    }\n    return total;\n}",
            "php": "function sumList($lst) {\n    $total = 0;\n    foreach ($lst as $num) {\n        $total += $num;\n    }\n    return $total;\n}"
        },
        2: {
            "python": "def count_vowels(s):\n    count = 0\n    for char in s.lower():\n        if char in 'aeiou':\n            count += 1\n    return count",
            "javascript": "function countVowels(s) {\n    let count = 0;\n    for (let char of s.toLowerCase()) {\n        if ('aeiou'.includes(char)) count++;\n    }\n    return count;\n}",
            "csharp": "public int CountVowels(string s) {\n    int count = 0;\n    foreach (char c in s.ToLower()) {\n        if (\"aeiou\".Contains(c)) count++;\n    }\n    return count;\n}",
            "java": "public static int countVowels(String s) {\n    int count = 0;\n    for (char c : s.toLowerCase().toCharArray()) {\n        if (\"aeiou\".indexOf(c) != -1) count++;\n    }\n    return count;\n}",
            "php": "function countVowels($s) {\n    $count = 0;\n    $s = strtolower($s);\n    for ($i = 0; $i < strlen($s); $i++) {\n        if (strpos('aeiou', $s[$i]) !== false) $count++;\n    }\n    return $count;\n}"
        },
        3: {
            "python": "def fizzbuzz(n):\n    if n % 15 == 0:\n        return 'FizzBuzz'\n    elif n % 3 == 0:\n        return 'Fizz'\n    elif n % 5 == 0:\n        return 'Buzz'\n    return str(n)",
            "javascript": "function fizzbuzz(n) {\n    if (n % 15 === 0) return 'FizzBuzz';\n    if (n % 3 === 0) return 'Fizz';\n    if (n % 5 === 0) return 'Buzz';\n    return String(n);\n}",
            "csharp": "public string Fizzbuzz(int n) {\n    if (n % 15 == 0) return \"FizzBuzz\";\n    if (n % 3 == 0) return \"Fizz\";\n    if (n % 5 == 0) return \"Buzz\";\n    return n.ToString();\n}",
            "java": "public static String fizzbuzz(int n) {\n    if (n % 15 == 0) return \"FizzBuzz\";\n    if (n % 3 == 0) return \"Fizz\";\n    if (n % 5 == 0) return \"Buzz\";\n    return String.valueOf(n);\n}",
            "php": "function fizzbuzz($n) {\n    if ($n % 15 == 0) return 'FizzBuzz';\n    if ($n % 3 == 0) return 'Fizz';\n    if ($n % 5 == 0) return 'Buzz';\n    return (string)$n;\n}"
        },
        4: {
            "python": "def is_palindrome(s):\n    return s == s[::-1]",
            "javascript": "function isPalindrome(s) {\n    return s === s.split('').reverse().join('');\n}",
            "csharp": "public bool IsPalindrome(string s) {\n    char[] arr = s.ToCharArray();\n    Array.Reverse(arr);\n    return s == new string(arr);\n}",
            "java": "public static boolean isPalindrome(String s) {\n    return s.equals(new StringBuilder(s).reverse().toString());\n}",
            "php": "function isPalindrome($s) {\n    return $s === strrev($s);\n}"
        },
        5: {
            "python": "def binary_search(arr, target):\n    left, right = 0, len(arr) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1",
            "javascript": "function binarySearch(arr, target) {\n    let left = 0, right = arr.length - 1;\n    while (left <= right) {\n        let mid = Math.floor((left + right) / 2);\n        if (arr[mid] === target) return mid;\n        if (arr[mid] < target) left = mid + 1;\n        else right = mid - 1;\n    }\n    return -1;\n}",
            "csharp": "public int BinarySearch(int[] arr, int target) {\n    int left = 0, right = arr.Length - 1;\n    while (left <= right) {\n        int mid = left + (right - left) / 2;\n        if (arr[mid] == target) return mid;\n        if (arr[mid] < target) left = mid + 1;\n        else right = mid - 1;\n    }\n    return -1;\n}",
            "java": "public static int binarySearch(int[] arr, int target) {\n    int left = 0, right = arr.length - 1;\n    while (left <= right) {\n        int mid = left + (right - left) / 2;\n        if (arr[mid] == target) return mid;\n        if (arr[mid] < target) left = mid + 1;\n        else right = mid - 1;\n    }\n    return -1;\n}",
            "php": "function binarySearch($arr, $target) {\n    $left = 0;\n    $right = count($arr) - 1;\n    while ($left <= $right) {\n        $mid = (int)(($left + $right) / 2);\n        if ($arr[$mid] == $target) return $mid;\n        if ($arr[$mid] < $target) $left = $mid + 1;\n        else $right = $mid - 1;\n    }\n    return -1;\n}"
        }
    },
    "hard": {
        1: {
            "python": "def fibonacci(n):\n    if n <= 1:\n        return n\n    a, b = 0, 1\n    for _ in range(2, n + 1):\n        a, b = b, a + b\n    return b",
            "javascript": "function fibonacci(n) {\n    if (n <= 1) return n;\n    let a = 0, b = 1;\n    for (let i = 2; i <= n; i++) {\n        let temp = a + b;\n        a = b;\n        b = temp;\n    }\n    return b;\n}",
            "csharp": "public int Fibonacci(int n) {\n    if (n <= 1) return n;\n    int a = 0, b = 1;\n    for (int i = 2; i <= n; i++) {\n        int temp = a + b;\n        a = b;\n        b = temp;\n    }\n    return b;\n}",
            "java": "public static int fibonacci(int n) {\n    if (n <= 1) return n;\n    int a = 0, b = 1;\n    for (int i = 2; i <= n; i++) {\n        int temp = a + b;\n        a = b;\n        b = temp;\n    }\n    return b;\n}",
            "php": "function fibonacci($n) {\n    if ($n <= 1) return $n;\n    $a = 0; $b = 1;\n    for ($i = 2; $i <= $n; $i++) {\n        $temp = $a + $b;\n        $a = $b;\n        $b = $temp;\n    }\n    return $b;\n}"
        },
        2: {
            "python": "def unique_elements(lst):\n    return list(set(lst))",
            "javascript": "function uniqueElements(lst) {\n    return [...new Set(lst)];\n}",
            "csharp": "public int[] UniqueElements(int[] lst) {\n    return lst.Distinct().ToArray();\n}",
            "java": "public static int[] uniqueElements(int[] lst) {\n    return java.util.Arrays.stream(lst).distinct().toArray();\n}",
            "php": "function uniqueElements($lst) {\n    return array_values(array_unique($lst));\n}"
        },
        3: {
            "python": "def merge_sorted(a, b):\n    i, j, result = 0, 0, []\n    while i < len(a) and j < len(b):\n        if a[i] < b[j]:\n            result.append(a[i])\n            i += 1\n        else:\n            result.append(b[j])\n            j += 1\n    result.extend(a[i:])\n    result.extend(b[j:])\n    return result",
            "javascript": "function mergeSorted(a, b) {\n    let i = 0, j = 0, result = [];\n    while (i < a.length && j < b.length) {\n        if (a[i] < b[j]) result.push(a[i++]);\n        else result.push(b[j++]);\n    }\n    while (i < a.length) result.push(a[i++]);\n    while (j < b.length) result.push(b[j++]);\n    return result;\n}",
            "csharp": "public int[] MergeSorted(int[] a, int[] b) {\n    int[] result = new int[a.Length + b.Length];\n    int i = 0, j = 0, k = 0;\n    while (i < a.Length && j < b.Length) {\n        if (a[i] < b[j]) result[k++] = a[i++];\n        else result[k++] = b[j++];\n    }\n    while (i < a.Length) result[k++] = a[i++];\n    while (j < b.Length) result[k++] = b[j++];\n    return result;\n}",
            "java": "public static int[] mergeSorted(int[] a, int[] b) {\n    int[] result = new int[a.length + b.length];\n    int i = 0, j = 0, k = 0;\n    while (i < a.length && j < b.length) {\n        if (a[i] < b[j]) result[k++] = a[i++];\n        else result[k++] = b[j++];\n    }\n    while (i < a.length) result[k++] = a[i++];\n    while (j < b.length) result[k++] = b[j++];\n    return result;\n}",
            "php": "function mergeSorted($a, $b) {\n    $result = [];\n    $i = 0; $j = 0;\n    while ($i < count($a) && $j < count($b)) {\n        if ($a[$i] < $b[$j]) $result[] = $a[$i++];\n        else $result[] = $b[$j++];\n    }\n    while ($i < count($a)) $result[] = $a[$i++];\n    while ($j < count($b)) $result[] = $b[$j++];\n    return $result;\n}"
        },
        4: {
            "python": "def bubble_sort(lst):\n    n = len(lst)\n    for i in range(n):\n        for j in range(0, n-i-1):\n            if lst[j] > lst[j+1]:\n                lst[j], lst[j+1] = lst[j+1], lst[j]\n    return lst",
            "javascript": "function bubbleSort(lst) {\n    let len = lst.length;\n    for (let i = 0; i < len; i++) {\n        for (let j = 0; j < len - i - 1; j++) {\n            if (lst[j] > lst[j + 1]) {\n                let temp = lst[j];\n                lst[j] = lst[j + 1];\n                lst[j + 1] = temp;\n            }\n        }\n    }\n    return lst;\n}",
            "csharp": "public int[] BubbleSort(int[] lst) {\n    int len = lst.Length;\n    for (int i = 0; i < len; i++) {\n        for (int j = 0; j < len - i - 1; j++) {\n            if (lst[j] > lst[j + 1]) {\n                int temp = lst[j];\n                lst[j] = lst[j + 1];\n                lst[j + 1] = temp;\n            }\n        }\n    }\n    return lst;\n}",
            "java": "public static int[] bubbleSort(int[] lst) {\n    int len = lst.length;\n    for (int i = 0; i < len; i++) {\n        for (int j = 0; j < len - i - 1; j++) {\n            if (lst[j] > lst[j + 1]) {\n                int temp = lst[j];\n                lst[j] = lst[j + 1];\n                lst[j + 1] = temp;\n            }\n        }\n    }\n    return lst;\n}",
            "php": "function bubbleSort($lst) {\n    $len = count($lst);\n    for ($i = 0; $i < $len; $i++) {\n        for ($j = 0; $j < $len - $i - 1; $j++) {\n            if ($lst[$j] > $lst[$j + 1]) {\n                $temp = $lst[$j];\n                $lst[$j] = $lst[$j + 1];\n                $lst[$j + 1] = $temp;\n            }\n        }\n    }\n    return $lst;\n}"
        },
        5: {
            "python": "def matrix_sum(matrix):\n    total = 0\n    for row in matrix:\n        for num in row:\n            total += num\n    return total",
            "javascript": "function matrixSum(matrix) {\n    let total = 0;\n    for (let row of matrix) {\n        for (let num of row) {\n            total += num;\n        }\n    }\n    return total;\n}",
            "csharp": "public int MatrixSum(int[][] matrix) {\n    int total = 0;\n    foreach (int[] row in matrix) {\n        foreach (int num in row) {\n            total += num;\n        }\n    }\n    return total;\n}",
            "java": "public static int matrixSum(int[][] matrix) {\n    int total = 0;\n    for (int[] row : matrix) {\n        for (int num : row) {\n            total += num;\n        }\n    }\n    return total;\n}",
            "php": "function matrixSum($matrix) {\n    $total = 0;\n    foreach ($matrix as $row) {\n        foreach ($row as $num) {\n            $total += $num;\n        }\n    }\n    return $total;\n}"
        }
    }
}

with open("populate_beautiful_lectures.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the LECTURES dict with code to use SOLUTIONS as well
# Wait, let's just insert SOLUTIONS dict at the top and modify the theory_md formatting string
# to use SOLUTIONS[diff_code][order_num][lang_code]

content = content.replace("f\"```{lang_code}\\n\"", "f\"```{lang_code}\\n\"")
content = content.replace("f\"{starter.strip()}\\n\"", "f\"{SOLUTIONS[diff_code][order_num].get(lang_code, starter.strip())}\\n\"")
content = content.replace("f\"**Синтаксис {lang_name} для этой задачи:**\\n\"", "f\"✅ **Пример решения на {lang_name}:**\\n\"")

new_content = "SOLUTIONS = " + json.dumps(SOLUTIONS, indent=4, ensure_ascii=False) + "\n\n" + content

with open("populate_beautiful_lectures.py", "w", encoding="utf-8") as f:
    f.write(new_content)
