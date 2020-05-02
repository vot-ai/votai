from .router import routers
import apps.surveys.urls
import apps.items.urls
import apps.annotators.urls


app_name = "api"
urlpatterns = []
for router in routers:
    urlpatterns += router.urls
