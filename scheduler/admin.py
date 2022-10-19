from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer, Clinic, Cabinet, Event



# admin.site.register(Profile, ProfileAdmin)
admin.site.register(Customer)
admin.site.register(Clinic)
admin.site.register(Cabinet)
admin.site.register(Event)
