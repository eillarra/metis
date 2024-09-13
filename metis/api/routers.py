from rest_framework.routers import DefaultRouter
from rest_framework.viewsets import ViewSet
from rest_framework_extensions.routers import NestedRouterMixin

from metis.api import views


class DummyViewSet(ViewSet):
    pass


class Router(NestedRouterMixin, DefaultRouter):
    """Router for Metis API."""

    def __init__(self, version="v1"):
        super().__init__()

        self.schema_title = f"Metis API {version}"

        # /users/

        self.register("users", views.UserViewSet, basename="user")

        # /rel/{parent_lookup_content_type_id}/{parent_lookup_object_id}/remarks/

        rel_routes_pql = ["content_type_id", "object_id"]
        rel_routes = self.register(r"rel/(?P<parent_lookup_content_type_id>\d+)", DummyViewSet, basename="rel")
        rel_routes.register("addresses", views.AddressViewSet, basename="address", parents_query_lookups=rel_routes_pql)
        rel_routes.register("files", views.FileViewSet, basename="file", parents_query_lookups=rel_routes_pql)
        rel_routes.register(
            "form-responses",
            views.CustomFormResponseViewSet,
            basename="form-response",
            parents_query_lookups=rel_routes_pql,
        )
        rel_routes.register(
            "phone-numbers", views.PhoneNumberViewSet, basename="phone-number", parents_query_lookups=rel_routes_pql
        )
        rel_routes.register("texts", views.TextEntryViewSet, basename="text", parents_query_lookups=rel_routes_pql)
        rel_routes.register("remarks", views.RemarkViewSet, basename="remark", parents_query_lookups=rel_routes_pql)

        # /educations/
        # /educations/{parent_lookup_education_id}/places/
        # /educations/{parent_lookup_education_id}/places/{parent_lookup_place_id}/contacts/
        # /educations/{parent_lookup_education_id}/projects/
        # /educations/{parent_lookup_education_id}/projects/{parent_lookup_project_id}/internships/
        # /educations/{parent_lookup_education_id}/projects/{parent_lookup_project_id}/places/
        # /educations/{parent_lookup_education_id}/projects/{parent_lookup_project_id}/questionings/
        # /educations/{parent_lookup_education_id}/projects/{parent_lookup_project_id}/students/

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
            "emails",
            views.ProjectEmailViewSet,
            basename="project-email",
            parents_query_lookups=["education_id", "project_id"],
        )
        project_routes.register(
            "places",
            views.ProjectPlaceViewSet,
            basename="project-place",
            parents_query_lookups=["education_id", "project_id"],
        )
        project_routes.register(
            "questionings",
            views.QuestioningViewSet,
            basename="project-questioning",
            parents_query_lookups=["education_id", "project_id"],
        )
        project_routes.register(
            "students",
            views.StudentViewSet,
            basename="project-student",
            parents_query_lookups=["education_id", "project_id"],
        )

        # /educations/{...education_id}/projects/{...project_id}/internships/{parent_lookup_internship_id}/absences/
        # /educations/{...education_id}/projects/{...project_id}/internships/{parent_lookup_internship_id}/timesheets/

        internship_routes = project_routes.register(
            "internships",
            views.InternshipViewSet,
            basename="project-internship",
            parents_query_lookups=["education_id", "project_id"],
        )
        internship_routes.register(
            "absences",
            views.AbsenceViewSet,
            basename="project-internship-absence",
            parents_query_lookups=["education_id", "project_id", "internship_id"],
        )
        internship_routes.register(
            "evaluations",
            views.EvaluationViewSet,
            basename="project-internship-evaluation",
            parents_query_lookups=["education_id", "project_id", "internship_id"],
        )
        internship_routes.register(
            "timesheets",
            views.TimesheetViewSet,
            basename="project-internship-timesheet",
            parents_query_lookups=["education_id", "project_id", "internship_id"],
        )

        # /user/
        # /user/contact/places/
        # /user/mentor/evaluations/
        # /user/mentor/internships/
        # /user/student/internships/
        # /user/student/projects/
        # /user/student/signatures/

        self.register("user", views.AuthUserViewSet, basename="auth-user")
        self.register("user/contact/places", views.ContactPlaceViewSet, basename="contact-place")
        # self.register("user/student/internships", views.PlaceViewSet, basename="student-internship")
        self.register("user/student/projects", views.AuthStudentViewSet, basename="student-set")
        self.register("user/student/signatures", views.AuthStudentSignatureViewSet, basename="student-signature")
        self.register("user/student/internships", views.AuthStudentInternshipViewSet, basename="student-internship")
        self.register(
            "user/student/preplanned-internships",
            views.AuthStudentProposeInternshipPlaceViewSet,
            basename="student-preplanned-internship",
        )
