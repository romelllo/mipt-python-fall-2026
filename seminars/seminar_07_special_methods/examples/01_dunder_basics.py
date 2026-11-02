"""Специальные методы: __repr__, __str__, __eq__, __len__.

Запуск:
    python seminars/seminar_07_special_methods/examples/01_dunder_basics.py
"""


# =============================================================================
# Что такое специальные методы
# =============================================================================
# Методы с двойным подчёркиванием по краям (__init__, __len__) называют
# специальными, или dunder-методами (double underscore).
#
# Их почти никогда не вызывают напрямую. Вместо этого Python вызывает их сам,
# когда вы пишете привычный код:
#
#   len(obj)        ->  obj.__len__()
#   print(obj)      ->  obj.__str__()
#   obj1 == obj2    ->  obj1.__eq__(obj2)
#   obj1 + obj2     ->  obj1.__add__(obj2)
#
# Один из них мы используем с семинара 5: __init__ вызывается при создании
# объекта. Остальные работают так же — это способ научить свой класс
# вести себя как встроенный тип.
class Product:
    """Товар в магазине (пока без специальных методов)."""

    def __init__(self, name, price):
        self.name = name
        self.price = price


milk = Product("молоко", 80)
print(milk)  # <__main__.Product object at 0x...> — бесполезно


# =============================================================================
# __repr__ — как объект выглядит в выводе
# =============================================================================
# __repr__ должен возвращать строку, по которой разработчику понятно,
# что это за объект. По соглашению — в виде вызова конструктора.
class ProductWithRepr:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Product({self.name!r}, {self.price})"


milk = ProductWithRepr("молоко", 80)
print(milk)  # Product('молоко', 80)
print([milk, ProductWithRepr("хлеб", 50)])  # работает и внутри списка

# !r внутри f-строки подставляет repr() значения — строка будет в кавычках.


# =============================================================================
# __str__ — как объект выглядит для пользователя
# =============================================================================
# Если нужен отдельный «человеческий» вид, добавляют __str__:
# его использует print() и f-строки, а __repr__ остаётся для разработчика.
class ProductWithStr:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Product({self.name!r}, {self.price})"

    def __str__(self):
        return f"{self.name} — {self.price} руб."


bread = ProductWithStr("хлеб", 50)
print(bread)  # хлеб — 50 руб.        (__str__)
print(repr(bread))  # Product('хлеб', 50)   (__repr__)
print([bread])  # [Product('хлеб', 50)] — в коллекциях всегда __repr__

# Если определить только __repr__, он будет использоваться и вместо __str__.
# Поэтому минимум для своего класса — это __repr__.


# =============================================================================
# __eq__ — сравнение объектов
# =============================================================================
# По умолчанию == сравнивает объекты по их адресу в памяти: два разных объекта
# с одинаковыми данными не равны.
print(ProductWithRepr("молоко", 80) == ProductWithRepr("молоко", 80))  # False


class Money:
    """Денежная сумма в заданной валюте."""

    def __init__(self, amount, currency="RUB"):
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"Money({self.amount}, {self.currency!r})"

    def __eq__(self, other):
        """Две суммы равны, если совпадают и значение, и валюта."""
        if not isinstance(other, Money):
            return NotImplemented  # сравнение с чем-то другим нас не касается
        return self.amount == other.amount and self.currency == other.currency


print(Money(100) == Money(100))  # True
print(Money(100) == Money(100, "USD"))  # False
print(Money(100) == 100)  # False — Python сам разберётся с NotImplemented

# NotImplemented — специальное значение: «я не знаю, как сравнить себя с этим».
# Python в таком случае попробует спросить второй объект и в итоге вернёт False.


# =============================================================================
# __len__ — длина объекта
# =============================================================================
# Если класс описывает коллекцию, ему стоит поддержать len().
class Cart:
    """Корзина покупок."""

    def __init__(self):
        self.products = []

    def add(self, product):
        self.products.append(product)

    def __len__(self):
        return len(self.products)

    def __repr__(self):
        return f"Cart({self.products!r})"


cart = Cart()
cart.add(ProductWithRepr("молоко", 80))
cart.add(ProductWithRepr("хлеб", 50))

print(len(cart))  # 2 — Python вызвал cart.__len__()
print(cart)

# Приятный побочный эффект: объект с __len__ можно проверять в условии —
# пустая коллекция считается ложью, непустая — истиной.
if cart:
    print("В корзине что-то есть")

empty_cart = Cart()
if not empty_cart:
    print("А эта корзина пуста")
