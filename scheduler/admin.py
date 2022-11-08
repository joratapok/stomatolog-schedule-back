from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer, Clinic, Cabinet, Event, Profile

admin.site.register(Profile)
admin.site.register(Customer)
admin.site.register(Clinic)
admin.site.register(Cabinet)
admin.site.register(Event)
