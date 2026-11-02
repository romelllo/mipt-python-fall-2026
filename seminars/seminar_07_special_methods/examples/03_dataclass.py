"""@dataclass: специальные методы, которые пишутся сами.

Запуск:
    python seminars/seminar_07_special_methods/examples/03_dataclass.py
"""

from dataclasses import dataclass, field

# =============================================================================
# Проблема: много однообразного кода
# =============================================================================
# Класс, который просто хранит данные, выглядит так:
#
#   class Product:
#       def __init__(self, name, price, quantity=1):
#           self.name = name
#           self.price = price
#           self.quantity = quantity
#
#       def __repr__(self):
#           return f"Product({self.name!r}, {self.price}, {self.quantity})"
#
#       def __eq__(self, other):
#           ...
#
# Имена полей повторяются по три-четыре раза, а сами методы однотипны.


# =============================================================================
# Решение: декоратор @dataclass
# =============================================================================
# Декоратор (семинар 6) @dataclass смотрит на аннотации типов в теле класса
# и сам создаёт __init__, __repr__ и __eq__.
@dataclass
class Product:
    """Товар в магазине."""

    name: str
    price: float
    quantity: int = 1  # значение по умолчанию работает как у функций


milk = Product("молоко", 80)
print(milk)  # Product(name='молоко', price=80, quantity=1)
print(milk == Product("молоко", 80))  # True — __eq__ сравнивает поля
print(milk.price)  # обычный атрибут

# Поля с значением по умолчанию идут последними — как параметры функции.


# =============================================================================
# Методы добавляются как обычно
# =============================================================================
@dataclass
class CartItem:
    """Позиция в корзине."""

    name: str
    price: float
    quantity: int = 1

    def total(self):
        """Стоимость позиции с учётом количества."""
        return self.price * self.quantity


item = CartItem("кофе", 180, 3)
print(item, item.total())


# =============================================================================
# Параметры декоратора
# =============================================================================
# order=True добавляет сравнения (__lt__, __gt__ и другие): объекты можно
# сортировать. Сравнение идёт по полям сверху вниз.
@dataclass(order=True)
class Payment:
    amount: int
    name: str


payments = [Payment(5_000, "аванс"), Payment(1_200, "бонус"), Payment(30_000, "оклад")]
print(sorted(payments))

# frozen=True делает объект неизменяемым: после создания поля менять нельзя.
# Такой объект можно класть в множество и использовать как ключ словаря.


@dataclass(frozen=True)
class Point:
    x: int
    y: int


point = Point(1, 2)
print(point, {point: "начало маршрута"})

# point.x = 10
# dataclasses.FrozenInstanceError: cannot assign to field 'x'


# =============================================================================
# Изменяемые значения по умолчанию
# =============================================================================
# Список нельзя записать в значение по умолчанию напрямую — он был бы общим
# для всех объектов. Для этого есть field(default_factory=...).
@dataclass
class Cart:
    """Корзина покупок."""

    owner: str
    items: list[CartItem] = field(default_factory=list)

    def add(self, item):
        self.items.append(item)

    def total(self):
        return sum(item.total() for item in self.items)


cart = Cart("Анна")
cart.add(CartItem("молоко", 80, 2))
cart.add(CartItem("кофе", 180))

print(cart)
print("Итого:", cart.total())

other_cart = Cart("Иван")
print("У второй корзины свой список:", other_cart.items)

# =============================================================================
# Когда использовать
# =============================================================================
# @dataclass хорош, когда класс в первую очередь ХРАНИТ данные.
# Если класс — это в основном поведение (методы), обычный class подходит лучше.
