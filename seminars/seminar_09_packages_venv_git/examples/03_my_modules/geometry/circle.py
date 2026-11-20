"""Модуль circle пакета geometry."""

import math


def area(radius):
    """Площадь круга."""
    return math.pi * radius**2


def perimeter(radius):
    """Длина окружности."""
    return 2 * math.pi * radius
