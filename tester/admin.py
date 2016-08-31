from django.contrib import admin

# Register your models here.
from .models import Feature, Scenario

admin.site.register(Feature)
admin.site.register(Scenario)