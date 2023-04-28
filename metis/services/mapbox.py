import os
import requests

from typing import Optional


class MapboxFeature:
    """
    {'id': 'address.3426848510991968', 'type': 'Feature', 'place_type': ['address'], 'relevance': 1, 'properties': {'accuracy': 'rooftop', 'mapbox_id': 'dXJuOm1ieGFkcjpjZjVhZGNjMS1kNDk3LTQ5ZTEtYjdiYi1jYzU4MjdkOTkyNzk'}, 'text_nl': 'Corneel Heymanslaan', 'place_name_nl': 'Corneel Heymanslaan 10, 9000 Gent, Oost-Vlaanderen, België', 'text': 'Corneel Heymanslaan', 'place_name': 'Corneel Heymanslaan 10, 9000 Gent, Oost-Vlaanderen, België', 'text_en': 'Corneel Heymanslaan', 'place_name_en': 'Corneel Heymanslaan 10, 9000 Ghent, East Flanders, Belgium', 'center': [3.727112, 51.02532], 'geometry': {'type': 'Point', 'coordinates': [3.727112, 51.02532]}, 'address': '10', 'context': [{'id': 'postcode.8474133', 'mapbox_id': 'dXJuOm1ieHBsYzpnVTRW', 'text_nl': '9000', 'text': '9000', 'text_en': '9000'}, {'id': 'locality.4876821', 'mapbox_id': 'dXJuOm1ieHBsYzpTbW9W', 'text_nl': 'Gent Zuid', 'text': 'Gent Zuid', 'text_en': 'Gent Zuid'}, {'id': 'place.1558549', 'wikidata': 'Q1296', 'mapbox_id': 'dXJuOm1ieHBsYzpGOGdW', 'text_nl': 'Gent', 'language_nl': 'nl', 'text': 'Gent', 'language': 'nl', 'text_en': 'Ghent', 'language_en': 'en'}, {'id': 'region.25621', 'short_code': 'BE-VOV', 'wikidata': 'Q1114', 'mapbox_id': 'dXJuOm1ieHBsYzpaQlU', 'text_nl': 'Oost-Vlaanderen', 'language_nl': 'nl', 'text': 'Oost-Vlaanderen', 'language': 'nl', 'text_en': 'East Flanders', 'language_en': 'en'}, {'id': 'country.8725', 'short_code': 'be', 'wikidata': 'Q31', 'mapbox_id': 'dXJuOm1ieHBsYzpJaFU', 'text_nl': 'België', 'language_nl': 'nl', 'text': 'België', 'language': 'nl', 'text_en': 'Belgium', 'language_en': 'en'}]}
    """

    def __init__(self, feature):
        self._raw = feature

    def __str__(self) -> str:
        return self._raw["place_name"]

    def __get_context(self, q: str, *, field: Optional[str] = None):
        for context in self._raw["context"]:
            if q in context["id"]:
                return context[field] if field else context

        return None

    @property
    def address(self) -> str:
        return self._raw["place_name"].split(",")[0]

    @property
    def city(self) -> Optional[str]:
        return self.__get_context("place", field="text")

    @property
    def postcode(self) -> Optional[str]:
        return self.__get_context("postcode", field="text")

    @property
    def region(self) -> Optional[dict]:
        return self.__get_context("region")

    @property
    def country(self) -> Optional[dict]:
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

    def geocode(self, address: str) -> Optional[MapboxFeature]:
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
        except requests.exceptions.HTTPError:
            return None

        if not data["features"]:
            return None

        return MapboxFeature(response.json()["features"][0])
