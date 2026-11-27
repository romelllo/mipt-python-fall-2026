"""Минимальное веб-приложение на Flask.

Тема для самостоятельного изучения. Flask уже записан в зависимости репозитория
курса, запускайте через uv (из корня репозитория):
    uv run python seminars/seminar_10_networking_sockets/examples/11_flask_app.py

Откройте в браузере:
    http://127.0.0.1:5001/
    http://127.0.0.1:5001/hello/Аня
    http://127.0.0.1:5001/square/12
"""

from flask import Flask
from markupsafe import escape

# Flask — фреймворк: он сам принимает соединения, разбирает HTTP-запросы
# и собирает ответы. Мы пишем только функции, которые возвращают страницы.
app = Flask(__name__)


# Декоратор route связывает адрес с функцией: на запрос «/» Flask вызовет index()
@app.route("/")
def index():
    return "<h1>Главная</h1><p>Привет от Flask!</p>"


# <name> — часть адреса, которая придёт в функцию аргументом
@app.route("/hello/<name>")
def hello(name):
    # escape: имя пришло от пользователя и может содержать HTML-код
    return f"<h1>Привет, {escape(name)}!</h1>"


# <int:number> — Flask сам проверит, что это целое, и преобразует его.
# Для /square/abc Flask ответит 404, а функция даже не будет вызвана.
@app.route("/square/<int:number>")
def square(number):
    return f"{number}² = {number**2}"


if __name__ == "__main__":
    # debug=True: сервер перезапускается сам при изменении кода и показывает
    # подробности ошибок в браузере. Только для разработки!
    # Порт 5001, а не стандартный для Flask 5000: на macOS порт 5000 занят
    # системной службой AirPlay.
    app.run(port=5001, debug=True)
