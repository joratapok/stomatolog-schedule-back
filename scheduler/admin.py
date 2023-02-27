from django.contrib import admin
from scheduler.models import Customer, Clinic, Cabinet, Event, DutyShift, TreatmentPlan


class ClinicAdmin(admin.ModelAdmin):
    list_display = ('title', 'phone', 'time_zone', 'start_of_the_day', 'end_of_the_day', 'is_active', 'is_main', 'price_list', )
    list_editable = ('time_zone', 'is_active', 'is_main', )
    list_filter = ('is_active', 'is_main', )
    prepopulated_fields = {'slug': ('title', )}


class CabinetAdmin(admin.ModelAdmin):
    list_display = ('name', 'clinic', 'is_active')
    list_filter = ('clinic', 'is_active')
    list_editable = ('is_active', )


class DutyShiftAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'cabinet', 'date_start', 'date_finish', )
    list_filter = ('doctor', 'cabinet', 'date_start', )
    list_editable = ('cabinet', )


class TreatmentPlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'tooth', 'plan')


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'date_of_birth', 'gender', 'phone', 'clinic', )
    list_filter = ('gender', 'clinic', )
    search_fields = ('last_name', 'first_name', 'phone', )
    list_editable = ('clinic', )


class EventAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'client', 'clinic', 'cabinet', 'date_start', 'date_finish', 'status', 'color', 'comment', )
    list_filter = ('cabinet__clinic__title', 'status', )
    list_editable = ('status', )
    search_fields = ('date_start', )

    def clinic(self, obj):
        try:
            clinic = Clinic.objects.get(cabinets__name=obj.cabinet.name).title
            return clinic
        except:
            return ''

    clinic.short_description = 'Клиника'


admin.site.register(Clinic, ClinicAdmin)
admin.site.register(TreatmentPlan, TreatmentPlanAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Cabinet, CabinetAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(DutyShift, DutyShiftAdmin)
