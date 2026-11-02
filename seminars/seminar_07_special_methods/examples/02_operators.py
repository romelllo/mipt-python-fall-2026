"""Перегрузка операторов: __add__, __mul__, __lt__, __getitem__.

Запуск:
    python seminars/seminar_07_special_methods/examples/02_operators.py
"""


# =============================================================================
# Арифметика: __add__ и __sub__
# =============================================================================
# Знак + для чисел складывает, для строк и списков склеивает (семинар 1).
# Это один и тот же механизм: Python вызывает метод __add__ левого операнда.
# Значит, своему классу тоже можно объяснить, что такое «сложить».
class Money:
    """Денежная сумма в заданной валюте."""

    def __init__(self, amount, currency="RUB"):
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"Money({self.amount}, {self.currency!r})"

    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount == other.amount and self.currency == other.currency

    def __add__(self, other):
        """Сложить две суммы одной валюты."""
        if not isinstance(other, Money) or other.currency != self.currency:
            return NotImplemented
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other):
        if not isinstance(other, Money) or other.currency != self.currency:
            return NotImplemented
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, number):
        """Умножить сумму на число: Money(100) * 3."""
        if not isinstance(number, int | float):
            return NotImplemented
        return Money(self.amount * number, self.currency)

    def __rmul__(self, number):
        """То же самое, но когда число стоит слева: 3 * Money(100)."""
        return self.__mul__(number)

    def __lt__(self, other):
        """Меньше — нужно для sorted() и оператора <."""
        if not isinstance(other, Money) or other.currency != self.currency:
            return NotImplemented
        return self.amount < other.amount


salary = Money(150_000)
bonus = Money(25_000)

print(salary + bonus)  # Money(175000, 'RUB')
print(salary - bonus)  # Money(125000, 'RUB')
print(salary * 2)  # Money(300000, 'RUB')  — вызвался __mul__
print(2 * salary)  # Money(300000, 'RUB')  — вызвался __rmul__

# Важно: операции возвращают НОВЫЙ объект, а не меняют существующий —
# ровно так же ведут себя числа и строки.

# Когда __add__ вернёт NotImplemented, Python сообщит об ошибке:
#   Money(100) + Money(100, "USD")
#   TypeError: unsupported operand type(s) for +: 'Money' and 'Money'

# =============================================================================
# Сравнение: __lt__ и сортировка
# =============================================================================
# Одного метода __lt__ достаточно, чтобы заработали sorted(), min() и max().
payments = [Money(5_000), Money(1_200), Money(30_000)]

print(sorted(payments))
print(min(payments), max(payments))
print(Money(100) < Money(200))

# Остальные сравнения описываются методами __le__, __gt__, __ge__.
# Писать их вручную не обязательно: на третьем блоке увидим, как это
# делает @dataclass.


# =============================================================================
# Обращение по индексу: __getitem__
# =============================================================================
# Квадратные скобки — тоже оператор. Метод __getitem__ позволяет обращаться
# к объекту как к списку или словарю.
class Cart:
    """Корзина, которая ведёт себя как список товаров."""

    def __init__(self):
        self.products = []

    def add(self, name, price):
        self.products.append((name, price))

    def __len__(self):
        return len(self.products)

    def __getitem__(self, index):
        return self.products[index]

    def __repr__(self):
        return f"Cart({self.products!r})"


cart = Cart()
cart.add("молоко", 80)
cart.add("хлеб", 50)
cart.add("кофе", 180)

print(cart[0])  # ('молоко', 80)
print(cart[-1])  # ('кофе', 180) — отрицательные индексы работают сами
print(cart[:2])  # срез тоже достался бесплатно

# Более того, объект с __getitem__ можно перебирать циклом for:
for name, price in cart:
    print(f"{name}: {price}")

# Python просто запрашивает элементы по индексам 0, 1, 2… пока не получит
# IndexError. Правильный способ сделать объект перебираемым — методы
# __iter__ и __next__ (см. раздел для самостоятельной работы).
