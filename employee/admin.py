from django.contrib import admin
from django.contrib.auth.models import User
from employee.models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    inlines = [ProfileInline]
    fields = ('username', 'password', 'first_name', 'last_name', 'is_superuser')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
