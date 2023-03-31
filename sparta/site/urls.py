from django.conf.urls import include
from django.contrib.flatpages.views import flatpage
from django.urls import path, re_path

from sparta.site import views


office_patterns = (
    [
        path("<slug:code>/", include([path("", views.OfficeView.as_view(), name="app")])),
    ],
    "office_patterns",
)

urlpatterns = [
    path("office/", include(office_patterns, namespace="office")),
    path("u/", include("allauth.urls")),
    # pages
    path("", views.HomeView.as_view(), name="homepage"),
]

# Flatpages “catchall” pattern

urlpatterns += [
    re_path(r"^(?P<url>.*/)$", flatpage),
]
