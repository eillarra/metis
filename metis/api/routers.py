from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import NestedRouterMixin

from metis.api import views


class Router(NestedRouterMixin, DefaultRouter):
    def __init__(self, version="v1"):
        super().__init__()

        self.schema_title = f"Metis API {version}"

        # /places/

        self.register("places", views.PlaceViewSet, basename="place")

        # /educations/
        # /educations/{parent_lookup_education}/places/
        # /educations/{parent_lookup_education}/places/{parent_lookup_education_place}/contacts/
        # /educations/{parent_lookup_education}/projects/
        # /educations/{parent_lookup_education}/projects/{parent_lookup_project}/places/

        education_routes = self.register("educations", views.EducationViewSet, basename="education")
        education_place_routes = education_routes.register(
            "places", views.EducationPlaceViewSet, basename="education-place", parents_query_lookups=["education"]
        )
        education_place_routes.register(
            "contacts",
            views.ContactViewSet,
            basename="education-place-contact",
            parents_query_lookups=["education_place__education", "education_place"],
        )
        project_routes = education_routes.register(
            "projects", views.ProjectViewSet, basename="project", parents_query_lookups=["education"]
        )
        project_routes.register(
            "places",
            views.ProjectPlaceViewSet,
            basename="project-place",
            parents_query_lookups=["project__education", "project"],
        )
