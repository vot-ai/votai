from django.urls import path, include
from django.conf import settings
from django.templatetags.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import api_urls
from .swagger_schema import TaggedDescriptionSchemaGenerator

SchemaView = get_schema_view(
    openapi.Info(
        title="Pairwise API",
        default_version="v1",
        description="""
""".replace(
            "https://unicaronas.com", settings.ROOT_URL
        ).replace(
            "http://unicaronas.com", settings.ROOT_URL
        ),
        terms_of_service="https://unicaronas.com/terms_and_conditions/",
        contact=openapi.Contact(
            name="Suporte",
            email="gustavomaronato@gmail.com",
            url="https://unicaronas.com",
        ),
        license=openapi.License(
            name="AGPL3", url="https://opensource.org/licenses/AGPL-3.0"
        ),
        x_logo={
            # "url": static("backend/img/social/og-image.jpg"),
            "backgroundColor": "#FFFFFF",
        },
    ),
    # validators=['flex', 'ssv'],
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=[path("", include(api_urls))],
    generator_class=TaggedDescriptionSchemaGenerator,
)

app_name = "docs"


docs_urlpatterns = [
    path(
        "swagger<str:format>",
        SchemaView.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        SchemaView.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("", SchemaView.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]


urlpatterns = [
    path("v1.0/", include((docs_urlpatterns, "docs"), namespace="v1.0")),
]
