from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Note


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Discord",
            {
                "fields": ("bot_admin", "discord_id", "api_authorized"),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Note)
