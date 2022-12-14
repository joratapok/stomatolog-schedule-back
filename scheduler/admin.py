from django.contrib import admin
from scheduler.models import Customer, Clinic, Cabinet, Event, DutyShift


class ClinicAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}


admin.site.register(Clinic, ClinicAdmin)
admin.site.register(Customer)
admin.site.register(Cabinet)
admin.site.register(Event)
admin.site.register(DutyShift)
