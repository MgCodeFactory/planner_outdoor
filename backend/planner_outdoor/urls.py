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
from po_app.validators_views import ValidationRulesView
from po_app.auth_views import (
    CustomTokenObtainPairView,
    CustomPasswordResetView,
    CustomPasswordResetConfirmView,
)
from po_app.views import (
    ApiRootView,
    UsersViewSet,
    ActivitiesViewSet,
    UserActivitiesViewSet,
    PlannedActivitiesViewSet,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from po_app.weather import (
    GeocodingView,
    WeatherView,
    WeatherDetailsView,
)

urlpatterns = [
    # django admin console
    path("admin/", admin.site.urls),
    # root api
    path('', ApiRootView.as_view(), name='api-root'),
    # validators help messages endpoint
    path("validators-rules/",
         ValidationRulesView.as_view(),
         name="validators-rules"
         ),
    # authentification endpoints
    path("auth/login/",
         CustomTokenObtainPairView.as_view(),
         name="token_obtain_pair",
         ),
    path("auth/register/",
         UsersViewSet.as_view({"post": "create"}),
         name="auth-register",
         ),
    path("auth/password-reset/",
         CustomPasswordResetView.as_view(),
         name="password-reset",
         ),
    path(
        "auth/password-reset-confirm/<str:uid>/<str:token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
    # po_app endpoints
    path(
        "users-list/",
        UsersViewSet.as_view({"get": "list"}),
        name="users-list",
    ),
    path(
        "user-detail/<int:pk>/",
        UsersViewSet.as_view(
            {
                "get": "retrieve",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="user-detail",
    ),
    path(
        "activities-list/",
        ActivitiesViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
        name="activities-list",
    ),
    path(
        "activity-detail/<int:pk>/",
        ActivitiesViewSet.as_view(
            {
                "get": "retrieve",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="activity-detail",
    ),
    path(
        "user-activities-list/",
        UserActivitiesViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
        name="user-activities-list",
    ),
    path(
        "user-activity-detail/<int:pk>/",
        UserActivitiesViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "delete": "destroy",
            }
        ),
        name="user-activity-detail",
    ),
    path(
        "planned-activities-list/",
        PlannedActivitiesViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
        name="planned-activities-list",
    ),
    path(
        "planned-activity-detail/<int:pk>",
        PlannedActivitiesViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "delete": "destroy",
            }
        ),
        name="planned-activity-detail",
    ),
    # Weather API endpoint
    path(
        "geocoding/<str:city>/",
        GeocodingView.as_view(),
        name="geocoding",
    ),
    path(
        "weather/<path:lat>/<path:lon>/",
        WeatherView.as_view(),
        name="weather",
    ),
    path(
        "weather-details/<path:lat>/<path:lon>/<path:day_id>/",
        WeatherDetailsView.as_view(),
        name="weather-details",
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
