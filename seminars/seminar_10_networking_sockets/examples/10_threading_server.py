"""Эхо-сервер на socketserver: каждый клиент — в отдельном потоке.

Тема для самостоятельного изучения.

Запуск:
    python seminars/seminar_10_networking_sockets/examples/10_threading_server.py

Подключите несколько клиентов 02_echo_client.py одновременно.
"""

import socketserver

HOST = "127.0.0.1"
PORT = 8000


# Модуль socketserver берёт на себя bind, listen, accept и закрытие сокетов.
# Нам остаётся унаследоваться от BaseRequestHandler (наследование — семинар 6)
# и переопределить метод handle(): он вызывается для каждого клиента.
class EchoHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # self.request — сокет этого клиента, self.client_address — его адрес
        print(f"Подключился {self.client_address}")
        while True:
            data = self.request.recv(1024)
            if not data:
                break
            text = data.decode("utf-8")
            self.request.sendall(text.upper().encode("utf-8"))
        print(f"Отключился {self.client_address}")


# ThreadingMixIn запускает handle() каждого клиента в отдельном потоке,
# поэтому клиенты не ждут друг друга. MixIn должен стоять ПЕРВЫМ в списке
# родителей. В модуле есть и готовый класс socketserver.ThreadingTCPServer.
class ThreadingEchoServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True  # потоки клиентов не мешают остановить сервер
    allow_reuse_address = True  # сразу занять порт после перезапуска


with ThreadingEchoServer((HOST, PORT), EchoHandler) as server:
    print(f"Сервер слушает {HOST}:{PORT}. Остановить — Ctrl+C")
    server.serve_forever()  # бесконечный цикл приёма клиентов
