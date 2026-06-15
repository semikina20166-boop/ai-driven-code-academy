import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text, select
from app.config import settings
from sqlalchemy.ext.asyncio import create_async_engine
from app.models import Level, Track, Difficulty, Language
from sqlalchemy.orm import sessionmaker

# 1. Base Topics (Detailed text without code)
# RU, EN, KZ strings
TOPICS = {
    "easy": [
        # Lesson 1: Variables
        {
            "ru": "### 📖 Лекция: Введение и Переменные\n\nПрограммирование начинается с данных. **Переменная** — это именованная область памяти, предназначенная для хранения данных. Представьте себе коробку с ярлыком, в которую вы можете положить число, текст или любой другой объект. Выделение памяти под переменные — одна из ключевых задач языка программирования. При объявлении переменной вы сообщаете компьютеру: «Зарезервируй мне место и назови его так-то».\n\nСуществуют языки со **строгой статической типизацией** (где тип коробки задается раз и навсегда) и **динамической типизацией** (когда коробка может менять тип содержимого). Независимо от типизации, переменные являются основой для написания любого алгоритма.\n\nПосмотрите на пример объявления переменной на вашем текущем языке:",
            "en": "### 📖 Lecture: Introduction and Variables\n\nProgramming starts with data. A **variable** is a named area of memory intended for storing data. Imagine a box with a label where you can put a number, text, or any other object. Allocating memory for variables is one of the key tasks of a programming language. When declaring a variable, you tell the computer: 'Reserve a place for me and name it this.'\n\nThere are languages with **strict static typing** (where the type of the box is set once and for all) and **dynamic typing** (when the box can change the type of content). Regardless of typing, variables are the foundation for writing any algorithm.\n\nLook at the example of declaring a variable in your current language:",
            "kz": "### 📖 Дәріс: Кіріспе және Айнымалылар\n\nБағдарламалау деректерден басталады. **Айнымалы** - бұл деректерді сақтауға арналған жадтың аталған аймағы. Ішіне сан, мәтін немесе кез келген басқа нысанды салуға болатын жапсырмасы бар қорапты елестетіңіз. Айнымалыларға жад бөлу - бағдарламалау тілінің негізгі міндеттерінің бірі. Айнымалыны жариялаған кезде сіз компьютерге: «Маған орын бөліп, оны осылай ата» деп айтасыз.\n\n**Қатаң статикалық типтеуі** бар тілдер (мұнда қорап түрі біржолата орнатылады) және **динамикалық типтеуі** бар тілдер (қорап мазмұн түрін өзгерте алатын кезде) бар. Типтеуге қарамастан, айнымалылар кез келген алгоритмді жазудың негізі болып табылады.\n\nАғымдағы тілде айнымалыны жариялау мысалын қараңыз:"
        },
        # Lesson 2: Operations
        {
            "ru": "### 📖 Лекция: Арифметические операции\n\nКогда у нас есть переменные, мы хотим ими манипулировать. **Арифметические операторы** (+, -, *, /) позволяют выполнять базовые математические действия. Но программирование идет дальше математики: оператор `=` означает **присваивание**, а не равенство! Выражение `x = x + 1` математически абсурдно, но в коде оно означает: «Возьми текущее значение x, прибавь к нему 1 и положи обратно в x».\n\nПомимо математики, существуют **логические операторы** (И, ИЛИ, НЕ), которые работают с истиной и ложью (boolean). Они лежат в основе работы любого процессора на уровне логических вентилей. В высокоуровневых языках они позволяют строить сложные проверки.",
            "en": "### 📖 Lecture: Arithmetic Operations\n\nWhen we have variables, we want to manipulate them. **Arithmetic operators** (+, -, *, /) allow you to perform basic mathematical operations. But programming goes beyond mathematics: the `=` operator means **assignment**, not equality! The expression `x = x + 1` is mathematically absurd, but in code it means: 'Take the current value of x, add 1 to it and put it back in x.'\n\nIn addition to mathematics, there are **logical operators** (AND, OR, NOT) that work with true and false (boolean). They are the basis of any processor's operation at the level of logic gates. In high-level languages, they allow building complex checks.",
            "kz": "### 📖 Дәріс: Арифметикалық амалдар\n\nБізде айнымалылар болған кезде, біз оларды басқарғымыз келеді. **Арифметикалық операторлар** (+, -, *, /) негізгі математикалық амалдарды орындауға мүмкіндік береді. Бірақ бағдарламалау математикадан асып түседі: `=` операторы теңдікті емес, **меншіктеуді** білдіреді! `x = x + 1` өрнегі математикалық тұрғыдан мағынасыз, бірақ кодта ол былай дейді: «x-тің ағымдағы мәнін ал, оған 1 қосып, x-ке қайта сал».\n\nМатематикадан басқа, шындық пен жалғандықпен (boolean) жұмыс істейтін **логикалық операторлар** (ЖӘНЕ, НЕМЕСЕ, ЕМЕС) бар. Олар логикалық қақпалар деңгейіндегі кез келген процессор жұмысының негізі болып табылады."
        },
        # Lesson 3: Conditionals
        {
            "ru": "### 📖 Лекция: Условные конструкции (if-else)\n\nПрограммы были бы скучными, если бы всегда выполняли одни и те же действия. **Ветвление** (условный оператор) позволяет программе принимать решения на основе данных. Мы используем конструкции `if`, `else if` и `else`.\n\nПод капотом компьютер вычисляет условие, и если оно возвращает `True`, процессор переходит к соответствующему блоку инструкций. Если `False` — пропускает его. Это называется **потоком управления** (control flow).\n\nВажно помнить про область видимости: переменные, созданные внутри блока `if`, могут быть недоступны за его пределами (в зависимости от языка).",
            "en": "### 📖 Lecture: Conditional Statements (if-else)\n\nPrograms would be boring if they always performed the same actions. **Branching** (conditional statement) allows the program to make decisions based on data. We use the constructs `if`, `else if`, and `else`.\n\nUnder the hood, the computer evaluates the condition, and if it returns `True`, the processor moves to the corresponding block of instructions. If `False` - it skips it. This is called **control flow**.\n\nIt is important to remember about scope: variables created inside the `if` block may not be accessible outside of it (depending on the language).",
            "kz": "### 📖 Дәріс: Шартты құрылымдар (if-else)\n\nЕгер бағдарламалар әрқашан бірдей әрекеттерді орындаса, олар қызықсыз болар еді. **Тармақталу** (шартты оператор) бағдарламаға деректер негізінде шешім қабылдауға мүмкіндік береді. Біз `if`, `else if` және `else` құрылымдарын қолданамыз.\n\nКапот астында компьютер шартты есептейді, егер ол `True` қайтарса, процессор тиісті нұсқаулықтар блогына өтеді. Егер `False` болса — оны өткізіп жібереді. Бұл **басқару ағыны** (control flow) деп аталады."
        },
        # Lesson 4: Loops
        {
            "ru": "### 📖 Лекция: Циклы\n\nГлавная сила компьютеров — в автоматизации рутины. **Циклы** позволяют выполнять блок кода многократно, пока выполняется определенное условие. \n\nВ программировании чаще всего встречаются два вида циклов:\n1. **Цикл с предусловием (`while`)**: выполняется, пока условие истинно. Отлично подходит, когда мы не знаем заранее, сколько шагов нужно сделать.\n2. **Цикл со счетчиком (`for`)**: идеально подходит для перебора коллекций или когда известно точное количество итераций.\n\nОстерегайтесь *бесконечных циклов*! Если условие выхода никогда не выполнится, программа зависнет навсегда, потребляя 100% процессора.",
            "en": "### 📖 Lecture: Loops\n\nThe main power of computers is in automating routine. **Loops** allow you to execute a block of code multiple times as long as a certain condition is met.\n\nIn programming, two types of loops are most common:\n1. **Precondition loop (`while`)**: executes while the condition is true. Great for when we don't know exactly how many steps to take in advance.\n2. **Counter loop (`for`)**: ideal for iterating over collections or when the exact number of iterations is known.\n\nBeware of *infinite loops*! If the exit condition is never met, the program will hang forever, consuming 100% of the CPU.",
            "kz": "### 📖 Дәріс: Циклдер\n\nКомпьютерлердің негізгі күші - рутинаны автоматтандыруда. **Циклдер** белгілі бір шарт орындалғанша код блогын бірнеше рет орындауға мүмкіндік береді.\n\nБағдарламалауда циклдердің екі түрі жиі кездеседі:\n1. **Алғы шартты цикл (`while`)**: шарт ақиқат болған кезде орындалады. Қанша қадам жасау керектігін алдын ала білмеген кезде тамаша.\n2. **Есептегіші бар цикл (`for`)**: топтамаларды қайталау үшін немесе итерациялардың нақты саны белгілі болған кезде өте қолайлы.\n\n*Шексіз циклдерден* сақ болыңыз! Егер шығу шарты ешқашан орындалмаса, бағдарлама процессордың 100% тұтынып, мәңгілікке қатып қалады."
        },
        # Lesson 5: Functions
        {
            "ru": "### 📖 Лекция: Функции\n\nПо мере роста программы, код становится сложно читать. **Функция** — это именованный блок кода, который решает одну конкретную задачу. Это способ создать собственную мини-программу внутри большой программы.\n\nПреимущества функций:\n- **Повторное использование (DRY)**: напиши один раз, используй везде.\n- **Читаемость**: вызов `calculate_tax()` понятнее, чем 10 строк математики.\n- **Изоляция**: переменные внутри функции живут только во время ее работы (локальная область видимости).\n\nФункция принимает **аргументы** (входные данные) и возвращает **результат** (output).",
            "en": "### 📖 Lecture: Functions\n\nAs the program grows, the code becomes difficult to read. A **function** is a named block of code that solves one specific task. It's a way to create your own mini-program inside a larger program.\n\nBenefits of functions:\n- **Reuse (DRY)**: write once, use everywhere.\n- **Readability**: calling `calculate_tax()` is clearer than 10 lines of math.\n- **Isolation**: variables inside a function live only during its execution (local scope).\n\nA function takes **arguments** (input data) and returns a **result** (output).",
            "kz": "### 📖 Дәріс: Функциялар\n\nБағдарлама өскен сайын кодты оқу қиындай түседі. **Функция** - бұл бір нақты тапсырманы шешетін аталған код блогы. Бұл үлкен бағдарламаның ішінде өзіңіздің шағын бағдарламаңызды құрудың жолы.\n\nФункциялардың артықшылықтары:\n- **Қайта пайдалану (DRY)**: бір рет жазыңыз, барлық жерде қолданыңыз.\n- **Оқылымдылық**: `calculate_tax()` шақыру 10 жол математикаға қарағанда түсінікті.\n- **Оқшаулау**: функция ішіндегі айнымалылар тек оның жұмысы кезінде өмір сүреді (жергілікті аумақ).\n\nФункция **аргументтерді** (кіріс деректер) қабылдайды және **нәтижені** (output) қайтарады."
        }
    ],
    "medium": [
        # Lesson 1: Arrays
        {
            "ru": "### 📖 Лекция: Массивы и Списки\n\nЕсли переменная — это коробка, то **массив** — это длинный стеллаж с пронумерованными ячейками. Массивы позволяют хранить тысячи элементов под одним именем.\n\nДоступ к элементам осуществляется по **индексу**, который в программировании почти всегда начинается с нуля (0). Это связано с тем, что индекс изначально означал смещение памяти от начала массива.\n\nСовременные языки предоставляют продвинутые списки, которые могут динамически изменять свой размер, добавлять и удалять элементы на лету.",
            "en": "### 📖 Lecture: Arrays and Lists\n\nIf a variable is a box, then an **array** is a long rack with numbered cells. Arrays allow you to store thousands of elements under one name.\n\nAccess to elements is done by **index**, which in programming almost always starts from zero (0). This is because the index originally meant the memory offset from the beginning of the array.\n\nModern languages provide advanced lists that can dynamically resize, add and remove elements on the fly.",
            "kz": "### 📖 Дәріс: Массивтер мен тізімдер\n\nЕгер айнымалы қорап болса, онда **массив** - нөмірленген ұяшықтары бар ұзын сөре. Массивтер бір атаумен мыңдаған элементтерді сақтауға мүмкіндік береді.\n\nЭлементтерге қол жеткізу **индекс** арқылы жүзеге асырылады, ол бағдарламалауда дерлік әрқашан нөлден (0) басталады. Себебі индекс бастапқыда массивтің басынан жадтың ығысуын білдірді.\n\nЗаманауи тілдер өлшемін динамикалық түрде өзгерте алатын, элементтерді жылдам қосып, өшіре алатын жетілдірілген тізімдерді ұсынады."
        },
        # Lesson 2: Dictionaries / Objects
        {
            "ru": "### 📖 Лекция: Словари и Хэш-таблицы\n\nМассивы удобны, если у нас есть порядок. Но что если нам нужно найти пользователя по его ID? Искать в массиве долго. На помощь приходят **Словари (Ассоциативные массивы, Hash Maps, Объекты)**.\n\nОни хранят данные в формате `Ключ: Значение`. Под капотом используется сложная математика хеширования, позволяющая мгновенно находить значение по ключу, даже если в словаре миллион записей. Обычные ключи — это строки или числа.",
            "en": "### 📖 Lecture: Dictionaries and Hash Tables\n\nArrays are handy if we have an order. But what if we need to find a user by their ID? Searching an array takes a long time. This is where **Dictionaries (Associative arrays, Hash Maps, Objects)** come to the rescue.\n\nThey store data in a `Key: Value` format. Under the hood, complex hashing math is used, allowing you to instantly find a value by a key, even if there are a million records in the dictionary. Common keys are strings or numbers.",
            "kz": "### 📖 Дәріс: Сөздіктер және Хэш-кестелер\n\nМассивтер тәртіп болған кезде ыңғайлы. Бірақ пайдаланушыны оның ID бойынша табу керек болса ше? Массивтен іздеу көп уақыт алады. Мұнда **Сөздіктер (Ассоциативті массивтер, Hash Maps, Нысандар)** көмекке келеді.\n\nОлар деректерді `Кілт: Мән` пішімінде сақтайды. Капоттың астында сөздікте миллион жазба болса да, кілт бойынша мәнді лезде табуға мүмкіндік беретін күрделі хэштеу математикасы қолданылады. Кәдімгі кілттер - жолдар немесе сандар."
        },
        # Lesson 3: Strings & Regex
        {
            "ru": "### 📖 Лекция: Работа со строками\n\nТекст в программировании представлен типом **String** (Строка). Это неизменяемый массив символов. Для работы со строками есть мощные встроенные методы: поиск подстроки, замена, разбиение на слова.\n\nДля очень сложного поиска программисты используют **Регулярные выражения (Regex)** — это своеобразный язык внутри языка, который позволяет описывать шаблоны текста. Например, проверить, является ли строка корректным email адресом.",
            "en": "### 📖 Lecture: Working with Strings\n\nText in programming is represented by the **String** type. It is an immutable array of characters. There are powerful built-in methods for working with strings: substring search, replacement, splitting into words.\n\nFor very complex searches, programmers use **Regular expressions (Regex)** - this is a kind of language within a language that allows you to describe text patterns. For example, to check if a string is a valid email address.",
            "kz": "### 📖 Дәріс: Жолдармен жұмыс (Strings)\n\nБағдарламалаудағы мәтін **String** (Жол) түрімен ұсынылған. Бұл таңбалардың өзгермейтін массиві. Жолдармен жұмыс істеуге арналған қуатты кірістірілген әдістер бар: ішкі жолды іздеу, ауыстыру, сөздерге бөлу.\n\nӨте күрделі іздеу үшін бағдарламашылар **Тұрақты өрнектерді (Regex)** пайдаланады - бұл мәтін үлгілерін сипаттауға мүмкіндік беретін тіл ішіндегі тіл. Мысалы, жолдың жарамды email мекенжайы екенін тексеру үшін."
        },
        # Lesson 4: Exceptions
        {
            "ru": "### 📖 Лекция: Обработка ошибок (Exceptions)\n\nНи одна программа не работает идеально. Сервер может упасть, файл может не существовать, пользователь может ввести буквы вместо цифр. \n\nЕсли не перехватить ошибку, программа аварийно завершится (crash). **Исключения (Exceptions)** позволяют элегантно перехватывать ошибки с помощью конструкции `try/catch`. Код, который может сломаться, оборачивается в блок `try`. Если происходит ошибка, выполнение передается в блок `catch`, где мы можем корректно обработать ситуацию.",
            "en": "### 📖 Lecture: Error Handling (Exceptions)\n\nNo program works perfectly. A server might crash, a file might not exist, a user might enter letters instead of numbers.\n\nIf you don't catch an error, the program will crash. **Exceptions** allow you to elegantly catch errors using the `try/catch` construct. Code that might break is wrapped in a `try` block. If an error occurs, execution is passed to the `catch` block, where we can properly handle the situation.",
            "kz": "### 📖 Дәріс: Қателерді өңдеу (Exceptions)\n\nЕшбір бағдарлама мінсіз жұмыс істемейді. Сервер істен шығуы мүмкін, файл болмауы мүмкін, пайдаланушы сандардың орнына әріптер енгізуі мүмкін.\n\nЕгер қатені ұстамасаңыз, бағдарлама апатты түрде жабылады (crash). **Ерекшеліктер (Exceptions)** `try/catch` құрылымын пайдаланып қателерді талғампаз түрде ұстауға мүмкіндік береді. Бұзылуы мүмкін код `try` блогына оралады. Егер қате орын алса, орындалу `catch` блогына беріледі, онда біз жағдайды дұрыс өңдей аламыз."
        },
        # Lesson 5: Intro OOP
        {
            "ru": "### 📖 Лекция: Введение в ООП\n\n**Объектно-ориентированное программирование (ООП)** — это парадигма, где мы моделируем реальный мир в коде. Главные понятия: **Класс** и **Объект**.\n\nКласс — это чертеж. Например, «Автомобиль». Объект — это конкретная реализация чертежа. Например, «Красная Toyota Camry». \nУ классов есть *Поля (свойства)* — это переменные внутри класса (цвет, марка). И *Методы* — это функции внутри класса (завести мотор, поехать).",
            "en": "### 📖 Lecture: Intro to OOP\n\n**Object-Oriented Programming (OOP)** is a paradigm where we model the real world in code. Main concepts: **Class** and **Object**.\n\nA class is a blueprint. For example, 'Car'. An object is a specific realization of the blueprint. For example, 'Red Toyota Camry'.\nClasses have *Fields (properties)* - these are variables inside the class (color, brand). And *Methods* - these are functions inside the class (start engine, drive).",
            "kz": "### 📖 Дәріс: ООП-қа кіріспе\n\n**Объектіге бағытталған бағдарламалау (ООП)** - бұл нақты әлемді кодта модельдейтін парадигма. Негізгі ұғымдар: **Класс** және **Объект**.\n\nКласс - бұл сызба. Мысалы, «Автомобиль». Объект - бұл сызбаның нақты жүзеге асырылуы. Мысалы, «Қызыл Toyota Camry».\nКласстарда *Өрістер (қасиеттер)* бар - бұл класс ішіндегі айнымалылар (түсі, маркасы). Және *Әдістер* - бұл класс ішіндегі функциялар (қозғалтқышты іске қосу, жүру)."
        }
    ],
    "hard": [
        # Lesson 1: Inheritance
        {
            "ru": "### 📖 Лекция: Наследование и Полиморфизм\n\n**Наследование** позволяет создать новый класс на основе существующего. Класс-наследник получает все свойства и методы родителя, но может добавить свои или изменить старые. Например, класс `Bird` наследует `Animal`, но добавляет метод `fly()`.\n\n**Полиморфизм** («множество форм») позволяет работать с разными объектами через единый интерфейс. Если у нас есть массив разных Животных, мы можем вызвать у всех `makeSound()`, и собака гавкнет, а кот мяукнет, хотя код вызова один и тот же.",
            "en": "### 📖 Lecture: Inheritance and Polymorphism\n\n**Inheritance** allows you to create a new class based on an existing one. The child class receives all the properties and methods of the parent, but can add its own or change the old ones. For example, the `Bird` class inherits from `Animal`, but adds the `fly()` method.\n\n**Polymorphism** ('many forms') allows working with different objects through a single interface. If we have an array of different Animals, we can call `makeSound()` on all of them, and the dog will bark, and the cat will meow, even though the calling code is the same.",
            "kz": "### 📖 Дәріс: Мұрагерлік және Полиморфизм\n\n**Мұрагерлік** бар класс негізінде жаңа класс құруға мүмкіндік береді. Мұрагер класс ата-ананың барлық қасиеттері мен әдістерін алады, бірақ өзінікін қоса алады немесе ескілерін өзгерте алады. Мысалы, `Bird` класы `Animal` класын мұра етеді, бірақ `fly()` әдісін қосады.\n\n**Полиморфизм** («көптеген формалар») әртүрлі объектілермен бірыңғай интерфейс арқылы жұмыс істеуге мүмкіндік береді. Егер бізде әртүрлі Жануарлар массиві болса, біз олардың барлығында `makeSound()` шақыра аламыз, ал шақыру коды бірдей болса да, ит үреді, ал мысық мияулайды."
        },
        # Lesson 2: Advanced Data Structures
        {
            "ru": "### 📖 Лекция: Продвинутые структуры данных\n\nМассивы и хэши — это лишь верхушка айсберга. В продвинутой разработке используются:\n- **Множества (Sets)**: коллекции уникальных элементов. Оптимизированы для проверки «содержит ли коллекция X?», которая происходит за O(1).\n- **Связанные списки (Linked Lists)**: где каждый элемент знает только о следующем. Быстро вставлять в середину, но долго искать.\n- **Деревья и Графы**: используются для моделирования иерархий, социальных сетей и маршрутизации.\nПонимание структур данных — ключ к высокопроизводительному коду.",
            "en": "### 📖 Lecture: Advanced Data Structures\n\nArrays and hashes are just the tip of the iceberg. Advanced development uses:\n- **Sets**: collections of unique elements. Optimized for checking 'does the collection contain X?', which happens in O(1).\n- **Linked Lists**: where each element only knows about the next one. Fast to insert in the middle, but slow to search.\n- **Trees and Graphs**: used to model hierarchies, social networks, and routing.\nUnderstanding data structures is the key to high-performance code.",
            "kz": "### 📖 Дәріс: Кеңейтілген деректер құрылымдары\n\nМассивтер мен хэштер - айсбергтің шыңы ғана. Жетілдірілген әзірлеуде мыналар қолданылады:\n- **Жиындар (Sets)**: бірегей элементтер топтамасы. O(1) уақытында орындалатын «топтамада X бар ма?» тексеруі үшін оңтайландырылған.\n- **Байланысқан тізімдер (Linked Lists)**: әр элемент тек келесісі туралы біледі. Ортасына кірістіру жылдам, бірақ іздеу баяу.\n- **Ағаштар мен Графтар**: иерархияларды, әлеуметтік желілерді және маршруттауды модельдеу үшін қолданылады.\nДеректер құрылымын түсіну - өнімділігі жоғары кодтың кілті."
        },
        # Lesson 3: Functional Programming
        {
            "ru": "### 📖 Лекция: Функциональное программирование\n\n**Функциональное программирование (ФП)** концентрируется на «чистых функциях» без побочных эффектов. В ФП переменные иммутабельны (неизменяемы). Вместо циклов `for` используются функции высшего порядка: `map`, `filter`, `reduce`.\n\n- `map`: применяет функцию к каждому элементу массива, создавая новый массив.\n- `filter`: оставляет только те элементы, для которых функция возвращает истину.\n- `Лямбда-выражения`: безымянные короткие функции, которые можно передавать как аргументы.",
            "en": "### 📖 Lecture: Functional Programming\n\n**Functional Programming (FP)** focuses on 'pure functions' with no side effects. In FP, variables are immutable. Instead of `for` loops, higher-order functions are used: `map`, `filter`, `reduce`.\n\n- `map`: applies a function to each element of an array, creating a new array.\n- `filter`: leaves only those elements for which the function returns true.\n- `Lambda expressions`: unnamed short functions that can be passed as arguments.",
            "kz": "### 📖 Дәріс: Функционалдық бағдарламалау\n\n**Функционалдық бағдарламалау (ФП)** жанама әсерлері жоқ «таза функцияларға» назар аударады. ФП-да айнымалылар өзгермейтін (иммутабельді). `For` циклдерінің орнына жоғары ретті функциялар қолданылады: `map`, `filter`, `reduce`.\n\n- `map`: жаңа массив құра отырып, массивтің әрбір элементіне функцияны қолданады.\n- `filter`: функция ақиқат қайтаратын элементтерді ғана қалдырады.\n- `Лямбда өрнектері`: аргумент ретінде беруге болатын атаусыз қысқа функциялар."
        },
        # Lesson 4: Asynchronous
        {
            "ru": "### 📖 Лекция: Асинхронность\n\nКогда программа делает сетевой запрос (например, качает файл), процессор простаивает миллисекунды. **Асинхронность** позволяет программе не блокироваться, а переключиться на другие задачи, пока файл качается.\n\nСовременный синтаксис — это `async / await`. Функция помечается как `async`, а перед долгой операцией ставится `await`. Это делает код, работающий параллельно с другими процессами, читаемым как обычный синхронный код. Под капотом создается **Event Loop** (цикл событий).",
            "en": "### 📖 Lecture: Asynchrony\n\nWhen a program makes a network request (e.g., downloading a file), the processor idles for milliseconds. **Asynchrony** allows the program not to block, but to switch to other tasks while the file is downloading.\n\nModern syntax is `async / await`. A function is marked as `async`, and `await` is placed before a long operation. This makes code that runs in parallel with other processes readable as regular synchronous code. Under the hood, an **Event Loop** is created.",
            "kz": "### 📖 Дәріс: Асинхрондылық\n\nБағдарлама желілік сұраныс жасағанда (мысалы, файлды жүктеп алу), процессор миллисекундтар бойы бос тұрады. **Асинхрондылық** бағдарламаға бұғатталмауға, бірақ файл жүктеліп жатқанда басқа тапсырмаларға ауысуға мүмкіндік береді.\n\nЗаманауи синтаксис - бұл `async / await`. Функция `async` деп белгіленеді, ал ұзақ операция алдына `await` қойылады. Бұл басқа процестермен параллель жұмыс істейтін кодты кәдімгі синхронды код ретінде оқуға мүмкіндік береді. Капоттың астында **Event Loop** (оқиғалар циклі) құрылады."
        },
        # Lesson 5: Design Patterns
        {
            "ru": "### 📖 Лекция: Паттерны проектирования\n\nКогда вы пишете большие приложения, вы сталкиваетесь с архитектурными проблемами. **Паттерны проектирования** — это готовые решения частых проблем архитектуры.\n\nПопулярные паттерны:\n- **Singleton (Одиночка)**: гарантирует, что у класса есть только один экземпляр (например, подключение к БД).\n- **Factory (Фабрика)**: инкапсулирует логику создания сложных объектов.\n- **Observer (Наблюдатель)**: позволяет одним объектам подписываться на события других (основа многих UI-фреймворков).\n\nПаттерны — это язык общения Senior-разработчиков.",
            "en": "### 📖 Lecture: Design Patterns\n\nWhen you write large applications, you encounter architectural problems. **Design Patterns** are ready-made solutions to common architectural problems.\n\nPopular patterns:\n- **Singleton**: ensures that a class has only one instance (e.g., a DB connection).\n- **Factory**: encapsulates the logic of creating complex objects.\n- **Observer**: allows some objects to subscribe to the events of others (the basis of many UI frameworks).\n\nPatterns are the language of communication of Senior developers.",
            "kz": "### 📖 Дәріс: Дизайн паттерндері\n\nҮлкен қолданбаларды жазған кезде архитектуралық мәселелерге тап боласыз. **Дизайн паттерндері** - жалпы архитектуралық мәселелердің дайын шешімдері.\n\nТанымал паттерндер:\n- **Singleton (Жалғыз)**: класта тек бір дананың болуын қамтамасыз етеді (мысалы, ДБ қосылымы).\n- **Factory (Фабрика)**: күрделі нысандарды құру логикасын инкапсуляциялайды.\n- **Observer (Бақылаушы)**: кейбір нысандарға басқалардың оқиғаларына жазылуға мүмкіндік береді (көптеген UI фреймворктерінің негізі).\n\nПаттерндер - бұл Senior әзірлеушілердің байланыс тілі."
        }
    ]
}

# 2. Code Snippets to append to topics
# Format: CODE_SNIPPETS[lang][difficulty][lesson_idx] -> str
CODE_SNIPPETS = {
    "python": {
        "easy": [
            "```python\n# Объявление переменной / Declaring a variable\nname = 'Academy'\nage = 20\nis_active = True\n```",
            "```python\n# Операторы / Operators\nx = 10\nx = x + 5  # Теперь x равно 15\n\nis_valid = (x > 10) and (x < 20)  # True\n```",
            "```python\n# Условия / Conditionals\nif score >= 90:\n    print('A')\nelif score >= 80:\n    print('B')\nelse:\n    print('C')\n```",
            "```python\n# Циклы / Loops\nfor i in range(5):\n    print('Итерация:', i)\n\ncounter = 0\nwhile counter < 3:\n    counter += 1\n```",
            "```python\n# Функции / Functions\ndef calculate_tax(amount, rate):\n    tax = amount * rate\n    return tax\n\nresult = calculate_tax(100, 0.2)\n```"
        ],
        "medium": [
            "```python\n# Списки / Lists\nfruits = ['apple', 'banana']\nfruits.append('orange')\nprint(fruits[0]) # 'apple'\n```",
            "```python\n# Словари / Dictionaries\nuser = {\n    'id': 1,\n    'name': 'Alex'\n}\nprint(user['name'])\n```",
            "```python\n# Строки и Regex\ntext = 'Hello, World!'\nwords = text.split(',')\n\nimport re\nis_email = re.match(r'^\\S+@\\S+\\.\\S+$', 'test@mail.com')\n```",
            "```python\n# Исключения / Exceptions\ntry:\n    result = 10 / 0\nexcept ZeroDivisionError as e:\n    print('Ошибка: деление на ноль!')\n```",
            "```python\n# Классы / Classes\nclass Car:\n    def __init__(self, color):\n        self.color = color\n    \n    def drive(self):\n        print(f'{self.color} car is driving')\n```"
        ],
        "hard": [
            "```python\n# Наследование / Inheritance\nclass Animal:\n    def speak(self): pass\n\nclass Dog(Animal):\n    def speak(self):\n        return 'Woof!'\n```",
            "```python\n# Множества / Sets\nunique_numbers = {1, 2, 3, 3, 2}\nprint(unique_numbers)  # {1, 2, 3}\n```",
            "```python\n# ФП (map/filter) \nnums = [1, 2, 3, 4]\nsquares = list(map(lambda x: x**2, nums))\nevens = list(filter(lambda x: x % 2 == 0, nums))\n```",
            "```python\n# Async/Await\nimport asyncio\n\nasync def fetch_data():\n    await asyncio.sleep(1) # Имитация запроса\n    return {'data': 'loaded'}\n```",
            "```python\n# Singleton\nclass Database:\n    _instance = None\n    def __new__(cls):\n        if cls._instance is None:\n            cls._instance = super().__new__(cls)\n        return cls._instance\n```"
        ]
    },
    "javascript": {
        "easy": [
            "```javascript\n// Variables\nlet name = 'Academy';\nconst age = 20;\nlet isActive = true;\n```",
            "```javascript\n// Operators\nlet x = 10;\nx += 5; // 15\n\nlet isValid = (x > 10) && (x < 20); // true\n```",
            "```javascript\n// Conditionals\nif (score >= 90) {\n    console.log('A');\n} else if (score >= 80) {\n    console.log('B');\n} else {\n    console.log('C');\n}\n```",
            "```javascript\n// Loops\nfor (let i = 0; i < 5; i++) {\n    console.log('Iteration:', i);\n}\n\nlet counter = 0;\nwhile (counter < 3) {\n    counter++;\n}\n```",
            "```javascript\n// Functions\nfunction calculateTax(amount, rate) {\n    return amount * rate;\n}\n\nconst result = calculateTax(100, 0.2);\n```"
        ],
        "medium": [
            "```javascript\n// Arrays\nconst fruits = ['apple', 'banana'];\nfruits.push('orange');\nconsole.log(fruits[0]); // 'apple'\n```",
            "```javascript\n// Objects\nconst user = {\n    id: 1,\n    name: 'Alex'\n};\nconsole.log(user.name);\n```",
            "```javascript\n// Strings and Regex\nconst text = 'Hello, World!';\nconst words = text.split(',');\n\nconst isEmail = /^\\S+@\\S+\\.\\S+$/.test('test@mail.com');\n```",
            "```javascript\n// Exceptions\ntry {\n    throw new Error('Something went wrong!');\n} catch (e) {\n    console.error('Error:', e.message);\n}\n```",
            "```javascript\n// Classes\nclass Car {\n    constructor(color) {\n        this.color = color;\n    }\n    drive() {\n        console.log(`${this.color} car is driving`);\n    }\n}\n```"
        ],
        "hard": [
            "```javascript\n// Inheritance\nclass Animal {\n    speak() { }\n}\n\nclass Dog extends Animal {\n    speak() {\n        return 'Woof!';\n    }\n}\n```",
            "```javascript\n// Sets and Maps\nconst uniqueNumbers = new Set([1, 2, 3, 3, 2]);\nconsole.log(uniqueNumbers); // Set(3) { 1, 2, 3 }\n```",
            "```javascript\n// FP (map/filter)\nconst nums = [1, 2, 3, 4];\nconst squares = nums.map(x => x ** 2);\nconst evens = nums.filter(x => x % 2 === 0);\n```",
            "```javascript\n// Async/Await\nasync function fetchData() {\n    const response = await fetch('https://api.example.com/data');\n    const data = await response.json();\n    return data;\n}\n```",
            "```javascript\n// Singleton\nclass Database {\n    constructor() {\n        if (Database.instance) {\n            return Database.instance;\n        }\n        Database.instance = this;\n    }\n}\n```"
        ]
    },
    "java": {
        "easy": [
            "```java\n// Variables\nString name = \"Academy\";\nint age = 20;\nboolean isActive = true;\n```",
            "```java\n// Operators\nint x = 10;\nx += 5; // 15\n\nboolean isValid = (x > 10) && (x < 20); // true\n```",
            "```java\n// Conditionals\nif (score >= 90) {\n    System.out.println(\"A\");\n} else if (score >= 80) {\n    System.out.println(\"B\");\n} else {\n    System.out.println(\"C\");\n}\n```",
            "```java\n// Loops\nfor (int i = 0; i < 5; i++) {\n    System.out.println(\"Iteration: \" + i);\n}\n\nint counter = 0;\nwhile (counter < 3) {\n    counter++;\n}\n```",
            "```java\n// Functions (Methods)\npublic double calculateTax(double amount, double rate) {\n    return amount * rate;\n}\n```"
        ],
        "medium": [
            "```java\n// Arrays and Lists\nArrayList<String> fruits = new ArrayList<>();\nfruits.add(\"apple\");\nfruits.add(\"banana\");\nSystem.out.println(fruits.get(0));\n```",
            "```java\n// HashMaps\nHashMap<String, String> user = new HashMap<>();\nuser.put(\"name\", \"Alex\");\nSystem.out.println(user.get(\"name\"));\n```",
            "```java\n// Strings and Regex\nString text = \"Hello, World!\";\nString[] words = text.split(\",\");\n\nboolean isEmail = \"test@mail.com\".matches(\"^\\\\S+@\\\\S+\\\\.\\\\S+$\");\n```",
            "```java\n// Exceptions\ntry {\n    int result = 10 / 0;\n} catch (ArithmeticException e) {\n    System.out.println(\"Error: division by zero!\");\n}\n```",
            "```java\n// Classes\npublic class Car {\n    private String color;\n    public Car(String color) {\n        this.color = color;\n    }\n    public void drive() {\n        System.out.println(color + \" car is driving\");\n    }\n}\n```"
        ],
        "hard": [
            "```java\n// Inheritance\npublic class Animal {\n    public void speak() { }\n}\n\npublic class Dog extends Animal {\n    @Override\n    public void speak() {\n        System.out.println(\"Woof!\");\n    }\n}\n```",
            "```java\n// Sets\nHashSet<Integer> uniqueNumbers = new HashSet<>(Arrays.asList(1, 2, 3, 3, 2));\nSystem.out.println(uniqueNumbers); // [1, 2, 3]\n```",
            "```java\n// Streams (FP)\nList<Integer> nums = Arrays.asList(1, 2, 3, 4);\nList<Integer> evens = nums.stream()\n    .filter(x -> x % 2 == 0)\n    .collect(Collectors.toList());\n```",
            "```java\n// CompletableFuture (Async)\nCompletableFuture.supplyAsync(() -> {\n    // Simulate delay\n    return \"Loaded data\";\n}).thenAccept(result -> {\n    System.out.println(result);\n});\n```",
            "```java\n// Singleton\npublic class Database {\n    private static Database instance;\n    private Database() {}\n    public static Database getInstance() {\n        if (instance == null) instance = new Database();\n        return instance;\n    }\n}\n```"
        ]
    },
    "csharp": {
        "easy": [
            "```csharp\n// Variables\nstring name = \"Academy\";\nint age = 20;\nbool isActive = true;\n```",
            "```csharp\n// Operators\nint x = 10;\nx += 5; // 15\n\nbool isValid = (x > 10) && (x < 20); // true\n```",
            "```csharp\n// Conditionals\nif (score >= 90) {\n    Console.WriteLine(\"A\");\n} else if (score >= 80) {\n    Console.WriteLine(\"B\");\n} else {\n    Console.WriteLine(\"C\");\n}\n```",
            "```csharp\n// Loops\nfor (int i = 0; i < 5; i++) {\n    Console.WriteLine(\"Iteration: \" + i);\n}\n\nint counter = 0;\nwhile (counter < 3) {\n    counter++;\n}\n```",
            "```csharp\n// Functions (Methods)\npublic double CalculateTax(double amount, double rate) {\n    return amount * rate;\n}\n```"
        ],
        "medium": [
            "```csharp\n// Lists\nList<string> fruits = new List<string> { \"apple\", \"banana\" };\nfruits.Add(\"orange\");\nConsole.WriteLine(fruits[0]);\n```",
            "```csharp\n// Dictionaries\nDictionary<string, string> user = new Dictionary<string, string>();\nuser[\"name\"] = \"Alex\";\nConsole.WriteLine(user[\"name\"]);\n```",
            "```csharp\n// Strings and Regex\nstring text = \"Hello, World!\";\nstring[] words = text.Split(',');\n\nbool isEmail = Regex.IsMatch(\"test@mail.com\", @\"^\\S+@\\S+\\.\\S+$\");\n```",
            "```csharp\n// Exceptions\ntry {\n    int result = 10 / 0;\n} catch (DivideByZeroException) {\n    Console.WriteLine(\"Error: division by zero!\");\n}\n```",
            "```csharp\n// Classes\npublic class Car {\n    public string Color { get; set; }\n    public Car(string color) {\n        Color = color;\n    }\n    public void Drive() {\n        Console.WriteLine($\"{Color} car is driving\");\n    }\n}\n```"
        ],
        "hard": [
            "```csharp\n// Inheritance\npublic class Animal {\n    public virtual void Speak() { }\n}\n\npublic class Dog : Animal {\n    public override void Speak() {\n        Console.WriteLine(\"Woof!\");\n    }\n}\n```",
            "```csharp\n// HashSets\nHashSet<int> uniqueNumbers = new HashSet<int> { 1, 2, 3, 3, 2 };\n// uniqueNumbers contains 1, 2, 3\n```",
            "```csharp\n// LINQ (FP)\nint[] nums = { 1, 2, 3, 4 };\nvar evens = nums.Where(x => x % 2 == 0).ToList();\nvar squares = nums.Select(x => x * x).ToList();\n```",
            "```csharp\n// Async/Await\npublic async Task<string> FetchDataAsync() {\n    await Task.Delay(1000);\n    return \"Loaded data\";\n}\n```",
            "```csharp\n// Singleton\npublic sealed class Database {\n    private static readonly Database instance = new Database();\n    private Database() {}\n    public static Database Instance => instance;\n}\n```"
        ]
    },
    "php": {
        "easy": [
            "```php\n// Variables\n$name = 'Academy';\n$age = 20;\n$isActive = true;\n```",
            "```php\n// Operators\n$x = 10;\n$x += 5; // 15\n\n$isValid = ($x > 10) && ($x < 20); // true\n```",
            "```php\n// Conditionals\nif ($score >= 90) {\n    echo 'A';\n} elseif ($score >= 80) {\n    echo 'B';\n} else {\n    echo 'C';\n}\n```",
            "```php\n// Loops\nfor ($i = 0; $i < 5; $i++) {\n    echo \"Iteration: $i\\n\";\n}\n\n$counter = 0;\nwhile ($counter < 3) {\n    $counter++;\n}\n```",
            "```php\n// Functions\nfunction calculateTax($amount, $rate) {\n    return $amount * $rate;\n}\n\n$result = calculateTax(100, 0.2);\n```"
        ],
        "medium": [
            "```php\n// Arrays\n$fruits = ['apple', 'banana'];\narray_push($fruits, 'orange');\necho $fruits[0]; // 'apple'\n```",
            "```php\n// Associative Arrays\n$user = [\n    'id' => 1,\n    'name' => 'Alex'\n];\necho $user['name'];\n```",
            "```php\n// Strings and Regex\n$text = 'Hello, World!';\n$words = explode(',', $text);\n\n$isEmail = preg_match('/^\\S+@\\S+\\.\\S+$/', 'test@mail.com');\n```",
            "```php\n// Exceptions\ntry {\n    throw new Exception('Something went wrong!');\n} catch (Exception $e) {\n    echo 'Error: ' . $e->getMessage();\n}\n```",
            "```php\n// Classes\nclass Car {\n    private $color;\n    public function __construct($color) {\n        $this->color = $color;\n    }\n    public function drive() {\n        echo \"{$this->color} car is driving\";\n    }\n}\n```"
        ],
        "hard": [
            "```php\n// Inheritance\nclass Animal {\n    public function speak() { }\n}\n\nclass Dog extends Animal {\n    public function speak() {\n        echo 'Woof!';\n    }\n}\n```",
            "```php\n// Sets (using arrays in PHP)\n$numbers = [1, 2, 3, 3, 2];\n$uniqueNumbers = array_unique($numbers);\nprint_r($uniqueNumbers);\n```",
            "```php\n// FP (array_map / array_filter)\n$nums = [1, 2, 3, 4];\n$squares = array_map(fn($x) => $x ** 2, $nums);\n$evens = array_filter($nums, fn($x) => $x % 2 == 0);\n```",
            "```php\n// Asynchrony (PHP Fibers 8.1+)\n$fiber = new Fiber(function (): void {\n    echo \"Inside fiber\\n\";\n    Fiber::suspend();\n    echo \"Fiber resumed\\n\";\n});\n$fiber->start();\n$fiber->resume();\n```",
            "```php\n// Singleton\nclass Database {\n    private static $instance = null;\n    private function __construct() {}\n    public static function getInstance() {\n        if (self::$instance == null) {\n            self::$instance = new Database();\n        }\n        return self::$instance;\n    }\n}\n```"
        ]
    }
}


async def generate():
    engine = create_async_engine(settings.database_url)
    async with engine.begin() as conn:
        # Load all levels
        result = await conn.execute(
            select(Level)
            .join(Level.track)
            .join(Track.language)
            .join(Level.difficulty)
        )
        # Using pure SQL to update since it's faster
        # But we need language code, diff code, order_num for each level
        
    # Standard AsyncSession
    from sqlalchemy.ext.asyncio import AsyncSession
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        result = await session.execute(
            select(Level)
            .join(Level.track)
            .join(Track.language)
            .join(Level.difficulty)
        )
        levels = result.scalars().all()
        
        updated = 0
        for lvl in levels:
            await session.refresh(lvl, ['track', 'difficulty'])
            await session.refresh(lvl.track, ['language'])
            lang_code = lvl.track.language.code
            diff_code = lvl.difficulty.code
            num = lvl.order_num - 1 # 0 to 4
            
            # Bound index
            if num < 0 or num >= 5:
                continue
                
            topic = TOPICS.get(diff_code)
            if not topic: continue
            
            lesson_text = topic[num] # dict with ru, en, kz
            snippets = CODE_SNIPPETS.get(lang_code, CODE_SNIPPETS["python"])
            code_block = snippets.get(diff_code, snippets["easy"])[num]
            
            lvl.theory_ru = f"{lesson_text['ru']}\n\n{code_block}"
            lvl.theory_en = f"{lesson_text['en']}\n\n{code_block}"
            lvl.theory_kz = f"{lesson_text['kz']}\n\n{code_block}"
            updated += 1
            
        await session.commit()
        print(f"Generated rich lectures for {updated} levels!")

if __name__ == "__main__":
    asyncio.run(generate())
