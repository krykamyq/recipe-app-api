from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {
            "fields": (
                'email', 'password', 'name',
            ),
        }),
        (_('Permissions'), {
            "fields": (
                'is_staff',
                'is_active',
                'is_superuser'
            ),
        }),
        (_('Important dates'), {
            "fields": ('last_login',)
        }),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'name',
                'password1',
                'password2',
                'is_active',
                'is_staff',
                'is_superuser',

            )
        }),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Recipe)
admin.site.register(models.Tags)
admin.site.register(models.Ingradient)
