"""
URL configuration for planner_outdoor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenVerifyView
from po_app.authenticate import CustomUserDetailsView
from dj_rest_auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmView,
)
from po_app.views import (
    UsersViewSet,
    ActivitiesViewSet,
    AllergensViewSet,
    UserActivitiesViewSet,
    UserAllergensViewSet,
    PlannedActivitiesViewSet,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

router = DefaultRouter()
router.register(r"users",
                UsersViewSet,
                basename="users")
router.register(r"activities",
                ActivitiesViewSet,
                basename="activities")
router.register(r"allergens",
                AllergensViewSet,
                basename="allergens")
router.register(r"user-activities",
                UserActivitiesViewSet,
                basename="user-activities")
router.register(r"user-allergens",
                UserAllergensViewSet,
                basename="user-allergens")
router.register(r"planned-activities",
                PlannedActivitiesViewSet,
                basename="planned-activities")

urlpatterns = [
    # Django admin console endpoint
    path("admin/", admin.site.urls),
    # po_app endpoints
    path("", include(router.urls)),
    # Authenticate endpoints
    path("auth/login/",
         LoginView.as_view(),
         name="auth_login",
         ),
    path("auth/logout/",
         LogoutView.as_view(),
         name="auth_logout",
         ),
    path(
        "auth/password/change/",
        PasswordChangeView.as_view(),
        name="auth_password_change",
    ),
    path(
        "auth/password/reset/",
        PasswordResetView.as_view(),
        name="auth_password_reset",
    ),
    path(
        "auth/password/reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name="auth_password_reset_confirm",
    ),
    path("auth/token/verify/",
         TokenVerifyView.as_view(),
         name="auth_token_verify",
         ),
    # Manage Authenticated user GET and PATCH
    path("auth/user/",
         CustomUserDetailsView.as_view(),
         name="auth_user",
         ),
    # Documentation API endpoints
    path("schema/",
         SpectacularAPIView.as_view(),
         name="schema",
         ),
    path(
        "schema/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
    ),
    path(
        "schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
