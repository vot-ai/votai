from django.urls import include, path
from .router import routers
import apps.surveys.urls  # pylint: disable=unused-import, wrong-import-order
import apps.items.urls  # pylint: disable=unused-import, wrong-import-order
import apps.annotators.urls  # pylint: disable=unused-import, wrong-import-order


app_name = "api"
urlpatterns = [path("auth/", include("apps.rest_auth.urls"))]
for router in routers:
    urlpatterns += router.urls
