"""Тот же эхо-сервер, но без create_server: все шаги по отдельности.

Так сервер записан в лекции. Модуль socket почти дословно повторяет системные
вызовы операционной системы: socket → bind → listen → accept → recv/send → close.

Запуск:
    python seminars/seminar_10_networking_sockets/examples/03_low_level_server.py

Проверить можно тем же клиентом 02_echo_client.py.
"""

import socket

HOST = "127.0.0.1"
PORT = 8000

# 1. socket() — создать сокет. По умолчанию AF_INET (адреса IPv4)
#    и SOCK_STREAM (протокол TCP), то есть то же, что socket.socket().
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Разрешить сразу занять порт после перезапуска сервера. Без этой строки
# после остановки сервера порт может ещё с минуту оставаться «занятым».
# В лекции используется SO_REUSEPORT, но его нет на Windows;
# SO_REUSEADDR есть везде. create_server делает это сам.
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    server.bind((HOST, PORT))  # 2. bind() — занять адрес и порт
    server.listen()  # 3. listen() — начать принимать подключения
    print(f"Сервер слушает {HOST}:{PORT}. Остановить — Ctrl+C")

    while True:
        conn, addr = server.accept()  # 4. accept() — дождаться клиента
        print("Подключился клиент", addr)
        try:
            while True:
                data = conn.recv(1024)  # 5. recv() — получить байты
                if not data:
                    break
                # send() может отправить только часть данных и возвращает,
                # сколько байт ушло. sendall() повторяет send(), пока не
                # отправит всё, — поэтому почти всегда используют его.
                reply = data.decode("utf-8").upper().encode("utf-8")
                conn.sendall(reply)  # 6. sendall() — отправить ответ
        finally:
            conn.close()  # 7. close() — закрыть сокет клиента
        print("Клиент отключился", addr)
finally:
    server.close()  # и серверный сокет — даже после Ctrl+C
