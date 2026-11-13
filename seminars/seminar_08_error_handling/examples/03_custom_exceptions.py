"""Собственные исключения: свой класс, атрибуты, иерархия, где обрабатывать.

Запуск:
    python seminars/seminar_08_error_handling/examples/03_custom_exceptions.py
"""


# =============================================================================
# Простейшее собственное исключение
# =============================================================================
# Исключение — обычный класс, унаследованный от Exception. Тело можно
# оставить пустым (достаточно докстринга): всё нужное достанется от родителя.
# Имя по соглашению заканчивается на Error.
class EmptyNameError(Exception):
    """Имя не может быть пустым."""


def greet(name):
    if not name.strip():
        raise EmptyNameError("Имя не может быть пустым")
    return f"Привет, {name}!"


try:
    print(greet("Аня"))
    print(greet("   "))
except EmptyNameError as error:
    print("Ошибка:", error)


# =============================================================================
# Исключение с дополнительными атрибутами
# =============================================================================
# В объекте исключения можно сохранить подробности: их прочитает тот,
# кто будет обрабатывать ошибку.
#
# super().__init__(сообщение) передаёт текст родителю — его и покажут
# print(error) и traceback.
#
# Наследуемся от ValueError: это тоже ошибка значения, и код, который
# ловит ValueError, поймает и NotInRangeError.
class NotInRangeError(ValueError):
    """Число вне допустимого диапазона."""

    def __init__(self, value, low, high):
        super().__init__(f"{value} не входит в диапазон [{low}, {high}]")
        self.value = value
        self.low = low
        self.high = high


def check_age(age):
    if not 0 <= age <= 120:
        raise NotInRangeError(age, 0, 120)
    return age


try:
    check_age(150)
except NotInRangeError as error:
    print(error)  # 150 не входит в диапазон [0, 120]
    print(f"Попробуйте число до {error.high}")

try:
    check_age(-5)
except ValueError as error:  # ловится и как родительский ValueError
    print("ValueError:", error)


# =============================================================================
# Ещё пример: код ответа сервера
# =============================================================================
class ServiceUnavailableError(Exception):
    """Сервис временно недоступен."""

    def __init__(self, status_code):
        super().__init__(f"Сервис недоступен, код ответа {status_code}")
        self.status_code = status_code


try:
    raise ServiceUnavailableError(503)
except ServiceUnavailableError as error:
    if error.status_code == 503:
        print("Сервер перегружен — попробуем позже")


# =============================================================================
# Своя иерархия исключений
# =============================================================================
# Для программы обычно заводят одно базовое исключение, а от него — частные.
# Тогда вызывающий код сам решает, насколько подробно реагировать.
class ShopError(Exception):
    """Базовая ошибка магазина."""


class ProductNotFoundError(ShopError):
    """Такого товара нет в каталоге."""

    def __init__(self, name):
        super().__init__(f"Товара «{name}» нет в каталоге")
        self.name = name


class OutOfStockError(ShopError):
    """Товар есть в каталоге, но закончился."""

    def __init__(self, name):
        super().__init__(f"Товар «{name}» закончился")
        self.name = name


class Shop:
    """Магазин: каталог товаров с ценами и остатками."""

    def __init__(self):
        self.prices = {"молоко": 80, "хлеб": 50, "сыр": 400}
        self.stock = {"молоко": 2, "хлеб": 0, "сыр": 1}

    def buy(self, name):
        """Купить товар и вернуть его цену.

        Метод не знает, кто его вызвал: консольная программа, сайт или тест.
        Поэтому сообщение пользователю он не печатает — только бросает
        исключение.
        """
        if name not in self.prices:
            raise ProductNotFoundError(name)
        if self.stock[name] == 0:
            raise OutOfStockError(name)
        self.stock[name] -= 1
        return self.prices[name]


# =============================================================================
# Где обрабатывать
# =============================================================================
# Правило: обрабатывать ошибку там, где хватает полномочий решить,
# что делать дальше. Как в организации: кассир не решает, давать ли скидку
# постоянному клиенту, — он зовёт администратора.
#
# Shop.buy() не знает, что делать, если товара нет, — он сообщает наверх.
# Главный цикл общается с пользователем — он и решает: напечатать сообщение
# и продолжить работу.
#
# Вместо input() — заранее заготовленный список покупок, чтобы пример
# запускался без ввода с клавиатуры.
shop = Shop()
total = 0
for name in ["молоко", "хлеб", "пиво", "сыр", "сыр"]:
    try:
        price = shop.buy(name)
    except ProductNotFoundError as error:
        print(f"{error}. Проверьте название")
    except OutOfStockError as error:
        print(f"{error}. Выберите другой товар")
    else:
        total += price
        print(f"Купили {name} за {price} руб.")
print("Итого:", total, "руб.")

# А здесь подробности не нужны — ловим все ошибки магазина разом:
try:
    shop.buy("хлеб")
except ShopError as error:
    print("Покупка не удалась:", error)
