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
from po_app.views import UsersViewSet, ActivitiesViewSet, AllergensViewSet, UserActivitiesViewSet, UserAllergensViewSet, PlannedActivitiesViewSet

router = DefaultRouter()
router.register(r'users', UsersViewSet, basename='users')
router.register(r'activities', ActivitiesViewSet, basename='activities')
router.register(r'allergens', AllergensViewSet, basename='allergens')
router.register(r'user-activities', UserActivitiesViewSet,
                basename='user-activities')
router.register(r'user-allergens', UserAllergensViewSet,
                basename='user-allergens')
router.register(r'planned-activities', PlannedActivitiesViewSet,
                basename='planned-activities')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api/auth/', include('dj_rest_auth.urls')),
]
