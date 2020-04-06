import requests


def find_businesses(ll, spn, request, lang='ru-RU'):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
    search_params = {
        "apikey": api_key,
        "text": request,
        "lang": lang,
        "ll": ll,
        "spn": spn,
        "type": "biz"
    }

    response = requests.get(search_api_server, params=search_params)
    if not response:
        raise RuntimeError(
            """Ошибка выполнения запроса:
            {request}
            Http статус: {status} ({reason})""".format(
            request=search_api_server, status=response.status_code, reason=response.reason))

    json_response = response.json()

    orgs = json_response["features"]
    return orgs


def find_bisiness(ll, spn, request, lang='ru-RU'):
    orgs = find_businesses(ll, spn, request, lang='ru-RU')
    if len(orgs):
        return orgs[0] # Ближайшая организация