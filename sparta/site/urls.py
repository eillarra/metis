from django.conf.urls import include
from django.contrib.flatpages.sitemaps import FlatPageSitemap
from django.contrib.flatpages.views import flatpage
from django.contrib.sitemaps import views as sitemap_views
from django.urls import path, re_path

from sparta.site import views

# from .sitemaps import


sitemaps = {
    "pages": FlatPageSitemap,
}


urlpatterns = [
    path("u/", include("allauth.urls")),
    # pages
    path("", views.HomeView.as_view(), name="homepage"),
    # sitemap
    path("sitemap.xml", sitemap_views.index, {"sitemaps": sitemaps}),
    path(
        "sitemap-<slug:section>.xml",
        sitemap_views.sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]

# Flatpages “catchall” pattern

urlpatterns += [
    re_path(r"^(?P<url>.*/)$", flatpage),
]
