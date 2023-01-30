from django.contrib import admin
from scheduler.models import Customer, Clinic, Cabinet, Event, DutyShift


class ClinicAdmin(admin.ModelAdmin):
    list_display = ('title', 'phone', 'time_zone', 'start_of_the_day', 'end_of_the_day', 'is_active', 'is_main', 'price_list', )
    list_editable = ('time_zone', 'is_active', 'is_main', )
    list_filter = ('is_active', 'is_main', )
    prepopulated_fields = {'slug': ('title', )}


class CabinetAdmin(admin.ModelAdmin):
    list_display = ('name', 'clinic', )
    list_filter = ('clinic', )


class DutyShiftAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'cabinet', 'date_start', 'date_finish', )
    list_filter = ('doctor', 'cabinet', 'date_start', )
    list_editable = ('cabinet', )


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'date_of_birth', 'gender', 'phone')
    list_filter = ('gender', )
    search_fields = ('last_name', 'first_name', 'phone', )


class EventAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'client', 'cabinet', 'date_start', 'date_finish', 'status', 'color', 'comment', )
    list_filter = ('cabinet', 'status', )
    list_editable = ('status', )


admin.site.register(Clinic, ClinicAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Cabinet, CabinetAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(DutyShift, DutyShiftAdmin)
