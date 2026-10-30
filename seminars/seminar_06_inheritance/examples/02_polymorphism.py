"""Полиморфизм и утиная типизация: один интерфейс — разные реализации.

Запуск:
    python seminars/seminar_06_inheritance/examples/02_polymorphism.py
"""


# =============================================================================
# Один вызов — разное поведение
# =============================================================================
# Полиморфизм («много форм») — это возможность вызывать один и тот же метод
# у объектов разных классов и получать поведение, подходящее каждому из них.
class Employee:
    """Сотрудник компании."""

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def monthly_pay(self):
        """Вернуть выплату за месяц."""
        return self.salary


class Manager(Employee):
    """Менеджер получает премию за закрытые сделки."""

    def __init__(self, name, salary, deals):
        super().__init__(name, salary)
        self.deals = deals

    def monthly_pay(self):
        return self.salary + self.deals * 5_000


class Contractor(Employee):
    """Подрядчик получает почасовую оплату."""

    def __init__(self, name, rate, hours):
        super().__init__(name, 0)
        self.rate = rate
        self.hours = hours

    def monthly_pay(self):
        return self.rate * self.hours


staff = [
    Employee("Ольга", 120_000),
    Manager("Анна", 150_000, 4),
    Contractor("Иван", 2_000, 90),
]

# Вызывающему коду не нужно знать, кто перед ним: он просто вызывает метод,
# а Python сам выбирает версию, описанную в классе конкретного объекта.
total = 0
for person in staff:
    print(f"{person.name}: {person.monthly_pay()}")
    total += person.monthly_pay()

print("Фонд оплаты труда:", total)

# Без полиморфизма пришлось бы писать длинную цепочку проверок:
#
#   if isinstance(person, Manager):
#       pay = person.salary + person.deals * 5_000
#   elif isinstance(person, Contractor):
#       ...
#
# Такой код приходится править при появлении каждого нового класса,
# а цикл выше — не приходится.


# =============================================================================
# Утиная типизация: наследование не обязательно
# =============================================================================
# «Если нечто выглядит как утка, плавает как утка и крякает как утка,
# то это, вероятно, и есть утка».
#
# Python не проверяет, от какого класса произошёл объект. Ему важно одно:
# есть ли у объекта нужный метод. Поэтому полиморфизм работает и без
# общего базового класса.
class CleaningRobot:
    """Робот-пылесос: не сотрудник, но тоже получает «выплату» за обслуживание."""

    name = "Робот-пылесос"

    def monthly_pay(self):
        return 3_000


def print_payroll(workers):
    """Напечатать выплаты для любых объектов, у которых есть monthly_pay()."""
    for worker in workers:
        print(f"{worker.name}: {worker.monthly_pay()}")


# В список попали и наследники Employee, и совершенно посторонний класс:
print_payroll([Manager("Анна", 150_000, 4), CleaningRobot()])

# Важно, что объект УМЕЕТ, а не от кого он произошёл. Это и есть утиная
# типизация: интерфейс важнее родословной.

# Обратная сторона: если у объекта нужного метода нет, ошибка обнаружится
# только при вызове:
#
#   print_payroll([5])
#   AttributeError: 'int' object has no attribute 'name'
