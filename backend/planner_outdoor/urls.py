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
from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView
# from po_app.authenticate import CustomUserDetailsView
from dj_rest_auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmView,
    UserDetailsView,
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

urlpatterns = [
    # Django admin console endpoint
    path("admin/", admin.site.urls),
    # po_app endpoints
    path(
        "users-list/",
        UsersViewSet.as_view(
            {
                'get': 'list',
                'post': 'create',
            }
        ),
        name="users-list",
    ),
    path(
        "user-detail/<int:pk>/",
        UsersViewSet.as_view(
            {
                'get': 'retrieve',
                'patch': 'partial_update',
                'delete': 'destroy',
            }
        ),
        name="user-detail",
    ),
    path(
        "activities-list/",
        ActivitiesViewSet.as_view(
            {
                'get': 'list',
                'post': 'create',
            }
        ),
        name="activities-list"
    ),
    path(
        "activity-detail/<int:pk>/",
        ActivitiesViewSet.as_view(
            {
                'get': 'retrieve',
                'patch': 'partial_update',
                'delete': 'destroy',
            }
        ),
        name="activity-detail"
    ),
    path(
        "allergens-list/",
        AllergensViewSet.as_view(
            {
                'get': 'list',
                'post': 'create',
            }
        ),
        name="allergens-list"
    ),
    path(
        "allergen-detail/<int:pk>/",
        AllergensViewSet.as_view(
            {
                'get': 'retrieve',
                'patch': 'partial_update',
                'delete': 'destroy',
            }
        ),
        name="allergen-detail"
    ),
    path(
        "user-activities-list/",
        UserActivitiesViewSet.as_view(
            {
                'get': 'list',
                'post': 'create',
            }
        ),
        name="user-activities-list"
    ),
    path(
        "user-activity-detail/<int:pk>/",
        UserActivitiesViewSet.as_view(
            {
                'get': 'retrieve',
                'put': 'update',
                'delete': 'destroy',
            }
        ),
        name="user-activity-detail"
    ),
    path(
        "user-allergens-list/",
        UserAllergensViewSet.as_view(
            {
                'get': 'list',
                'post': 'create',
            }
        ),
        name="user-allergens-list"
    ),
    path(
        "user-allergen-detail/<int:pk>",
        UserAllergensViewSet.as_view(
            {
                'get': 'retrieve',
                'put': 'update',
                'delete': 'destroy',
            }
        ),
        name="user-allergen-detail"
    ),
    path(
        "planned-activities-list/",
        PlannedActivitiesViewSet.as_view(
            {
                'get': 'list',
                'post': 'create',
            }
        ),
        name="planned-activities-list"
    ),
    path(
        "planned-activity-detail/<int:pk>",
        PlannedActivitiesViewSet.as_view(
            {
                'get': 'retrieve',
                'put': 'update',
                'delete': 'destroy',
            }
        ),
        name="planned-activity-detail"
    ),
    # Authenticate endpoints
    path(
        "auth/login/",
        LoginView.as_view(),
        name="auth_login",
    ),
    path(
        "auth/logout/",
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
    path(
        "auth/token/verify/",
        TokenVerifyView.as_view(),
        name="auth_token_verify",
    ),
    # auth user endpoints
    path(
        "auth/user/",
        UserDetailsView.as_view(),
        name="auth_user",
    ),
    # Documentation API endpoints
    path(
        "schema/",
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
