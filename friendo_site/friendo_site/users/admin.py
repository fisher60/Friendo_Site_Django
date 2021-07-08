from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Note


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Discord",
            {
                "fields": (
                    "bot_admin",
                    "discord_username",
                    "discord_discriminator",
                    "discord_id",
                    "api_authorized",
                    "timezone_name",
                ),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Note)
