# Семинар 7: Специальные методы классов. Механизм работы классов

**Модуль:** 1 — Основы программирования на Python  
**Дата:** 09.11.2026, 18:40–20:10  
**Презентация:** [ссылка](https://docs.google.com/presentation/d/1rDy4W0b4u_hIL47vWQle1F2lTtag2kvdPqMyIAw7-Hw/edit?usp=sharing)

---

## Цели семинара

После этого семинара вы сможете:

- Объяснить, что такое специальные (dunder) методы и когда Python их вызывает
- Сделать так, чтобы объект осмысленно печатался: `__repr__` и `__str__`
- Сравнивать объекты по содержимому через `__eq__`
- Поддержать в своём классе `len()` и обращение по индексу
- Перегружать операторы `+`, `-`, `*` и сравнения для собственных классов
- Использовать `@dataclass`, чтобы не писать `__init__`, `__repr__` и `__eq__` вручную
- Понимать, когда подходит обычный класс, а когда — датакласс

---

## Подготовка

Нужен Python 3.10+ и редактор — всё как на прошлых семинарах
(если что-то не установилось: [`docs/installation.md`](../../docs/installation.md)).

Запуск примеров:

```bash
python seminars/seminar_07_special_methods/examples/01_dunder_basics.py
python seminars/seminar_07_special_methods/examples/02_operators.py
python seminars/seminar_07_special_methods/examples/03_dataclass.py
```

> Для каждой задачи есть **заготовка** в папке [`exercises/starter/`](exercises/starter/).

Семинар опирается на классы из прошлых занятий: пригодятся
[классы и методы](../seminar_05_files_and_classes/README.md#блок-3-методы-и-состояние-объекта-10-мин)
и [декораторы](../seminar_06_inheritance/README.md#темы-лекции-которые-мы-не-разбираем-на-занятии).

---

## План семинара

После каждого блока теории — 15 минут на упражнения из файла
[`exercises/special_methods_practice.md`](exercises/special_methods_practice.md).

| Время | Тема | Практика |
|-------|------|----------|
| 5 мин | Организационное: повторение семинара 6, план занятия | — |
| 10 мин | Блок 1: Базовые специальные методы | — |
| 15 мин | Практика | → Упражнения: Часть 1 |
| 10 мин | Блок 2: Перегрузка операторов | — |
| 15 мин | Практика | → Упражнения: Часть 2 |
| 10 мин | Блок 3: Декоратор @dataclass | — |
| 15 мин | Практика | → Упражнения: Часть 3 |

> **Примечание:** в таблице 80 минут, оставшиеся ~10 минут — на вопросы и разбор задач.
> Хеширование, свои итераторы, контекстные менеджеры, а также абстрактные классы
> и протоколы вынесены в раздел
> [«Темы лекции, которые мы не разбираем на занятии»](#темы-лекции-которые-мы-не-разбираем-на-занятии).

---

## Блок 1: Базовые специальные методы (10 мин)

### Что это такое

Методы с двойным подчёркиванием по краям называют **специальными**, или
**dunder-методами** (от double underscore). Их почти никогда не вызывают напрямую:
Python вызывает их сам, когда вы пишете привычный код.

| Что пишем | Что вызывает Python |
|-----------|---------------------|
| `Product("молоко", 80)` | `__init__` |
| `len(cart)` | `cart.__len__()` |
| `print(product)` | `product.__str__()` |
| `product1 == product2` | `product1.__eq__(product2)` |
| `money1 + money2` | `money1.__add__(money2)` |
| `cart[0]` | `cart.__getitem__(0)` |

Один такой метод мы используем с семинара 5 — `__init__`. Остальные работают так же
и позволяют научить свой класс вести себя как встроенный тип.

### __repr__ и __str__

Без специальных методов объект печатается бесполезно:

```python
print(milk)  # <__main__.Product object at 0x104a2b9d0>
```

`__repr__` возвращает строку для разработчика — по соглашению похожую на вызов
конструктора. `__str__` — строку для пользователя:

```python
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Product({self.name!r}, {self.price})"

    def __str__(self):
        return f"{self.name} — {self.price} руб."


print(milk)  # молоко — 80 руб.     (__str__)
print(repr(milk))  # Product('молоко', 80)  (__repr__)
print([milk])  # [Product('молоко', 80)] — в коллекциях всегда __repr__
```

> `!r` внутри f-строки подставляет `repr()` значения — строка окажется в кавычках.

Если определить только `__repr__`, он будет использоваться и вместо `__str__`.
Поэтому минимум для своего класса — это `__repr__`.

### __eq__

По умолчанию `==` сравнивает объекты по адресу в памяти, поэтому два разных объекта
с одинаковыми данными не равны:

```python
Product("молоко", 80) == Product("молоко", 80)  # False
```

Метод `__eq__` задаёт сравнение по содержимому:

```python
def __eq__(self, other):
    if not isinstance(other, Product):
        return NotImplemented
    return self.name == other.name and self.price == other.price
```

`NotImplemented` означает «я не знаю, как сравнить себя с этим объектом». Python тогда
спросит второй объект и в итоге вернёт `False` — программа не упадёт.

### __len__

Если класс описывает коллекцию, стоит поддержать `len()`:

```python
class Cart:
    def __init__(self):
        self.products = []

    def __len__(self):
        return len(self.products)


len(cart)  # 2
```

Приятный побочный эффект: объект с `__len__` можно проверять в условии — пустая
коллекция считается ложью, непустая — истиной:

```python
if cart:
    print("В корзине что-то есть")
```

> **Подробнее:** см. файл [`examples/01_dunder_basics.py`](examples/01_dunder_basics.py)

### Практика

Перейдите к разделу **Часть 1: Базовые специальные методы** в файле
[`exercises/special_methods_practice.md`](exercises/special_methods_practice.md#часть-1-базовые-специальные-методы).

---

## Блок 2: Перегрузка операторов (10 мин)

### Арифметика

Знак `+` складывает числа и склеивает строки — это один и тот же механизм: Python
вызывает `__add__` левого операнда. Значит, своему классу тоже можно объяснить,
что такое «сложить»:

```python
class Money:
    def __init__(self, amount, currency="RUB"):
        self.amount = amount
        self.currency = currency

    def __add__(self, other):
        if not isinstance(other, Money) or other.currency != self.currency:
            return NotImplemented
        return Money(self.amount + other.amount, self.currency)


Money(150_000) + Money(25_000)  # Money(175000, 'RUB')
```

| Оператор | Метод |
|----------|-------|
| `a + b` | `__add__` |
| `a - b` | `__sub__` |
| `a * b` | `__mul__` |
| `a / b` | `__truediv__` |
| `a ** b` | `__pow__` |

Важно: операция возвращает **новый** объект, а не меняет существующий — так же
ведут себя числа и строки.

### Когда число стоит слева

`money * 2` вызовет `money.__mul__(2)`, а `2 * money` — сначала `(2).__mul__(money)`.
Число не знает, как умножаться на деньги, поэтому Python спросит правый операнд
методом `__rmul__` («right multiply»):

```python
def __mul__(self, number):
    return Money(self.amount * number, self.currency)


def __rmul__(self, number):
    return self.__mul__(number)
```

### Сравнение и сортировка

Одного метода `__lt__` («less than») достаточно, чтобы заработали `sorted()`,
`min()` и `max()`:

```python
def __lt__(self, other):
    return self.amount < other.amount


sorted([Money(5_000), Money(1_200), Money(30_000)])
```

Остальные сравнения описываются методами `__le__`, `__gt__`, `__ge__` — но писать
их вручную обычно не нужно, это умеет `@dataclass` из следующего блока.

### Обращение по индексу

Квадратные скобки — тоже оператор:

```python
class Cart:
    def __init__(self):
        self.products = []

    def __getitem__(self, index):
        return self.products[index]


cart[0]  # первый товар
cart[-1]  # последний — отрицательные индексы работают сами
cart[:2]  # срез достался бесплатно
```

Более того, объект с `__getitem__` можно перебирать циклом `for`: Python запрашивает
элементы по индексам 0, 1, 2… пока не получит ошибку. Правильный способ сделать объект
перебираемым — методы `__iter__` и `__next__` (см. раздел для самостоятельной работы).

> **Подробнее:** см. файл [`examples/02_operators.py`](examples/02_operators.py)

### Практика

Перейдите к разделу **Часть 2: Перегрузка операторов** в файле
[`exercises/special_methods_practice.md`](exercises/special_methods_practice.md#часть-2-перегрузка-операторов).

---

## Блок 3: Декоратор @dataclass (10 мин)

### Проблема: много однообразного кода

Класс, который просто хранит данные, занимает два десятка строк: имена полей
повторяются в `__init__`, в `__repr__` и в `__eq__`, а сами методы однотипны.

### Решение

Декоратор `@dataclass` смотрит на аннотации типов в теле класса и сам создаёт
`__init__`, `__repr__` и `__eq__`:

```python
from dataclasses import dataclass


@dataclass
class Product:
    """Товар в магазине."""

    name: str
    price: float
    quantity: int = 1  # значение по умолчанию работает как у функций


milk = Product("молоко", 80)
print(milk)  # Product(name='молоко', price=80, quantity=1)
print(milk == Product("молоко", 80))  # True
```

Обычные методы добавляются как всегда — датакласс остаётся обычным классом.

### Полезные параметры

| Параметр | Что делает |
|----------|------------|
| `order=True` | добавляет сравнения — объекты можно сортировать (по полям сверху вниз) |
| `frozen=True` | делает объект неизменяемым; такой объект можно класть в множество и словарь |

```python
@dataclass(order=True)
class Payment:
    amount: int
    name: str


sorted(payments)  # сортировка по amount, затем по name
```

### Изменяемые значения по умолчанию

Список нельзя записать в значение по умолчанию напрямую — он стал бы общим для всех
объектов. Для этого есть `field(default_factory=...)`:

```python
from dataclasses import dataclass, field


@dataclass
class Cart:
    owner: str
    items: list = field(default_factory=list)
```

> **Когда использовать.** `@dataclass` хорош, когда класс в первую очередь **хранит
> данные**. Если класс — это в основном поведение, обычный `class` подходит лучше.

> **Подробнее:** см. файл [`examples/03_dataclass.py`](examples/03_dataclass.py)

### Практика

Перейдите к разделу **Часть 3: @dataclass** в файле
[`exercises/special_methods_practice.md`](exercises/special_methods_practice.md#часть-3-dataclass).

---

## Темы лекции, которые мы не разбираем на занятии

Короткая теория для самостоятельного чтения. Примеры — в файлах
[`examples/04_abc_and_protocol.py`](examples/04_abc_and_protocol.py)
и [`examples/05_hash_iter_context.py`](examples/05_hash_iter_context.py),
задачи — в разделе
[«Для самостоятельной работы»](exercises/special_methods_practice.md#для-самостоятельной-работы).

### Абстрактные классы и протоколы

Обещанное продолжение семинара 6: два способа описать ожидаемый интерфейс заранее,
а не узнавать об отсутствии метода в момент вызова.

```python
from abc import ABC, abstractmethod


class Sensor(ABC):
    @abstractmethod
    def read(self):
        """Наследник обязан это реализовать."""
```

Класс с нереализованным абстрактным методом создать нельзя — ошибка возникнет сразу.

`Protocol` описывает интерфейс **без наследования** — это формальная запись утиной
типизации: классу достаточно иметь подходящие методы.

```python
from typing import Protocol


class Readable(Protocol):
    def read(self) -> float: ...


def show_reading(device: Readable) -> None:
    print(device.read())
```

Выбор: `ABC` — когда у классов есть общий код и наследование уместно по смыслу;
`Protocol` — когда нужен только интерфейс.

### Хеширование: __hash__ и __eq__

Словарь ищет значение не перебором, а по **хешу** ключа — числу, вычисленному
из объекта. Поэтому ключами бывают только неизменяемые объекты: список изменился бы
и «потерялся» в своей ячейке.

Равные объекты обязаны иметь одинаковый хеш, поэтому `__hash__` определяют вместе
с `__eq__`:

```python
def __hash__(self):
    return hash((self.name, self.price))
```

Если класс определяет `__eq__` и не определяет `__hash__`, объекты становятся
нехешируемыми. Самый простой способ получить корректный хеш — `@dataclass(frozen=True)`.

### Свои итераторы: __iter__ и __next__

Цикл `for` не знает про индексы. Он вызывает `iter(коллекция)`, получает итератор
и дёргает `next()`, пока не получит `StopIteration`:

```python
class Countdown:
    def __iter__(self):
        self.current = self.start
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1
```

### Контекстные менеджеры: __enter__ и __exit__

Конструкция `with` из семинара 5 — это пара специальных методов: `__enter__`
вызывается на входе в блок, `__exit__` — на выходе, причём даже если внутри произошла
ошибка. Именно так устроен `open()`: `__enter__` открывает файл, `__exit__` закрывает.

---

## Итоги семинара

- Поняли, что специальные методы — это способ подключить свой класс к обычному
  синтаксису Python
- Научились делать осмысленный вывод объекта через `__repr__` и `__str__`
- Научились сравнивать объекты по содержимому с помощью `__eq__`
- Поддержали в своих классах `len()` и обращение по индексу
- Научились перегружать арифметические операторы и сравнения
- Освоили `@dataclass` и его параметры `order` и `frozen`
- Разобрались, когда нужен датакласс, а когда обычный класс

**Дальше:** на семинаре 8 разберём работу с ошибками — исключения, `try`/`except`
и собственные типы ошибок. Пригодится и `StopIteration`, который мы встретили здесь.

---

## Файлы семинара

| Файл | Описание |
|------|----------|
| [`README.md`](README.md) | Этот файл — основной материал семинара |
| [`examples/01_dunder_basics.py`](examples/01_dunder_basics.py) | `__repr__`, `__str__`, `__eq__`, `__len__` |
| [`examples/02_operators.py`](examples/02_operators.py) | `__add__`, `__mul__`, `__rmul__`, `__lt__`, `__getitem__` |
| [`examples/03_dataclass.py`](examples/03_dataclass.py) | `@dataclass`, `order`, `frozen`, `field` |
| [`examples/04_abc_and_protocol.py`](examples/04_abc_and_protocol.py) | Абстрактные классы и протоколы |
| [`examples/05_hash_iter_context.py`](examples/05_hash_iter_context.py) | Хеширование, итераторы, контекстные менеджеры |
| [`exercises/special_methods_practice.md`](exercises/special_methods_practice.md) | Задания с подсказками и решениями |
| [`exercises/starter/`](exercises/starter/) | Заготовки файлов для каждой задачи |

---

## Дополнительные материалы

- [Документация: модель данных и специальные методы](https://docs.python.org/3/reference/datamodel.html#special-method-names)
- [Документация: модуль `dataclasses`](https://docs.python.org/3/library/dataclasses.html)
- [Документация: модуль `abc`](https://docs.python.org/3/library/abc.html)
- [Real Python: Operator and Function Overloading](https://realpython.com/operator-function-overloading/)
- [Real Python: Data Classes](https://realpython.com/python-data-classes/)
