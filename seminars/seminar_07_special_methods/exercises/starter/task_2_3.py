"""Задание 2.3. Плейлист как последовательность.

Дополните класс Playlist так, чтобы к песням можно было обращаться
по индексу и перебирать их циклом:

    playlist[0]      -> первая песня
    playlist[-1]     -> последняя песня
    for song in playlist: ...

Менять метод добавления и список внутри класса не нужно.
"""


class Song:
    def __init__(self, title, artist, seconds):
        self.title = title
        self.artist = artist
        self.seconds = seconds

    def __repr__(self):
        return f"Song({self.title!r}, {self.artist!r}, {self.seconds})"


class Playlist:
    def __init__(self, title):
        self.title = title
        self.songs = []

    def add(self, song):
        self.songs.append(song)

    def __len__(self):
        return len(self.songs)


# TODO: добавьте в Playlist метод, который позволит обращаться по индексу


# TODO: создайте плейлист из трёх песен

# TODO: выведите первую и последнюю песню и переберите плейлист циклом for
