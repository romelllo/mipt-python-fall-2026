# Семинар 9: Установка внешних библиотек. Виртуальные окружения. Работа с Git

**Модуль:** 1 — Основы программирования на Python  
**Дата:** 23.11.2026, 18:40–20:10  
**Презентация:** [ссылка](https://docs.google.com/presentation/d/1Yn423CrL75gX4T9iY-EBMz1NquHITeGqNCCvBiqJyhg/edit?usp=sharing)

---

## Цели семинара

После этого семинара вы сможете:

- Подключать модули разными формами `import` и объяснить, чем опасен `import *`
- Разбить программу на несколько файлов: свой модуль и свой пакет
- Объяснить, зачем нужна проверка `if __name__ == "__main__"`
- Пользоваться модулями стандартной библиотеки `random`, `datetime` и `json`
- Создать проект с виртуальным окружением через `uv` и установить в него внешнюю
  библиотеку
- Объяснить, что хранится в `pyproject.toml`, `uv.lock` и `.venv` и что из этого
  передаётся другим людям
- Вести историю проекта в Git: `status`, `add`, `commit`, `log`, `diff`, `restore`
- Исключать лишние файлы из репозитория через `.gitignore`

---

## Подготовка

На этом семинаре понадобятся две программы, которые ставятся **до занятия**.

**1. uv** — менеджер проектов и пакетов Python
(подробнее — в [`docs/installation.md`](../../docs/installation.md#5-установка-окружения-для-репозитория-курса-по-желанию)):

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**2. Git** — система контроля версий. На macOS и Linux обычно уже есть; на Windows
установите [Git for Windows](https://git-scm.com/download/win) (вместе с ним
поставится терминал Git Bash).

Проверьте, что всё работает, и представьтесь Git один раз — имя и почта попадут
в каждый ваш коммит:

```bash
uv --version
git --version

git config --global user.name "Иван Иванов"
git config --global user.email "ivan@example.com"
```

> **Где выполнять упражнения.** Примеры Блока 1 запускаются из репозитория курса:
>
> ```bash
> python seminars/seminar_09_packages_venv_git/examples/01_imports.py
> python seminars/seminar_09_packages_venv_git/examples/02_stdlib.py
> python seminars/seminar_09_packages_venv_git/examples/03_my_modules/main.py
> ```
>
> А проекты для Блоков 2 и 3 создавайте в **отдельной папке вне репозитория курса**,
> например `python-practice` в домашней папке. Репозиторий курса сам является
> uv-проектом и Git-репозиторием, и проект внутри проекта только запутает.
>
> Для `uv add` нужен интернет.

---

## План семинара

После каждого блока теории — 15 минут на упражнения из файла
[`exercises/packages_venv_git_practice.md`](exercises/packages_venv_git_practice.md).

| Время | Тема | Практика |
|-------|------|----------|
| 5 мин | Организационное: повторение семинара 8, проверка, что uv и Git установлены | — |
| 10 мин | Блок 1: Модули и пакеты | — |
| 15 мин | Практика | → Упражнения: Часть 1 |
| 10 мин | Блок 2: Проект и зависимости с uv | — |
| 15 мин | Практика | → Упражнения: Часть 2 |
| 10 мин | Блок 3: Основы Git | — |
| 15 мин | Практика | → Упражнения: Часть 3 |

> **Примечание:** в таблице 80 минут, оставшиеся ~10 минут — на вопросы и разбор задач.
> Обзор остальной стандартной библиотеки, ручная работа с `venv` и `pip`, несколько
> версий Python, ветки Git и GitHub вынесены в раздел
> [«Темы лекции, которые мы не разбираем на занятии»](#темы-лекции-которые-мы-не-разбираем-на-занятии).

---

## Блок 1: Модули и пакеты (10 мин)

### Формы import

**Модуль** — это файл с кодом на Python. Мы уже подключали модули на
[семинаре 7](../seminar_07_special_methods/README.md#блок-3-декоратор-dataclass-10-мин)
(`from dataclasses import dataclass`), теперь разберёмся, как это устроено.

```python
import math  # подключить модуль целиком

print(math.sqrt(16))  # обращаемся через имя модуля

from math import sqrt, pi  # взять из модуля отдельные имена

print(sqrt(16), pi)

import datetime as dt  # подключить под другим именем

print(dt.date.today())
```

Псевдоним `as` используют для длинных имён и общепринятых сокращений вроде
`import numpy as np`. Злоупотреблять им не стоит: читателю придётся запоминать,
что скрывается за каждым коротким именем.

### Почему не import *

`from модуль import *` вываливает в программу **все** имена модуля. Они могут молча
заменить ваши или встроенные:

```python
from gzip import *

file = open("notes.txt", "w")  # это уже не встроенный open, а gzip.open!
file.write("Привет")  # TypeError: a bytes-like object is required, not 'str'
```

В программах `import *` не используют — разве что чтобы быстро попробовать модуль
в интерактивной консоли.

### Свой модуль

Любой файл `.py` можно импортировать по имени без расширения. Пусть рядом лежат
два файла:

```python
# greetings.py
def greet(name):
    return f"Привет, {name}!"


if __name__ == "__main__":
    print(greet("тест"))  # выполнится, только если запустить сам greetings.py
```

```python
# main.py
import greetings

print(greetings.greet("Аня"))
```

При импорте Python **выполняет весь файл модуля**. Чтобы код проверки не срабатывал
при каждом импорте, его прячут под `if __name__ == "__main__":`. Переменная
`__name__` равна `"__main__"`, только когда файл запущен напрямую; при импорте в ней
имя модуля (`"greetings"`).

> **Не называйте свои файлы как модули стандартной библиотеки** (`random.py`,
> `json.py`): Python сначала ищет модуль в папке программы, и ваш файл «заслонит»
> настоящий.

### Пакет

Когда модулей становится много, их складывают в **пакет** — папку с файлом
`__init__.py` (он может быть пустым):

```
03_my_modules/
├── main.py
├── greetings.py
└── geometry/            ← пакет
    ├── __init__.py
    ├── circle.py
    └── rectangle.py
```

```python
from geometry import circle  # модуль из пакета
from geometry.rectangle import area  # функция из модуля пакета

print(circle.area(2))
print(area(3, 4))
```

### Три модуля стандартной библиотеки

Стандартная библиотека устанавливается вместе с Python — ничего ставить не нужно.

```python
import json
import random
from datetime import date, timedelta

random.randint(1, 6)  # случайное целое от 1 до 6 включительно
random.choice(["камень", "ножницы", "бумага"])  # случайный элемент
random.shuffle(students)  # перемешать список на месте

today = date.today()  # сегодняшняя дата
deadline = today + timedelta(days=7)  # через неделю
print(deadline.strftime("%d.%m.%Y"))  # например, 30.11.2026
print((deadline - today).days)  # 7

data = {"name": "Аня", "scores": [5, 4, 5]}
with open("data.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=2)  # сохранить в файл
with open("data.json", encoding="utf-8") as file:
    loaded = json.load(file)  # прочитать обратно: снова словарь
```

> `random` годится для игр и моделирования, но **не для паролей**: его числа
> предсказуемы. Для секретов есть модуль `secrets`.

> **Подробнее:** см. файлы [`examples/01_imports.py`](examples/01_imports.py),
> [`examples/02_stdlib.py`](examples/02_stdlib.py) и папку
> [`examples/03_my_modules/`](examples/03_my_modules/)

### Практика

Перейдите к разделу **Часть 1: Модули и пакеты** в файле
[`exercises/packages_venv_git_practice.md`](exercises/packages_venv_git_practice.md#часть-1-модули-и-пакеты).

---

## Блок 2: Проект и зависимости с uv (10 мин)

### Зачем виртуальное окружение

Внешние библиотеки (их миллионы на [PyPI](https://pypi.org)) не входят в Python —
их нужно устанавливать. Если ставить всё в один системный Python:

- двум проектам нужны **разные версии** одной библиотеки — а установить можно одну;
- на Linux и macOS системный Python нужен самой операционной системе, и лишние
  пакеты могут её сломать;
- непонятно, какие библиотеки нужны именно этому проекту, чтобы запустить его
  на другом компьютере.

**Виртуальное окружение** — отдельная папка (обычно `.venv`) со своим
интерпретатором и своими библиотеками. У каждого проекта — своё окружение.

### uv: один инструмент вместо нескольких

Классически окружение создают командой `python -m venv`, библиотеки ставят через
`pip`, а версии Python — через `pyenv`. **uv** делает всё это сам (и намного
быстрее). Этот репозиторий курса тоже управляется через uv.

```bash
uv init --python 3.12 habit-tracker   # создать проект с Python 3.12
cd habit-tracker
uv run main.py                         # запустить; .venv создастся сам
```

`uv init` создаёт файлы проекта:

| Файл | Что в нём |
|------|-----------|
| `pyproject.toml` | описание проекта: имя, версия Python, **список зависимостей** |
| `.python-version` | какую версию Python использовать |
| `main.py` | заготовка программы |
| `README.md` | описание проекта |
| `.gitignore` | что не нужно хранить в Git (мы вернёмся к нему в Блоке 3) |

### Установка библиотеки

```bash
uv add tqdm          # установить библиотеку в окружение проекта
uv run progress.py   # запустить программу в этом окружении
uv remove tqdm       # удалить библиотеку
```

```python
# progress.py
import time

from tqdm import tqdm

for day in tqdm(range(30)):  # цикл, обёрнутый в tqdm, рисует полосу прогресса
    time.sleep(0.1)
```

`uv add` делает три вещи: ставит библиотеку в `.venv`, записывает её
в `pyproject.toml` и фиксирует **точные** версии всех пакетов в `uv.lock`:

```toml
# pyproject.toml
dependencies = [
    "tqdm>=4.70.1",
]
```

### Что передавать другим

| Передаём (и храним в Git) | Не передаём |
|---------------------------|-------------|
| `pyproject.toml`, `uv.lock`, `.python-version`, код | `.venv` — она большая и зависит от компьютера |

Коллега, получив проект, выполняет одну команду, и uv воссоздаёт точно такое же
окружение:

```bash
uv sync
```

Если запустить программу обычным `python progress.py`, а не через `uv run`, будет
использован системный Python — и вы увидите `ModuleNotFoundError: No module named
'tqdm'`: в системном Python этой библиотеки нет.

> **Подробнее:** см. файл [`examples/04_uv_workflow.sh`](examples/04_uv_workflow.sh)

### Практика

Перейдите к разделу **Часть 2: Проект и зависимости с uv** в файле
[`exercises/packages_venv_git_practice.md`](exercises/packages_venv_git_practice.md#часть-2-проект-и-зависимости-с-uv).

---

## Блок 3: Основы Git (10 мин)

### Зачем контроль версий

Копии папок `project_v2_final_точно_последний` занимают место, их легко забыть
сделать, и по ним не видно, **что и зачем** поменялось. **Git** хранит историю
проекта: каждое сохранённое состояние, его автора, время и описание.

### Основные понятия

- **Репозиторий** — папка проекта, историю которой ведёт Git (сама история лежит
  в скрытой папке `.git`, руками её не трогаем).
- **Коммит** — сохранённый снимок файлов с сообщением «что сделано». У каждого
  коммита есть идентификатор (хеш), например `a1b2c3d`.
- Git **не сохраняет изменения сам**: вы решаете, какие изменения войдут
  в следующий коммит.

### Жизненный цикл изменения

```
 изменили файл ──git add──▶ подготовлен ──git commit──▶ в истории
   (working dir)              (staging)                  (commit)
```

```bash
git init                       # сделать папку репозиторием (uv init уже сделал это)
git status                     # что изменилось, что подготовлено — главная команда
git add main.py                # подготовить файл к коммиту (git add . — все файлы)
git commit -m "Add main menu"  # сохранить снимок с сообщением
git log --oneline              # история коммитов
```

Сообщение коммита пишут коротко и по делу: **что** сделано — «Add habit list»,
а не «fix» или «asdf».

### Посмотреть и отменить изменения

```bash
git diff               # что поменялось в файлах с последнего коммита
git restore main.py    # вернуть файл к состоянию последнего коммита
```

> `git restore` **безвозвратно** выбрасывает несохранённые изменения файла.

### .gitignore

Не всё стоит хранить в репозитории: окружение `.venv`, кеш `__pycache__`, временные
файлы, пароли. Шаблоны таких файлов перечисляют в `.gitignore`, и Git перестаёт их
замечать:

```gitignore
.venv
__pycache__/
*.log
secrets.txt
```

`uv init` уже создал `.gitignore`, в котором есть `.venv`. Сам `.gitignore`
коммитят — это общее правило для всех, кто работает с проектом.

> **Подробнее:** см. файл [`examples/05_git_workflow.sh`](examples/05_git_workflow.sh)

### Практика

Перейдите к разделу **Часть 3: Основы Git** в файле
[`exercises/packages_venv_git_practice.md`](exercises/packages_venv_git_practice.md#часть-3-основы-git).

---

## Темы лекции, которые мы не разбираем на занятии

Короткая теория для самостоятельного чтения. Примеры — в файлах
[`examples/02_stdlib.py`](examples/02_stdlib.py) (в конце) и
[`examples/06_more_stdlib.py`](examples/06_more_stdlib.py), задачи — в разделе
[«Для самостоятельной работы»](exercises/packages_venv_git_practice.md#для-самостоятельной-работы).

### Обзор стандартной библиотеки

Полный список — в [документации](https://docs.python.org/3/library/index.html).
Модули, которые стоит знать:

| Задача | Модули |
|--------|--------|
| Математика | `math`, `decimal` (точные десятичные дроби: `0.1 * 3` без `0.30000000000000004`), `fractions` (обыкновенные дроби), `statistics` (среднее, медиана) |
| Текст и вывод | `textwrap` (перенос строк по ширине), `pprint` (красивая печать вложенных структур), `reprlib` (сокращённый вывод огромных списков) |
| Контейнеры и перебор | `collections.Counter` (подсчёт элементов), `itertools` (сочетания, перестановки), `enum` (набор именованных вариантов) |
| Система | `os` (файлы и папки, переменные окружения), `sys` (версия и путь интерпретатора), `time` |
| Форматы файлов | `json`, `csv`, `tomllib`, `zipfile` и другие |
| Прочее | `contextlib.suppress` (подавить исключение — см. [семинар 8](../seminar_08_error_handling/README.md)) |

Попробуйте в консоли `import this` — это «Дзен Python».

### venv и pip без uv

uv — относительно новый инструмент, и в чужих проектах и инструкциях вы часто
встретите классический способ. Он делает то же самое, но вручную:

```bash
python -m venv .venv                  # создать окружение
source .venv/bin/activate             # активировать (macOS / Linux)
.venv\Scripts\activate                # активировать (Windows)
pip install tqdm                      # установить библиотеку
pip freeze > requirements.txt         # записать список установленных пакетов
pip install -r requirements.txt       # установить всё по списку на другом компьютере
deactivate                            # выйти из окружения
```

| Классический способ | uv |
|---------------------|----|
| `python -m venv .venv` + `activate` | создаётся сам при `uv run` / `uv sync` |
| `pip install tqdm` | `uv add tqdm` |
| `requirements.txt` | `pyproject.toml` + `uv.lock` |
| `pip install -r requirements.txt` | `uv sync` |
| `pyenv install 3.12` | `uv python install 3.12` |
| `pyenv local 3.12` | `uv python pin 3.12` |

Существуют и другие обёртки над `venv` и `pip` — `pipenv` и `poetry` (ссылки —
в дополнительных материалах). Принцип у всех одинаковый: отдельное окружение
на проект и файл со списком зависимостей.

### Несколько версий Python

Разным проектам бывают нужны разные версии Python: новые версии не всегда полностью
совместимы со старыми. Классические инструменты — `pyenv`, `conda`, Docker. В uv это
встроено:

```bash
uv python list           # какие версии есть и какие можно скачать
uv python install 3.13   # скачать версию
uv python pin 3.13       # использовать её в этом проекте (запишется в .python-version)
```

### Git: путешествие по истории

```bash
git checkout a1b2c3d     # посмотреть, как проект выглядел в старом коммите
git switch main          # вернуться к актуальному состоянию
git tag v1.0             # дать коммиту понятное имя
git commit --amend       # исправить сообщение последнего коммита
git reset --soft HEAD~1  # отменить последний коммит, сохранив изменения в файлах
git reset --hard HEAD~1  # отменить последний коммит вместе с изменениями (опасно!)
```

После `git checkout <хеш>` Git сообщает о состоянии **detached HEAD**: смотреть
можно, а коммитить не стоит — такие коммиты легко потерять. `HEAD~1` означает «на
один коммит назад от текущего».

### Git: ветки

Ветка — независимая линия истории. В ней можно спокойно пробовать новую идею,
не ломая рабочую версию:

```bash
git switch -c new-feature   # создать ветку и перейти в неё
# ...изменения и коммиты...
git switch main             # вернуться в основную ветку
git merge new-feature       # влить изменения из ветки
```

### Git: GitHub и работа в команде

[GitHub](https://github.com) хранит копию репозитория на сервере — это и резервная
копия, и способ работать вместе.

```bash
git remote add origin https://github.com/имя/проект.git  # связать с репозиторием на GitHub
git push -u origin main    # отправить коммиты на сервер
git pull                   # забрать чужие изменения
git clone <адрес>          # скачать репозиторий целиком
```

Если двое изменили одни и те же строки, при `git pull` возникнет **конфликт**: Git
покажет оба варианта прямо в файле, и нужно вручную оставить правильный, а затем
закоммитить результат. Отправленную на сервер историю переписывать (`reset`,
`--amend`) нельзя — у коллег она уже скачана.

Работать с Git можно и без терминала: в VS Code и PyCharm есть панель Source Control /
Commit с теми же действиями.

---

## Итоги семинара

- Разобрали формы `import` и поняли, почему не стоит писать `import *`
- Научились разбивать программу на модули и пакеты и прятать проверочный код
  под `if __name__ == "__main__"`
- Попробовали модули стандартной библиотеки `random`, `datetime` и `json`
- Создали проект с виртуальным окружением через `uv` и установили внешнюю библиотеку
- Разобрались, зачем нужны `pyproject.toml` и `uv.lock` и почему `.venv` не передают
  другим
- Начали вести историю проекта в Git и настроили `.gitignore`

**Дальше:** на семинаре 10 программы начнут общаться по сети — сокеты и протоколы
TCP/IP.

---

## Файлы семинара

| Файл | Описание |
|------|----------|
| [`README.md`](README.md) | Этот файл — основной материал семинара |
| [`examples/01_imports.py`](examples/01_imports.py) | Формы `import`, `dir()`, почему не `import *` |
| [`examples/02_stdlib.py`](examples/02_stdlib.py) | `random`, `datetime`, `json` |
| [`examples/03_my_modules/`](examples/03_my_modules/) | Свой модуль, `__name__`, свой пакет |
| [`examples/04_uv_workflow.sh`](examples/04_uv_workflow.sh) | Команды uv с пояснениями |
| [`examples/05_git_workflow.sh`](examples/05_git_workflow.sh) | Команды Git с пояснениями |
| [`examples/06_more_stdlib.py`](examples/06_more_stdlib.py) | Обзор других модулей стандартной библиотеки |
| [`exercises/packages_venv_git_practice.md`](exercises/packages_venv_git_practice.md) | Задания с подсказками и решениями |
| [`exercises/starter/`](exercises/starter/) | Заготовки файлов для задач |

---

## Дополнительные материалы

- [Документация: стандартная библиотека Python](https://docs.python.org/3/library/index.html)
- [Документация: модули и пакеты (учебник)](https://docs.python.org/3/tutorial/modules.html)
- [Документация uv](https://docs.astral.sh/uv/)
- [Документация: установка модулей Python (pip)](https://docs.python.org/3/installing/index.html)
- [Документация: модуль `venv`](https://docs.python.org/3/library/venv.html)
- [Pipenv](https://pipenv.pypa.io/) и [Poetry](https://python-poetry.org/docs/) — другие менеджеры зависимостей
- [pyenv](https://github.com/pyenv/pyenv) — классический менеджер версий Python
- [Книга Pro Git на русском](https://git-scm.com/book/ru/v2)
- [Learn Git Branching](https://learngitbranching.js.org/?locale=ru_RU) — интерактивный тренажёр по Git
- [GitHub Docs: Hello World](https://docs.github.com/ru/get-started/start-your-journey/hello-world)
