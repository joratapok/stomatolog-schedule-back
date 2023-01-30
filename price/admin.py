from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from price.models import PriceList, Service, Teeth, DentalChart


class ServiceResource(resources.ModelResource):
    class Meta:
        model = Service


class ServiceAdmin(ImportExportModelAdmin):
    list_display = ('price_list', 'title', 'price', 'type', 'code', )
    list_filter = ('price_list', 'type', )
    search_fields = ('title', 'price', 'code', )
    resource_class = ServiceResource


class TeethAdmin(admin.ModelAdmin):
    list_display = ('dental_chart', 'tooth_number', 'count', 'event', )
    list_editable = ('tooth_number', 'count', )


admin.site.register(PriceList)
admin.site.register(Service, ServiceAdmin)
admin.site.register(DentalChart)
admin.site.register(Teeth, TeethAdmin)
