from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = User
    list_display = (
        'email',
        'username',
        'first_name',
        'last_name',
        'is_staff', 'is_active',
    )
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(User, UserAdmin)
