from backend.routers import SingleInstanceNestedRouter
from apps.surveys.urls import base_router
from backend.router import routers
from .viewsets import SurveyItemViewset

items_router = SingleInstanceNestedRouter(base_router, "surveys", lookup="survey")
items_router.register("items", SurveyItemViewset)

routers.append(items_router)
