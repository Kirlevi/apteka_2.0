import sys
import math
from io import BytesIO
import requests
from PIL import Image
import GeocoderParams
import OrgSearch


def distance(a, b):
    degree_to_meters_factor = 111 * 1000  # 111 километров в метрах
    a_lon, a_lat = a
    b_lon, b_lat = b

    # Берем среднюю по широте точку и считаем коэффициент для нее.
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    # Вычисляем смещения в метрах по вертикали и горизонтали.
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    # Вычисляем расстояние между точками.
    distance = math.sqrt(dx * dx + dy * dy)

    return distance


# program1.py Москва, ул. Ак. Королева, 12

toponym_to_find = " ".join(sys.argv[1:])

toponym = GeocoderParams.address_to_geocode(toponym_to_find)

lat, lon = GeocoderParams.get_coordinates(toponym_to_find)
coord = f'{lat},{lon}'
span = '0.005,0.005'

org = OrgSearch.find_bisiness(coord, span, 'аптека')

# для метки на карте и подсчета расстояния
org_lat, org_lon = org['geometry']['coordinates']

# расстояние между точками
distance = distance([lat, lon], [org_lat, org_lon])

snippet = {'address': org['properties']['CompanyMetaData']['address'],
           'name': org['properties']['CompanyMetaData']['name'],
           'hours': org['properties']['CompanyMetaData']['Hours']['text']}
for key,val in snippet.items():
    print(f'{key}: {val}')
print(f'{int(distance)} метров')

map_params = {
    "ll": ",".join([str(lat), str(lon)]),
    "pt": ",".join([str(lat), str(lon), 'org']) + '~' + ",".join([str(org_lat), str(org_lon), 'org']),
    "l": "map"
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response.content)).show()