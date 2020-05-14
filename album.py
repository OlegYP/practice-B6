import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()

class Error(Exception):
    pass


class AlreadyExists(Error):
    pass


class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find(artist=None):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    if artist is not None:
        albums = session.query(Album).filter(Album.artist == artist).all()
    else:
        albums = session.query(Album).all()
    return albums


def save(year, artist, genre, album):
    assert (len(str(artist)) > 1), "Что-то не так с названием артиста"
    assert (len(str(genre)) > 1), "Жанр указан неправильно"
    assert (len(str(album)) > 1),   "Проверьте название альбома"

    session = connect_db()
    saved_album = session.query(Album).filter(Album.album == album, Album.artist == artist).first()
    if saved_album is not None:
        raise AlreadyExists("Album already exists and has #{}".format(saved_album.id))

    album = Album(
        year=year,
        artist=artist,
        genre=genre,
        album=album
    )
    session.add(album)
    session.commit()
    return album