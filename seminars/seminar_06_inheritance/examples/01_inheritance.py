"""Наследование: базовый и дочерний классы, super(), isinstance().

Запуск:
    python seminars/seminar_06_inheritance/examples/01_inheritance.py
"""


# =============================================================================
# Проблема: два почти одинаковых класса
# =============================================================================
# Опишем менеджера и разработчика так, как умеем с семинара 5.
class ManagerWithoutInheritance:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def describe(self):
        return f"{self.name}, зарплата {self.salary}"


class DeveloperWithoutInheritance:
    def __init__(self, name, salary):  # точно такой же конструктор
        self.name = name
        self.salary = salary

    def describe(self):  # и точно такой же метод
        return f"{self.name}, зарплата {self.salary}"


# Код повторяется. Если понадобится третий класс сотрудника или изменится
# формат описания, править придётся в нескольких местах.


# =============================================================================
# Наследование: общее выносим в базовый класс
# =============================================================================
# Класс-наследник получает все атрибуты и методы базового класса.
class Employee:
    """Сотрудник компании — базовый класс."""

    company = "МФТИ"  # атрибут класса: общий для всех сотрудников

    def __init__(self, name, salary):
        self.name = name  # атрибуты экземпляра: свои у каждого объекта
        self.salary = salary

    def describe(self):
        """Вернуть описание сотрудника."""
        return f"{self.name}, зарплата {self.salary}"

    def work(self):
        """Описать, чем занят сотрудник."""
        return f"{self.name} работает"


class Manager(Employee):  # Manager — наследник Employee
    """Менеджер."""


manager = Manager("Анна", 150_000)
print(manager.describe())  # метод достался от базового класса
print(manager.work())
print(manager.company)  # атрибут класса — тоже

# Базовый класс называют родительским, а класс-наследник — дочерним.


# =============================================================================
# Расширение: новые атрибуты и super()
# =============================================================================
# Чаще наследнику нужны свои данные. Тогда он описывает свой __init__
# и вызывает конструктор базового класса через super().
class Developer(Employee):
    """Разработчик: сотрудник, который знает языки программирования."""

    def __init__(self, name, salary, language):
        super().__init__(name, salary)  # базовый класс заполнит name и salary
        self.language = language  # а это — собственный атрибут


developer = Developer("Иван", 180_000, "Python")
print(developer.describe())  # метод базового класса знает про name и salary
print(developer.language)

# Без super() пришлось бы повторять строки self.name = name и self.salary = salary.


# =============================================================================
# Переопределение методов
# =============================================================================
# Наследник может заменить метод базового класса своей версией.
class Designer(Employee):
    """Дизайнер: описывает себя по-своему."""

    def work(self):
        return f"{self.name} рисует макеты"


class TeamLead(Employee):
    """Тимлид: дополняет поведение базового класса, а не заменяет его."""

    def work(self):
        base = super().work()  # сначала то, что делает базовый класс
        return base + " и проводит встречи"


print(Designer("Мария", 140_000).work())
print(TeamLead("Пётр", 200_000).work())

# Python ищет метод сначала в классе объекта, потом в базовом классе.


# =============================================================================
# isinstance(): объект наследника — представитель обоих классов
# =============================================================================
print(isinstance(developer, Developer))  # True
print(isinstance(developer, Employee))  # True — наследник «является» сотрудником

employee = Employee("Ольга", 120_000)
print(isinstance(employee, Developer))  # False — обратное неверно

# Любой объект в Python наследуется от общего предка object:
print(isinstance(developer, object), isinstance(5, object), isinstance("текст", object))
