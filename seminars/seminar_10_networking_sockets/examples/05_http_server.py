"""Простой HTTP-сервер на сокетах — без библиотек.

Запуск:
    python seminars/seminar_10_networking_sockets/examples/05_http_server.py

Откройте в браузере:
    http://127.0.0.1:8080/         → 200 OK
    http://127.0.0.1:8080/admin    → 403 Forbidden
    http://127.0.0.1:8080/abc      → 404 Not Found

В терминале сервера будет видно, какие запросы присылает браузер.
"""

import socket
from html import escape

HOST = "127.0.0.1"
PORT = 8080

# Код ответа → его текстовое описание (reason phrase)
REASONS = {
    200: "OK",
    400: "Bad Request",
    403: "Forbidden",
    404: "Not Found",
}


def make_response(status, body):
    """Собрать HTTP-ответ: стартовая строка, заголовки, пустая строка, тело."""
    body_bytes = body.encode("utf-8")
    head = (
        f"HTTP/1.1 {status} {REASONS[status]}\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        # Длина тела — в БАЙТАХ, а не в символах: «Привет» — 6 символов, 12 байт
        f"Content-Length: {len(body_bytes)}\r\n"
        "Connection: close\r\n"  # после ответа закроем соединение
        "\r\n"  # пустая строка отделяет заголовки от тела
    )
    return head.encode("utf-8") + body_bytes


def route(path):
    """Выбрать код ответа и страницу по пути из запроса."""
    if path == "/":
        return 200, "<h1>Главная</h1><p>Привет от сервера на сокетах!</p>"
    if path == "/admin":
        return 403, "<h1>403</h1><p>Сюда нельзя</p>"
    # escape() заменяет < и > на безопасные &lt; и &gt;: иначе в адрес можно
    # подставить HTML-код, и браузер выполнит его как часть нашей страницы
    return 404, f"<h1>404</h1><p>Страницы {escape(path)} нет</p>"


with socket.create_server((HOST, PORT)) as server:
    print(f"Откройте в браузере http://{HOST}:{PORT}/  Остановить — Ctrl+C")

    while True:
        conn, addr = server.accept()
        with conn:
            # Браузер иногда открывает соединение «про запас» и ничего в него
            # не пишет. Без тайм-аута наш сервер ждал бы его вечно.
            conn.settimeout(2)
            try:
                request = conn.recv(4096).decode("utf-8")
            except TimeoutError:
                continue
            if not request:  # клиент подключился и сразу ушёл
                continue

            # Запрос — это текст. Первая строка: «GET /admin HTTP/1.1»,
            # дальше заголовки «Имя: значение», каждая строка кончается \r\n
            print(request)
            first_line = request.split("\r\n")[0]
            try:
                method, path, version = first_line.split()
            except ValueError:  # в первой строке не три слова — это не HTTP
                conn.sendall(make_response(400, "<h1>400</h1>"))
                continue

            status, body = route(path)
            conn.sendall(make_response(status, body))
            print(f"→ {status} {REASONS[status]}\n")
