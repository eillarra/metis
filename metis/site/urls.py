from django.contrib.flatpages.views import flatpage
from django.urls import path, re_path

from metis.site import views


urlpatterns = [
    # main apps
    path("places/<int:place_id>/", views.PlaceOfficeView.as_view(), name="place_office"),
    path("stagebureau/<slug:education_code>/", views.EducationOfficeView.as_view(), name="education_office"),
    path(
        "stagebureau/<slug:education_code>/files/p/<int:period_id>/<slug:code>.<slug:file_type>",
        views.EducationOfficePeriodReportView.as_view(),
        name="education_office_report",
    ),
    path("stages/<slug:education_code>/", views.StudentAreaView.as_view(), name="student_area"),
    path(
        "stages/<slug:education_code>/stageplaats/",
        views.StudentProposeInternshipPlaceView.as_view(),
        name="student_propose_place",
    ),
    path(
        "stages/<slug:education_code>/files/p/<int:period_id>/<slug:code>.<slug:file_type>",
        views.StudentAreaPeriodReportView.as_view(),
        name="student_area_report",
    ),
    # pages
    path("", views.HomeView.as_view(), name="homepage"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    # files  # TODO: refactor
    path("files/project_<int:project_id>.xlsx", views.ProjectPlanningFileView.as_view(), name="project_planning_excel"),
    path("files/q/<int:questioning_id>.<slug:file_type>", views.QuestioningFileView.as_view(), name="questioning_file"),
    path("files/q/planning/<int:questioning_id>.xlsx", views.PlanningFileView.as_view(), name="planning_file"),
    path("files/e/<uuid:uuid>.pdf", views.EvaluationPdfView.as_view(), name="evaluation_pdf"),
    path("files/i/<uuid:uuid>_<slug:template_code>.pdf", views.InternshipPdfView.as_view(), name="internship_pdf"),
    path("files/s/<uuid:uuid>.pdf", views.SignaturePdfView.as_view(), name="signature_pdf"),
]

# Flatpages “catchall” pattern

urlpatterns += [
    re_path(r"^(?P<url>.*/)$", flatpage),
]
