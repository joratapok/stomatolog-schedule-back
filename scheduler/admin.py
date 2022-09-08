from django.contrib import admin
from .models import Employee, Customer, Clinic, Cabinet, Event

admin.site.register(Employee)
admin.site.register(Customer)
admin.site.register(Clinic)
admin.site.register(Cabinet)
admin.site.register(Event)
