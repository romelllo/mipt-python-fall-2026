# Программирование на Python — 1 семестр (МФТИ, осень 2026)

Добро пожаловать в репозиторий курса «Программирование на Python» для студентов МФТИ!

## О курсе

Курс знакомит с языком Python с нуля: от первых программ и базовых конструкций до
объектно-ориентированного программирования, работы с сетью и инструментов контроля
качества кода. Курс состоит из 11 семинаров и полностью опирается на стандартную
библиотеку Python (внешние библиотеки появляются только в семинарах 9–10).

**Время занятий:** по понедельникам, 18:40–20:10.

## Структура курса

### Модуль 1: Основы программирования на Python

| # | Семинар | Дата | Описание |
|---|---------|------|----------|
| 1 | [Введение в программирование на Python](./seminars/seminar_01_intro_to_python/README.md) | 28.09.2026 | Установка Python, интерпретатор, первая программа |
| 2 | [Типы данных. Конструкции языка](./seminars/seminar_02_data_types_and_control_flow/) | 05.10.2026 | Числа, строки, bool, условия, циклы |
| 3 | [Коллекции](./seminars/seminar_03_collections/) | 12.10.2026 | list, tuple, dict, set, срезы, comprehensions |
| 4 | [Функции](./seminars/seminar_04_functions/) | 19.10.2026 | Аргументы, возвращаемые значения, области видимости |
| 5 | [Работа с файлами. Классы и объекты](./seminars/seminar_05_files_and_classes/) | 26.10.2026 | open, контекстные менеджеры, class, атрибуты, методы |
| 6 | [Наследование](./seminars/seminar_06_inheritance/) | 02.11.2026 | Базовые и производные классы, super(), MRO |
| 7 | [Специальные методы классов. Механизм работы классов](./seminars/seminar_07_special_methods/) | 09.11.2026 | Dunder-методы, свойства, устройство классов |
| 8 | [Работа с ошибками](./seminars/seminar_08_error_handling/) | 16.11.2026 | Исключения, try/except/finally, свои исключения |
| 9 | [Установка внешних библиотек. Виртуальные окружения. Работа с Git](./seminars/seminar_09_packages_venv_git/) | 23.11.2026 | pip, uv, venv, git, GitHub |
| 10 | [Работа с сетью. Сокеты](./seminars/seminar_10_networking_sockets/) | 30.11.2026 | TCP/IP, socket, клиент-серверное взаимодействие |
| 11 | [Контроль качества программного кода](./seminars/seminar_11_code_quality/) | 07.12.2026 | PEP 8, линтеры, форматтеры, тесты, типы |

## Требования

- Python 3.10 или выше (рекомендуется 3.12)
- Git
- [uv](https://docs.astral.sh/uv/) — современный менеджер пакетов Python

## Установка

### Установка Python

> Подробная пошаговая инструкция со скриншотами типичных проблем —
> [`docs/installation.md`](./docs/installation.md).

**macOS (через Homebrew):**
```bash
# Если Homebrew не установлен:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

brew install python@3.12
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install python3 python3-venv python3-pip
```

**Windows:**
1. Скачайте установщик с [python.org](https://www.python.org/downloads/)
2. При установке обязательно отметьте галочку **«Add python.exe to PATH»**
3. Откройте новый терминал и проверьте: `python --version`

### Установка проекта

```bash
# Клонировать репозиторий
git clone https://github.com/romelllo/mipt-python-fall-2026.git
cd mipt-python-fall-2026

# Установить uv (если ещё не установлен)
# macOS/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows:
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Создать виртуальное окружение и установить зависимости
uv sync

# Установить зависимости вместе с dev-инструментами (ruff, pytest, ty)
uv sync --all-extras

# Активировать виртуальное окружение
source .venv/bin/activate  # Linux/Mac
# или
.venv\Scripts\activate     # Windows
```

> **Примечание:** uv сам скачает нужную версию Python, если её нет в системе —
> версия зафиксирована в файле `.python-version`.

### Альтернативная установка (pip)

```bash
# Создать виртуальное окружение
python -m venv .venv
source .venv/bin/activate

# Установить зависимости
pip install -e ".[dev]"
```

## Инструменты разработки

| Инструмент | Назначение | Команда |
|------------|------------|---------|
| [uv](https://docs.astral.sh/uv/) | Менеджер пакетов | `uv sync`, `uv add <pkg>` |
| [ruff](https://docs.astral.sh/ruff/) | Линтер и форматтер | `ruff check .`, `ruff format .` |
| [pytest](https://pytest.org/) | Тестирование | `pytest` |
| [ty](https://docs.astral.sh/ty/) | Проверка типов | `ty check` |

### Быстрый старт с инструментами

```bash
# Форматирование кода
uv run ruff format .

# Проверка на ошибки
uv run ruff check .

# Автоисправление ошибок
uv run ruff check --fix .

# Запуск тестов
uv run pytest

# Проверка типов
uv run ty check
```

## Структура репозитория

```
mipt-python-fall-2026/
├── seminars/
│   ├── seminar_01_intro_to_python/
│   │   ├── README.md      # материал семинара
│   │   ├── examples/      # примеры кода
│   │   └── exercises/     # практические задания
│   ├── seminar_02_data_types_and_control_flow/
│   └── ... (seminar_03 — seminar_11)
├── docs/
│   └── installation.md    # установка Python и выбор редактора
├── pyproject.toml         # конфигурация проекта (uv, ruff, pytest, ty)
├── CLAUDE.md              # инструкции для AI-агентов
├── AGENTS.md              # симлинк на CLAUDE.md
├── README.md              # этот файл
└── RESOURCES.md           # дополнительные материалы по курсу
```

## Использование

Каждый семинар содержит:

- `README.md` — теория, разбитая на блоки, с примерами и ссылками на практику
- `examples/` — примеры кода к блокам теории
- `exercises/` — практические задания с подсказками и решениями
- `data/` — данные и вспомогательные файлы (где применимо)

Для начала работы перейдите в директорию нужного семинара и следуйте инструкциям в `README.md`.

> 🚧 Материалы семинаров публикуются по мере прохождения курса: пока в директориях
> лежат заготовки, содержание появляется ближе к дате занятия.

## Содействие

Если вы нашли ошибку или хотите предложить улучшение, создайте issue или pull request.

## Лицензия

Этот проект предназначен для образовательных целей.

## Контакты

Для вопросов и предложений обращайтесь к преподавателям курса.
