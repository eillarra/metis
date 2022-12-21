from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.urls import path


admin.autodiscover()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("sparta.api.urls")),
    path("", include("sparta.site.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
