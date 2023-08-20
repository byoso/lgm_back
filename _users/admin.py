from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = User
    list_display = (
        'email',
        'username',
        'last_login', 'is_confirmed', 'date_joined',
        'is_staff', 'is_active', 'is_subscriber',
    )
    list_filter = ['is_confirmed', 'is_active', 'is_staff', 'is_subscriber']
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(User, UserAdmin)
