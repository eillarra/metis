from rest_framework.routers import DefaultRouter
from rest_framework.viewsets import ViewSet
from rest_framework_extensions.routers import NestedRouterMixin

from metis.api import views


class DummyViewSet(ViewSet):
    pass


class Router(NestedRouterMixin, DefaultRouter):
    def __init__(self, version="v1"):
        super().__init__()

        self.schema_title = f"Metis API {version}"

        # /rel/{parent_lookup_content_type_id}/{parent_lookup_object_id}/remarks/

        rel_routes_pql = ["content_type_id", "object_id"]
        rel_routes = self.register(r"rel/(?P<parent_lookup_content_type_id>\d+)", DummyViewSet, basename="rel")
        rel_routes.register("remarks", views.RemarkViewSet, basename="remark", parents_query_lookups=rel_routes_pql)

        # /educations/
        # /educations/{parent_lookup_education_id}/places/
        # /educations/{parent_lookup_education_id}/places/{parent_lookup_place_id}/contacts/
        # /educations/{parent_lookup_education_id}/projects/
        # /educations/{parent_lookup_education_id}/projects/{parent_lookup_project_id}/places/

        education_routes = self.register("educations", views.EducationViewSet, basename="education")
        education_place_routes = education_routes.register(
            "places", views.PlaceViewSet, basename="education-place", parents_query_lookups=["education_id"]
        )
        education_place_routes.register(
            "contacts",
            views.ContactViewSet,
            basename="education-place-contact",
            parents_query_lookups=["education_id", "place_id"],
        )
        project_routes = education_routes.register(
            "projects", views.ProjectViewSet, basename="project", parents_query_lookups=["education_id"]
        )
        project_routes.register(
            "places",
            views.ProjectPlaceViewSet,
            basename="project-place",
            parents_query_lookups=["education_id", "project_id"],
        )
