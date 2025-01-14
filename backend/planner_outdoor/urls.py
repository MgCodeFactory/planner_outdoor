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

admin.autodiscover()

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
    # auth user endpoints
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
