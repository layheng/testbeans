from django.contrib import admin

# Register your models here.
from .models import Feature, Scenario, UserData

admin.site.register(Feature)
admin.site.register(Scenario)
admin.site.register(UserData)