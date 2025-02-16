from django.contrib import admin
from .models import Users, Activities, UserActivities, PlannedActivities


admin.site.register(Users)
admin.site.register(Activities)
admin.site.register(UserActivities)
admin.site.register(PlannedActivities)
