"""Композиция: отношение «имеет» вместо «является».

Запуск:
    python seminars/seminar_06_inheritance/examples/03_composition.py
"""


# =============================================================================
# Два способа связать классы
# =============================================================================
# Наследование отвечает на вопрос «чем объект ЯВЛЯЕТСЯ»,
# композиция — «что у объекта ЕСТЬ».
#
#   Менеджер ЯВЛЯЕТСЯ сотрудником   -> наследование
#   У сотрудника ЕСТЬ рабочий график -> композиция
#
# При композиции объект просто хранится в атрибуте другого объекта.
class Schedule:
    """Рабочий график сотрудника."""

    def __init__(self, hours_per_week, remote):
        self.hours_per_week = hours_per_week
        self.remote = remote

    def describe(self):
        place = "удалённо" if self.remote else "в офисе"
        return f"{self.hours_per_week} ч/неделю, {place}"


class Employee:
    """Сотрудник, у которого есть график."""

    def __init__(self, name, schedule):
        self.name = name
        self.schedule = schedule  # не наследуем график, а храним его

    def describe(self):
        return f"{self.name}: {self.schedule.describe()}"


full_time = Schedule(40, remote=False)
part_time = Schedule(20, remote=True)

print(Employee("Анна", full_time).describe())
print(Employee("Иван", part_time).describe())

# Один и тот же объект-график можно переиспользовать для разных сотрудников,
# а при необходимости заменить его другим — объекту это безразлично.


# =============================================================================
# Класс, который состоит из других объектов
# =============================================================================
# Отдел не «является» сотрудником — он из них состоит.
class Department:
    """Отдел компании: имеет название и список сотрудников."""

    def __init__(self, title):
        self.title = title
        self.employees = []

    def hire(self, employee):
        """Принять сотрудника в отдел."""
        self.employees.append(employee)

    def headcount(self):
        """Вернуть количество сотрудников."""
        return len(self.employees)

    def describe(self):
        """Вернуть описание отдела со всеми сотрудниками."""
        lines = [f"Отдел «{self.title}», сотрудников: {self.headcount()}"]
        for employee in self.employees:
            lines.append("  - " + employee.describe())
        return "\n".join(lines)


development = Department("Разработка")
development.hire(Employee("Анна", full_time))
development.hire(Employee("Иван", part_time))

print(development.describe())


# =============================================================================
# Когда наследование подводит
# =============================================================================
# Соблазнительно сделать «отдел — это список сотрудников» и унаследоваться
# от list. Но тогда отдел получит весь интерфейс списка: его можно будет
# отсортировать, перевернуть, сложить с другим списком — действия, которые
# для отдела не имеют смысла.
#
#   class Department(list):   # так лучше не делать
#       ...
#
# Композиция даёт ровно те действия, которые нужны: hire() и headcount().
# Поэтому общее правило — начинать с композиции, а наследование использовать,
# когда объект действительно ЯВЛЯЕТСЯ частным случаем другого.

print("Сотрудников в отделе:", development.headcount())
