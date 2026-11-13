# Практические задания: Работа с ошибками

## Подготовка

Для каждой задачи есть **заготовка** в папке [`starter/`](starter/). Задача 1.3 читает
файл из папки `data/`, поэтому запускайте заготовки **из директории семинара**:

```bash
cd seminars/seminar_08_error_handling
python exercises/starter/task_1_1.py
```

Примеры кода к каждой части — в папке [`../examples/`](../examples/).

> **Как работать с заданиями:** прочитайте условие, напишите и **запустите** свою версию,
> и только потом раскройте решение для сверки. Если ваш код работает правильно,
> он тоже верный — решение здесь не единственное.
>
> Проверяйте не только «хороший» ввод: в этих задачах самое интересное происходит,
> когда пользователь вводит что-то не то.

---

## Часть 1: Перехват исключений

> **Теория:** [README.md — Блок 1](../README.md#блок-1-перехват-исключений-10-мин) | **Примеры:** [`examples/01_catching.py`](../examples/01_catching.py)

### Задание 1.1

Заготовка: [`starter/task_1_1.py`](starter/task_1_1.py)

Программа продаёт билеты в кино и спрашивает, сколько билетов нужно. Сейчас она
падает, если ввести не число. Сделайте так, чтобы программа переспрашивала, пока
не получит целое число **от 1 до 10**:

```
Сколько билетов? два
«два» — не целое число, попробуйте ещё раз
Сколько билетов? 15
Можно купить от 1 до 10 билетов
Сколько билетов? 3
Билетов: 3
```

<details>
<summary>Подсказка</summary>

Внутри бесконечного цикла `while True` оберните `int()` в `try`/`except ValueError`.
Проверку диапазона и выход из цикла через `break` удобно поместить в блок `else` —
он выполнится, только если число разобралось без ошибки.

</details>

<details>
<summary>Решение</summary>

```python
while True:
    text = input("Сколько билетов? ")
    try:
        tickets = int(text)
    except ValueError:
        print(f"«{text}» — не целое число, попробуйте ещё раз")
    else:
        if 1 <= tickets <= 10:
            break
        print("Можно купить от 1 до 10 билетов")

print("Билетов:", tickets)
```

В `try` стоит только одна строка — та, которая может упасть. Проверка диапазона —
это не исключение, а обычное условие, поэтому она живёт в `else`.

</details>

### Задание 1.2

Заготовка: [`starter/task_1_2.py`](starter/task_1_2.py)

Программа считает среднюю скорость по расстоянию (км) и времени в пути (ч).
Обработайте две ошибки **по-разному**:

```
Расстояние, км: сто
Расстояние и время должны быть числами
Расчёт окончен
```

```
Расстояние, км: 120
Время в пути, ч: 0
Время в пути не может быть нулевым
Расчёт окончен
```

```
Расстояние, км: 120
Время в пути, ч: 1.5
Средняя скорость: 80.0 км/ч
Расчёт окончен
```

Строка «Расчёт окончен» печатается в любом случае.

<details>
<summary>Подсказка</summary>

Нужны два блока `except` — для `ValueError` и для `ZeroDivisionError`. Результат
печатайте в `else`, а финальную строку — в `finally`.

</details>

<details>
<summary>Решение</summary>

```python
distance_text = input("Расстояние, км: ")
hours_text = input("Время в пути, ч: ")

try:
    speed = float(distance_text) / float(hours_text)
except ValueError:
    print("Расстояние и время должны быть числами")
except ZeroDivisionError:
    print("Время в пути не может быть нулевым")
else:
    print(f"Средняя скорость: {speed:.1f} км/ч")
finally:
    print("Расчёт окончен")
```

Обратите внимание: в примере выше программа спрашивает время, даже если расстояние
введено неверно, — оба `input()` стоят до `try`. Это нормально: в `try` мы кладём
только вычисление, которое может упасть.

</details>

### Задание 1.3

Заготовка: [`starter/task_1_3.py`](starter/task_1_3.py)

В файле [`data/readings.txt`](../data/readings.txt) записаны показания счётчика,
по одному в строке. Некоторые строки испорчены. Посчитайте среднее по правильным
строкам, а про испорченные сообщите с номером строки:

```
Строка 3 пропущена: 'нет данных'
Строка 5 пропущена: ''
Строка 6 пропущена: '131,5'
Строка 8 пропущена: 'ошибка датчика'
Правильных показаний: 5, среднее: 128.22
```

Если файла нет, программа должна вывести понятное сообщение, а не traceback.
Проверьте: временно поменяйте имя файла в заготовке на несуществующее.

<details>
<summary>Подсказка</summary>

Здесь два независимых `try`. Первый — вокруг открытия файла (`FileNotFoundError`).
Второй — внутри цикла по строкам, вокруг `float(line)`: ошибка в одной строке
не должна останавливать обработку остальных.

</details>

<details>
<summary>Решение</summary>

```python
path = "data/readings.txt"

try:
    with open(path, encoding="utf-8") as file:
        lines = file.readlines()
except FileNotFoundError:
    print(f"Файл {path} не найден — проверьте, из какой папки запущена программа")
else:
    values = []
    for line_number, line in enumerate(lines, start=1):
        try:
            values.append(float(line))
        except ValueError:
            print(f"Строка {line_number} пропущена: {line.strip()!r}")

    if values:
        average = sum(values) / len(values)
        print(f"Правильных показаний: {len(values)}, среднее: {average:.2f}")
    else:
        print("В файле нет ни одного правильного показания")
```

`enumerate(lines, start=1)` выдаёт пары «номер, строка» — так не нужно вести
счётчик вручную.

Строка `'131,5'` не разобралась, потому что `float()` понимает только точку. Это
пример того, почему EAFP надёжнее: заранее перечислить все неправильные форматы
трудно, а `float()` сам знает, что он умеет.

</details>

---

## Часть 2: Генерация исключений и их иерархия

> **Теория:** [README.md — Блок 2](../README.md#блок-2-генерация-исключений-и-их-иерархия-10-мин) | **Примеры:** [`examples/02_raising.py`](../examples/02_raising.py)

### Задание 2.1

Заготовка: [`starter/task_2_1.py`](starter/task_2_1.py)

Напишите функцию `parse_time(text)`, которая принимает время в формате `ЧЧ:ММ`
и возвращает число минут от начала суток. При неправильных данных функция должна
бросать `ValueError` с понятным сообщением:

```
'09:30' -> 570
'23:59' -> 1439
'24:00' -> ошибка: Часы должны быть от 0 до 23, получено 24
'12:75' -> ошибка: Минуты должны быть от 0 до 59, получено 75
'полдень' -> ошибка: Ожидался формат ЧЧ:ММ, получено 'полдень'
```

Сама функция ничего не печатает — печатает вызывающий код.

<details>
<summary>Подсказка</summary>

Разбейте строку по `":"` и проверьте, что частей ровно две. Для каждой проверки —
`if` и `raise ValueError(f"...")`. Если в часах окажутся буквы, `int()` сам бросит
`ValueError` — отдельно это проверять не нужно.

</details>

<details>
<summary>Решение</summary>

```python
def parse_time(text):
    """Перевести время «ЧЧ:ММ» в минуты от начала суток."""
    parts = text.split(":")
    if len(parts) != 2:
        raise ValueError(f"Ожидался формат ЧЧ:ММ, получено {text!r}")

    hours = int(parts[0])
    minutes = int(parts[1])
    if not 0 <= hours <= 23:
        raise ValueError(f"Часы должны быть от 0 до 23, получено {hours}")
    if not 0 <= minutes <= 59:
        raise ValueError(f"Минуты должны быть от 0 до 59, получено {minutes}")

    return hours * 60 + minutes


for text in ["09:30", "23:59", "24:00", "12:75", "полдень", "ab:cd"]:
    try:
        print(f"{text!r} -> {parse_time(text)}")
    except ValueError as error:
        print(f"{text!r} -> ошибка: {error}")
```

Для `'ab:cd'` сообщение придёт от самого `int()`: *invalid literal for int()…*.
Тип тот же — `ValueError`, поэтому вызывающему коду не нужно знать, какая
именно проверка не прошла.

</details>

### Задание 2.2

Заготовка: [`starter/task_2_2.py`](starter/task_2_2.py)

В заготовке функция `lookup(data, key)` с тремя блоками `except`.

1. **Не запуская программу**, запишите, что напечатает каждый из трёх вызовов.
2. Запустите и сравните. Объясните, почему так вышло.
3. Исправьте функцию, чтобы каждый случай получил своё сообщение:

```
Нет ключа 'b'
Нет элемента с индексом 5
Объект типа int не поддерживает обращение по ключу
```

<details>
<summary>Подсказка</summary>

`except` проверяются сверху вниз, и срабатывает **первый** подходящий. А подходящий —
это тот, чей класс совпадает с исключением **или является его родителем**. Нарисуйте
кусок иерархии: `Exception` → `LookupError` → `KeyError` / `IndexError`.

</details>

<details>
<summary>Решение</summary>

В исходной версии все три вызова печатают «Неизвестная ошибка»: `except Exception`
стоит первым и ловит любое обычное исключение. До остальных блоков очередь
не доходит никогда.

```python
def lookup(data, key):
    try:
        return data[key]
    except KeyError:
        print(f"Нет ключа {key!r}")
    except IndexError:
        print(f"Нет элемента с индексом {key}")
    except TypeError:
        print(f"Объект типа {type(data).__name__} не поддерживает обращение по ключу")


lookup({"a": 1}, "b")
lookup([10, 20], 5)
lookup(42, 0)
print(lookup({"a": 1}, "a"))  # 1 — без ошибки функция просто возвращает значение
```

Заодно мы заменили `except Exception` на конкретный `TypeError`: теперь, если
в функции появится опечатка (`NameError`), она не спрячется за сообщением
«Неизвестная ошибка».

</details>

### Задание 2.3

Заготовка: [`starter/task_2_3.py`](starter/task_2_3.py)

Программа печатает средние оценки студентов и падает. Запустите её и, **не читая
код целиком**, только по traceback ответьте:

1. Какого типа исключение и какое у него сообщение?
2. В какой функции и в какой строке оно возникло?
3. Через какую цепочку вызовов программа туда попала?

Затем найдите настоящую причину и исправьте её.

<details>
<summary>Подсказка</summary>

Читайте traceback снизу вверх. Место, где исключение возникло, и место, где
допущена ошибка, — не обязательно одно и то же. Посмотрите, какие данные пришли
в упавшую функцию.

</details>

<details>
<summary>Решение</summary>

Traceback (номера строк могут отличаться):

```
Иванов     4.67
Traceback (most recent call last):
  File "task_2_3.py", line 34, in <module>
    print_report(grades)
  File "task_2_3.py", line 31, in print_report
    print(format_line(name, marks))
  File "task_2_3.py", line 26, in format_line
    return f"{name:<10} {average(marks):.2f}"
  File "task_2_3.py", line 22, in average
    return sum(marks) / len(marks)
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

1. `TypeError`: нельзя сложить `int` и `str`.
2. В функции `average`, в строке с `sum(marks)`.
3. `print_report` → `format_line` → `average`.

Функция `average` написана правильно — ей передали неправильные данные. Первая
строка отчёта (Иванов) напечаталась, значит, сломался второй студент. У Петровой
одна оценка записана строкой `"5"`. Исправление — в данных:

```python
grades = {
    "Иванов": [5, 4, 5],
    "Петрова": [4, 5, 3],
    "Сидоров": [3, 4],
}
```

Вывод: исключение возникает там, где данные **использовали**, а ошибка часто
там, где их **создали**.

</details>

---

## Часть 3: Собственные исключения

> **Теория:** [README.md — Блок 3](../README.md#блок-3-собственные-исключения-10-мин) | **Примеры:** [`examples/03_custom_exceptions.py`](../examples/03_custom_exceptions.py)

Во всех задачах части — библиотека. Словарь `books` хранит, у кого сейчас книга:
`None` означает, что книга на полке.

### Задание 3.1

Заготовка: [`starter/task_3_1.py`](starter/task_3_1.py)

Сейчас метод `take()` молча «выдаёт» даже книгу, которой в библиотеке нет, — это
логическая ошибка. Создайте:

- базовое исключение `LibraryError`;
- его наследника `BookNotFoundError` с атрибутом `title` и сообщением
  `Книги «…» нет в библиотеке`.

Пусть `take()` бросает `BookNotFoundError`, если книги нет. Проверьте:

```
Аня: выдана книга «Война и мир»
Ошибка: Книги «Гарри Поттер» нет в библиотеке
Название из исключения: Гарри Поттер
```

<details>
<summary>Подсказка</summary>

Текст сообщения передайте в `super().__init__(...)`, а название сохраните
в `self.title` — как у `NotInRangeError` из теории.

</details>

<details>
<summary>Решение</summary>

```python
class LibraryError(Exception):
    """Базовая ошибка библиотеки."""


class BookNotFoundError(LibraryError):
    """Такой книги в библиотеке нет."""

    def __init__(self, title):
        super().__init__(f"Книги «{title}» нет в библиотеке")
        self.title = title


class Library:
    def __init__(self):
        self.books = {
            "Мастер и Маргарита": None,
            "Война и мир": None,
            "Дюна": "Петя",
        }

    def take(self, title, reader):
        if title not in self.books:
            raise BookNotFoundError(title)
        self.books[title] = reader


library = Library()

library.take("Война и мир", "Аня")
print("Аня: выдана книга «Война и мир»")

try:
    library.take("Гарри Поттер", "Аня")
except BookNotFoundError as error:
    print("Ошибка:", error)
    print("Название из исключения:", error.title)
```

</details>

### Задание 3.2

Заготовка: [`starter/task_3_2.py`](starter/task_3_2.py)

Добавьте исключение `BookAlreadyTakenError` (наследник `LibraryError`) с атрибутами
`title` и `reader` — у кого сейчас книга. Пусть `take()` бросает его, если книга
уже выдана.

Обработайте список заявок и для каждой ошибки выведите **своё** сообщение,
используя атрибуты исключения:

```
Аня: выдана книга «Война и мир»
«Дюна» сейчас у читателя Петя — встаньте в очередь
«Гарри Поттер» — такой книги нет, проверьте название
«Война и мир» сейчас у читателя Аня — встаньте в очередь
```

<details>
<summary>Подсказка</summary>

`__init__` исключения принимает два параметра и сохраняет оба. В цикле по заявкам
нужны два `except` — по одному на каждый тип ошибки, — и `else` для успешной выдачи.

</details>

<details>
<summary>Решение</summary>

```python
class BookAlreadyTakenError(LibraryError):
    """Книга уже выдана другому читателю."""

    def __init__(self, title, reader):
        super().__init__(f"Книга «{title}» уже у читателя {reader}")
        self.title = title
        self.reader = reader


class Library:
    def __init__(self):
        self.books = {
            "Мастер и Маргарита": None,
            "Война и мир": None,
            "Дюна": "Петя",
        }

    def take(self, title, reader):
        if title not in self.books:
            raise BookNotFoundError(title)
        if self.books[title] is not None:
            raise BookAlreadyTakenError(title, self.books[title])
        self.books[title] = reader


library = Library()
requests = [
    ("Война и мир", "Аня"),
    ("Дюна", "Вася"),
    ("Гарри Поттер", "Аня"),
    ("Война и мир", "Боря"),
]

for title, reader in requests:
    try:
        library.take(title, reader)
    except BookAlreadyTakenError as error:
        print(f"«{error.title}» сейчас у читателя {error.reader} — встаньте в очередь")
    except BookNotFoundError as error:
        print(f"«{error.title}» — такой книги нет, проверьте название")
    else:
        print(f"{reader}: выдана книга «{title}»")
```

Атрибуты пригодились: сообщение для пользователя мы собрали сами, а не взяли
готовый текст исключения.

</details>

### Задание 3.3

Заготовка: [`starter/task_3_3.py`](starter/task_3_3.py)

В заготовке — готовая библиотека с исключениями и консольное меню. Методы класса
`Library` **ничего не печатают и не спрашивают** — они только бросают исключения.
Ваша задача — решить, где эти исключения обработать:

1. Добавьте в метод `give_back()` ошибку `BookNotTakenError`, если книга и так
   на полке.
2. Сделайте так, чтобы неизвестная команда не роняла программу.
3. Сделайте так, чтобы **любая** ошибка библиотеки печаталась и меню продолжало
   работать.

```
Команда (взять/вернуть/список/выход): взять
Название: Дюна
Ваше имя: Аня
Ошибка: Книга «Дюна» уже у читателя Петя
Команда (взять/вернуть/список/выход): читать
Неизвестная команда: читать
Команда (взять/вернуть/список/выход): вернуть
Название: Война и мир
Ошибка: Книга «Война и мир» и так в библиотеке
Команда (взять/вернуть/список/выход): выход
```

<details>
<summary>Подсказка</summary>

Команды хранятся в словаре «название → функция»; поиск неизвестной команды
в словаре бросает `KeyError`. Ошибки библиотеки удобно ловить одним
`except LibraryError` — он поймает всех наследников. Ловить их стоит в главном
цикле: именно он общается с пользователем.

</details>

<details>
<summary>Решение</summary>

```python
class BookNotTakenError(LibraryError):
    """Книгу пытаются вернуть, хотя её никто не брал."""

    def __init__(self, title):
        super().__init__(f"Книга «{title}» и так в библиотеке")
        self.title = title


# в классе Library:
def give_back(self, title):
    if title not in self.books:
        raise BookNotFoundError(title)
    if self.books[title] is None:
        raise BookNotTakenError(title)
    self.books[title] = None


# главный цикл:
library = Library()

while True:
    command = input("Команда (взять/вернуть/список/выход): ").strip()
    if command == "выход":
        break

    try:
        action = COMMANDS[command]
    except KeyError:
        print("Неизвестная команда:", command)
        continue

    try:
        action(library)
    except LibraryError as error:
        print("Ошибка:", error)
```

Почему не обрабатывать ошибки внутри `Library`? Класс не знает, кто его
использует: консольное меню, сайт или тест. Печатать сообщение пользователю —
это решение интерфейса, поэтому его принимает главный цикл. Так работает принцип
«обрабатывать на том уровне, у которого хватает полномочий».

Два `try` вместо одного — тоже не случайность: `KeyError` при поиске команды
и ошибки библиотеки возникают в разных местах и обрабатываются по-разному.

</details>

---

## Для самостоятельной работы

Задачи, которые не поместились в занятие, и темы, которые мы не разбирали на семинаре
(см. [README — Темы лекции, которые мы не разбираем на занятии](../README.md#темы-лекции-которые-мы-не-разбираем-на-занятии)).
Сдавать их не нужно, но решить очень советуем. Примеры — в файле
[`examples/04_chaining_and_assert.py`](../examples/04_chaining_and_assert.py).

### Задание 4.1

Найдите в коде все «типичные ошибки новичков» из Блока 1 и перепишите функцию.
Файл с ценами — строки вида `название;цена`.

```python
def load_prices(path):
    try:
        prices = {}
        with open(path, encoding="utf-8") as file:
            for line in file:
                name, price = line.split(";")
                prices[name] = float(price)
        return prices
    except:
        pass
```

Что должно получиться: если файла нет — функция сообщает об этом и возвращает
пустой словарь; испорченная строка пропускается с сообщением, а остальные строки
читаются.

<details>
<summary>Подсказка</summary>

Найдите три проблемы: что ловит `except:`, что происходит после `pass` (что вернёт
функция?) и сколько строк внутри `try`. Какие ошибки здесь вообще ожидаемы?
Их всего две, и они возникают в разных местах.

</details>

<details>
<summary>Решение</summary>

Проблемы исходного кода:

1. Голый `except:` ловит всё — даже опечатку в имени переменной или Ctrl+C.
2. `pass` прячет ошибку, а функция молча возвращает `None` вместо словаря.
3. Весь код в одном `try`: одна испорченная строка выбрасывает весь файл.

```python
def load_prices(path):
    """Прочитать цены из файла со строками «название;цена»."""
    try:
        with open(path, encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Файл {path} не найден")
        return {}

    prices = {}
    for line in lines:
        try:
            name, price = line.split(";")
            prices[name] = float(price)
        except ValueError:
            print(f"Строка пропущена: {line.strip()!r}")
    return prices
```

`ValueError` ловит обе проблемы строки: и «не две части» при распаковке,
и «не число» во `float()`.

</details>

### Задание 4.2

Сравните LBYL и EAFP на практике. Напишите две функции, которые проверяют, можно ли
превратить строку в дробное число:

- `is_float_lbyl(text)` — только проверками, без `try`;
- `is_float_eafp(text)` — через `try`/`except`.

Сравните их на строках `"3.14"`, `" -2 "`, `"1e3"`, `".5"`, `"3,14"`, `""`, `"1_000.5"`,
`"inf"`. Где LBYL ошибается?

<details>
<summary>Решение</summary>

```python
def is_float_lbyl(text):
    text = text.strip()
    if text.startswith(("-", "+")):
        text = text[1:]
    return text.replace(".", "", 1).isdigit()


def is_float_eafp(text):
    try:
        float(text)
    except ValueError:
        return False
    return True


for text in ["3.14", " -2 ", "1e3", ".5", "3,14", "", "1_000.5", "inf"]:
    print(
        f"{text!r:>10}  LBYL: {is_float_lbyl(text)!s:<5}  EAFP: {is_float_eafp(text)}"
    )
```

LBYL не знает про экспоненциальную запись `1e3`, про подчёркивания `1_000.5`
и про специальное значение `inf` (бесконечность). Каждый такой случай — ещё одна
проверка, и всё равно легко что-то пропустить. EAFP-версия совпадает с поведением
`float()` по определению.

</details>

### Задание 4.3

Файл настроек — строки вида `ключ=число`. Напишите исключение `SettingsError`
с атрибутом `line_number` и функцию `parse_settings(lines)`, которая возвращает
словарь. Если строка не содержит `=` или значение не число, функция бросает
`SettingsError`. Во втором случае исходный `ValueError` должен сохраниться
в цепочке исключений.

```python
parse_settings(["width=80", "height=24"])  # {'width': 80, 'height': 24}
parse_settings(["width=80", "height=abc"])
# SettingsError: Строка 2: значение должно быть числом, получено 'abc'
```

<details>
<summary>Подсказка</summary>

Внутри `except ValueError as error` бросьте своё исключение через
`raise SettingsError(...) from error`. Исходная ошибка окажется в атрибуте
`__cause__`.

</details>

<details>
<summary>Решение</summary>

```python
class SettingsError(Exception):
    """Ошибка в файле настроек."""

    def __init__(self, line_number, message):
        super().__init__(f"Строка {line_number}: {message}")
        self.line_number = line_number


def parse_settings(lines):
    """Разобрать строки «ключ=число» в словарь."""
    settings = {}
    for line_number, line in enumerate(lines, start=1):
        if "=" not in line:
            raise SettingsError(line_number, f"ожидался формат ключ=число: {line!r}")
        key, value = line.split("=", 1)
        try:
            settings[key.strip()] = int(value)
        except ValueError as error:
            raise SettingsError(
                line_number, f"значение должно быть числом, получено {value!r}"
            ) from error
    return settings


print(parse_settings(["width=80", "height=24"]))

try:
    parse_settings(["width=80", "height=abc"])
except SettingsError as error:
    print(error)
    print("Номер строки:", error.line_number)
    print("Исходная ошибка:", repr(error.__cause__))
```

Вызывающему коду достаточно ловить `SettingsError` — ему не нужно знать, что
внутри используется `int()`. Но при отладке исходная ошибка не потеряна: она видна
и в traceback, и в `__cause__`.

</details>

### Задание 4.4

Опишите класс `Translator` со словарём переводов и методом `translate(word)`.
Для неизвестного слова метод бросает `UnknownWordError(word)`. Сделайте так, чтобы
в traceback не было видно внутреннего `KeyError`: то, что переводы лежат в словаре, —
деталь реализации.

Сравните traceback с `from None` и без него.

<details>
<summary>Решение</summary>

```python
class UnknownWordError(Exception):
    """Слова нет в словаре переводчика."""

    def __init__(self, word):
        super().__init__(f"Не знаю, как перевести «{word}»")
        self.word = word


class Translator:
    def __init__(self):
        self._words = {"кот": "cat", "собака": "dog"}

    def translate(self, word):
        try:
            return self._words[word]
        except KeyError:
            raise UnknownWordError(word) from None


translator = Translator()
print(translator.translate("кот"))
translator.translate("ёж")  # traceback покажет только UnknownWordError
```

Без `from None` traceback покажет сначала `KeyError: 'ёж'`, затем фразу
*During handling of the above exception, another exception occurred* и только
потом `UnknownWordError`. Пользователю класса первая половина ничего не говорит.

</details>

### Задание 4.5

Напишите простые тесты на `assert` для функции `parse_time` из задания 2.1:

- правильное время переводится в правильное число минут (минимум три проверки,
  включая `00:00` и `23:59`);
- на `"24:00"`, `"12:60"` и `"полдень"` функция бросает `ValueError`.

Если все проверки прошли, программа печатает «Все тесты пройдены».

Ответьте на вопрос: почему внутри самой `parse_time` нельзя заменить `raise` на `assert`?

<details>
<summary>Подсказка</summary>

Чтобы проверить, что исключение **было**, напишите вспомогательную функцию
`raises_value_error(text)`: она вызывает `parse_time` в `try` и возвращает `True`,
если пойман `ValueError`, и `False` — если функция отработала без ошибки.

</details>

<details>
<summary>Решение</summary>

```python
def raises_value_error(text):
    """Проверить, что parse_time(text) бросает ValueError."""
    try:
        parse_time(text)
    except ValueError:
        return True
    return False


assert parse_time("00:00") == 0
assert parse_time("09:30") == 570
assert parse_time("23:59") == 1439

assert raises_value_error("24:00")
assert raises_value_error("12:60")
assert raises_value_error("полдень")

print("Все тесты пройдены")
```

`assert` нельзя использовать для проверки входных данных: при запуске
`python -O` все `assert` отключаются, и `parse_time("24:00")` молча вернёт
`1440`. `assert` проверяет предположения программиста, а неправильный ввод — это
нормальная ситуация, на которую программа должна реагировать всегда.

На [семинаре 11](../../seminar_11_code_quality/README.md) те же проверки
превратятся в тесты pytest, а проверку исключения возьмёт на себя `pytest.raises`.

</details>
