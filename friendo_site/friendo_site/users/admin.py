from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, AuthToken


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Discord",
            {
                "fields": ("bot_admin",),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(AuthToken)
