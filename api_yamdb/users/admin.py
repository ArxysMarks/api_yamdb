from django.contrib import admin

from users.models import User


class UsersAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
    )


admin.site.register(User, UsersAdmin)