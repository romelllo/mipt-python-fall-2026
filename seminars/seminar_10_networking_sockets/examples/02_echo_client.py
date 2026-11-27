"""Клиент для эхо-сервера.

Сначала запустите сервер 01_echo_server.py в отдельном окне терминала, затем:
    python seminars/seminar_10_networking_sockets/examples/02_echo_client.py
"""

import socket

HOST = "127.0.0.1"
PORT = 8000

# create_connection создаёт TCP-сокет и подключается к серверу.
# Клиенту свой порт выбирать не нужно — ОС назначит свободный сама.
with socket.create_connection((HOST, PORT)) as sock:
    print("Подключились к серверу, наш адрес:", sock.getsockname())

    for message in ["привет", "как дела?", "пока"]:
        sock.sendall(message.encode("utf-8"))  # отправить все байты сообщения
        reply = sock.recv(1024)  # ждём ответ
        print(f"{message!r} → {reply.decode('utf-8')!r}")

# Здесь сокет уже закрыт: сервер получит b"" и поймёт, что мы ушли.
print("Соединение закрыто")
