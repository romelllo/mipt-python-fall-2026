# Установка Python и выбор редактора

Инструкция для первого семинара. Нужны две вещи: **интерпретатор Python** (он выполняет
ваши программы) и **редактор** (в нём вы пишете текст программы).

---

## 1. Проверьте, установлен ли Python

Откройте терминал:

- **Windows** — «Пуск» → наберите `PowerShell` → Enter
- **macOS** — Cmd+Space → наберите `Терминал` → Enter
- **Linux** — Ctrl+Alt+T

и выполните:

```bash
python --version
```

Если команда не найдена, попробуйте:

```bash
python3 --version
```

Если в ответ вы видите `Python 3.10.x` или новее — переходите к разделу
[«Выбор редактора»](#3-выбор-редактора). Если нет — ставим Python.

> **Важно:** Python 2 (версии `2.7.x`) не подходит — это другой, устаревший язык.

---

## 2. Установка Python

### Windows

1. Откройте [python.org/downloads](https://www.python.org/downloads/) и скачайте
   установщик последней версии 3.12 или новее
2. Запустите установщик
3. **Обязательно** отметьте галочку **«Add python.exe to PATH»** внизу первого экрана —
   без неё команда `python` не заработает в терминале
4. Нажмите «Install Now» и дождитесь конца установки
5. **Закройте и откройте терминал заново** и проверьте:

```powershell
python --version
```

<details>
<summary>Если терминал пишет «python не является внутренней или внешней командой»</summary>

Скорее всего, не была отмечена галочка «Add python.exe to PATH». Проще всего запустить
установщик ещё раз, выбрать «Modify» и добавить Python в PATH. Либо переустановить,
не забыв про галочку.

</details>

<details>
<summary>Если открывается Microsoft Store вместо запуска Python</summary>

Windows подставляет свою «заглушку». Отключите её:
«Параметры» → «Приложения» → «Дополнительные параметры приложений» →
«Псевдонимы выполнения приложения» → выключите оба переключателя для `python.exe`
и `python3.exe`.

</details>

### macOS

В системе уже есть Python, но лучше поставить свежую версию через
[Homebrew](https://brew.sh/):

```bash
# Если Homebrew ещё не установлен:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

brew install python@3.12
python3 --version
```

Альтернатива без Homebrew — установщик с [python.org/downloads](https://www.python.org/downloads/).

> На macOS команда обычно называется `python3`, а не `python`. Это нормально.

### Linux (Ubuntu / Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 --version
```

### Linux (Fedora / RHEL)

```bash
sudo dnf install python3 python3-pip
python3 --version
```

---

## 3. Выбор редактора

Программа на Python — это обычный текстовый файл с расширением `.py`. Подойдёт **любой**
редактор; на то, как работает программа, выбор не влияет.

| Вариант | Примеры | Когда подходит |
|---------|---------|----------------|
| Текстовый редактор | Блокнот, TextEdit, nano, Vim | Работает всегда, но без подсказок и подсветки |
| Редактор кода | [VS Code](https://code.visualstudio.com/), [Zed](https://zed.dev/), Sublime Text | Подсветка синтаксиса, автодополнение, встроенный терминал |
| IDE | [PyCharm](https://www.jetbrains.com/pycharm/) (есть бесплатная Community-версия) | Всё то же плюс отладчик и работа с большими проектами |

**Рекомендация для курса — VS Code:**

1. Скачайте с [code.visualstudio.com](https://code.visualstudio.com/) и установите
2. Откройте вкладку Extensions (Ctrl+Shift+X / Cmd+Shift+X)
3. Найдите расширение **Python** от Microsoft и установите его
4. Откройте папку с вашими файлами: File → Open Folder

> **Не устанавливайте всё сразу.** Достаточно одного редактора. Переключиться на другой
> можно в любой момент — код от этого не меняется.

**Если ничего не установилось**, на первом семинаре можно работать в браузере:
[Python Online](https://www.online-python.com/) или
[Programiz](https://www.programiz.com/python-programming/online-compiler/).
Это временное решение: начиная с семинара 5 понадобится локальный Python.

---

## 4. Проверка: первая программа

1. Создайте файл `hello.py` в любой папке
2. Напишите в нём одну строку:

```python
print("Hello, world!")
```

3. Откройте терминал **в той же папке** и выполните:

```bash
cd путь/к/папке     # перейти в папку с файлом
python hello.py     # или python3 hello.py
```

Если на экране появилось `Hello, world!` — всё готово к семинару.

<details>
<summary>Терминал пишет «can't open file ... No such file or directory»</summary>

Вы находитесь не в той папке, где лежит файл. Проверьте текущую папку командой
`pwd` (macOS/Linux) или `cd` без аргументов (Windows), посмотрите список файлов
командой `ls` (macOS/Linux) или `dir` (Windows) и перейдите в нужную через `cd`.

</details>

---

## 5. Установка окружения для репозитория курса (по желанию)

Чтобы запускать примеры прямо из репозитория, склонируйте его и установите
зависимости через [uv](https://docs.astral.sh/uv/):

```bash
git clone https://github.com/romelllo/mipt-python-fall-2026.git
cd mipt-python-fall-2026

# Установка uv
# macOS/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows:
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

uv sync --all-extras
```

Это не обязательно для первых семинаров: примеры — обычные `.py`-файлы, они
запускаются и просто через `python`. Git и виртуальные окружения подробно
разберём на **семинаре 9**.
