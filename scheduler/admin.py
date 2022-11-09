from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer, Clinic, Cabinet, Event, Profile


class ClinicAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}


admin.site.register(Clinic, ClinicAdmin)
admin.site.register(Profile)
admin.site.register(Customer)
admin.site.register(Cabinet)
admin.site.register(Event)


