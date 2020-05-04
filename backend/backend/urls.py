"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from dj_rest_auth.registration.views import VerifyEmailView as DjVerifyEmailView


urlpatterns = [
    path("admin/", admin.site.urls),
    # API and docs
    path("docs/", include("backend.docs_urls")),
    path("", include("backend.api_urls")),
    # Django Rest Explorer UI
    path("api-auth/", include("rest_framework.urls")),
    # Authentication
    path("auth/", include("dj_rest_auth.urls")),
    path(
        "auth/registration/account-confirm-email/",
        DjVerifyEmailView.as_view(),
        name="account_email_verification_sent",
    ),
    # Monitoring
    path("", include("django_prometheus.urls")),
    path("health/", include("health_check.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
