"""Задание 3.3. Где обрабатывать ошибки.

Ниже — готовая библиотека с исключениями и консольное меню. Методы класса
Library ничего не печатают и не спрашивают — они только бросают исключения.

1. Добавьте в give_back() ошибку BookNotTakenError, если книга и так на полке.
2. Сделайте так, чтобы неизвестная команда не роняла программу.
3. Сделайте так, чтобы любая ошибка библиотеки печаталась, а меню продолжало
   работать.

Пример работы:
    Команда (взять/вернуть/список/выход): взять
    Название: Дюна
    Ваше имя: Аня
    Ошибка: Книга «Дюна» уже у читателя Петя
    Команда (взять/вернуть/список/выход): читать
    Неизвестная команда: читать
    Команда (взять/вернуть/список/выход): выход
"""


# =============================================================================
# Исключения
# =============================================================================
class LibraryError(Exception):
    """Базовая ошибка библиотеки."""


class BookNotFoundError(LibraryError):
    """Такой книги в библиотеке нет."""

    def __init__(self, title):
        super().__init__(f"Книги «{title}» нет в библиотеке")
        self.title = title


class BookAlreadyTakenError(LibraryError):
    """Книга уже выдана другому читателю."""

    def __init__(self, title, reader):
        super().__init__(f"Книга «{title}» уже у читателя {reader}")
        self.title = title
        self.reader = reader


# TODO: опишите исключение «книгу пытаются вернуть, хотя её никто не брал»
#       с сообщением «Книга «…» и так в библиотеке»


# =============================================================================
# Библиотека: только данные и правила, без print() и input()
# =============================================================================
class Library:
    def __init__(self):
        # название книги -> кто её взял (None — книга на полке)
        self.books = {
            "Мастер и Маргарита": None,
            "Война и мир": None,
            "Дюна": "Петя",
        }

    def take(self, title, reader):
        if title not in self.books:
            raise BookNotFoundError(title)
        if self.books[title] is not None:
            raise BookAlreadyTakenError(title, self.books[title])
        self.books[title] = reader

    def give_back(self, title):
        if title not in self.books:
            raise BookNotFoundError(title)
        # TODO: если книга и так на полке — сообщите об ошибке
        self.books[title] = None


# =============================================================================
# Команды меню: общаются с пользователем и вызывают методы библиотеки
# =============================================================================
def take_book(library):
    title = input("Название: ")
    reader = input("Ваше имя: ")
    library.take(title, reader)
    print(f"Книга «{title}» выдана")


def return_book(library):
    title = input("Название: ")
    library.give_back(title)
    print(f"Книга «{title}» возвращена")


def show_books(library):
    for title, reader in library.books.items():
        status = "на полке" if reader is None else f"у читателя {reader}"
        print(f"  «{title}» — {status}")


COMMANDS = {
    "взять": take_book,
    "вернуть": return_book,
    "список": show_books,
}


# =============================================================================
# Главный цикл
# =============================================================================
library = Library()

while True:
    command = input("Команда (взять/вернуть/список/выход): ").strip()
    if command == "выход":
        break

    # TODO: неизвестная команда не должна ронять программу —
    #       сообщите о ней и спросите снова
    action = COMMANDS[command]

    # TODO: любая ошибка библиотеки должна печататься, а меню — продолжать работу
    action(library)
