"""Цепочки исключений (raise ... from) и инструкция assert.

Тема для самостоятельного изучения.

Запуск:
    python seminars/seminar_08_error_handling/examples/04_chaining_and_assert.py
"""

import traceback

# =============================================================================
# Ошибка во время обработки другой ошибки: __context__
# =============================================================================
# Если внутри except возникает новое исключение, Python не теряет старое:
# оно сохраняется в атрибуте __context__ нового исключения, и traceback
# показывает оба, разделяя их фразой
#   During handling of the above exception, another exception occurred:
prices = {"молоко": 80}

try:
    try:
        price = prices["хлеб"]
    except KeyError:
        price = int("нет цены")  # ошибка внутри обработчика
except ValueError as error:
    print("Новое исключение:", repr(error))
    print("Исходное (__context__):", repr(error.__context__))


# =============================================================================
# Подмена исключения: raise ... from
# =============================================================================
# Часто низкоуровневую ошибку хочется заменить понятной ошибкой своего
# уровня. Пример: настройки читаются из строк, и вызывающему коду важно
# знать «в настройках ошибка», а не «int() не смог разобрать строку».
class ConfigError(Exception):
    """Ошибка в настройках программы."""


def read_port(text):
    try:
        port = int(text)
    except ValueError as error:
        raise ConfigError(f"Порт должен быть числом: {text!r}") from error
    if not 1 <= port <= 65535:
        raise ConfigError(f"Порт должен быть от 1 до 65535, получено {port}")
    return port


try:
    read_port("80a")
except ConfigError:
    print()
    print(traceback.format_exc())
    print()

# В traceback видны обе ошибки, а между ними — фраза
#   The above exception was the direct cause of the following exception:
# Исходная ошибка сохранена в атрибуте __cause__.


# =============================================================================
# Скрыть детали реализации: raise ... from None
# =============================================================================
# Пользователю класса PhoneBook неважно, что внутри лежит словарь.
# KeyError в traceback — лишняя подробность, которая только запутает.
class ContactNotFoundError(Exception):
    """Контакта нет в телефонной книге."""

    def __init__(self, name):
        super().__init__(f"Контакт «{name}» не найден")
        self.name = name


class PhoneBook:
    def __init__(self):
        self._contacts = {"Аня": "+7 900 000-00-01"}

    def get_phone(self, name):
        try:
            return self._contacts[name]
        except KeyError:
            raise ContactNotFoundError(name) from None


book = PhoneBook()
try:
    book.get_phone("Боря")
except ContactNotFoundError:
    print(traceback.format_exc())  # только ContactNotFoundError, без KeyError
    print()


# =============================================================================
# assert — проверка того, что должно быть истинно всегда
# =============================================================================
# assert условие, "сообщение"
# Если условие ложно — бросается AssertionError с этим сообщением.
def average(grades):
    """Среднее значение оценок. Список не должен быть пустым."""
    assert len(grades) > 0, "Список оценок не должен быть пустым"
    return sum(grades) / len(grades)


print(average([4, 5, 5]))

try:
    average([])
except AssertionError as error:
    print("AssertionError:", error)

# Важно: assert — инструмент ОТЛАДКИ. Запуск с флагом -O
#     python -O program.py
# отключает все assert. Поэтому:
#   - assert проверяет предположения программиста о собственном коде;
#   - ввод пользователя и внешние данные проверяют через if + raise.


# =============================================================================
# assert для простых тестов
# =============================================================================
# Набор assert'ов — простейший тест: если всё молчит, функция работает.
assert average([4, 5]) == 4.5
assert average([3]) == 3
assert read_port("8080") == 8080
print("Все проверки пройдены")
# На семинаре 11 увидим, что тесты в pytest пишутся точно так же.
