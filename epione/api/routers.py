from rest_framework.routers import DefaultRouter

from epione.api import views


class Router(DefaultRouter):
    def __init__(self, version="v1"):
        super().__init__()

        self.schema_title = f"Epione API {version}"

    def get_urls(self):
        return [url for url in super().get_urls() if url.name != "auth-user-detail"]
