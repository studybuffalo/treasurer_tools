from django.contrib import admin
from django.contrib.auth import get_user_model

class UserAdmin(admin.ModelAdmin):
    fields = (
        'username', 'name', 'email', 'groups', 'user_permissions',
        'is_staff', 'is_active',
    )

# Register the sites
admin.site.register(get_user_model(), UserAdmin)
