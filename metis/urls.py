from django.conf import settings
from django.conf.urls import include
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path
from django.views.i18n import set_language


admin.autodiscover()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("metis.api.urls")),
    path("i18n/setlang/", set_language, name="set_language"),
    path("u/", include("allauth.urls")),
]

urlpatterns += i18n_patterns(path("", include("metis.site.urls")))

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
