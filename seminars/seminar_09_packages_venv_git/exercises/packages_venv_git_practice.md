# Практические задания: Модули, uv и Git

## Подготовка

Перед началом проверьте, что установлены uv и Git, и что Git знает ваше имя
(см. [README — Подготовка](../README.md#подготовка)):

```bash
uv --version
git --version
git config user.name
```

Задания выполняются в двух местах:

| Часть | Где работаем |
|-------|--------------|
| Часть 1 | в репозитории курса, заготовки — в папке [`starter/`](starter/) |
| Части 2 и 3 | в **своей папке вне репозитория курса**, например `python-practice` в домашней папке |

```bash
# Часть 1 — из корня репозитория курса
python seminars/seminar_09_packages_venv_git/exercises/starter/task_1_2.py

# Части 2 и 3 — в отдельной папке
mkdir python-practice
cd python-practice
```

> На macOS и Linux вместо `python` может понадобиться `python3`.

Примеры кода к каждой части — в папке [`../examples/`](../examples/).

> **Как работать с заданиями:** прочитайте условие, выполните его сами и только потом
> раскройте решение для сверки. В Частях 2 и 3 вы пишете не столько код, сколько
> команды в терминале: после каждой команды читайте, что она вывела, — в этом
> половина пользы.

---

## Часть 1: Модули и пакеты

> **Теория:** [README.md — Блок 1](../README.md#блок-1-модули-и-пакеты-10-мин) | **Примеры:** [`examples/01_imports.py`](../examples/01_imports.py), [`examples/02_stdlib.py`](../examples/02_stdlib.py), [`examples/03_my_modules/`](../examples/03_my_modules/)

### Задание 1.1

Заготовка: папка [`starter/task_1_1/`](starter/task_1_1/)

В заготовке — программа `main.py` и пакет `units` с двумя модулями. Модуль
`temperature.py` готов, его можно взять за образец.

1. Допишите в `units/length.py` функции `km_to_miles(km)` и `miles_to_km(miles)`
   и проверки, которые выполняются **только при запуске самого файла**. Запустите
   его напрямую — должно появиться «Проверки модуля length пройдены».
2. В `main.py` подключите модуль `length` целиком, а из `temperature` — только
   функцию `celsius_to_fahrenheit`. Получите вывод:

```
42.195 км = 26.22 миль
10 миль = 16.09 км
36.6 °C = 97.9 °F
```

При запуске `main.py` строки о проверках появляться не должны.

<details>
<summary>Подсказка</summary>

Проверки положите под `if __name__ == "__main__":`. Модуль из пакета подключается
так: `from units import length`, а отдельная функция — через точку в пути:
`from units.temperature import ...`. Для двух знаков после точки используйте
`:.2f` в f-строке.

</details>

<details>
<summary>Решение</summary>

`units/length.py`:

```python
"""Модуль length: перевод расстояний."""

KM_IN_MILE = 1.609344


def km_to_miles(km):
    """Перевести километры в мили."""
    return km / KM_IN_MILE


def miles_to_km(miles):
    """Перевести мили в километры."""
    return miles * KM_IN_MILE


if __name__ == "__main__":
    assert miles_to_km(1) == KM_IN_MILE
    assert round(km_to_miles(KM_IN_MILE), 6) == 1
    print("Проверки модуля length пройдены")
```

`main.py`:

```python
from units import length
from units.temperature import celsius_to_fahrenheit

marathon_km = 42.195
distance_miles = 10
body_celsius = 36.6

print(f"{marathon_km} км = {length.km_to_miles(marathon_km):.2f} миль")
print(f"{distance_miles} миль = {length.miles_to_km(distance_miles):.2f} км")
print(f"{body_celsius} °C = {celsius_to_fahrenheit(body_celsius):.1f} °F")
```

Почему `round(..., 6)` во второй проверке? Деление и умножение `float` могут дать
`0.9999999999999999` вместо `1` — это та же особенность дробных чисел, что и
`0.1 * 3`.

</details>

### Задание 1.2

Заготовка: [`starter/task_1_2.py`](starter/task_1_2.py)

Составьте график дежурств: студенты дежурят по одному в день, начиная с завтра,
порядок при каждом запуске случайный.

```
вт 24.11 — Вика
ср 25.11 — Аня
чт 26.11 — Гриша
пт 27.11 — Боря
```

<details>
<summary>Подсказка</summary>

Перемешать список — `random.shuffle()`. Сегодняшняя дата — `date.today()`, дата
через `n` дней — `today + timedelta(days=n)`. Номер дня недели (0 — понедельник)
даёт метод `weekday()`, дату в виде `ДД.ММ` — `strftime("%d.%m")`.

</details>

<details>
<summary>Решение</summary>

```python
import random
from datetime import date, timedelta

students = ["Аня", "Боря", "Вика", "Гриша"]
weekdays = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]

random.shuffle(students)
today = date.today()

for number, name in enumerate(students, start=1):
    duty_day = today + timedelta(days=number)
    weekday = weekdays[duty_day.weekday()]
    print(f"{weekday} {duty_day.strftime('%d.%m')} — {name}")
```

`timedelta` сам учитывает конец месяца и года: 30.11 + 1 день = 01.12.

</details>

### Задание 1.3

Заготовка: [`starter/task_1_3.py`](starter/task_1_3.py)

Напишите список дел, который хранится в файле `todo.json` и не теряется между
запусками программы:

```
Новое дело (Enter — пропустить): сдать лабу
1. [2026-11-23] сдать лабу
```

```
Новое дело (Enter — пропустить): купить молоко
1. [2026-11-23] сдать лабу
2. [2026-11-23] купить молоко
```

При самом первом запуске файла ещё нет — программа не должна падать. Откройте
`todo.json` в редакторе и посмотрите, как выглядят данные.

<details>
<summary>Подсказка</summary>

Каждое дело — словарь `{"text": ..., "created": ...}`, а весь список дел — список
таких словарей. Отсутствие файла обработайте через `try`/`except FileNotFoundError`,
как на [семинаре 8](../../seminar_08_error_handling/README.md#else-и-finally).
Сохраняйте с `ensure_ascii=False` и `indent=2`, а дату — строкой через
`isoformat()`.

</details>

<details>
<summary>Решение</summary>

```python
import json
from datetime import date

path = "todo.json"

try:
    with open(path, encoding="utf-8") as file:
        tasks = json.load(file)
except FileNotFoundError:
    tasks = []

text = input("Новое дело (Enter — пропустить): ").strip()
if text:
    tasks.append({"text": text, "created": date.today().isoformat()})

with open(path, "w", encoding="utf-8") as file:
    json.dump(tasks, file, ensure_ascii=False, indent=2)

for number, task in enumerate(tasks, start=1):
    print(f"{number}. [{task['created']}] {task['text']}")
```

Содержимое `todo.json`:

```json
[
  {
    "text": "сдать лабу",
    "created": "2026-11-23"
  }
]
```

Дату храним строкой: в JSON нет отдельного типа для дат. Обратно в объект `date`
её превращает `date.fromisoformat(task["created"])`.

</details>

---

## Часть 2: Проект и зависимости с uv

> **Теория:** [README.md — Блок 2](../README.md#блок-2-проект-и-зависимости-с-uv-10-мин) | **Примеры:** [`examples/04_uv_workflow.sh`](../examples/04_uv_workflow.sh)

Все задания этой и следующей части выполняются в папке `python-practice` вне
репозитория курса. В Части 3 мы продолжим работать с тем же проектом.

### Задание 2.1

Заготовка: [`starter/task_2_1.py`](starter/task_2_1.py)

1. Создайте проект `habit-tracker` на Python 3.12 и перейдите в его папку.
2. Посмотрите, какие файлы создал uv (включая скрытые) и что написано
   в `pyproject.toml`.
3. Запустите `main.py` через uv. Какая папка появилась после запуска?
4. Скопируйте заготовку в проект под именем `where_am_i.py`, допишите её и запустите
   двумя способами: обычным `python` и через `uv run`. Сравните пути
   к интерпретатору и версии.

<details>
<summary>Подсказка</summary>

Нужные команды: `uv init --python 3.12 habit-tracker`, `uv run main.py`. Скрытые
файлы показывает `ls -a` (на Windows — `dir /a`). Путь к интерпретатору хранится
в `sys.executable`, версия — в `sys.version`.

</details>

<details>
<summary>Решение</summary>

```bash
uv init --python 3.12 habit-tracker
cd habit-tracker
ls -a          # Windows: dir /a
cat pyproject.toml
uv run main.py
```

uv создал `pyproject.toml`, `.python-version`, `main.py`, `README.md`,
`.gitignore` и скрытую папку `.git` — проект сразу стал Git-репозиторием.
После `uv run` появилась папка `.venv` — виртуальное окружение.

`where_am_i.py`:

```python
import sys

print("Интерпретатор:", sys.executable)
print("Версия:", sys.version.split()[0])
```

```
$ python3 where_am_i.py
Интерпретатор: /opt/homebrew/bin/python3.14
Версия: 3.14.6

$ uv run where_am_i.py
Интерпретатор: /Users/anya/python-practice/habit-tracker/.venv/bin/python3
Версия: 3.12.13
```

Пути у вас будут свои. Главное — `uv run` запускает Python **из папки `.venv`
внутри проекта** (на Windows — `.venv\Scripts\python.exe`), причём той версии,
что записана в `.python-version`. Обычный `python` — это системный интерпретатор,
общий для всех программ на компьютере.

</details>

### Задание 2.2

Заготовка: [`starter/task_2_2.py`](starter/task_2_2.py)

1. Установите в проект библиотеку `tqdm`. Посмотрите, что изменилось
   в `pyproject.toml` и какой новый файл появился.
2. Скопируйте заготовку в проект под именем `progress.py`, допишите её и запустите
   через uv — должна нарисоваться полоса прогресса.
3. Запустите ту же программу обычным `python progress.py`. Объясните ошибку.

<details>
<summary>Подсказка</summary>

Библиотека ставится командой `uv add`. Чтобы появилась полоса прогресса, перебирайте
не `range(days)`, а `tqdm(range(days))`; подпись задаётся параметром `desc`.

</details>

<details>
<summary>Решение</summary>

```bash
uv add tqdm
cat pyproject.toml   # в dependencies появилось "tqdm>=..."
uv tree              # дерево зависимостей проекта
```

Появился файл `uv.lock` с точными версиями всех пакетов.

`progress.py`:

```python
import random
import time

from tqdm import tqdm

days = 30
done_days = 0

for _ in tqdm(range(days), desc="Обработка дней"):
    time.sleep(0.05)
    if random.random() < 0.7:
        done_days += 1

print(f"Привычка выполнена в {done_days} из {days} дней")
```

```bash
uv run progress.py      # работает: полоса прогресса и итог
python progress.py      # ModuleNotFoundError: No module named 'tqdm'
```

`tqdm` установлена в окружение `.venv` проекта, а обычный `python` — системный
интерпретатор, в котором этой библиотеки нет. Это и есть изоляция: проект
не засоряет систему, а система не влияет на проект.

Обратите внимание на порядок импортов: сначала стандартная библиотека (`random`,
`time`), пустая строка, затем внешние библиотеки (`tqdm`). Так принято в PEP 8.

</details>

### Задание 2.3

Заготовка не нужна — используйте файлы из заданий 2.1 и 2.2.

Представьте, что вы отправили проект другу.

1. Удалите папку `.venv` — у друга её не будет. Восстановите окружение одной
   командой и убедитесь, что `progress.py` снова работает.
2. Переключите проект на Python 3.13 и запустите `where_am_i.py` через uv: версия
   должна поменяться.
3. Ответьте: какие файлы проекта нужно передать другу, а какие — нет?

<details>
<summary>Подсказка</summary>

Окружение по `uv.lock` воссоздаёт `uv sync`. Версия Python для проекта задаётся
командой `uv python pin`; если нужной версии нет на компьютере, uv скачает её сам.

</details>

<details>
<summary>Решение</summary>

```bash
rm -rf .venv            # Windows PowerShell: Remove-Item -Recurse -Force .venv
uv sync                 # создаёт .venv и ставит tqdm той же версии из uv.lock
uv run progress.py

uv python pin 3.13      # .python-version: 3.12 -> 3.13
uv run where_am_i.py    # Версия: 3.13.x — uv пересоздал окружение сам
cat .python-version
```

Передавать нужно `pyproject.toml`, `uv.lock`, `.python-version` и код. Папку `.venv`
не передают: она большая, внутри — пути, привязанные к вашему компьютеру,
а `uv sync` за секунды соберёт её заново.

> Python 3.11 «прикрепить» не получится: в `pyproject.toml` написано
> `requires-python = ">=3.12"`, и uv откажется — версия не подходит проекту.

</details>

---

## Часть 3: Основы Git

> **Теория:** [README.md — Блок 3](../README.md#блок-3-основы-git-10-мин) | **Примеры:** [`examples/05_git_workflow.sh`](../examples/05_git_workflow.sh)

Работаем в том же проекте `habit-tracker`. Заготовки не нужны: задания выполняются
командами в терминале.

### Задание 3.1

1. Выполните `git status`. Почему Git уже работает в этой папке, хотя вы не писали
   `git init`? Почему среди новых файлов нет папки `.venv`?
2. Сохраните текущее состояние проекта первым коммитом.
3. Посмотрите историю коммитов в коротком виде.

<details>
<summary>Подсказка</summary>

Команды: `git status`, `git add .`, `git commit -m "сообщение"`,
`git log --oneline`. Если Git отвечает *Please tell me who you are* — вы не
выполнили `git config` из подготовки.

</details>

<details>
<summary>Решение</summary>

```bash
git status
git add .
git status          # все файлы теперь в разделе «Changes to be committed»
git commit -m "Create habit-tracker project"
git log --oneline
```

```
a1b2c3d (HEAD -> main) Create habit-tracker project
```

`uv init` сам выполнил `git init` и создал `.gitignore`. В нём есть строка `.venv`,
поэтому Git не показывает окружение среди новых файлов, и оно не попадёт
в репозиторий.

</details>

### Задание 3.2

1. Измените `progress.py`: пусть программа считает 60 дней вместо 30. Посмотрите
   изменения через `git diff` и сохраните их коммитом.
2. «Случайно» сотрите всё содержимое `main.py` и сохраните файл. Что показывает
   `git status`? Верните файл без ручного набора.
3. Убедитесь, что в истории два коммита, а `git status` сообщает, что изменений нет.

<details>
<summary>Подсказка</summary>

В выводе `git diff` строки с `-` удалены, с `+` — добавлены. Вернуть файл
к состоянию последнего коммита помогает `git restore`.

</details>

<details>
<summary>Решение</summary>

```bash
git diff
```

```diff
-days = 30
+days = 60
```

```bash
git add progress.py
git commit -m "Count habits over 60 days"

git status              # modified: main.py
git restore main.py     # файл вернулся к версии из последнего коммита
git status              # nothing to commit, working tree clean
git log --oneline
```

```
d4e5f6a (HEAD -> main) Count habits over 60 days
a1b2c3d Create habit-tracker project
```

`git restore` не спрашивает подтверждения и не кладёт изменения в корзину: если бы
в `main.py` были ценные несохранённые правки, они пропали бы вместе с ошибкой.

</details>

### Задание 3.3

1. Создайте в проекте файлы `debug.log` и `secrets.txt` с любым текстом
   (например, `password=123`). Что показывает `git status`?
2. Сделайте так, чтобы Git перестал замечать **все** файлы `.log` и файл
   `secrets.txt`.
3. Сохраните это правило коммитом. Убедитесь, что сами `debug.log` и `secrets.txt`
   в коммит не попали.

<details>
<summary>Подсказка</summary>

Допишите две строки в конец файла `.gitignore`. `*` в шаблоне означает «любые
символы». Сам `.gitignore` — обычный файл проекта, его нужно добавить и закоммитить.

</details>

<details>
<summary>Решение</summary>

```bash
echo "отладка" > debug.log
echo "password=123" > secrets.txt
git status --short
```

```
?? debug.log
?? secrets.txt
```

Добавьте в конец `.gitignore`:

```gitignore
# Логи и секреты
*.log
secrets.txt
```

```bash
git status --short      # теперь виден только  M .gitignore
git add .gitignore
git commit -m "Ignore logs and secrets"
git show --stat HEAD    # в коммите только .gitignore
```

Пароли, ключи и токены **никогда** не должны попадать в репозиторий: из истории
Git их очень трудно удалить, а после публикации на GitHub их найдут боты
за минуты.

</details>

---

## Для самостоятельной работы

Задачи, которые не поместились в занятие, и темы, которые мы не разбирали на семинаре
(см. [README — Темы лекции, которые мы не разбираем на занятии](../README.md#темы-лекции-которые-мы-не-разбираем-на-занятии)).
Сдавать их не нужно, но решить очень советуем. Примеры — в файле
[`examples/06_more_stdlib.py`](../examples/06_more_stdlib.py).

### Задание 4.1

**Не запуская** код, ответьте: что произойдёт и почему? Затем проверьте и исправьте.

```python
from gzip import *

with open("notes.txt", "w") as file:
    file.write("Купить хлеб")
```

<details>
<summary>Решение</summary>

Программа упадёт:

```
TypeError: a bytes-like object is required, not 'str'
```

В модуле `gzip` есть своя функция `open`, и `import *` молча подменил ею встроенную.
`gzip.open` создаёт сжатый файл и в режиме `"w"` ждёт байты, а не строку.

Исправление — не использовать `*`. Если `gzip` действительно нужен, подключайте
модуль целиком, тогда видно, где чья функция:

```python
import gzip

with open("notes.txt", "w", encoding="utf-8") as file:  # встроенный open
    file.write("Купить хлеб")

with gzip.open("notes.txt.gz", "wt", encoding="utf-8") as file:  # сжатый файл
    file.write("Купить хлеб")
```

</details>

### Задание 4.2

С помощью `collections.Counter` найдите три самых частых слова в тексте. Регистр
не важен, знаки препинания `.,!?` не считаются частью слова.

```python
text = "Кот ловит мышь. Мышь бежит от кота. Кот снова ловит мышь, а мышь снова бежит!"
```

```
мышь — 4
кот — 2
ловит — 2
```

<details>
<summary>Подсказка</summary>

Приведите текст к нижнему регистру через `lower()`, разбейте на слова через
`split()` и у каждого слова срежьте знаки препинания по краям через `strip(".,!?")`.
`Counter` принимает список и умеет `most_common(n)`.

</details>

<details>
<summary>Решение</summary>

```python
from collections import Counter

text = "Кот ловит мышь. Мышь бежит от кота. Кот снова ловит мышь, а мышь снова бежит!"

words = [word.strip(".,!?") for word in text.lower().split()]
counter = Counter(words)

for word, count in counter.most_common(3):
    print(f"{word} — {count}")
```

«кот» и «кота» посчитались как разные слова: чтобы объединять формы слов, нужны
специальные библиотеки — например, `pymorphy3` (её можно поставить через `uv add`).

</details>

### Задание 4.3

Повторите задание 2.2 **без uv** — классическими `venv` и `pip`, которые вы встретите
во многих инструкциях:

1. В новой папке `progress-pip` создайте окружение, активируйте его и проверьте,
   какой `python` теперь запускается.
2. Установите `tqdm`, посмотрите список пакетов и сохраните его в `requirements.txt`.
3. Выйдите из окружения. Удалите `.venv` и восстановите всё по `requirements.txt`.

<details>
<summary>Решение</summary>

```bash
mkdir progress-pip
cd progress-pip

python -m venv .venv            # создать окружение в папке .venv
source .venv/bin/activate       # macOS / Linux
# .venv\Scripts\activate        # Windows

which python                    # Windows: where python — путь внутри .venv
pip install tqdm
pip list
pip freeze > requirements.txt   # tqdm==4.70.1
deactivate

rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Отличия от uv: окружение нужно создавать и активировать вручную, версию Python
выбрать нельзя (используется та, которой запустили `venv`), а `requirements.txt`
нужно не забыть обновить после каждой установки. uv делает всё это сам.

</details>

### Задание 4.4

Попутешествуйте по истории проекта `habit-tracker`:

1. Перейдите к **первому** коммиту и убедитесь, что в `progress.py` снова 30 дней.
   Что Git говорит о состоянии *detached HEAD*? Вернитесь обратно.
2. Пометьте первый коммит тегом `v0.1`.
3. Исправьте сообщение последнего коммита.
4. Отмените последний коммит, **сохранив** изменения в файлах, и закоммитьте их
   заново.

<details>
<summary>Решение</summary>

```bash
git log --oneline
git checkout a1b2c3d          # хеш первого коммита из вашего git log
cat progress.py               # days = 30
git switch main               # вернуться к актуальному состоянию

git tag v0.1 a1b2c3d
git log --oneline             # у первого коммита появилась метка tag: v0.1

git commit --amend -m "Ignore log files and secrets"

git reset --soft HEAD~1       # коммит отменён, изменения остались подготовленными
git status
git commit -m "Ignore logs and secrets"
```

*Detached HEAD* означает, что вы смотрите на старый коммит, а не на ветку. Новые
коммиты в этом состоянии легко потерять, поэтому только смотрим и возвращаемся
через `git switch main`.

`--amend` и `reset` переписывают историю. Пока коммиты есть только у вас — это
нормально; после `git push` так делать нельзя.

</details>

### Задание 4.5

Добавьте в `habit-tracker` новую возможность в отдельной ветке:

1. Создайте ветку `reminders` и перейдите в неё.
2. Создайте файл `reminders.py` с функцией, которая печатает напоминание, и сделайте
   коммит.
3. Вернитесь в `main`: куда делся файл? Влейте ветку `reminders` в `main`
   и удалите ветку.

<details>
<summary>Решение</summary>

```bash
git switch -c reminders
```

`reminders.py`:

```python
def remind(habit):
    print(f"Не забудьте: {habit}!")


if __name__ == "__main__":
    remind("зарядка")
```

```bash
git add reminders.py
git commit -m "Add reminders"

git switch main
ls                       # reminders.py нет — он существует только в ветке reminders
git merge reminders      # теперь есть и в main
git branch -d reminders  # ветка больше не нужна
git log --oneline
```

Ветки позволяют пробовать идеи, не ломая рабочую версию: если идея не удалась,
ветку просто удаляют, а `main` остаётся нетронутой.

</details>

### Задание 4.6

Опубликуйте `habit-tracker` на GitHub:

1. Зарегистрируйтесь на [github.com](https://github.com) и создайте **пустой**
   репозиторий `habit-tracker` (без README и `.gitignore`).
2. Свяжите локальный репозиторий с GitHub и отправьте коммиты.
3. Склонируйте репозиторий в другую папку, сделайте там коммит и отправьте его.
   Заберите изменение в исходную папку.

<details>
<summary>Подсказка</summary>

Команды для первой отправки GitHub покажет сам на странице пустого репозитория.
При первом `git push` понадобится войти в аккаунт: в Git for Windows откроется окно
браузера, на macOS и Linux проще всего установить
[GitHub CLI](https://cli.github.com/) и выполнить `gh auth login`.

</details>

<details>
<summary>Решение</summary>

```bash
# в папке habit-tracker
git remote add origin https://github.com/ВАШ_ЛОГИН/habit-tracker.git
git push -u origin main         # -u: запомнить, куда отправлять, дальше просто git push

# в другой папке
cd ..
git clone https://github.com/ВАШ_ЛОГИН/habit-tracker.git habit-tracker-copy
cd habit-tracker-copy
uv sync                         # окружение собирается по uv.lock — .venv в Git не было
echo "Трекер привычек" > README.md
git add README.md
git commit -m "Describe the project"
git push

# обратно в исходную папку
cd ../habit-tracker
git pull                        # README.md обновился
```

Заметьте: после `git clone` проект сразу запускается через `uv sync` и `uv run`,
хотя `.venv` в репозитории нет. Ради этого `pyproject.toml` и `uv.lock` хранят
в Git, а `.venv` — нет.

</details>
