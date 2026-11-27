# Практические задания: Работа с сетью. Сокеты

## Подготовка

Все команды выполняются из **корня репозитория курса**. Один раз установите
зависимости проекта — среди них библиотеки httpx и Flask (нужен интернет):

```bash
uv sync
```

На этом семинаре почти в каждой задаче работают **две программы сразу**: сервер
и клиент. Откройте два окна терминала (в VS Code и PyCharm — две вкладки
терминала) и в обоих перейдите в корень репозитория.

```bash
# Окно 1 — сервер
python seminars/seminar_10_networking_sockets/examples/01_echo_server.py

# Окно 2 — клиент
python seminars/seminar_10_networking_sockets/exercises/starter/task_1_1_client.py
```

- Сервер работает, пока его не остановят: **Ctrl+C** в его окне. Traceback
  с `KeyboardInterrupt` после этого — нормально.
- На порту 8000 одновременно может работать только **один** сервер. Перед запуском
  нового остановите предыдущий, иначе будет `OSError: Address already in use`.
- На Windows Ctrl+C иногда срабатывает только после следующего подключения
  к серверу. Если сервер не останавливается, запустите клиент ещё раз или закройте
  окно терминала.
- На macOS и Linux вместо `python` может понадобиться `python3`. Программы
  с httpx (Часть 3) запускайте через `uv run python`.

Примеры кода к каждой части — в папке [`../examples/`](../examples/).

> **Как работать с заданиями:** прочитайте условие, выполните его сами и только потом
> раскройте решение для сверки. Заготовки лежат в папке [`starter/`](starter/).

---

## Часть 1: Сокеты: клиент и сервер

> **Теория:** [README.md — Блок 1](../README.md#блок-1-сокеты-клиент-и-сервер-10-мин) | **Примеры:** [`examples/01_echo_server.py`](../examples/01_echo_server.py), [`examples/02_echo_client.py`](../examples/02_echo_client.py)

### Задание 1.1

Заготовка: [`starter/task_1_1_client.py`](starter/task_1_1_client.py)

Запустите в первом окне эхо-сервер из примеров
([`examples/01_echo_server.py`](../examples/01_echo_server.py)). Допишите клиент:
он спрашивает строку, отправляет её серверу и печатает ответ.

```
Сообщение: привет, сервер
Ответ сервера: ПРИВЕТ, СЕРВЕР
```

Посмотрите, что при этом вывел сервер в своём окне. Потом остановите сервер
и запустите клиент ещё раз. Какая ошибка появилась и почему?

<details>
<summary>Подсказка</summary>

Подключение — `socket.create_connection((HOST, PORT))` внутри `with`. Строку
перед отправкой превратите в байты: `message.encode("utf-8")`, отправьте через
`sendall()`. Ответ получите через `recv(1024)` и превратите обратно в строку
методом `decode("utf-8")`.

</details>

<details>
<summary>Решение</summary>

```python
import socket

HOST = "127.0.0.1"
PORT = 8000

message = input("Сообщение: ")

with socket.create_connection((HOST, PORT)) as sock:
    sock.sendall(message.encode("utf-8"))
    reply = sock.recv(1024).decode("utf-8")

print("Ответ сервера:", reply)
```

Без сервера клиент падает с `ConnectionRefusedError: [Errno 61] Connection refused`
(номер ошибки зависит от системы): на порту 8000 никто не слушает, и операционная
система отклоняет подключение. Как обработать эту ошибку, разберём в Блоке 2.

</details>

### Задание 1.2

Заготовка: [`starter/task_1_2_server.py`](starter/task_1_2_server.py)

Теперь напишите сервер сами. Он принимает клиентов по очереди: клиент присылает
своё имя, сервер отвечает приветствием с номером гостя и закрывает соединение.
Проверьте его клиентом из задания 1.1: запустите клиент несколько раз
с разными именами.

```
Сообщение: Аня
Ответ сервера: Привет, Аня! Ты гость №1
```

```
Сообщение: Боря
Ответ сервера: Привет, Боря! Ты гость №2
```

В окне сервера:

```
Сервер слушает 127.0.0.1:8000. Остановить — Ctrl+C
Гость №1: Аня ('127.0.0.1', 51234)
Гость №2: Боря ('127.0.0.1', 51236)
```

<details>
<summary>Подсказка</summary>

Сервер создаётся через `socket.create_server((HOST, PORT))`, клиент принимается
через `conn, addr = server.accept()` внутри `while True`. Соединение с клиентом
закроется само, если работать с `conn` внутри `with conn:`. Счётчик гостей
живёт **вне** цикла, иначе он будет обнуляться для каждого клиента.

</details>

<details>
<summary>Решение</summary>

```python
import socket

HOST = "127.0.0.1"
PORT = 8000

guest_count = 0

with socket.create_server((HOST, PORT)) as server:
    print(f"Сервер слушает {HOST}:{PORT}. Остановить — Ctrl+C")

    while True:
        conn, addr = server.accept()
        with conn:
            name = conn.recv(1024).decode("utf-8")
            guest_count += 1
            print(f"Гость №{guest_count}: {name} {addr}")
            greeting = f"Привет, {name}! Ты гость №{guest_count}"
            conn.sendall(greeting.encode("utf-8"))
```

Обратите внимание: порт у каждого клиента свой (51234, 51236, …) — его выбирает
операционная система при подключении.

</details>

### Задание 1.3

Заготовки: [`starter/task_1_3_server.py`](starter/task_1_3_server.py) и готовый
клиент [`starter/task_1_3_client.py`](starter/task_1_3_client.py)

Напишите сервер-переводчик. Клиент присылает слово за словом, сервер на каждое
отвечает переводом из словаря или фразой «Не знаю слова …». Разговор
продолжается, пока клиент не отключится; потом сервер ждёт следующего клиента.

```
Подключились к серверу
Запрос (Enter — выход): кот
Ответ: cat
Запрос (Enter — выход): Сеть
Ответ: network
Запрос (Enter — выход): жираф
Ответ: Не знаю слова жираф
Запрос (Enter — выход):
Соединение закрыто
```

Когда сервер заработает, запустите **два** клиента в двух окнах (сервер —
в третьем). Что происходит со вторым клиентом, пока первый подключён? Почему?

<details>
<summary>Подсказка</summary>

Внутри `with conn:` нужен второй цикл `while True`: получить данные, и если
`recv` вернул пустые байты `b""` — клиент отключился, выходим из цикла через
`break`. Перевод удобно искать методом словаря `get()` со значением по умолчанию,
а регистр выровнять через `lower()`.

</details>

<details>
<summary>Решение</summary>

```python
with socket.create_server((HOST, PORT)) as server:
    print(f"Сервер слушает {HOST}:{PORT}. Остановить — Ctrl+C")

    while True:
        conn, addr = server.accept()
        print("Подключился", addr)
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                word = data.decode("utf-8")
                translation = DICTIONARY.get(word.lower(), f"Не знаю слова {word}")
                conn.sendall(translation.encode("utf-8"))
        print("Отключился", addr)
```

Второй клиент подключается (операционная система ставит его в очередь), но ответа
не получает: сервер занят разговором с первым и вызовет `accept()` снова, только
когда первый клиент уйдёт. Как обслуживать нескольких клиентов одновременно, —
в README, раздел
[«Несколько клиентов одновременно»](../README.md#несколько-клиентов-одновременно),
и в заданиях 4.2–4.3.

</details>

---

## Часть 2: Тайм-ауты и сетевые ошибки

> **Теория:** [README.md — Блок 2](../README.md#блок-2-тайм-ауты-и-сетевые-ошибки-10-мин) | **Примеры:** [`examples/04_network_errors.py`](../examples/04_network_errors.py)

### Задание 2.1

Заготовка: [`starter/task_2_1.py`](starter/task_2_1.py)

Допишите функцию `check(host, port)`: она пробует подключиться к серверу, ждёт
не дольше 2 секунд и возвращает строку с результатом.

```
127.0.0.1:8000 — никто не слушает этот порт
example.com:80 — доступен
no-such-host.invalid:80 — имя не найдено
10.255.255.1:80 — нет ответа за 2 с
```

Запустите программу дважды: без сервера и с работающим эхо-сервером из примеров.
Как изменится первая строка?

> Адрес `10.255.255.1` обычно никому не принадлежит, и подключение «висит» до
> тайм-аута. В некоторых сетях система сразу отвечает, что адрес недоступен, —
> тогда сработает ветка «ошибка: …». Без интернета `example.com` выдаст «имя
> не найдено».

<details>
<summary>Подсказка</summary>

Тайм-аут передаётся в `socket.create_connection((host, port), timeout=TIMEOUT)`.
Нужные исключения: `socket.gaierror`, `ConnectionRefusedError`, `TimeoutError`
и общий `OSError`. Все они — наследники `OSError`, поэтому `except OSError`
должен идти **последним**.

</details>

<details>
<summary>Решение</summary>

```python
def check(host, port):
    """Проверить, принимает ли сервер host:port подключения."""
    try:
        with socket.create_connection((host, port), timeout=TIMEOUT):
            return "доступен"
    except socket.gaierror:
        return "имя не найдено"
    except ConnectionRefusedError:
        return "никто не слушает этот порт"
    except TimeoutError:
        return f"нет ответа за {TIMEOUT} с"
    except OSError as error:
        return f"ошибка: {error}"
```

`with` без `as` здесь подходит: сокет нам не нужен, важно только, что
подключение удалось, а закрыть соединение всё равно надо.

</details>

### Задание 2.2

Заготовки: готовый медленный сервер
[`starter/task_2_2_slow_server.py`](starter/task_2_2_slow_server.py) и клиент
[`starter/task_2_2_client.py`](starter/task_2_2_client.py)

Медленный сервер отвечает с задержкой от 0 до 4 секунд. Допишите клиент: в каждой
попытке он заново подключается к серверу, отправляет сообщение и ждёт ответ
не дольше 2 секунд. Попыток — не больше трёх.

```
Попытка 1: сервер не ответил за 2 с
Попытка 2: ответ — ПРИВЕТ
```

Если сервер не запущен, это тоже неудачная попытка:

```
Попытка 1: сервер не запущен
Попытка 2: сервер не запущен
Попытка 3: сервер не запущен
Сервер так и не ответил
```

Запустите клиент несколько раз и посмотрите, что пишет сервер в своём окне.

<details>
<summary>Подсказка</summary>

Попытки — цикл `for attempt in range(1, MAX_ATTEMPTS + 1)`. Внутри — `try` вокруг
подключения, отправки и `recv`. Удачный исход удобно обработать в блоке `else`
у `try` (он выполняется, если исключений не было,
см. [семинар 8](../../seminar_08_error_handling/README.md#else-и-finally)) и выйти
из цикла через `break`.

</details>

<details>
<summary>Решение</summary>

```python
message = "привет"
reply = None

for attempt in range(1, MAX_ATTEMPTS + 1):
    try:
        with socket.create_connection((HOST, PORT), timeout=TIMEOUT) as sock:
            sock.sendall(message.encode("utf-8"))
            reply = sock.recv(1024).decode("utf-8")
    except ConnectionRefusedError:
        print(f"Попытка {attempt}: сервер не запущен")
    except TimeoutError:
        print(f"Попытка {attempt}: сервер не ответил за {TIMEOUT} с")
    else:
        print(f"Попытка {attempt}: ответ — {reply}")
        break

if reply is None:
    print("Сервер так и не ответил")
```

Тайм-аут из `create_connection` действует не только на подключение, но и на все
следующие операции с сокетом, в том числе на `recv`.

</details>

### Задание 2.3

Заготовка: [`starter/task_2_3_server.py`](starter/task_2_3_server.py), клиент —
из задания 1.3

Напишите сервер-калькулятор. Клиент присылает выражения вида «число операция
число», сервер отвечает результатом. На любой неправильный запрос сервер отвечает
сообщением об ошибке и **продолжает работать**: один клиент с опечаткой не должен
«уронить» сервер для всех.

```
Запрос (Enter — выход): 2 + 3
Ответ: 5
Запрос (Enter — выход): 7 / 2
Ответ: 3.5
Запрос (Enter — выход): 1 / 0
Ответ: Ошибка: деление на ноль
Запрос (Enter — выход): 2 ^ 3
Ответ: Ошибка: неизвестная операция ^
Запрос (Enter — выход): два + три
Ответ: Ошибка: нужно «число операция число», например 2 + 3
```

<details>
<summary>Подсказка</summary>

`expression.split()` разобьёт «2 + 3» на три части; если частей не три,
распаковка `left, operation, right = ...` бросит `ValueError`, как и `float("два")`.
Собственное исключение `UnknownOperationError` уже объявлено в заготовке —
бросьте его через `raise`, как на
[семинаре 8](../../seminar_08_error_handling/README.md#блок-3-собственные-исключения-10-мин).
На сервере вызов `calculate` оберните в `try` и обработайте три исключения
по отдельности. Формат `:g` в f-строке выводит `5.0` как `5`.

</details>

<details>
<summary>Решение</summary>

```python
def calculate(expression):
    """Вычислить выражение вида «2 + 3»."""
    left, operation, right = expression.split()  # не три части — ValueError
    a = float(left)  # не число — ValueError
    b = float(right)
    if operation == "+":
        return a + b
    if operation == "-":
        return a - b
    if operation == "*":
        return a * b
    if operation == "/":
        return a / b  # деление на ноль — ZeroDivisionError
    raise UnknownOperationError(operation)
```

Цикл разговора с клиентом:

```python
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                expression = data.decode("utf-8")
                try:
                    reply = f"{calculate(expression):g}"
                except ZeroDivisionError:
                    reply = "Ошибка: деление на ноль"
                except UnknownOperationError as error:
                    reply = f"Ошибка: неизвестная операция {error}"
                except ValueError:
                    reply = "Ошибка: нужно «число операция число», например 2 + 3"
                conn.sendall(reply.encode("utf-8"))
```

Ошибку ловим там, где знаем, **что ответить**: функция `calculate` ничего не знает
о сети и только сообщает о проблеме, а сервер превращает исключение в понятный
ответ клиенту.

</details>

---

## Часть 3: HTTP и httpx

> **Теория:** [README.md — Блок 3](../README.md#блок-3-протокол-http-и-библиотека-httpx-10-мин) | **Примеры:** [`examples/05_http_server.py`](../examples/05_http_server.py), [`examples/07_httpx_client.py`](../examples/07_httpx_client.py)

### Задание 3.1

Заготовка: [`starter/task_3_1_server.py`](starter/task_3_1_server.py)

Цикл приёма запросов в заготовке уже написан. Допишите функции `make_response`
и `route`, чтобы сервер отвечал браузеру:

| Адрес | Код | Страница |
|-------|-----|----------|
| http://127.0.0.1:8080/ | 200 | заголовок «Главная» и ссылка на `/time` |
| http://127.0.0.1:8080/time | 200 | текущее время, например «Сейчас 19:42:07» |
| http://127.0.0.1:8080/abc | 404 | «Страницы /abc нет» |

Откройте эти адреса в браузере и перейдите по ссылке. Обновите страницу `/time`:
время должно меняться. В окне сервера видно, какие запросы приходят — например,
браузер сам просит `/favicon.ico` (значок вкладки).

<details>
<summary>Подсказка</summary>

Ответ — это строка: `HTTP/1.1 200 OK\r\n`, затем заголовки
`Content-Type: text/html; charset=utf-8\r\n` и `Content-Length: ...\r\n`, пустая
строка `\r\n` и тело. Длина тела считается **в байтах**: `len(body.encode("utf-8"))`.
Текущее время — `datetime.now().strftime("%H:%M:%S")`, как на
[семинаре 9](../../seminar_09_packages_venv_git/README.md#три-модуля-стандартной-библиотеки).
Ссылка в HTML: `<a href="/time">текст</a>`.

</details>

<details>
<summary>Решение</summary>

```python
import socket
from datetime import datetime
from html import escape

...


def make_response(status, body):
    """Собрать HTTP-ответ с кодом status и HTML-страницей body."""
    body_bytes = body.encode("utf-8")
    head = (
        f"HTTP/1.1 {status} {REASONS[status]}\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body_bytes)}\r\n"
        "\r\n"
    )
    return head.encode("utf-8") + body_bytes


def route(path):
    """Вернуть пару (код ответа, HTML-страница) для пути path."""
    if path == "/":
        return 200, '<h1>Главная</h1><p><a href="/time">Который час?</a></p>'
    if path == "/time":
        now = datetime.now().strftime("%H:%M:%S")
        return 200, f"<h1>Сейчас {now}</h1>"
    return 404, f"<h1>Страницы {escape(path)} нет</h1>"
```

`escape()` нужен, потому что путь приходит от пользователя: без него адрес
вида `/<script>...` превратился бы в HTML-код на нашей странице.

Если в `Content-Length` указать длину строки в символах, а не в байтах, браузер
обрежет русский текст: каждая кириллическая буква в UTF-8 занимает 2 байта.

</details>

### Задание 3.2

Заготовка: [`starter/task_3_2.py`](starter/task_3_2.py)

Проверьте свой сервер из задания 3.1 программой, а не браузером. Запустите сервер
в одном окне, а программу — через uv в другом:

```bash
uv run python seminars/seminar_10_networking_sockets/exercises/starter/task_3_2.py
```

```
/      → 200 OK, 72 байт
/time  → 200 OK, 30 байт
/abc   → 404 Not Found
```

Размер тела зависит от ваших страниц. Если сервер не запущен, программа выводит
«Сервер не запущен» один раз и завершает проверку.

<details>
<summary>Подсказка</summary>

`httpx.get(url)` возвращает ответ: код — `status_code`, его описание —
`reason_phrase`, тело в байтах — `content`. Успешность ответа (код 2xx) показывает
свойство `is_success`. Если сервер не запущен, `httpx.get` бросает
`httpx.ConnectError`. Выровнять путь по ширине поможет формат `{path:6}`.

</details>

<details>
<summary>Решение</summary>

```python
import httpx

BASE_URL = "http://127.0.0.1:8080"
paths = ["/", "/time", "/abc"]

for path in paths:
    try:
        response = httpx.get(BASE_URL + path)
    except httpx.ConnectError:
        print("Сервер не запущен")
        break
    line = f"{path:6} → {response.status_code} {response.reason_phrase}"
    if response.is_success:
        line += f", {len(response.content)} байт"
    print(line)
```

Ответ 404 — не исключение: сервер ответил, просто кодом «не найдено». Исключение
возникает, только если ответа нет совсем.

</details>

### Задание 3.3

Заготовка: [`starter/task_3_3.py`](starter/task_3_3.py)

Напишите конвертер валют по курсу Центрального банка. Курсы в формате JSON
публикует сервис [cbr-xml-daily.ru](https://www.cbr-xml-daily.ru/): откройте
адрес `https://www.cbr-xml-daily.ru/daily_json.js` в браузере и посмотрите, как
устроены данные. Нужен интернет.

```
Код валюты: usd
Сумма: 100
100.0 USD = 8227.32 ₽ (курс ЦБ на 28.11.2026)
```

```
Код валюты: xyz
Сумма: 1
Валюты XYZ нет в списке ЦБ
```

Если загрузить курсы не удалось (нет интернета, сервис недоступен), программа
сообщает об этом, а не падает с traceback.

<details>
<summary>Подсказка</summary>

Курсы лежат в словаре `data["Valute"]` по коду валюты, например
`data["Valute"]["USD"]`. Курс в поле `Value` указан за `Nominal` единиц (для
японской иены — за 100), поэтому курс одной единицы — `Value / Nominal`. Дату курса
из строки `data["Date"]` превратит в объект `datetime.fromisoformat()`. Все ошибки
httpx — и сетевые, и от `raise_for_status()` — наследники `httpx.HTTPError`.

</details>

<details>
<summary>Решение</summary>

```python
from datetime import datetime

import httpx

URL = "https://www.cbr-xml-daily.ru/daily_json.js"

code = input("Код валюты: ").strip().upper()
amount = float(input("Сумма: "))

try:
    response = httpx.get(URL, timeout=10)
    response.raise_for_status()
except httpx.HTTPError as error:
    print("Не удалось загрузить курсы:", error)
else:
    data = response.json()
    currencies = data["Valute"]
    if code in currencies:
        currency = currencies[code]
        rate = currency["Value"] / currency["Nominal"]  # курс за одну единицу
        date = datetime.fromisoformat(data["Date"]).strftime("%d.%m.%Y")
        print(f"{amount} {code} = {amount * rate:.2f} ₽ (курс ЦБ на {date})")
    else:
        print(f"Валюты {code} нет в списке ЦБ")
```

Проверьте японскую иену (`JPY`): без деления на `Nominal` сумма получится
в 100 раз больше.

</details>

---

## Для самостоятельной работы

Задачи по темам из раздела README
[«Темы лекции, которые мы не разбираем на занятии»](../README.md#темы-лекции-которые-мы-не-разбираем-на-занятии).
Сдавать их не нужно, решения — под спойлерами.

### Задание 4.1

Для сайтов `python.org`, `mipt.ru`, `google.com` и `no-such-site.invalid` выведите
их IPv4- и IPv6-адреса (без повторов). Для несуществующего имени — «имя не найдено».

```
python.org: IPv4 ['151.101.0.223', '151.101.128.223', ...], IPv6 ['2a04:4e42::223', ...]
mipt.ru: IPv4 ['192.188.189.148'], IPv6 —
no-such-site.invalid: имя не найдено
```

Адреса у вас могут отличаться. Если в вашей сети нет IPv6, система не вернёт
IPv6-адреса ни для одного сайта.

<details>
<summary>Подсказка</summary>

`socket.getaddrinfo(site, 443, proto=socket.IPPROTO_TCP)` возвращает список
кортежей, адрес — первый элемент последнего поля. Повторы уберёт множество.
Версию адреса покажет `ipaddress.ip_address(text).version`. Пример —
[`examples/08_addresses.py`](../examples/08_addresses.py).

</details>

<details>
<summary>Решение</summary>

```python
import ipaddress
import socket

sites = ["python.org", "mipt.ru", "google.com", "no-such-site.invalid"]

for site in sites:
    try:
        infos = socket.getaddrinfo(site, 443, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        print(f"{site}: имя не найдено")
        continue
    addresses = sorted({sockaddr[0] for _, _, _, _, sockaddr in infos})
    ipv4 = [a for a in addresses if ipaddress.ip_address(a).version == 4]
    ipv6 = [a for a in addresses if ipaddress.ip_address(a).version == 6]
    print(f"{site}: IPv4 {ipv4 or '—'}, IPv6 {ipv6 or '—'}")
```

</details>

### Задание 4.2

Перепишите сервер-переводчик из задания 1.3 на `select`, чтобы он отвечал
нескольким клиентам одновременно. Проверьте: два клиента
[`starter/task_1_3_client.py`](starter/task_1_3_client.py) в двух окнах должны
получать переводы, не дожидаясь друг друга.

<details>
<summary>Подсказка</summary>

Возьмите за образец [`examples/09_select_server.py`](../examples/09_select_server.py):
список `monitoring`, `select.select(monitoring, [], [])`, отдельная ветка для
серверного сокета (новый клиент) и для клиентских (пришло слово или клиент ушёл).

</details>

<details>
<summary>Решение</summary>

```python
import select
import socket

HOST = "127.0.0.1"
PORT = 8000

DICTIONARY = {"кот": "cat", "собака": "dog", "сеть": "network"}

with socket.create_server((HOST, PORT)) as server:
    print(f"Сервер слушает {HOST}:{PORT}. Остановить — Ctrl+C")
    monitoring = [server]

    while True:
        ready, _, _ = select.select(monitoring, [], [])
        for sock in ready:
            if sock is server:
                conn, addr = server.accept()
                monitoring.append(conn)
                print("Подключился", addr)
                continue

            data = sock.recv(1024)
            if not data:
                print("Отключился", sock.getpeername())
                monitoring.remove(sock)
                sock.close()
                continue

            word = data.decode("utf-8")
            translation = DICTIONARY.get(word.lower(), f"Не знаю слова {word}")
            sock.sendall(translation.encode("utf-8"))
```

</details>

### Задание 4.3

Перепишите сервер-калькулятор из задания 2.3 на модуле `socketserver` так, чтобы
каждый клиент обслуживался в отдельном потоке. Проверьте двумя клиентами
одновременно.

<details>
<summary>Подсказка</summary>

Образец — [`examples/10_threading_server.py`](../examples/10_threading_server.py).
Цикл разговора с клиентом переезжает в метод `handle()` класса-наследника
`BaseRequestHandler`; вместо `conn` — `self.request`. Функция `calculate`
и класс `UnknownOperationError` остаются без изменений.

</details>

<details>
<summary>Решение</summary>

```python
import socketserver

HOST = "127.0.0.1"
PORT = 8000


# class UnknownOperationError и def calculate — как в задании 2.3


class CalculatorHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print(f"Подключился {self.client_address}")
        while True:
            data = self.request.recv(1024)
            if not data:
                break
            try:
                reply = f"{calculate(data.decode('utf-8')):g}"
            except ZeroDivisionError:
                reply = "Ошибка: деление на ноль"
            except UnknownOperationError as error:
                reply = f"Ошибка: неизвестная операция {error}"
            except ValueError:
                reply = "Ошибка: нужно «число операция число», например 2 + 3"
            self.request.sendall(reply.encode("utf-8"))
        print(f"Отключился {self.client_address}")


class CalculatorServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True


with CalculatorServer((HOST, PORT), CalculatorHandler) as server:
    print(f"Калькулятор слушает {HOST}:{PORT}. Остановить — Ctrl+C")
    server.serve_forever()
```

</details>

### Задание 4.4

Выведите прогноз минимальной и максимальной температуры в Долгопрудном на три дня
вперёд с сервиса Open-Meteo (как в
[`examples/07_httpx_client.py`](../examples/07_httpx_client.py), но с параметром
`daily`):

```
пн 30.11: от -6.2 до -3.3 °C
вт 01.12: от -7.0 до -2.1 °C
ср 02.12: от -4.5 до -0.8 °C
```

<details>
<summary>Подсказка</summary>

Параметры запроса: `"daily": "temperature_2m_min,temperature_2m_max"`,
`"timezone": "Europe/Moscow"`, `"forecast_days": 3`. В ответе `data["daily"]`
лежат три списка одинаковой длины: даты, минимумы и максимумы. Пройти по ним
одновременно поможет `zip()`.

</details>

<details>
<summary>Решение</summary>

```python
from datetime import date

import httpx

URL = "https://api.open-meteo.com/v1/forecast"
WEEKDAYS = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]

params = {
    "latitude": 55.94,
    "longitude": 37.52,
    "daily": "temperature_2m_min,temperature_2m_max",
    "timezone": "Europe/Moscow",
    "forecast_days": 3,
}

try:
    response = httpx.get(URL, params=params, timeout=10)
    response.raise_for_status()
except httpx.HTTPError as error:
    print("Не удалось получить прогноз:", error)
else:
    daily = response.json()["daily"]
    days = zip(daily["time"], daily["temperature_2m_min"], daily["temperature_2m_max"])
    for day_text, t_min, t_max in days:
        day = date.fromisoformat(day_text)
        weekday = WEEKDAYS[day.weekday()]
        print(f"{weekday} {day.strftime('%d.%m')}: от {t_min} до {t_max} °C")
```

</details>

### Задание 4.5

Сделайте сайт из задания 3.1 на Flask: страницы `/` и `/time` и новая страница
`/hello/<имя>`, которая здоровается по имени из адреса. Сравните, сколько кода
понадобилось.

```bash
uv run python путь/к/файлу.py
```

<details>
<summary>Подсказка</summary>

Образец — [`examples/11_flask_app.py`](../examples/11_flask_app.py). Каждая страница —
функция с декоратором `@app.route(...)`, которая возвращает HTML-строку. Код 404
для остальных адресов Flask вернёт сам.

</details>

<details>
<summary>Решение</summary>

```python
from datetime import datetime

from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def index():
    return '<h1>Главная</h1><p><a href="/time">Который час?</a></p>'


@app.route("/time")
def current_time():
    now = datetime.now().strftime("%H:%M:%S")
    return f"<h1>Сейчас {now}</h1>"


@app.route("/hello/<name>")
def hello(name):
    return f"<h1>Привет, {escape(name)}!</h1>"


if __name__ == "__main__":
    app.run(port=5001, debug=True)
```

Разбор запроса, коды ответов, `Content-Length`, тайм-ауты и цикл `accept()` Flask
взял на себя — осталась только логика страниц.

</details>
