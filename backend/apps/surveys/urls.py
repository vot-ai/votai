from backend.router import base_router
from .viewsets import SurveyViewset

base_router.register("surveys", SurveyViewset, "survey")
