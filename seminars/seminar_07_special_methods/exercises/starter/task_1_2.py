"""Задание 1.2. Сравнение песен по содержимому.

Сейчас две песни с одинаковыми данными не равны:

    Song("Yesterday", "The Beatles", 125) == Song("Yesterday", "The Beatles", 125)
    False

Сделайте так, чтобы песни считались равными, если совпадают название
и исполнитель (длительность не важна — это может быть другая запись).

Сравнение песни с объектом другого типа не должно приводить к ошибке.
"""


class Song:
    def __init__(self, title, artist, seconds):
        self.title = title
        self.artist = artist
        self.seconds = seconds

    def __repr__(self):
        return f"Song({self.title!r}, {self.artist!r}, {self.seconds})"


# TODO: добавьте в класс метод сравнения на равенство


# TODO: проверьте три случая:
#       одинаковые песни с разной длительностью -> True
#       разные песни                            -> False
#       песня и строка                          -> False
