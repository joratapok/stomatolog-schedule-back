from django.utils.translation import gettext_lazy as _

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from employee.models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile


class UserProfileAdmin(UserAdmin):
    inlines = [ProfileInline]
    fieldsets = (
        (None, {'fields': ['username', 'password', ]}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', )}),
        (_('Permissions'),   {'fields': ('is_superuser', )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'is_superuser'),
            },
        ),
    )


admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
