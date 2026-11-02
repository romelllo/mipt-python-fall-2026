"""Хеширование, свои итераторы и контекстные менеджеры.

Темы для самостоятельного изучения.

Запуск:
    python seminars/seminar_07_special_methods/examples/05_hash_iter_context.py
"""

from dataclasses import dataclass

# =============================================================================
# __hash__ и __eq__: как работают словари и множества
# =============================================================================
# Словарь ищет значение не перебором, а по хешу ключа — числу, которое
# вычисляется из самого объекта. Поэтому поиск в словаре быстрый и почти
# не зависит от его размера.

print(hash("кофе"))
print(hash((1, 2)))  # кортеж хешируется
# print(hash([1, 2]))  # TypeError: unhashable type: 'list'

# Список нельзя захешировать, потому что его можно изменить: объект попал бы
# в одну «ячейку», а после изменения должен был бы оказаться в другой.
# По той же причине ключами словаря бывают только неизменяемые объекты.


# Своему классу хеш определяют методом __hash__ — вместе с __eq__:
# равные объекты обязаны иметь одинаковый хеш.
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Product({self.name!r}, {self.price})"

    def __eq__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        return self.name == other.name and self.price == other.price

    def __hash__(self):
        return hash((self.name, self.price))  # хеш кортежа из тех же полей


basket = {Product("молоко", 80), Product("молоко", 80), Product("хлеб", 50)}
print(basket)  # дубликат исчез: объекты равны и имеют одинаковый хеш

# Важно: если класс определяет __eq__ и не определяет __hash__, Python делает
# объекты нехешируемыми — чтобы равные объекты не попали в разные ячейки.
#
# Самый простой способ получить корректный хеш — frozen-датакласс:


@dataclass(frozen=True)
class Point:
    x: int
    y: int


print({Point(1, 2), Point(1, 2)})  # один элемент: __hash__ создан автоматически


# =============================================================================
# __iter__ и __next__: как на самом деле работает for
# =============================================================================
# Цикл for не знает про индексы. Он делает две вещи:
#   1. вызывает iter(коллекция)  ->  получает итератор;
#   2. вызывает next(итератор)   ->  пока не получит исключение StopIteration.
numbers = [10, 20]
iterator = iter(numbers)
print(next(iterator))  # 10
print(next(iterator))  # 20
# print(next(iterator))  # StopIteration — элементы кончились


class Countdown:
    """Обратный отсчёт: свой итератор от start до 1."""

    def __init__(self, start):
        self.start = start

    def __iter__(self):
        """Вернуть итератор. Здесь объект сам им и является."""
        self.current = self.start
        return self

    def __next__(self):
        """Вернуть следующий элемент или сообщить, что они кончились."""
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1


for number in Countdown(3):
    print(number)  # 3, 2, 1

print(list(Countdown(5)))  # итератор понимают и list(), и sum(), и for


# =============================================================================
# __enter__ и __exit__: что делает with
# =============================================================================
# Конструкция with из семинара 5 — это тоже пара специальных методов:
#   __enter__ вызывается на входе в блок, __exit__ — на выходе,
#   причём __exit__ сработает даже если внутри случилась ошибка.
class Timer:
    """Контекстный менеджер: сообщает, сколько шагов выполнено внутри блока."""

    def __init__(self, title):
        self.title = title
        self.steps = 0

    def __enter__(self):
        print(f"{self.title}: начали")
        return self  # это значение попадёт в переменную после as

    def step(self):
        self.steps += 1

    def __exit__(self, exc_type, exc_value, traceback):
        print(f"{self.title}: закончили, шагов — {self.steps}")
        return False  # False означает «ошибку не подавляем»


with Timer("Обработка данных") as timer:
    for _ in range(3):
        timer.step()

# Именно так работает open(): __enter__ открывает файл, __exit__ его закрывает.
# Три аргумента __exit__ описывают ошибку, если она произошла внутри блока;
# подробнее об исключениях — на семинаре 8.
