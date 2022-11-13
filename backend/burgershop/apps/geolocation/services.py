import requests

from django.conf import settings
from .models import PlaceLocation


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']
    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def get_places_coordinats(addresses: list):
    '''
    Принимает список адресов, возвращает словарь
    в формате: адрес: координаты
    '''

    saved_locations = PlaceLocation.objects.filter(address__in=addresses)
    saved_addresses = [location.address for location in saved_locations]
    serialized_coordinats = {}
    for address in addresses:
        if address in saved_addresses:
            continue

        coordinats = fetch_coordinates(settings.YANDEX_API_TOKEN, address)
        place = PlaceLocation(address=address)
        if coordinats:
            place.latitude, place.longitude = map(float, coordinats)

        serialized_coordinats[address] = coordinats

    for place in saved_locations:
        if place.address not in serialized_coordinats and \
           all((place.latitude, place.longitude)):
            serialized_coordinats[place.address] = (
                str(place.latitude),                
                str(place.longitude)
            )

    return serialized_coordinats