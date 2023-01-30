from django.utils.translation import gettext_lazy as _

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from employee.models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile


class UserProfileAdmin(UserAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'role', 'date_of_birth', 'phone', 'speciality', )
    inlines = [ProfileInline]
    fieldsets = (
        (None, {'fields': ['username', 'password', ]}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {'fields': ('is_superuser',)}),
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

    def middle_name(self, obj):
        try:
            middle_name = obj.profile.middle_name
            return middle_name
        except:
            return ''

    def role(self, obj):
        try:
            role = obj.profile.role
            return role
        except:
            return ''

    def date_of_birth(self, obj):
        try:
            date_of_birth = obj.profile.date_of_birth
            return date_of_birth
        except:
            return ''

    def phone(self, obj):
        try:
            phone = obj.profile.phone
            return phone
        except:
            return ''

    def speciality(self, obj):
        try:
            speciality = obj.profile.speciality
            return speciality
        except:
            return ''

    middle_name.short_description = 'Отчество'
    role.short_description = 'Роль'
    date_of_birth.short_description = 'Дата рождения'
    phone.short_description = 'Телефон'
    speciality.short_description = 'Специальность'


admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
