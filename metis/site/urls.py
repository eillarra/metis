from django.conf.urls import include
from django.contrib.flatpages.views import flatpage
from django.urls import path, re_path

from metis.site import views


office_patterns = (
    [
        path("<slug:code>/", include([path("", views.OfficeView.as_view(), name="app")])),
    ],
    "office_patterns",
)

urlpatterns = [
    path("office/", include(office_patterns, namespace="office")),
    # pages
    path("", views.HomeView.as_view(), name="homepage"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
]

# Flatpages “catchall” pattern

urlpatterns += [
    re_path(r"^(?P<url>.*/)$", flatpage),
]
