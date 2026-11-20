"""Модуль temperature: перевод температуры. Готов — используйте как образец."""


def celsius_to_fahrenheit(celsius):
    """Перевести градусы Цельсия в градусы Фаренгейта."""
    return celsius * 9 / 5 + 32


def fahrenheit_to_celsius(fahrenheit):
    """Перевести градусы Фаренгейта в градусы Цельсия."""
    return (fahrenheit - 32) * 5 / 9


if __name__ == "__main__":
    assert celsius_to_fahrenheit(100) == 212
    assert fahrenheit_to_celsius(32) == 0
    print("Проверки модуля temperature пройдены")
