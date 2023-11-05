from allauth.account.views import logout
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path
from django.views.i18n import set_language

from metis.site.views.files import MediaFileView
from metis.ugent_provider.views import oauth2_callback, oauth2_login


admin.autodiscover()


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("metis.api.urls")),
    path("i18n/setlang/", set_language, name="set_language"),
    # modified allauth urls to disable regular signup and login and only allow UGent login
    # https://github.com/pennersr/django-allauth/blob/main/allauth/urls.py
    path("u/logout/", logout, name="account_logout"),
    path("u/ugent/login/", oauth2_login, name="ugent_login"),
    path("u/ugent/login/callback/", oauth2_callback, name="ugent_callback"),
    # media
    path("media/<path:file>", MediaFileView.as_view(), name="media_file"),
]

urlpatterns += i18n_patterns(path("", include("metis.site.urls")))

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()


# error handlers

handler500 = "metis.site.views.errors.server_error"
