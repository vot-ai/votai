from backend.routers.nested import SingleInstanceNestedRouter
from backend.router import routers, base_router
from .viewsets import SurveyAnnotatorViewset

items_router = SingleInstanceNestedRouter(base_router, "surveys", lookup="survey")
items_router.register("annotators", SurveyAnnotatorViewset)

routers.append(items_router)
