"""Эхо-сервер для нескольких клиентов одновременно — через select.

Тема для самостоятельного изучения.

Запуск:
    python seminars/seminar_10_networking_sockets/examples/09_select_server.py

Подключите два клиента 02_echo_client.py (или клиента из задания 1.3) в двух
окнах терминала: сервер отвечает обоим, не дожидаясь, пока первый уйдёт.
"""

import select
import socket

HOST = "127.0.0.1"
PORT = 8000

with socket.create_server((HOST, PORT)) as server:
    print(f"Сервер слушает {HOST}:{PORT}. Остановить — Ctrl+C")

    # Список сокетов, за которыми следим: сначала только серверный
    monitoring = [server]

    while True:
        # select ждёт, пока хотя бы один сокет из списка не станет «готов»:
        # у серверного — появился новый клиент, у клиентского — пришли данные.
        # Возвращает три списка: готовые к чтению, к записи, с ошибками.
        ready, _, _ = select.select(monitoring, [], [])

        for sock in ready:
            if sock is server:
                # Новый клиент: accept() не заблокируется — клиент уже ждёт
                conn, addr = server.accept()
                monitoring.append(conn)
                print("Подключился", addr, "— всего клиентов:", len(monitoring) - 1)
            else:
                # Данные от клиента: recv() не заблокируется — данные уже пришли
                data = sock.recv(1024)
                if data:
                    text = data.decode("utf-8")
                    sock.sendall(text.upper().encode("utf-8"))
                else:
                    # Пустые байты — клиент отключился
                    print("Отключился", sock.getpeername())
                    monitoring.remove(sock)
                    sock.close()
