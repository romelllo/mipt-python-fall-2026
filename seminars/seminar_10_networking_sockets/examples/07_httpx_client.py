"""HTTP-запросы с библиотекой httpx.

httpx — внешняя библиотека. В репозитории курса она уже записана в зависимости,
поэтому запускайте пример через uv (из корня репозитория):
    uv run python seminars/seminar_10_networking_sockets/examples/07_httpx_client.py

Для части 1 запустите в другом окне сервер 05_http_server.py.
Для части 2 нужен интернет.
"""

import httpx

# =============================================================================
# 1. Запрос к своему серверу
# =============================================================================
try:
    response = httpx.get("http://127.0.0.1:8080/admin")
    print(response.status_code)  # 403
    print(response.headers["Content-Type"])  # text/html; charset=utf-8
    print(response.text)  # тело ответа — уже строка
except httpx.ConnectError:
    print("Сервер не запущен: сначала запустите 05_http_server.py")


# =============================================================================
# 2. Публичный API: погода в Долгопрудном (сервис Open-Meteo, ключ не нужен)
# =============================================================================
URL = "https://api.open-meteo.com/v1/forecast"

# Параметры запроса передаём словарём — httpx сам соберёт из них адрес
# вида ...?latitude=55.94&longitude=37.52&current=temperature_2m
params = {
    "latitude": 55.94,
    "longitude": 37.52,
    "current": "temperature_2m,wind_speed_10m",
}

response = httpx.get(URL, params=params, timeout=10)  # тайм-аут по умолчанию — 5 с
print(response.url)  # итоговый адрес с параметрами
print(response.status_code)  # 200

data = response.json()  # тело в формате JSON → словарь
current = data["current"]
print(f"Сейчас {current['temperature_2m']} °C, ветер {current['wind_speed_10m']} км/ч")


# =============================================================================
# 3. Коды ошибок: raise_for_status
# =============================================================================
# Ответ 4xx или 5xx — это НЕ исключение: httpx просто вернёт ответ с таким кодом.
response = httpx.get(URL, params={"latitude": 999, "longitude": 0}, timeout=10)
print(response.status_code)  # 400 — широта вне диапазона
print(response.json()["reason"])  # сервис объясняет, что не так

# Чтобы ошибочный код превратился в исключение, вызывают raise_for_status():
try:
    response.raise_for_status()
except httpx.HTTPStatusError as error:
    print("Ошибка HTTP:", error.response.status_code)


# =============================================================================
# 4. Сетевые ошибки
# =============================================================================
# Иерархия исключений httpx (как у socket — от частного к общему):
#   httpx.HTTPError
#   ├── httpx.HTTPStatusError      ← ответ пришёл, но код 4xx/5xx
#   └── httpx.RequestError         ← ответа нет вообще
#       ├── httpx.ConnectError     ← не удалось подключиться
#       └── httpx.TimeoutException ← истёк тайм-аут
try:
    httpx.get("http://no-such-host.invalid/")
except httpx.ConnectError as error:
    print("Не удалось подключиться:", error)
