from django.contrib import admin
from .models import Users, Activities, Allergens, UserActivities, UserAllergens, PlannedActivities


admin.site.register(Users)
admin.site.register(Activities)
admin.site.register(Allergens)
admin.site.register(UserActivities)
admin.site.register(UserAllergens)
admin.site.register(PlannedActivities)
