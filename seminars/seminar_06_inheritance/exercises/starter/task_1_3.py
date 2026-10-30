"""Задание 1.3. Переопределение метода и проверка типа.

Опишите класс ElectricCar — наследника Car, который переопределяет метод
describe() так, чтобы к описанию добавлялась пометка «электромобиль»:

    Tesla, 2023 год (электромобиль)

Описание базового класса при этом не дублируйте — переиспользуйте его.

Затем создайте электромобиль и проверьте функцией isinstance(), что он
является и ElectricCar, и Car, и Vehicle, но обычный автомобиль
электромобилем не является.
"""


class Vehicle:
    def __init__(self, brand, year):
        self.brand = brand
        self.year = year

    def describe(self):
        return f"{self.brand}, {self.year} год"


class Car(Vehicle):
    def __init__(self, brand, year, doors):
        super().__init__(brand, year)
        self.doors = doors


# TODO: опишите класс ElectricCar с переопределённым методом describe


# TODO: создайте электромобиль и обычный автомобиль

# TODO: выведите четыре проверки isinstance из условия
