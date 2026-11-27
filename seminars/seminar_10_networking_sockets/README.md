# Семинар 10: Работа с сетью. Сокеты

**Модуль:** 1 — Основы программирования на Python  
**Дата:** 30.11.2026, 18:40–20:10  
**Презентация:** [ссылка](https://docs.google.com/presentation/d/13wKUdxgGn6EjBUHakrdQ9BhYiFhMygwrEMufYSzEgek/edit?usp=sharing)

---

## Цели семинара

После этого семинара вы сможете:

- Объяснить, что такое IP-адрес, порт и сокет и чем TCP отличается от UDP
- Написать TCP-сервер и клиент на модуле `socket` и обменяться между ними
  сообщениями
- Переводить строки в байты и обратно для передачи по сети
- Обрабатывать сетевые ошибки и задавать тайм-ауты, чтобы программа не зависала
- Объяснить, как устроены HTTP-запрос и HTTP-ответ, и написать простой веб-сервер
  на сокетах
- Делать HTTP-запросы с библиотекой `httpx` и разбирать ответы в формате JSON

---

## Подготовка

Все примеры запускаются из **корня репозитория курса**. Один раз установите
зависимости проекта — среди них библиотеки `httpx` и `Flask` (нужен интернет):

```bash
uv sync
```

> Это тот же `uv sync`, что на
> [семинаре 9](../seminar_09_packages_venv_git/README.md#что-передавать-другим):
> uv читает `pyproject.toml` и `uv.lock` репозитория и создаёт окружение `.venv`.

На этом семинаре почти всегда работают **две программы сразу** — сервер и клиент.
Откройте два окна терминала (в VS Code и PyCharm — две вкладки терминала):

```bash
# Окно 1 — сервер
python seminars/seminar_10_networking_sockets/examples/01_echo_server.py

# Окно 2 — клиент
python seminars/seminar_10_networking_sockets/examples/02_echo_client.py

# Программы с внешними библиотеками — через uv
uv run python seminars/seminar_10_networking_sockets/examples/07_httpx_client.py
```

Сервер работает, пока его не остановят: **Ctrl+C** в его окне.

---

## План семинара

После каждого блока теории — 15 минут на упражнения из файла
[`exercises/networking_practice.md`](exercises/networking_practice.md).

| Время | Тема | Практика |
|-------|------|----------|
| 5 мин | Организационное и [вступление: как устроена сеть](#вступление-как-устроена-сеть) | — |
| 10 мин | Блок 1: Сокеты: клиент и сервер | — |
| 15 мин | Практика | → Упражнения: Часть 1 |
| 10 мин | Блок 2: Тайм-ауты и сетевые ошибки | — |
| 15 мин | Практика | → Упражнения: Часть 2 |
| 10 мин | Блок 3: Протокол HTTP и библиотека httpx | — |
| 15 мин | Практика | → Упражнения: Часть 3 |

> **Примечание:** в таблице 80 минут, оставшиеся ~10 минут — на вопросы и разбор задач.
> Модель OSI, DNS, обслуживание нескольких клиентов одновременно (`select`, потоки)
> и Flask вынесены в раздел
> [«Темы лекции, которые мы не разбираем на занятии»](#темы-лекции-которые-мы-не-разбираем-на-занятии).

---

## Вступление: как устроена сеть

**Протокол** — набор правил, по которым программы обмениваются данными. Протоколы
устроены слоями: каждый слой пользуется нижним и не думает о его деталях. Интернет
работает по стеку **TCP/IP**:

| Уровень | Что делает | Протоколы |
|---------|-----------|-----------|
| Прикладной | смысл данных: страница, письмо, файл | HTTP, DNS, SMTP, SSH |
| Транспортный | доставка данных нужной программе | TCP, UDP |
| Сетевой | доставка пакетов нужному компьютеру | IP |
| Канальный | передача по проводу или радио | Ethernet, Wi-Fi |

- **IP-адрес** — адрес компьютера в сети, например `151.101.0.223` (IPv4) или
  `2001:db8::1` (IPv6). Адрес **`127.0.0.1`** означает «этот же компьютер» — на
  семинаре сервер и клиент работают на одной машине.
- **Порт** — число от 0 до 65535. По нему операционная система понимает, какой
  программе адресованы данные. Стандартные порты: 80 — HTTP, 443 — HTTPS, 22 — SSH.
- **Сокет** — конечная точка соединения: пара «IP-адрес + порт», например
  `("127.0.0.1", 8000)`. В Python это объект, через который программа отправляет
  и получает данные.
- **TCP** гарантирует, что данные дойдут целыми и в правильном порядке, а при потере
  перешлёт их заново. **UDP** проще и быстрее, но ничего не гарантирует (используется
  для видеозвонков и игр, где опоздавший пакет уже не нужен). На семинаре — только
  TCP.

---

## Блок 1: Сокеты: клиент и сервер (10 мин)

### Клиент и сервер

**Сервер** заранее занимает порт и ждёт подключений. **Клиент** подключается
к серверу по его адресу и порту. После подключения оба могут отправлять и получать
данные.

```
 СЕРВЕР                                    КЛИЕНТ
 create_server(("127.0.0.1", 8000))
 accept() — ждёт клиента...                create_connection(("127.0.0.1", 8000))
          ◀──────────── подключение ──────────────
 recv()   ◀──────────── sendall(b"hi") ───────────
 sendall(b"HI") ──────────────────────▶    recv()
 close()                                   close()
```

### Сервер

```python
import socket

with socket.create_server(("127.0.0.1", 8000)) as server:
    while True:  # клиенты по очереди, один за другим
        conn, addr = server.accept()  # ждём клиента; conn — сокет для разговора с ним
        with conn:
            text = conn.recv(1024).decode("utf-8")  # получить до 1024 байт
            conn.sendall(text.upper().encode("utf-8"))  # отправить ответ
```

`accept()` **блокирует** программу: она стоит на этой строке, пока кто-нибудь
не подключится. `recv()` так же ждёт, пока придут данные.

### Клиент

```python
import socket

with socket.create_connection(("127.0.0.1", 8000)) as sock:
    sock.sendall("привет".encode("utf-8"))
    reply = sock.recv(1024)
    print(reply.decode("utf-8"))  # ПРИВЕТ
```

`with` закрывает сокет при выходе из блока, как файл на
[семинаре 5](../seminar_05_files_and_classes/README.md#open-и-with).

### Байты, а не строки

По сети передаются **байты** (`bytes`), а не строки. Строку перед отправкой
кодируют, полученные байты декодируют:

```python
data = "привет".encode("utf-8")  # b'\xd0\xbf\xd1\x80...' — 12 байт
text = data.decode("utf-8")  # 'привет'
```

Когда другая сторона закрывает соединение, `recv()` возвращает **пустые байты**
`b""`. По этому признаку сервер понимает, что клиент ушёл:

```python
while True:
    data = conn.recv(1024)
    if not data:  # b"" — клиент отключился
        break
    conn.sendall(data)
```

### Что внутри create_server

`create_server` и `create_connection` — короткие формы. Внутри сервер проходит
те же шаги, что и системные вызовы операционной системы (так сервер записан
в лекции):

| Шаг | Вызов | Что делает |
|-----|-------|-----------|
| 1 | `socket.socket()` | создать сокет (по умолчанию IPv4 и TCP) |
| 2 | `bind((host, port))` | занять адрес и порт |
| 3 | `listen()` | начать принимать подключения |
| 4 | `accept()` | дождаться клиента, получить сокет для разговора с ним |
| 5 | `recv()` / `sendall()` | обменяться данными |
| 6 | `close()` | закрыть сокет |

`sendall()` отправляет все данные, а `send()` — сколько получится за раз и возвращает
число отправленных байт. Поэтому почти всегда используют `sendall()`.

> **Порт после перезапуска.** Без дополнительной настройки порт остаётся занятым
> ещё некоторое время после остановки сервера. В лекции для этого используется
> `setsockopt(SOL_SOCKET, SO_REUSEPORT, True)`, но `SO_REUSEPORT` нет на Windows;
> переносимый вариант — `SO_REUSEADDR`. `create_server` настраивает это сам.

> **TCP передаёт поток байтов, а не отдельные сообщения.** Один `sendall` может
> прийти несколькими `recv`, а два `sendall` — одним. На семинаре сообщения
> короткие и идут по очереди «запрос — ответ», поэтому одного `recv` хватает.
> В настоящих протоколах границы сообщений обозначают явно — так делает HTTP
> из Блока 3. Размер буфера `recv(1024)` — просто верхняя граница; степень двойки —
> лишь традиция.

> **Подробнее:** см. файлы [`examples/01_echo_server.py`](examples/01_echo_server.py),
> [`examples/02_echo_client.py`](examples/02_echo_client.py) и
> [`examples/03_low_level_server.py`](examples/03_low_level_server.py) (все шаги
> по отдельности)

### Практика

Перейдите к разделу **Часть 1: Сокеты: клиент и сервер** в файле
[`exercises/networking_practice.md`](exercises/networking_practice.md#часть-1-сокеты-клиент-и-сервер).

---

## Блок 2: Тайм-ауты и сетевые ошибки (10 мин)

### Что может пойти не так

Сеть ненадёжна: сервер может быть выключен, адрес — опечатан, ответ — задерживаться.

| Исключение | Когда возникает |
|------------|-----------------|
| `socket.gaierror` | имя сервера не удалось превратить в IP-адрес (опечатка, нет интернета) |
| `ConnectionRefusedError` | на этом порту никто не слушает |
| `TimeoutError` | истёк тайм-аут: ответа нет слишком долго |
| `ConnectionResetError` | другая сторона оборвала соединение |
| `OSError: Address already in use` | порт уже занят другим сервером |

### Все они — OSError

Исключения — это классы с наследованием
([семинар 8](../seminar_08_error_handling/README.md#иерархия-исключений)). Все ошибки
модуля `socket` — наследники `OSError`:

```
OSError
├── socket.gaierror
├── TimeoutError                 ← socket.timeout в Python 3.10+ — то же самое
└── ConnectionError
    ├── ConnectionRefusedError
    └── ConnectionResetError
```

Поэтому частные случаи перехватывают **раньше**, а `OSError` — последним, на всё
остальное:

```python
try:
    with socket.create_connection((host, port), timeout=3) as sock:
        sock.sendall(b"ping")
        reply = sock.recv(1024)
except socket.gaierror:
    print("Адрес не найден")
except TimeoutError:
    print("Сервер не ответил за 3 с")
except ConnectionRefusedError:
    print("Сервер не запущен")
except OSError as error:
    print("Другая сетевая ошибка:", error)
```

### Тайм-аут

По умолчанию тайм-аута **нет**: `recv()` будет ждать ответа хоть вечно, и программа
зависнет. Тайм-аут в секундах задают при подключении или для уже созданного сокета:

```python
sock = socket.create_connection((host, port), timeout=3)  # на все операции
conn.settimeout(2)  # для сокета, который уже есть
```

Когда время истекает, операция бросает `TimeoutError`.

### Ошибки на стороне сервера

Сервер обслуживает многих клиентов, поэтому ошибка в обработке **одного** запроса
не должна останавливать весь сервер. Обработку запроса оборачивают в `try`
и отвечают клиенту сообщением об ошибке:

```python
try:
    reply = str(int(text) ** 2)
except ValueError:
    reply = "Ошибка: нужно целое число"
conn.sendall(reply.encode("utf-8"))
```

> **Подробнее:** см. файл [`examples/04_network_errors.py`](examples/04_network_errors.py) —
> все ошибки из таблицы на живых примерах, без интернета

### Практика

Перейдите к разделу **Часть 2: Тайм-ауты и сетевые ошибки** в файле
[`exercises/networking_practice.md`](exercises/networking_practice.md#часть-2-тайм-ауты-и-сетевые-ошибки).

---

## Блок 3: Протокол HTTP и библиотека httpx (10 мин)

### HTTP — текст поверх TCP

Браузер общается с сайтами по протоколу **HTTP**. Это обычный текст, который
передаётся через TCP-сокет. Запрос:

```
GET /admin HTTP/1.1          ← метод, путь, версия
Host: 127.0.0.1:8080         ← заголовки «Имя: значение»
User-Agent: Mozilla/5.0
                             ← пустая строка: заголовки кончились
```

Ответ:

```
HTTP/1.1 403 Forbidden                      ← версия, код, описание
Content-Type: text/html; charset=utf-8      ← что в теле
Content-Length: 40                          ← сколько байт в теле
                                            ← пустая строка
<h1>403</h1><p>Сюда нельзя</p>              ← тело
```

- Строки разделяются символами `\r\n`, заголовки от тела — пустой строкой
  `\r\n\r\n`.
- Заголовок `Host` обязателен: на одном сервере может работать много сайтов.
- `Content-Length` считается **в байтах**: «Привет» — 6 символов, но 12 байт.

### Коды ответа

| Код | Значение | Примеры |
|-----|----------|---------|
| 1xx | информационные | `101 Switching Protocols` |
| 2xx | успех | `200 OK`, `201 Created` |
| 3xx | перенаправление | `301 Moved Permanently` |
| 4xx | ошибка клиента | `400 Bad Request`, `403 Forbidden`, `404 Not Found` |
| 5xx | ошибка сервера | `500 Internal Server Error` |

### HTTP-сервер своими руками

Веб-сервер — это TCP-сервер, который читает текст запроса и отправляет текст ответа:

```python
def make_response(status, body):
    body_bytes = body.encode("utf-8")
    head = (
        f"HTTP/1.1 {status} {REASONS[status]}\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body_bytes)}\r\n"
        "\r\n"
    )
    return head.encode("utf-8") + body_bytes


request = conn.recv(4096).decode("utf-8")
method, path, version = request.split("\r\n")[0].split()  # GET /admin HTTP/1.1
conn.sendall(make_response(200, "<h1>Привет!</h1>"))
```

Запустите [`examples/05_http_server.py`](examples/05_http_server.py) и откройте
в браузере http://127.0.0.1:8080/ — в окне сервера будет виден полный текст запроса
браузера.

### Библиотека httpx

Писать HTTP вручную долго, а настоящие сайты добавляют сжатие, шифрование (HTTPS),
перенаправления и ответы частями. На практике используют библиотеку — например,
**httpx** (или похожую `requests`). Она внешняя и ставится через uv, как на
[семинаре 9](../seminar_09_packages_venv_git/README.md#блок-2-проект-и-зависимости-с-uv-10-мин);
в репозитории курса она уже есть в зависимостях.

```python
import httpx

response = httpx.get("http://127.0.0.1:8080/admin")
response.status_code  # 403
response.headers["Content-Type"]  # 'text/html; charset=utf-8'
response.text  # тело ответа — строка

response = httpx.get(
    "https://api.open-meteo.com/v1/forecast",
    params={"latitude": 55.94, "longitude": 37.52, "current": "temperature_2m"},
    timeout=10,  # по умолчанию 5 с
)
data = response.json()  # JSON → словарь
print(data["current"]["temperature_2m"])
```

Ответ с кодом 4xx или 5xx — **не исключение**: httpx просто вернёт ответ с этим
кодом. Чтобы превратить его в исключение, вызывают `response.raise_for_status()`.

| Исключение httpx | Когда |
|------------------|-------|
| `httpx.ConnectError` | не удалось подключиться |
| `httpx.TimeoutException` | истёк тайм-аут |
| `httpx.HTTPStatusError` | `raise_for_status()` при коде 4xx/5xx |
| `httpx.HTTPError` | общий предок всех ошибок выше |

> **Подробнее:** см. файлы [`examples/05_http_server.py`](examples/05_http_server.py),
> [`examples/06_raw_http_client.py`](examples/06_raw_http_client.py) (HTTP-запрос
> через сокет) и [`examples/07_httpx_client.py`](examples/07_httpx_client.py)

### Практика

Перейдите к разделу **Часть 3: HTTP и httpx** в файле
[`exercises/networking_practice.md`](exercises/networking_practice.md#часть-3-http-и-httpx).

---

## Темы лекции, которые мы не разбираем на занятии

Короткая теория для самостоятельного чтения. Примеры — в файлах
[`examples/08_addresses.py`](examples/08_addresses.py)–[`examples/11_flask_app.py`](examples/11_flask_app.py),
задачи — в разделе
[«Для самостоятельной работы»](exercises/networking_practice.md#для-самостоятельной-работы).

### Модель OSI и подробнее про IP

Модель **OSI** делит сетевые протоколы на 7 уровней: прикладной, представления,
сеансовый, транспортный, сетевой, канальный, физический. Стек TCP/IP из вступления —
её упрощённый вариант: верхние три уровня OSI в нём объединены в прикладной,
а нижние два — в канальный.

- **IPv4** — 32 бита, около 4,3 млрд адресов; свободные адреса давно закончились.
- **IPv6** — 128 бит, около 3,4·10³⁸ адресов. Запись сокращают: ведущие нули
  в группах опускают, одну серию нулевых групп заменяют на `::`
  (`2001:0db8:0000:0000:0000:0000:0000:0001` → `2001:db8::1`). Актуальную долю
  IPv6 можно посмотреть в [статистике Google](https://www.google.com/intl/ru/ipv6/statistics.html) —
  сейчас это почти половина запросов.
- **Специальные адреса:** `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16` —
  локальные сети (домашний роутер раздаёт адреса вида `192.168.x.x`); `127.0.0.1`
  (IPv6: `::1`) — этот компьютер без участия сетевой карты; `0.0.0.0` при запуске
  сервера — «на всех сетевых интерфейсах», то есть сервер доступен и с других
  компьютеров.
- Данные передаются **пакетами** до 64 КБ с заголовком (20 байт в IPv4, 40 в IPv6).
  Благодаря пакетам по одному каналу идут сразу много соединений, а при потере
  пересылается только потерянный пакет.

### Имена и адреса: DNS

Программы подключаются по IP-адресам, а людям удобнее имена. Имя в адрес переводит
система **DNS**:

```python
socket.getaddrinfo("python.org", 443)  # все адреса (IPv4 и IPv6) для имени
socket.gethostbyname("python.org")  # один IPv4-адрес
socket.gethostbyaddr("8.8.8.8")  # обратно: адрес → имя (есть не у всех адресов)
```

Модуль `ipaddress` разбирает и проверяет адреса:
`ipaddress.ip_address("192.168.1.10").is_private` → `True`.

### Несколько клиентов одновременно

Сервер из Блока 1 обслуживает клиентов **по очереди**: пока он разговаривает
с одним, `accept()` для следующего не вызывается (это видно в задании 1.3).
Держать соединения открытыми при этом выгодно: установка соединения — дорогая
операция. Три способа обслуживать многих сразу:

1. **`select`** — один цикл следит за всеми сокетами сразу. Функция
   `select.select(read, write, err)` ждёт, пока хоть один сокет станет готов,
   и возвращает готовые. Если готов серверный сокет — пришёл новый клиент
   (`accept()`), если клиентский — пришли данные (`recv()`). На Windows `select`
   работает только с сокетами. Пример — [`examples/09_select_server.py`](examples/09_select_server.py).
2. **Потоки** — каждый клиент обслуживается в отдельном потоке. Модуль
   `socketserver` берёт на себя `bind`, `listen` и `accept`: достаточно унаследоваться
   от `BaseRequestHandler`
   ([наследование — семинар 6](../seminar_06_inheritance/README.md#блок-1-наследование-10-мин))
   и переопределить `handle()`. Клиентский сокет там — `self.request`.

   ```python
   class Handler(socketserver.BaseRequestHandler):
       def handle(self):
           data = self.request.recv(1024)
           self.request.sendall(data)  # вернуть клиенту то же самое


   class Server(socketserver.ThreadingMixIn, socketserver.TCPServer):  # MixIn — первым
       daemon_threads = True
       allow_reuse_address = True


   with Server(("127.0.0.1", 8000), Handler) as server:
       server.serve_forever()
   ```

   Пример — [`examples/10_threading_server.py`](examples/10_threading_server.py).
3. **Асинхронность** (`asyncio`) — тема следующих лекций.

### HTTP в стандартной библиотеке

В стандартной библиотеке есть модули `http` (`http.client`, `http.server`,
`http.cookies`) и `urllib` (`urllib.request`, `urllib.parse`). Ими пользуются в основном
авторы библиотек и фреймворков, но одна команда пригодится всем — раздать файлы
текущей папки по HTTP:

```bash
python -m http.server 8000   # откройте http://127.0.0.1:8000/
```

> Если в запросе вручную указать заголовок `Accept-Encoding: gzip`, сервер пришлёт
> тело в сжатом виде, и без распаковки его не прочитать. httpx распаковывает ответы
> сам.

### Ещё о httpx

```python
httpx.post(url, json={"name": "Аня"})  # отправить JSON в теле запроса
httpx.get(url, headers={"User-Agent": "my-app"})  # свои заголовки
httpx.get(url, follow_redirects=True)  # переходить по 3xx (по умолчанию — нет)

with httpx.Client(base_url="https://api.example.com", timeout=10) as client:
    client.get("/users")  # одно соединение и общие настройки на много запросов
```

### Flask

**Flask** — фреймворк для веб-приложений. Разница между библиотекой и фреймворком:
библиотеку (httpx) вызывает ваш код, а фреймворк сам управляет программой
и вызывает ваши функции — когда приходит запрос на нужный адрес.

```python
from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route("/")  # декоратор связывает адрес с функцией
def index():
    return "<h1>Главная</h1>"


@app.route("/hello/<name>")  # часть адреса приходит аргументом
def hello(name):
    return f"<h1>Привет, {escape(name)}!</h1>"  # escape — защита от вставки HTML
```

Бывают параметры с типом: `<int:post_id>` (целое число), `<path:subpath>` (путь
со слешами). Запуск с автоперезагрузкой при изменении кода:
`uv run flask --app hello --debug run`. Декораторы мы встречали на
[семинаре 7](../seminar_07_special_methods/README.md#блок-3-декоратор-dataclass-10-мин).
Пример — [`examples/11_flask_app.py`](examples/11_flask_app.py).

---

## Итоги семинара

- Разобрались, как устроена сеть: IP-адрес, порт, сокет, TCP и UDP
- Написали TCP-сервер и клиент на модуле `socket` и научились передавать байты
- Обработали сетевые ошибки и защитили программы от зависания тайм-аутами
- Увидели, что HTTP — это текст поверх TCP, и написали веб-сервер на сокетах
- Делали HTTP-запросы с библиотекой `httpx` и разбирали ответы в JSON

**Дальше:** на семинаре 11 — качество кода: PEP 8, линтеры, тесты и аннотации
типов.

---

## Файлы семинара

| Файл | Описание |
|------|----------|
| [`README.md`](README.md) | Этот файл — основной материал семинара |
| [`examples/01_echo_server.py`](examples/01_echo_server.py) | Эхо-сервер на `create_server` |
| [`examples/02_echo_client.py`](examples/02_echo_client.py) | Клиент для эхо-сервера |
| [`examples/03_low_level_server.py`](examples/03_low_level_server.py) | Эхо-сервер по шагам: `socket`, `bind`, `listen`, `accept` |
| [`examples/04_network_errors.py`](examples/04_network_errors.py) | Сетевые ошибки и тайм-ауты |
| [`examples/05_http_server.py`](examples/05_http_server.py) | HTTP-сервер на сокетах |
| [`examples/06_raw_http_client.py`](examples/06_raw_http_client.py) | HTTP-запрос через сокет |
| [`examples/07_httpx_client.py`](examples/07_httpx_client.py) | Запросы с библиотекой httpx |
| [`examples/08_addresses.py`](examples/08_addresses.py) | DNS и модуль `ipaddress` |
| [`examples/09_select_server.py`](examples/09_select_server.py) | Несколько клиентов через `select` |
| [`examples/10_threading_server.py`](examples/10_threading_server.py) | Несколько клиентов через `socketserver` и потоки |
| [`examples/11_flask_app.py`](examples/11_flask_app.py) | Веб-приложение на Flask |
| [`exercises/networking_practice.md`](exercises/networking_practice.md) | Задания с подсказками и решениями |
| [`exercises/starter/`](exercises/starter/) | Заготовки файлов для задач |

---

## Дополнительные материалы

- [Документация: модуль `socket`](https://docs.python.org/3/library/socket.html)
- [Документация: Socket Programming HOWTO](https://docs.python.org/3/howto/sockets.html)
- [Документация: модуль `socketserver`](https://docs.python.org/3/library/socketserver.html)
- [Документация: модуль `select`](https://docs.python.org/3/library/select.html)
- [Документация: модуль `ipaddress`](https://docs.python.org/3/library/ipaddress.html)
- [MDN: обзор протокола HTTP](https://developer.mozilla.org/ru/docs/Web/HTTP/Overview)
- [MDN: коды ответа HTTP](https://developer.mozilla.org/ru/docs/Web/HTTP/Status)
- [Документация httpx](https://www.python-httpx.org/)
- [Документация Flask: Quickstart](https://flask.palletsprojects.com/en/stable/quickstart/)
