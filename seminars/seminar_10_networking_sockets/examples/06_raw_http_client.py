"""HTTP-запрос «вручную»: обычный текст, отправленный через сокет.

Нужен интернет.

Запуск:
    python seminars/seminar_10_networking_sockets/examples/06_raw_http_client.py
"""

import socket

HOST = "example.com"
PORT = 80  # 80 — стандартный порт HTTP, 443 — HTTPS

# Стартовая строка, заголовки, пустая строка. Каждая строка кончается \r\n.
# Host обязателен: на одном сервере (одном IP-адресе) может жить много сайтов.
request = (
    "GET / HTTP/1.1\r\n"
    f"Host: {HOST}\r\n"
    "Connection: close\r\n"  # попросить сервер закрыть соединение после ответа
    "\r\n"
)

with socket.create_connection((HOST, PORT), timeout=5) as sock:
    sock.sendall(request.encode("ascii"))

    # Ответ может не поместиться в один recv: читаем, пока сервер
    # не закроет соединение (recv вернёт пустые байты).
    response = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        response += chunk

text = response.decode("utf-8", errors="replace")
head, _, body = text.partition("\r\n\r\n")  # заголовки отделены пустой строкой

print("=== Стартовая строка и заголовки ===")
print(head)
print()
print("=== Начало тела ===")
print(body[:300])

# Сервер может прислать тело частями (заголовок Transfer-Encoding: chunked) —
# тогда перед каждой частью стоит её длина в шестнадцатеричном виде. Разбирать
# такие подробности вручную — работа для библиотек вроде httpx (файл 07).
