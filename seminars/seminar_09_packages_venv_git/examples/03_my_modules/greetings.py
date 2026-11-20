"""Свой модуль: функции, которые можно импортировать из других файлов.

Запуск самого модуля (сработает проверка внизу файла):
    python seminars/seminar_09_packages_venv_git/examples/03_my_modules/greetings.py
"""

print(f"Выполняется greetings.py, __name__ = {__name__!r}")

DEFAULT_NAME = "незнакомец"


def greet(name=DEFAULT_NAME):
    """Вернуть приветствие."""
    return f"Привет, {name}!"


def farewell(name=DEFAULT_NAME):
    """Вернуть прощание."""
    return f"Пока, {name}!"


# Этот блок выполнится, только если запустить greetings.py напрямую.
# При import greetings переменная __name__ равна "greetings", и проверки
# не мешают программе, которая импортирует модуль.
if __name__ == "__main__":
    assert greet("Аня") == "Привет, Аня!"
    assert farewell() == "Пока, незнакомец!"
    print("Проверки модуля greetings пройдены")
