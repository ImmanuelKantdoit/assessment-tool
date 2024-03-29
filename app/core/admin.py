"""
Django admin customization
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users"""
    ordering = ['id']
    list_display = ['id', 'email', 'firstname', 'lastname', 'role']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('firstname', 'lastname', 'role')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login', 'id']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'id',
                'email',
                'password1',
                'password2',
                'firstname',
                'lastname',
                'role',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Question)
admin.site.register(models.Choice)
admin.site.register(models.Examinee_Answer)
