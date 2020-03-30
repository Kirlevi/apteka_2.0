from business import find_business
from geocoder import get_coordinates
from distance import lonlat_distance
from mapapi import show_map

import sys


def main():
    toponym_to_find = " ".join(sys.argv[1:])

    lat, lon = get_coordinates(toponym_to_find)
    address_ll = "{0},{1}".format(lat, lon)
    span = "0.005,0.005"

    # Получаем координаты ближайшей аптеки.
    organization = find_business(address_ll, span, "аптека")
    point = organization["geometry"]["coordinates"]
    org_lat = float(point[0])
    org_lon = float(point[1])
    point_param = "pt={0},{1},pm2dgl".format(org_lat, org_lon)

    show_map("ll={0}&spn={1}".format(address_ll, span), "map", add_params=point_param)

    # Добавляем на карту точку с исходным адресом.
    points_param = point_param + "~{0},pm2rdl".format(address_ll)

    show_map("ll={0}&spn={1}".format(address_ll, span), "map", add_params=points_param)

    # Автопозиционирование
    show_map(map_type="map", add_params=points_param)

    # Сниппет
    # Название организации.
    name = organization["properties"]["CompanyMetaData"]["name"]
    # Адрес организации.
    address = organization["properties"]["CompanyMetaData"]["address"]
    # Время работы
    time = organization["properties"]["CompanyMetaData"]["Hours"]["text"]
    # Расстояние
    distance = round(lonlat_distance((lon, lat), (org_lon, org_lat)))

    snippet = u"Название:\t{name}\nАдрес:\t{address}\nВремя работы:\t{time}\nРасстояние:\t{distance}м.".format(
        **locals())
    print(snippet)


if __name__ == "__main__":
    main()