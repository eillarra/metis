from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import NestedRouterMixin

from metis.api import views


class Router(NestedRouterMixin, DefaultRouter):
    def __init__(self, version="v1"):
        super().__init__()

        self.schema_title = f"Metis API {version}"

        self.register("places", views.PlaceViewSet, basename="place")

        education_routes = self.register("educations", views.EducationViewSet, basename="education")
        education_routes.register(
            "places", views.EducationPlaceViewSet, basename="education-place", parents_query_lookups=["education"]
        )
        education_routes.register(
            "projects", views.ProjectViewSet, basename="education-project", parents_query_lookups=["education"]
        )
