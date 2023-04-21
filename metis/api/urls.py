from django.conf.urls import include
from django.urls import path
from rest_framework.schemas import get_schema_view

from .routers import Router


urlpatterns = [
    path("openapi.yaml", get_schema_view(title="Metis API", version="1.0.0"), name="openapi_schema"),
    path("v1/", include((Router("v1").urls, "api"), namespace="v1")),
]
