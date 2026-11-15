"""Генерация исключений: raise, traceback, иерархия исключений.

Запуск:
    python seminars/seminar_08_error_handling/examples/02_raising.py
"""

import traceback

# =============================================================================
# raise — бросить исключение самому
# =============================================================================
# Своя функция тоже может сообщить, что её вызвали неправильно.
# Для этого создаём объект исключения и бросаем его инструкцией raise.


def make_discount(price, percent):
    """Вернуть цену со скидкой percent процентов."""
    if price < 0:
        raise ValueError(f"Цена не может быть отрицательной: {price}")
    if not 0 <= percent <= 100:
        raise ValueError(f"Скидка должна быть от 0 до 100, получено {percent}")
    return price * (100 - percent) / 100


print(make_discount(1000, 15))  # 850.0

# Функция не решает, что делать с ошибкой, — это решает вызывающий код:
try:
    make_discount(1000, 120)
except ValueError as error:
    print("Не удалось посчитать скидку:", error)

# Какой тип выбрать? Тот, который выбрал бы сам Python в похожей ситуации:
#   ValueError  — тип правильный, а значение неподходящее
#   TypeError   — передали объект не того типа
#   KeyError    — нет такого ключа
#   IndexError  — нет такого индекса


# =============================================================================
# Как читать traceback
# =============================================================================
# Traceback показывает цепочку вызовов, которая привела к ошибке.
# Модуль traceback позволяет напечатать его, не останавливая программу, —
# так мы увидим его прямо в выводе примера.


def price_with_discount(item, percent):
    return make_discount(item["price"], percent)


def checkout(cart):
    total = 0
    for item in cart:
        total += price_with_discount(item, 120)
    return total


try:
    checkout([{"name": "чай", "price": 300}])
except ValueError:
    print()
    print(traceback.format_exc())
    print()

# Traceback читают СНИЗУ ВВЕРХ:
#   1. Последняя строка — тип исключения и сообщение.
#   2. Над ней — строка, где исключение было брошено (raise в make_discount).
#   3. Выше — кто кого вызывал: checkout -> price_with_discount -> make_discount.
# Ошибка не обязательно там, где бросили исключение: здесь виноват
# checkout, который передаёт скидку 120.


# =============================================================================
# Иерархия исключений
# =============================================================================
# Исключения — это классы, и они наследуются друг от друга:
#
#   BaseException
#   ├── KeyboardInterrupt        <- пользователь нажал Ctrl+C
#   ├── SystemExit               <- вызван sys.exit()
#   └── Exception                <- все «обычные» ошибки
#       ├── ArithmeticError
#       │   └── ZeroDivisionError
#       ├── LookupError
#       │   ├── IndexError
#       │   └── KeyError
#       ├── OSError
#       │   └── FileNotFoundError
#       ├── TypeError
#       └── ValueError
#
# Проверим через issubclass (аналог isinstance для классов):
print(issubclass(ZeroDivisionError, ArithmeticError))  # True
print(issubclass(KeyError, LookupError))  # True
print(issubclass(FileNotFoundError, OSError))  # True
print(issubclass(KeyboardInterrupt, Exception))  # False!


# =============================================================================
# except ловит класс и всех его наследников
# =============================================================================
def get_item(collection, key):
    """Достать элемент из списка или словаря; None, если его нет."""
    try:
        return collection[key]
    except LookupError:  # поймает и IndexError, и KeyError
        return None


print(get_item([10, 20, 30], 5))  # None — был IndexError
print(get_item({"a": 1}, "b"))  # None — был KeyError
print(get_item({"a": 1}, "a"))  # 1


# =============================================================================
# Порядок except важен
# =============================================================================
# except проверяются сверху вниз, выполняется ПЕРВЫЙ подходящий.
# Поэтому частные случаи пишут раньше общих.
try:
    {"a": 1}["b"]
except KeyError:
    print("Нет такого ключа")  # сработает этот
except LookupError:
    print("Что-то не нашлось")

# Если поменять их местами, до KeyError очередь не дойдёт никогда:
# LookupError поймает его первым.


# =============================================================================
# Почему KeyboardInterrupt не наследуется от Exception
# =============================================================================
# Чтобы «except Exception» не мешал остановить программу по Ctrl+C.
# А голый «except:» ловит вообще всё, включая KeyboardInterrupt, —
# ещё одна причина так не писать.
#
# StopIteration с семинара 7 — тоже наследник Exception: цикл for
# перехватывает его сам, когда итератор заканчивается.
print(issubclass(StopIteration, Exception))  # True
