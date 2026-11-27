"""Сетевые ошибки и тайм-ауты.

Все примеры работают без интернета: нужные ситуации программа создаёт сама.
Перед запуском остановите другие серверы на порту 8000.

Запуск:
    python seminars/seminar_10_networking_sockets/examples/04_network_errors.py
"""

import socket

HOST = "127.0.0.1"
PORT = 8000

# =============================================================================
# Все ошибки сети — наследники OSError
# =============================================================================
# Иерархию исключений разбирали на семинаре 8.
print(issubclass(socket.gaierror, OSError))  # True
print(issubclass(ConnectionRefusedError, OSError))  # True
print(issubclass(TimeoutError, OSError))  # True
print(socket.timeout is TimeoutError)  # True: в Python 3.10+ это одно и то же


# =============================================================================
# Одна функция — разные ошибки
# =============================================================================
def ask(host, port, message, timeout):
    """Отправить сообщение серверу и вернуть ответ или описание ошибки."""
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            sock.sendall(message.encode("utf-8"))
            return sock.recv(1024).decode("utf-8")
    # Порядок важен: частные случаи — раньше общего OSError.
    except socket.gaierror:
        return "адрес не найден: такого имени нет"
    except TimeoutError:
        return f"сервер не ответил за {timeout} с"
    except ConnectionRefusedError:
        return "соединение отклонено: на этом порту никто не слушает"
    except OSError as error:
        return f"другая сетевая ошибка: {error}"


# 1. Имя, которое нельзя найти (домен .invalid зарезервирован и не существует)
print(ask("no-such-host.invalid", 80, "привет", timeout=2))

# 2. Порт, на котором никто не слушает
print(ask(HOST, PORT, "привет", timeout=2))

# 3. Сервер, который принимает подключения, но ничего не отвечает.
#    Без тайм-аута recv() ждал бы ответа вечно.
with socket.create_server((HOST, PORT)) as silent_server:
    # accept() мы не вызываем, но ОС всё равно примет подключение в очередь,
    # так что клиент подключится — и будет ждать ответа.
    print(ask(HOST, PORT, "привет", timeout=1))

    # 4. Порт уже занят: второй сервер на тот же адрес не запустится
    try:
        socket.create_server((HOST, PORT)).close()
    except OSError as error:
        # На macOS errno = 48, на Linux — 98, на Windows — 10048
        print("Не удалось запустить второй сервер:", error.strerror)


# =============================================================================
# settimeout — тайм-аут для уже созданного сокета
# =============================================================================
# По умолчанию тайм-аута нет: accept() и recv() ждут сколько угодно.
with socket.create_server((HOST, PORT)) as server:
    server.settimeout(0.5)  # ждать подключения не дольше 0.5 с
    try:
        server.accept()
    except TimeoutError:
        print("За 0.5 с никто не подключился")


# =============================================================================
# Обращение к закрытому сокету
# =============================================================================
sock = socket.socket()
sock.close()
try:
    sock.connect((HOST, PORT))
except OSError as error:
    print("Сокет уже закрыт:", error)  # Bad file descriptor
