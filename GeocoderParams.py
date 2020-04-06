import requests

def address_to_geocode(address):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": address,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if response:
        json_response = response.json()
        # Получаем первый топоним из ответа геокодера.
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        return toponym


def get_coordinates(address):
    toponym = address_to_geocode(address)
    if not toponym:
        pass
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    return float(toponym_longitude), float(toponym_lattitude)


def get_scale(address):
    toponym = address_to_geocode(address)
    left, bot = toponym['boundedBy']['Envelope']['lowerCorner'].split(" ")
    right, top = toponym['boundedBy']['Envelope']['upperCorner'].split(" ")
    # формулы для перевода в градусную меру
    dx = str(abs(float(left) - float(right)) / 2.0)
    dy = str(abs(float(top) - float(bot)) / 2.0)
    return [dx, dy]