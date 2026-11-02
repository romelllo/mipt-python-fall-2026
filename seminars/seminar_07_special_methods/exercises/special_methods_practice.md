# Практические задания: Специальные методы классов

## Подготовка

Для каждой задачи есть **заготовка** в папке [`starter/`](starter/).

```bash
python seminars/seminar_07_special_methods/exercises/starter/task_1_1.py
```

Примеры кода к каждой части — в папке [`../examples/`](../examples/).

> **Как работать с заданиями:** прочитайте условие, напишите и **запустите** свою версию,
> и только потом раскройте решение для сверки. Если ваш код работает правильно,
> он тоже верный — решение здесь не единственное.

---

## Часть 1: Базовые специальные методы

> **Теория:** [README.md — Блок 1](../README.md#блок-1-базовые-специальные-методы-10-мин) | **Примеры:** [`examples/01_dunder_basics.py`](../examples/01_dunder_basics.py)

### Задание 1.1

Заготовка: [`starter/task_1_1.py`](starter/task_1_1.py)

Добавьте в класс `Song` два представления:

```
Song('Yesterday', 'The Beatles', 125)    для разработчика
Yesterday — The Beatles (2:05)           для пользователя
```

Проверьте оба вида вывода, в том числе для списка песен.

<details>
<summary>Подсказка</summary>

Минуты и секунды считаются делением нацело и остатком (семинар 2). Чтобы секунды
печатались как `05`, пригодится формат `{seconds:02d}` внутри f-строки.

</details>

<details>
<summary>Решение</summary>

```python
class Song:
    def __init__(self, title, artist, seconds):
        self.title = title
        self.artist = artist
        self.seconds = seconds

    def __repr__(self):
        return f"Song({self.title!r}, {self.artist!r}, {self.seconds})"

    def __str__(self):
        minutes = self.seconds // 60
        seconds = self.seconds % 60
        return f"{self.title} — {self.artist} ({minutes}:{seconds:02d})"


song = Song("Yesterday", "The Beatles", 125)
other = Song("Let It Be", "The Beatles", 243)

print(song)  # Yesterday — The Beatles (2:05)
print(repr(song))  # Song('Yesterday', 'The Beatles', 125)
print([song, other])  # в списке всегда __repr__
```

</details>

### Задание 1.2

Заготовка: [`starter/task_1_2.py`](starter/task_1_2.py)

Сделайте так, чтобы песни считались равными при совпадении названия и исполнителя
(длительность не важна — это может быть другая запись). Сравнение с объектом другого
типа не должно приводить к ошибке.

<details>
<summary>Подсказка</summary>

Если объект не того типа, верните `NotImplemented` — Python сам превратит это
в `False`.

</details>

<details>
<summary>Решение</summary>

```python
def __eq__(self, other):
    if not isinstance(other, Song):
        return NotImplemented
    return self.title == other.title and self.artist == other.artist


print(Song("Yesterday", "The Beatles", 125) == Song("Yesterday", "The Beatles", 130))
# True — длительность в сравнении не участвует

print(Song("Yesterday", "The Beatles", 125) == Song("Let It Be", "The Beatles", 243))
# False

print(Song("Yesterday", "The Beatles", 125) == "Yesterday")
# False — программа не упала
```

</details>

### Задание 1.3

Заготовка: [`starter/task_1_3.py`](starter/task_1_3.py)

Опишите класс `Playlist` с названием, списком песен, методом `add(song)` и поддержкой
функции `len()`. Проверьте в условии пустой и непустой плейлисты.

<details>
<summary>Решение</summary>

```python
class Playlist:
    """Плейлист со списком песен."""

    def __init__(self, title):
        self.title = title
        self.songs = []

    def add(self, song):
        self.songs.append(song)

    def __len__(self):
        return len(self.songs)


playlist = Playlist("Для работы")
playlist.add(Song("Yesterday", "The Beatles", 125))
playlist.add(Song("Let It Be", "The Beatles", 243))

print(len(playlist))  # 2

if playlist:
    print("В плейлисте есть песни")

if not Playlist("Пустой"):
    print("А этот плейлист пуст")
```

Условие работает благодаря `__len__`: объект с нулевой длиной считается ложью.

</details>

---

## Часть 2: Перегрузка операторов

> **Теория:** [README.md — Блок 2](../README.md#блок-2-перегрузка-операторов-10-мин) | **Примеры:** [`examples/02_operators.py`](../examples/02_operators.py)

### Задание 2.1

Заготовка: [`starter/task_2_1.py`](starter/task_2_1.py)

Опишите класс `Vector` с координатами `x` и `y`, который поддерживает сложение
и вычитание и осмысленно печатается:

```
Vector(1, 2) + Vector(3, 4)  ->  Vector(4, 6)
Vector(5, 7) - Vector(1, 2)  ->  Vector(4, 5)
```

Операции должны возвращать новый вектор, а не менять существующий.

<details>
<summary>Решение</summary>

```python
class Vector:
    """Вектор на плоскости."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x - other.x, self.y - other.y)


first = Vector(1, 2)
second = Vector(3, 4)

print(first + second)  # Vector(4, 6)
print(Vector(5, 7) - Vector(1, 2))  # Vector(4, 5)
print(first)  # Vector(1, 2) — исходный вектор не изменился
```

</details>

### Задание 2.2

Заготовка: [`starter/task_2_2.py`](starter/task_2_2.py)

Добавьте умножение вектора на число, работающее с обеих сторон, и сравнение
на равенство.

<details>
<summary>Подсказка</summary>

Когда число стоит слева, Python сначала спрашивает число — оно не умеет умножаться
на вектор, поэтому вызывается «правый» вариант метода у вектора.

</details>

<details>
<summary>Решение</summary>

```python
def __mul__(self, number):
    if not isinstance(number, int | float):
        return NotImplemented
    return Vector(self.x * number, self.y * number)


def __rmul__(self, number):
    return self.__mul__(number)


def __eq__(self, other):
    if not isinstance(other, Vector):
        return NotImplemented
    return self.x == other.x and self.y == other.y


print(Vector(2, 3) * 3)  # Vector(6, 9)
print(3 * Vector(2, 3))  # Vector(6, 9) — сработал __rmul__
print(Vector(2, 3) == Vector(2, 3))  # True
```

</details>

### Задание 2.3

Заготовка: [`starter/task_2_3.py`](starter/task_2_3.py)

Дополните `Playlist` так, чтобы к песням можно было обращаться по индексу
и перебирать их циклом `for`.

<details>
<summary>Подсказка</summary>

Достаточно одного метода, который принимает индекс и возвращает элемент из списка
внутри объекта. Отрицательные индексы и перебор заработают сами.

</details>

<details>
<summary>Решение</summary>

```python
def __getitem__(self, index):
    return self.songs[index]


playlist = Playlist("Для работы")
playlist.add(Song("Yesterday", "The Beatles", 125))
playlist.add(Song("Let It Be", "The Beatles", 243))
playlist.add(Song("Come Together", "The Beatles", 259))

print(playlist[0])  # первая песня
print(playlist[-1])  # последняя песня

for song in playlist:  # перебор работает благодаря __getitem__
    print(song.title)
```

Python запрашивает элементы по индексам 0, 1, 2… пока список не кончится.

</details>

---

## Часть 3: @dataclass

> **Теория:** [README.md — Блок 3](../README.md#блок-3-декоратор-dataclass-10-мин) | **Примеры:** [`examples/03_dataclass.py`](../examples/03_dataclass.py)

### Задание 3.1

Заготовка: [`starter/task_3_1.py`](starter/task_3_1.py)

Перепишите `Song` через `@dataclass`: конструктор, представление и сравнение должны
появиться сами. Добавьте метод `duration()`, возвращающий длительность в формате `2:05`.

<details>
<summary>Решение</summary>

```python
from dataclasses import dataclass


@dataclass
class Song:
    """Песня в плейлисте."""

    title: str
    artist: str
    seconds: int = 0

    def duration(self):
        """Вернуть длительность в формате «минуты:секунды»."""
        return f"{self.seconds // 60}:{self.seconds % 60:02d}"


song = Song("Yesterday", "The Beatles", 125)

print(song)  # Song(title='Yesterday', artist='The Beatles', seconds=125)
print(song == Song("Yesterday", "The Beatles", 125))  # True
print(song.duration())  # 2:05
```

Сравните с заданием 1.1: три метода заменились одной строкой декоратора. Правда,
`__eq__` теперь сравнивает **все** поля, включая длительность.

</details>

### Задание 3.2

Заготовка: [`starter/task_3_2.py`](starter/task_3_2.py)

Опишите датакласс `Track` (длительность и название) так, чтобы треки можно было
сортировать по длительности. Выведите отсортированный список, самый короткий
и самый длинный трек.

<details>
<summary>Подсказка</summary>

Сравнение добавляется параметром декоратора, а сравниваются поля сверху вниз —
значит, порядок полей в классе определяет, по чему идёт сортировка.

</details>

<details>
<summary>Решение</summary>

```python
from dataclasses import dataclass


@dataclass(order=True)
class Track:
    """Трек: сравнивается по длительности, затем по названию."""

    seconds: int
    title: str


tracks = [
    Track(243, "Let It Be"),
    Track(125, "Yesterday"),
    Track(259, "Come Together"),
]

print(sorted(tracks))
print("Самый короткий:", min(tracks))  # Track(seconds=125, title='Yesterday')
print("Самый длинный:", max(tracks))  # Track(seconds=259, title='Come Together')
```

Если поставить `title` первым полем, сортировка пойдёт по алфавиту — порядок полей
важен.

</details>

### Задание 3.3

Заготовка: [`starter/task_3_3.py`](starter/task_3_3.py)

Опишите датакласс `Playlist` с названием и списком песен (по умолчанию пустым),
методом `add(song)` и методом `total_seconds()`. Убедитесь, что у двух разных
плейлистов свои независимые списки.

<details>
<summary>Подсказка</summary>

Пустой список в значении по умолчанию стал бы общим для всех объектов, поэтому
для изменяемых значений используется отдельная функция из модуля `dataclasses`.

</details>

<details>
<summary>Решение</summary>

```python
from dataclasses import dataclass, field


@dataclass
class Playlist:
    """Плейлист со списком песен."""

    title: str
    songs: list[Song] = field(default_factory=list)

    def add(self, song):
        self.songs.append(song)

    def total_seconds(self):
        return sum(song.seconds for song in self.songs)


playlist = Playlist("Для работы")
playlist.add(Song("Yesterday", "The Beatles", 125))
playlist.add(Song("Let It Be", "The Beatles", 243))

print(playlist)
print("Общая длительность:", playlist.total_seconds())  # 368

print(Playlist("Пустой").songs)  # [] — свой независимый список
```

</details>

---

## Для самостоятельной работы

Задачи на темы, которые мы не разбираем на занятии: абстрактные классы и протоколы,
хеширование, свои итераторы и контекстные менеджеры (теория — в
[README](../README.md#темы-лекции-которые-мы-не-разбираем-на-занятии), примеры —
в файлах [`examples/04_abc_and_protocol.py`](../examples/04_abc_and_protocol.py)
и [`examples/05_hash_iter_context.py`](../examples/05_hash_iter_context.py)).

### Задание 4.1

Опишите абстрактный класс `Notification` с методом `send(text)`, который обязаны
реализовать наследники, и обычным методом `describe()`. Сделайте два наследника:
`EmailNotification` (печатает «Письмо на адрес …») и `SmsNotification`
(печатает «SMS на номер …»). Проверьте, что создать сам `Notification` нельзя.

<details>
<summary>Решение</summary>

```python
from abc import ABC, abstractmethod


class Notification(ABC):
    """Уведомление пользователю."""

    def __init__(self, address):
        self.address = address

    @abstractmethod
    def send(self, text):
        """Отправить уведомление. Наследник обязан это реализовать."""

    def describe(self):
        return f"{type(self).__name__} -> {self.address}"


class EmailNotification(Notification):
    def send(self, text):
        print(f"Письмо на адрес {self.address}: {text}")


class SmsNotification(Notification):
    def send(self, text):
        print(f"SMS на номер {self.address}: {text}")


for notification in [
    EmailNotification("anna@example.com"),
    SmsNotification("+7 900 000-00-00"),
]:
    print(notification.describe())
    notification.send("Семинар в понедельник")

# Notification("adress")
# TypeError: Can't instantiate abstract class Notification with abstract method send
```

`type(self).__name__` возвращает имя класса объекта — удобно для отладочного вывода.

</details>

### Задание 4.2

Опишите протокол `Playable` с методом `play()` и функцию `play_all(items)`, которая
вызывает `play()` у каждого объекта списка. Сделайте два класса, которые **не
наследуют** протокол, но подходят под него, и проверьте работу функции.

<details>
<summary>Решение</summary>

```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class Playable(Protocol):
    """Всё, что можно воспроизвести."""

    def play(self) -> str: ...


class Song:
    def play(self) -> str:
        return "играет песня"


class Podcast:
    def play(self) -> str:
        return "играет подкаст"


def play_all(items: list[Playable]) -> None:
    for item in items:
        print(item.play())


play_all([Song(), Podcast()])

print(isinstance(Song(), Playable))  # True — подходит по методам
print(isinstance(42, Playable))  # False
```

Ни `Song`, ни `Podcast` не знают о существовании протокола — этим `Protocol`
и отличается от абстрактного класса.

</details>

### Задание 4.3

Сделайте класс `Song` (название и исполнитель) пригодным для хранения в множестве,
чтобы дубликаты исчезали. Решите задачу двумя способами: вручную и с помощью
датакласса.

<details>
<summary>Подсказка</summary>

Равные объекты обязаны иметь одинаковый хеш. Проще всего взять хеш кортежа
из тех же полей, которые участвуют в сравнении.

</details>

<details>
<summary>Решение</summary>

```python
class Song:
    def __init__(self, title, artist):
        self.title = title
        self.artist = artist

    def __repr__(self):
        return f"Song({self.title!r}, {self.artist!r})"

    def __eq__(self, other):
        if not isinstance(other, Song):
            return NotImplemented
        return self.title == other.title and self.artist == other.artist

    def __hash__(self):
        return hash((self.title, self.artist))


library = {Song("Yesterday", "The Beatles"), Song("Yesterday", "The Beatles")}
print(library)  # один элемент


# То же самое неизменяемым датаклассом — методы создаются автоматически:
from dataclasses import dataclass


@dataclass(frozen=True)
class FrozenSong:
    title: str
    artist: str


print({FrozenSong("Yesterday", "The Beatles"), FrozenSong("Yesterday", "The Beatles")})
```

Если определить `__eq__` и забыть `__hash__`, объекты станут нехешируемыми
и в множество их положить не получится.

</details>

### Задание 4.4

Опишите класс `EvenNumbers(limit)`, который можно перебирать циклом `for`: он выдаёт
чётные числа от 2 до `limit` включительно.

```
for number in EvenNumbers(10):
    print(number)   # 2 4 6 8 10
```

<details>
<summary>Подсказка</summary>

Нужны два метода: один возвращает итератор и готовит начальное состояние, второй
выдаёт следующее значение, а когда числа кончились — сообщает об этом исключением
`StopIteration`.

</details>

<details>
<summary>Решение</summary>

```python
class EvenNumbers:
    """Чётные числа от 2 до limit включительно."""

    def __init__(self, limit):
        self.limit = limit

    def __iter__(self):
        self.current = 0
        return self

    def __next__(self):
        self.current += 2
        if self.current > self.limit:
            raise StopIteration
        return self.current


for number in EvenNumbers(10):
    print(number)

print(list(EvenNumbers(7)))  # [2, 4, 6]
print(sum(EvenNumbers(10)))  # 30
```

Любая функция, которая умеет перебирать коллекции (`list`, `sum`, `max`), теперь
работает и с этим классом.

</details>

### Задание 4.5

Опишите контекстный менеджер `Section(title)`, который печатает заголовок в рамке
на входе в блок и разделитель на выходе:

```
=== Отчёт ===
строка отчёта
=============
```

<details>
<summary>Решение</summary>

```python
class Section:
    """Печатает заголовок и разделитель вокруг блока кода."""

    def __init__(self, title):
        self.title = title

    def __enter__(self):
        self.header = f"=== {self.title} ==="
        print(self.header)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("=" * len(self.header))
        return False


with Section("Отчёт"):
    print("строка отчёта")
```

`__exit__` выполнится в любом случае — даже если внутри блока произойдёт ошибка.
Именно поэтому `with` безопасен для работы с файлами.

</details>
