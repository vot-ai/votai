from rest_framework.exceptions import ValidationError


class InactiveSurveyError(ValidationError):
    default_detail = "Operation not allowed: Inactive Survey"
    default_code = "inactive_survey"


class MaxBudgetReachedError(ValidationError):
    default_detail = "Operation not allowed: Maximum survey budget reached"
    default_code = "survey_budget_reached"
