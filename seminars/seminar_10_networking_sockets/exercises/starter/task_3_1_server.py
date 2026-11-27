"""Задание 3.1. Свой веб-сервер.

Допишите функции make_response и route, чтобы сервер отвечал браузеру:

    http://127.0.0.1:8080/       → 200, главная страница со ссылкой на /time
    http://127.0.0.1:8080/time   → 200, страница с текущим временем
    http://127.0.0.1:8080/abc    → 404, «Страницы /abc нет»

Цикл приёма запросов уже написан. Запуск:
    python seminars/seminar_10_networking_sockets/exercises/starter/task_3_1_server.py

Откройте эти адреса в браузере. Обновите страницу /time — время должно меняться.
"""

import socket

HOST = "127.0.0.1"
PORT = 8080

REASONS = {200: "OK", 404: "Not Found"}


def make_response(status, body):
    """Собрать HTTP-ответ с кодом status и HTML-страницей body.

    Возвращает байты, готовые к отправке.
    """
    # TODO: соберите стартовую строку, заголовки Content-Type и Content-Length,
    #       пустую строку и тело; верните всё это байтами
    return b""


def route(path):
    """Вернуть пару (код ответа, HTML-страница) для пути path."""
    # TODO: «/» — главная страница со ссылкой на /time
    # TODO: «/time» — страница с текущим временем в формате ЧЧ:ММ:СС
    # TODO: любой другой путь — код 404 и текст «Страницы ... нет»
    return 404, ""


with socket.create_server((HOST, PORT)) as server:
    print(f"Откройте в браузере http://{HOST}:{PORT}/  Остановить — Ctrl+C")

    while True:
        conn, addr = server.accept()
        with conn:
            conn.settimeout(2)  # браузер иногда открывает соединение и молчит
            try:
                request = conn.recv(4096).decode("utf-8")
            except TimeoutError:
                continue
            if not request:
                continue

            first_line = request.split("\r\n")[0]  # например, GET /time HTTP/1.1
            parts = first_line.split()
            if len(parts) != 3:  # это не HTTP-запрос
                continue
            path = parts[1]

            status, body = route(path)
            conn.sendall(make_response(status, body))
            print(f"{first_line} → {status}")
