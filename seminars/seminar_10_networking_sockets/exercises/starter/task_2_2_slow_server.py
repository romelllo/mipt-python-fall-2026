"""Задание 2.2. Медленный сервер — готов, его дописывать не нужно.

Сервер отвечает на сообщение заглавными буквами, но перед ответом «думает»
случайное время — от 0 до 4 секунд.

Запуск (в отдельном окне терминала):
    python seminars/seminar_10_networking_sockets/exercises/starter/task_2_2_slow_server.py
"""

import random
import socket
import time

HOST = "127.0.0.1"
PORT = 8000

with socket.create_server((HOST, PORT)) as server:
    print(f"Медленный сервер слушает {HOST}:{PORT}. Остановить — Ctrl+C")

    while True:
        conn, addr = server.accept()
        with conn:
            data = conn.recv(1024)
            if not data:
                continue
            delay = random.randint(0, 4)
            print(f"{addr}: думаю {delay} с...")
            time.sleep(delay)
            try:
                conn.sendall(data.decode("utf-8").upper().encode("utf-8"))
                print(f"{addr}: ответ отправлен")
            except ConnectionError:
                # Клиент не дождался ответа и уже закрыл соединение.
                # Сервер не должен из-за этого падать — ждём следующего.
                print(f"{addr}: клиент уже ушёл")
