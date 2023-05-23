from django.contrib.flatpages.views import flatpage
from django.urls import path, re_path

from metis.site import views


urlpatterns = [
    path("stagebureau/<slug:education_code>/", views.EducationOfficeView.as_view(), name="education_office"),
    path("stages/<slug:education_code>/", views.StudentAreaView.as_view(), name="student_area"),
    path("places/<int:place_id>/", views.PlaceOfficeView.as_view(), name="place_office"),
    # pages
    path("", views.HomeView.as_view(), name="homepage"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
]

# Flatpages “catchall” pattern

urlpatterns += [
    re_path(r"^(?P<url>.*/)$", flatpage),
]
