from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request


import album

@route('/')
def index():
    return '''
        <h2> Домашнее задание по модулю B6 </h2>
        <br>
        <h4> Пункт 1. GET запросы. </h4>
        <p><a href="/artists/"> Посмотреть список артистов в базе в целях демонстрации метода GET</a></p>
        <br>
        <h4> Пункт 2. POST запросы. </h4>
        <p> Для создания Post запроса можно заполнить форму ниже </p>
        <span>-------------------------------------------------------------</span>
        <form action="/albums/" method="POST">
            <br><br>
            Введите название артиста: <input name="artist" type="text" />
            <br><br>
            Введите название альбома: <input name="album" type="text" />
            <br><br>
            Укажите жанр : <input name="genre" type="text" />
            <br><br>
            Укажите год создания : <input name="year" type="text" />
            <br><br>
         
            <input value="Добавить" type="submit" />
        </form>
        <span>-------------------------------------------------------------</span>
        '''

@route("/albums/<artist>", method="GET")
def albums(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = "Артист - {}. Количество альбомов - {}<br>".format(artist, len(albums_list))
        result += "<br>Список его альбомов :<br>"
        result += "<br>".join(album_names)
    return result

@route("/artists/", method="GET")
def artists():
    albums_list = album.find()
    if not albums_list:
        message = "Ничего не найдено"
        result = HTTPError(404, message)
    else:
        artist_names = [album.artist for album in albums_list]
        artist_names = list(set(artist_names))
        result = "Количество артистов в базе  - {}<br>".format(len(artist_names))
        result += "<br><br>Ссылки кликабельны. Будет сформирован GET запрос вида /albums/&#60artist&#62: <br><br>"
        for artist in artist_names:
           result += "<p><a href = '/albums/{}'>{}</a></p>".format(artist,artist)
    return result

@route("/albums/", method="POST")
def create_album():
    year = request.forms.get("year")
    artist = request.forms.get("artist")
    genre = request.forms.get("genre")
    album_name = request.forms.get("album")

    try:
        year = int(year)
    except ValueError:
        return HTTPError(400, "Указан некорректный год альбома")
    if (int(year) < 1900) or (int(year) > 2020):
        return HTTPError(400, "Указан некорректный год альбома")

    try:
        new_album = album.save(year, artist, genre, album_name)
    except AssertionError as err:
        result = HTTPError(400, str(err))
    except album.AlreadyExists as err:
        result = HTTPError(409, str(err))
    else:
        # print("New #{} album successfully saved".format(new_album.id))
        result = "Альбом #{} успешно сохранен".format(new_album.id)
    return result

if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)
