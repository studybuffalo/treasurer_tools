from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


USER = get_user_model()


class MyUserChangeForm(UserChangeForm):
    """Extending user change form."""
    class Meta(UserChangeForm.Meta):
        model = USER


class MyUserCreationForm(UserCreationForm):
    """Extending user creation form."""
    class Meta(UserCreationForm.Meta):
        model = USER
        fields = ('name', 'email')


@admin.register(USER)
class UserAdmin(admin.ModelAdmin):
    form = MyUserChangeForm
    fieldsets = (
        (
            None,
            {'fields': ('email', 'password')}
        ),
        (
            'Personal info',
            {'fields': ('name',)}
        ),
        (
            'Permissions',
            {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}
        ),
        (
            'Important dates',
            {'fields': ('last_login', 'date_joined')}
        ),
    )
    add_form = MyUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'password1', 'password2'),
        }),
    )
