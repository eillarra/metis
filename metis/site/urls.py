from django.contrib.flatpages.views import flatpage
from django.urls import path, re_path
from django.views.decorators.cache import never_cache

from metis.site import views


urlpatterns = [
    # main apps
    path(
        "stagebureau/<slug:education_code>/reports/pdf/<int:project_id>/<slug:code>.pdf",
        views.EducationOfficePdfReportView.as_view(),
        name="education_office_pdf_report",
    ),
    path("stagebureau/<slug:education_code>/", views.EducationOfficeView.as_view(), name="education_office"),
    path("stages/<slug:education_code>/", views.StudentAreaView.as_view(), name="student_area"),
    path("places/<int:place_id>/", views.PlaceOfficeView.as_view(), name="place_office"),
    # pages
    path("", views.HomeView.as_view(), name="homepage"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    # invitations
    path("i/<uuid:uuid>/<slug:secret>/", never_cache(views.InvitationView.as_view()), name="invitation"),
]

# Flatpages “catchall” pattern

urlpatterns += [
    re_path(r"^(?P<url>.*/)$", flatpage),
]
