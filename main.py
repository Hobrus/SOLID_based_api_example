import requests
from abc import ABC, abstractmethod


class GeoLocatorInterface(ABC):

    @abstractmethod
    def get_coordinates(self, address: str) -> tuple:
        pass


class YandexGeoLocator(GeoLocatorInterface):

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = f"https://geocode-maps.yandex.ru/1.x/?apikey={api_key}&format=json"

    def get_coordinates(self, address: str) -> tuple:
        call_url = f"{self.base_url}&geocode={address}"
        response = requests.get(call_url)
        json_response = response.json()
        lat_lon = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point'][
            'pos'].split(' ')
        return lat_lon[1], lat_lon[0]


class LocationService:

    def __init__(self, geo_locator: GeoLocatorInterface):
        self.geo_locator = geo_locator

    def get_location(self, address: str) -> tuple:
        return self.geo_locator.get_coordinates(address)


api_key = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
locator = YandexGeoLocator(api_key)
service = LocationService(locator)
print(service.get_location("Москва, ул. Ак. Королева, 12"))
