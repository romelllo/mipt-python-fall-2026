# Семинар 8: Работа с ошибками

**Модуль:** 1 — Основы программирования на Python  
**Дата:** 16.11.2026, 18:40–20:10  
**Презентация:** _ссылка будет добавлена_

---

## Цели семинара

После этого семинара вы сможете:

- Различать синтаксические, логические ошибки и ошибки времени выполнения
- Перехватывать исключения конструкцией `try`/`except` и не давать программе падать
- Понимать, зачем нужны блоки `else` и `finally`
- Объяснить разницу между подходами LBYL («проверь заранее») и EAFP («попробуй
  и обработай ошибку»)
- Генерировать исключения инструкцией `raise` с понятным сообщением
- Читать traceback и находить по нему место ошибки
- Ориентироваться в иерархии встроенных исключений
- Создавать собственные классы исключений и решать, где их обрабатывать

---

## Подготовка

Нужен Python 3.10+ и редактор — всё как на прошлых семинарах
(если что-то не установилось: [`docs/installation.md`](../../docs/installation.md)).

> **Важно:** одна из задач читает файл из папки [`data/`](data/) по относительному
> пути — как на [семинаре 5](../seminar_05_files_and_classes/README.md#подготовка),
> запускайте программы **из директории семинара**:

```bash
cd seminars/seminar_08_error_handling

python examples/01_catching.py
python examples/02_raising.py
python examples/03_custom_exceptions.py
```

> Для каждой задачи есть **заготовка** в папке [`exercises/starter/`](exercises/starter/).

Семинар опирается на [классы](../seminar_05_files_and_classes/README.md#блок-2-классы-и-объекты-10-мин)
и [наследование](../seminar_06_inheritance/README.md#блок-1-наследование-10-мин):
собственное исключение — это обычный класс-наследник.

---

## План семинара

После каждого блока теории — 15 минут на упражнения из файла
[`exercises/error_handling_practice.md`](exercises/error_handling_practice.md).

| Время | Тема | Практика |
|-------|------|----------|
| 5 мин | Организационное: повторение семинара 7, план занятия | — |
| 10 мин | Блок 1: Перехват исключений | — |
| 15 мин | Практика | → Упражнения: Часть 1 |
| 10 мин | Блок 2: Генерация исключений и их иерархия | — |
| 15 мин | Практика | → Упражнения: Часть 2 |
| 10 мин | Блок 3: Собственные исключения | — |
| 15 мин | Практика | → Упражнения: Часть 3 |

> **Примечание:** в таблице 80 минут, оставшиеся ~10 минут — на вопросы и разбор задач.
> Цепочки исключений (`raise ... from`) и инструкция `assert` вынесены в раздел
> [«Темы лекции, которые мы не разбираем на занятии»](#темы-лекции-которые-мы-не-разбираем-на-занятии).

---

## Блок 1: Перехват исключений (10 мин)

### Какие бывают ошибки

| Вид | Когда обнаруживается | Пример |
|-----|----------------------|--------|
| Синтаксическая | до запуска программы | забыли двоеточие после `if` |
| Логическая | никогда — программа «работает», но неправильно | `<` вместо `<=` |
| Ошибка времени выполнения | во время работы | деление на ноль, нет файла |

Сегодня говорим о третьем виде. Когда такая ошибка происходит, Python создаёт
**исключение** — объект, описывающий, что случилось. Если его никто не перехватил,
программа завершается и печатает **traceback**:

```
Traceback (most recent call last):
  File "example.py", line 1, in <module>
    age = int("двадцать")
ValueError: invalid literal for int() with base 10: 'двадцать'
```

Сообщить об ошибке можно и без исключений — например, вернуть специальное значение.
Сравните два метода строки, которые ищут подстроку:

```python
"hello".find("z")  # -1 — «не нашёл», и это значение легко забыть проверить
"hello".index("z")  # ValueError: substring not found — забыть не получится
```

### try / except

Код, который может упасть, помещают в блок `try`, а реакцию на ошибку — в `except`:

```python
text = input("Сколько вам лет? ")
try:
    age = int(text)
except ValueError:
    print("Это не целое число")
```

Если в `try` ошибки нет, `except` пропускается. Если есть — выполнение `try`
прерывается и сразу переходит в подходящий `except`.

Разные ошибки можно обработать по-разному, а через `as` получить сам объект
исключения:

```python
try:
    result = int(a) / int(b)
except ValueError:
    print("Нужны числа")
except ZeroDivisionError as error:
    print("Ошибка:", error)  # Ошибка: division by zero
```

### else и finally

```python
try:
    number = int(text)
except ValueError:
    print("Это не число")
else:
    print("Квадрат:", number**2)  # только если ошибки НЕ было
finally:
    print("Проверка завершена")  # ВСЕГДА — даже после return или ошибки
```

Зачем `else`, если можно дописать строку в конец `try`? Чтобы в `try` осталась
только строка, которая может упасть, — тогда `except` не перехватит случайно ошибку
из другого места.

Обещанное на [семинаре 5](../seminar_05_files_and_classes/README.md#если-файла-нет):
отсутствующий файл больше не роняет программу.

```python
try:
    with open("data/readings.txt", encoding="utf-8") as file:
        content = file.read()
except FileNotFoundError:
    print("Файл не найден — проверьте, из какой папки запущена программа")
```

### LBYL или EAFP

Есть две стратегии работы с возможной ошибкой:

- **LBYL** (*Look Before You Leap*, «семь раз отмерь») — сначала проверить, потом
  делать;
- **EAFP** (*Easier to Ask Forgiveness than Permission*, «легче попросить прощения»)
  — сделать и обработать ошибку, если она случилась.

```python
# LBYL: проверка обрастает условиями — пробелы, минус, «1_000»...
if text.strip().lstrip("-").isdigit():
    number = int(text)

# EAFP: int() сам лучше всех знает, что он умеет разбирать
try:
    number = int(text)
except ValueError:
    print("Не число")
```

В Python принят стиль **EAFP**: он короче и не пропускает случаи, о которых вы
не подумали.

### Типичные ошибки новичков

| Плохо | Почему | Как лучше |
|-------|--------|-----------|
| `except:` или `except Exception:` | ловит **всё**, включая опечатки в именах | указывать конкретный тип: `except ValueError:` |
| `except ValueError: pass` | ошибка молча исчезает, искать её будет больно | хотя бы сообщить пользователю |
| весь код функции внутри `try` | непонятно, какая строка упала | в `try` — только строка, которая может упасть |

> **Подробнее:** см. файл [`examples/01_catching.py`](examples/01_catching.py)

### Практика

Перейдите к разделу **Часть 1: Перехват исключений** в файле
[`exercises/error_handling_practice.md`](exercises/error_handling_practice.md#часть-1-перехват-исключений).

---

## Блок 2: Генерация исключений и их иерархия (10 мин)

### raise

Исключения бросает не только Python — своя функция тоже может сообщить, что её
вызвали неправильно. Для этого есть `raise`:

```python
def make_discount(price, percent):
    if not 0 <= percent <= 100:
        raise ValueError(f"Скидка должна быть от 0 до 100, получено {percent}")
    return price * (100 - percent) / 100
```

Тип исключения подбирают по смыслу, как это делают встроенные функции:

| Исключение | Когда бросать |
|------------|---------------|
| `ValueError` | тип правильный, а значение нет: отрицательная цена, пустое имя |
| `TypeError` | передали объект не того типа |
| `KeyError` / `IndexError` | нет такого ключа / индекса |

Функция, которая бросает исключение, **не решает, что делать с ошибкой**: это решит
тот, кто её вызвал.

### Как читать traceback

Traceback читают **снизу вверх**:

```
Traceback (most recent call last):
  File "shop.py", line 9, in <module>
    total = checkout(cart)
  File "shop.py", line 5, in checkout
    return price_with_discount(item, 120)
  File "shop.py", line 2, in price_with_discount
    raise ValueError(f"Скидка должна быть от 0 до 100, получено {percent}")
ValueError: Скидка должна быть от 0 до 100, получено 120
```

1. Последняя строка — **тип** исключения и **сообщение**.
2. Над ней — строка, где исключение возникло.
3. Выше — цепочка вызовов, которая к ней привела. Ищите первую снизу строку **вашего**
   кода: там чаще всего и ошибка.

### Иерархия исключений

Исключения — это классы, и они наследуются друг от друга
(как на [семинаре 6](../seminar_06_inheritance/README.md#блок-1-наследование-10-мин)):

```
BaseException
├── KeyboardInterrupt        ← Ctrl+C
├── SystemExit               ← sys.exit()
└── Exception                ← все «обычные» ошибки
    ├── ArithmeticError
    │   └── ZeroDivisionError
    ├── LookupError
    │   ├── IndexError
    │   └── KeyError
    ├── OSError
    │   └── FileNotFoundError
    ├── TypeError
    └── ValueError
```

`except` ловит указанный класс **и всех его наследников**:

```python
try:
    value = data[key]
except LookupError:  # поймает и IndexError у списка, и KeyError у словаря
    value = None
```

Отсюда два правила:

- `except` проверяются **сверху вниз** — частные случаи пишут раньше общих;
- `KeyboardInterrupt` и `SystemExit` не наследуются от `Exception` специально:
  `except Exception` не должен мешать пользователю остановить программу.

> **Подробнее:** см. файл [`examples/02_raising.py`](examples/02_raising.py)

### Практика

Перейдите к разделу **Часть 2: Генерация исключений и их иерархия** в файле
[`exercises/error_handling_practice.md`](exercises/error_handling_practice.md#часть-2-генерация-исключений-и-их-иерархия).

---

## Блок 3: Собственные исключения (10 мин)

### Зачем свой класс

`ValueError("Товар закончился")` работает, но перехватить **именно** эту ошибку
и отличить её от любой другой `ValueError` не получится. Свой класс исключения
решает проблему:

```python
class OutOfStockError(Exception):
    """Товара нет на складе."""
```

Этого достаточно: тело класса может быть пустым, всё нужное достаётся от `Exception`.
Имя по соглашению заканчивается на `Error`.

### Дополнительные атрибуты

Исключение — обычный объект, и в нём можно хранить подробности, полезные тому,
кто будет его обрабатывать:

```python
class NotInRangeError(ValueError):
    """Число вне допустимого диапазона."""

    def __init__(self, value, low, high):
        super().__init__(f"{value} не входит в диапазон [{low}, {high}]")
        self.value = value
        self.low = low
        self.high = high


try:
    raise NotInRangeError(150, 0, 120)
except NotInRangeError as error:
    print(error)  # 150 не входит в диапазон [0, 120]
    print(error.high)  # 120
```

`super().__init__(сообщение)` передаёт текст родителю — именно его печатает
`print(error)` и traceback. Наследование от `ValueError` позволяет поймать ошибку
и как `NotInRangeError`, и как более общую `ValueError`.

### Своя иерархия

Для модуля или программы обычно заводят **базовое** исключение, а от него — частные:

```python
class ShopError(Exception):
    """Базовая ошибка магазина."""


class ProductNotFoundError(ShopError):
    """Такого товара нет в каталоге."""


class OutOfStockError(ShopError):
    """Товар есть в каталоге, но закончился."""
```

Теперь вызывающий код выбирает, насколько подробно реагировать: ловить конкретную
ошибку или сразу все ошибки магазина через `except ShopError`.

### Где обрабатывать

Хорошее правило: **обрабатывать ошибку там, где хватает полномочий решить, что
делать дальше.** Как в организации: кассир не решает, давать ли скидку постоянному
клиенту, — он зовёт администратора.

- Метод `Shop.buy()` не знает, кто его вызвал: консольная программа, сайт или тест.
  Поэтому он только **бросает** `OutOfStockError`.
- Главный цикл программы общается с пользователем — он **ловит** ошибку, печатает
  понятное сообщение и предлагает выбрать другой товар.

```python
while True:
    name = input("Что купить? ")
    try:
        shop.buy(name)
    except ProductNotFoundError:
        print("Такого товара нет")
    except OutOfStockError:
        print("Товар закончился, выберите другой")
```

> **Подробнее:** см. файл [`examples/03_custom_exceptions.py`](examples/03_custom_exceptions.py)

### Практика

Перейдите к разделу **Часть 3: Собственные исключения** в файле
[`exercises/error_handling_practice.md`](exercises/error_handling_practice.md#часть-3-собственные-исключения).

---

## Темы лекции, которые мы не разбираем на занятии

Короткая теория для самостоятельного чтения. Примеры — в файле
[`examples/04_chaining_and_assert.py`](examples/04_chaining_and_assert.py),
задачи — в разделе
[«Для самостоятельной работы»](exercises/error_handling_practice.md#для-самостоятельной-работы).

### Цепочки исключений: raise ... from

Если во время обработки одного исключения возникает другое, Python помнит оба:
первое сохраняется в атрибуте `__context__` нового, и traceback показывает оба
со словами *During handling of the above exception, another exception occurred*.

Часто низкоуровневую ошибку хочется **заменить** на понятную ошибку своего уровня.
Для этого есть `raise ... from`:

```python
class ConfigError(Exception):
    """Ошибка в файле настроек."""


def read_port(text):
    try:
        return int(text)
    except ValueError as error:
        raise ConfigError(f"Порт должен быть числом: {text!r}") from error
```

Исходная ошибка сохраняется в `__cause__`, а traceback говорит
*The above exception was the direct cause of the following exception*.

`raise ... from None` скрывает исходную ошибку — например, когда то, что внутри
класса лежит словарь, — это деталь реализации, которую пользователю класса знать
не нужно:

```python
def get_phone(self, name):
    try:
        return self._contacts[name]
    except KeyError:
        raise ContactNotFoundError(name) from None
```

### Инструкция assert

`assert условие, "сообщение"` бросает `AssertionError`, если условие ложно:

```python
def average(grades):
    assert len(grades) > 0, "Список оценок не должен быть пустым"
    return sum(grades) / len(grades)
```

`assert` — инструмент **отладки**: он проверяет то, что по замыслу программиста
должно быть истинно всегда (инвариант). Запуск `python -O program.py` отключает все
`assert`, поэтому проверять ими ввод пользователя нельзя — для этого есть `raise`.

Ещё `assert` удобен для простых тестов:

```python
assert average([4, 5]) == 4.5
assert average([3]) == 3
```

На [семинаре 11](../seminar_11_code_quality/README.md) мы увидим, что тесты
в pytest пишутся именно так.

---

## Итоги семинара

- Разобрались, что такое исключение и чем оно лучше специального значения вроде `-1`
- Научились перехватывать исключения через `try`/`except`, использовать `else`
  и `finally`
- Сравнили подходы LBYL и EAFP и узнали, почему в Python принят EAFP
- Научились бросать исключения инструкцией `raise` и читать traceback
- Познакомились с иерархией исключений и поняли, почему `except` ловит наследников
- Научились создавать собственные исключения с дополнительными атрибутами
- Обсудили, на каком уровне программы стоит обрабатывать ошибку

**Дальше:** на семинаре 9 выйдем за пределы стандартной библиотеки — пакеты,
виртуальные окружения, `pip`/`uv` и git.

---

## Файлы семинара

| Файл | Описание |
|------|----------|
| [`README.md`](README.md) | Этот файл — основной материал семинара |
| [`examples/01_catching.py`](examples/01_catching.py) | `try`/`except`/`else`/`finally`, LBYL и EAFP |
| [`examples/02_raising.py`](examples/02_raising.py) | `raise`, traceback, иерархия исключений |
| [`examples/03_custom_exceptions.py`](examples/03_custom_exceptions.py) | Собственные исключения и где их обрабатывать |
| [`examples/04_chaining_and_assert.py`](examples/04_chaining_and_assert.py) | `raise ... from` и `assert` |
| [`exercises/error_handling_practice.md`](exercises/error_handling_practice.md) | Задания с подсказками и решениями |
| [`exercises/starter/`](exercises/starter/) | Заготовки файлов для каждой задачи |
| [`data/readings.txt`](data/readings.txt) | Показания счётчика для задачи 1.3 |

---

## Дополнительные материалы

- [Документация: ошибки и исключения (учебник)](https://docs.python.org/3/tutorial/errors.html)
- [Документация: встроенные исключения и их иерархия](https://docs.python.org/3/library/exceptions.html#exception-hierarchy)
- [Документация: инструкция `assert`](https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement)
- [Real Python: Python Exceptions — An Introduction](https://realpython.com/python-exceptions/)
- [Real Python: LBYL vs EAFP](https://realpython.com/python-lbyl-vs-eafp/)
