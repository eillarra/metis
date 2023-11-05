import os

import requests


class MapboxFeature:
    def __init__(self, feature: dict):
        self._raw = feature

    def __str__(self) -> str:
        return self._raw["place_name"]

    def __get_context(self, q: str, *, field: str | None = None):
        for context in self._raw["context"]:
            if q in context["id"]:
                return context[field] if field else context
        return None

    @property
    def address(self) -> str:
        return self._raw["place_name"].split(",")[0]

    @property
    def full_address(self) -> str:
        return self._raw["place_name"]

    @property
    def city(self) -> str | None:
        return self.__get_context("place", field="text")

    @property
    def postcode(self) -> str | None:
        return self.__get_context("postcode", field="text")

    @property
    def region(self) -> dict | None:
        return self.__get_context("region")

    @property
    def country(self) -> dict | None:
        return self.__get_context("country")

    @property
    def coordinates(self) -> list:
        return self._raw["geometry"]["coordinates"]

    @property
    def latitude(self) -> float:
        return self.coordinates[1]

    @property
    def longitude(self) -> float:
        return self.coordinates[0]

    def to_dict(self) -> dict:
        return self._raw


class Mapbox:
    access_token = os.environ.get("MAPBOX_TOKEN")
    api_endpoint = "https://api.mapbox.com"
    api_version = "v5"

    def __enter__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()

    def geocode(self, address: str) -> MapboxFeature | None:
        try:
            url = f"{self.api_endpoint}/geocoding/{self.api_version}/mapbox.places/{address}.json"
            params = {
                "access_token": self.access_token,
                "country": "be",
                "types": "address",
                "limit": 1,
                "language": "nl,en",
            }
            response = self.session.get(url, params=params)
            response.raise_for_status()

            if response.status_code == 404:
                return None

            data = response.json()
        except requests.exceptions.HTTPError as exc:
            raise Exception(f"Mapbox API error: {exc}") from exc

        if not data["features"]:
            return None

        return MapboxFeature(response.json()["features"][0])
