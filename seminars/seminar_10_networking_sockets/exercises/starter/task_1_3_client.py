"""Задание 1.3. Готовый клиент — его дописывать не нужно.

Клиент отправляет серверу строку за строкой и печатает ответы, пока вы
не введёте пустую строку. Пригодится в заданиях 1.3 и 2.3.

Запуск (сервер должен быть уже запущен):
    python seminars/seminar_10_networking_sockets/exercises/starter/task_1_3_client.py
"""

import socket

HOST = "127.0.0.1"
PORT = 8000

with socket.create_connection((HOST, PORT)) as sock:
    print("Подключились к серверу")
    while True:
        message = input("Запрос (Enter — выход): ").strip()
        if not message:
            break
        sock.sendall(message.encode("utf-8"))
        reply = sock.recv(1024).decode("utf-8")
        print("Ответ:", reply)

print("Соединение закрыто")
