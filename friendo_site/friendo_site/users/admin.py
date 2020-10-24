from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, AuthToken, Note


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Discord",
            {
                "fields": (
                    "bot_admin",
                    "discord_id",
                ),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(AuthToken)
admin.site.register(Note)
