"""Имена и адреса: DNS и модуль ipaddress.

Тема для самостоятельного изучения. Для getaddrinfo нужен интернет.

Запуск:
    python seminars/seminar_10_networking_sockets/examples/08_addresses.py
"""

import ipaddress
import socket

# =============================================================================
# getaddrinfo — найти адреса по имени (запрос к DNS)
# =============================================================================
# Возвращает список кортежей (family, type, proto, canonname, sockaddr).
# Нас интересуют семейство адресов и сам адрес — первый элемент sockaddr.
for family, _, _, _, sockaddr in socket.getaddrinfo(
    "python.org", 443, proto=socket.IPPROTO_TCP
):
    print(family.name, sockaddr[0])  # AF_INET — IPv4, AF_INET6 — IPv6

# Короче, если нужен один IPv4-адрес:
print(socket.gethostbyname("python.org"))

# Имя нашего компьютера
print(socket.gethostname())

# Стандартные порты известных протоколов
print(socket.getservbyname("http"), socket.getservbyname("https"))  # 80 443


# =============================================================================
# ipaddress — разбор и проверка адресов
# =============================================================================
for text in ["127.0.0.1", "192.168.1.10", "10.0.0.5", "8.8.8.8", "::1"]:
    address = ipaddress.ip_address(text)
    print(
        f"{text:>14}  IPv{address.version}  "
        f"не из Интернета: {address.is_private!s:5}  "
        f"этот компьютер: {address.is_loopback}"
    )

# IPv6: ведущие нули опускаются, группа нулей заменяется на ::
long_ipv6 = ipaddress.ip_address("2001:0db8:0000:0000:0000:0000:0000:0001")
print(long_ipv6)  # 2001:db8::1
print(long_ipv6.exploded)  # обратно в полную запись

# Сеть 192.168.0.0/16: первые 16 бит адреса общие для всей сети
home_network = ipaddress.ip_network("192.168.0.0/16")
print(home_network.num_addresses)  # 65536
print(ipaddress.ip_address("192.168.5.7") in home_network)  # True

# Ошибка в адресе — ValueError
try:
    ipaddress.ip_address("256.1.1.1")
except ValueError as error:
    print(error)
