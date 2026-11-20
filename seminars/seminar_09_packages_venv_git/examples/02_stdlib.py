"""Стандартная библиотека: random, datetime, json.

Запуск:
    python seminars/seminar_09_packages_venv_git/examples/02_stdlib.py
"""

import json
import random
import secrets
import tempfile
from datetime import date, datetime, timedelta
from pathlib import Path

# =============================================================================
# random — случайные числа
# =============================================================================
print(random.randint(1, 6))  # целое от 1 до 6 ВКЛЮЧИТЕЛЬНО (кубик)
print(random.random())  # дробное от 0 до 1
print(random.uniform(1.5, 2.5))  # дробное в заданном диапазоне
print(random.choice(["камень", "ножницы", "бумага"]))  # случайный элемент

students = ["Аня", "Боря", "Вика", "Гриша"]
random.shuffle(students)  # перемешивает список НА МЕСТЕ, ничего не возвращает
print(students)

print(random.sample(range(1, 50), 6))  # 6 разных чисел — как в лотерее

# Числа random не по-настоящему случайные: их вычисляет формула из начального
# значения (seed). Одинаковый seed даёт одинаковую последовательность —
# это удобно для проверки программ:
random.seed(42)
first = [random.randint(1, 100) for _ in range(3)]
random.seed(42)
second = [random.randint(1, 100) for _ in range(3)]
print(first == second)  # True

# Раз числа предсказуемы, для паролей и токенов random не используют.
# Для секретов есть модуль secrets:
print(secrets.token_hex(8))  # например, '3f9a1c0be27d4e65'


# =============================================================================
# datetime — даты и время
# =============================================================================
today = date.today()  # сегодняшняя дата
now = datetime.now()  # дата и время сейчас
print(today, now)

birthday = date(2008, 3, 15)  # дата из года, месяца и дня
print(birthday.year, birthday.month, birthday.day)

# timedelta — промежуток времени. Даты можно складывать с ним и вычитать:
deadline = today + timedelta(days=7)
print("Срок сдачи:", deadline)
print("Дней до срока:", (deadline - today).days)  # 7

# Дни недели: weekday() даёт 0 для понедельника ... 6 для воскресенья
weekdays = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]
print("Сегодня", weekdays[today.weekday()])

# strftime — дата в строку по шаблону; strptime — строка в дату
print(today.strftime("%d.%m.%Y"))  # например, 23.11.2026
parsed = datetime.strptime("01.09.2026", "%d.%m.%Y").date()
print(parsed, (today - parsed).days, "дней с начала учебного года")

# isoformat — стандартная запись «ГГГГ-ММ-ДД», удобна для хранения в файлах
print(today.isoformat())


# =============================================================================
# json — сохранить данные в файл и прочитать обратно
# =============================================================================
# JSON — текстовый формат, похожий на словари и списки Python. Его понимают
# почти все языки и программы, поэтому в нём удобно хранить и передавать данные.
student = {
    "name": "Аня",
    "group": "Б01-001",
    "scores": [5, 4, 5],
    "is_active": True,
}

# json.dumps / json.loads — в строку и обратно
text = json.dumps(student, ensure_ascii=False)
print(text)  # {"name": "Аня", ..., "is_active": true}
print(json.loads(text) == student)  # True

# json.dump / json.load — сразу в файл и из файла.
# ensure_ascii=False — чтобы кириллица записалась как есть, а не Аня;
# indent=2 — красивые отступы.
# (Пишем во временную папку, чтобы пример не мусорил в репозитории.)
path = Path(tempfile.gettempdir()) / "student.json"
with open(path, "w", encoding="utf-8") as file:
    json.dump(student, file, ensure_ascii=False, indent=2)

with open(path, encoding="utf-8") as file:
    loaded = json.load(file)

print(loaded["scores"])  # [5, 4, 5] — снова обычный список

# В JSON нет дат, множеств и кортежей. Дату сохраняют строкой через
# isoformat() и восстанавливают через date.fromisoformat():
record = {"created": today.isoformat()}
restored = date.fromisoformat(json.loads(json.dumps(record))["created"])
print(restored == today)  # True
