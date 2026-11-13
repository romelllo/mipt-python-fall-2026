"""Задание 2.3. Прочитайте traceback.

Программа печатает средние оценки студентов и падает. Запустите её и, НЕ читая
код целиком, только по traceback ответьте на вопросы ниже. Затем найдите
настоящую причину ошибки и исправьте её.
"""

# TODO: ответы по traceback
#   1. Тип исключения и сообщение:
#   2. Функция и строка, где оно возникло:
#   3. Цепочка вызовов, которая туда привела:
#   4. Настоящая причина ошибки:

grades = {
    "Иванов": [5, 4, 5],
    "Петрова": [4, "5", 3],
    "Сидоров": [3, 4],
}


def average(marks):
    return sum(marks) / len(marks)


def format_line(name, marks):
    return f"{name:<10} {average(marks):.2f}"


def print_report(grades):
    for name, marks in grades.items():
        print(format_line(name, marks))


print_report(grades)
