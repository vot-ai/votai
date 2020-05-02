from backend.routers import SingleInstanceNestedRouter
from apps.surveys.urls import base_router
from backend.router import routers
from .viewsets import SurveyAnnotatorViewset

items_router = SingleInstanceNestedRouter(base_router, "surveys", lookup="survey")
items_router.register("annotators", SurveyAnnotatorViewset)

routers.append(items_router)
