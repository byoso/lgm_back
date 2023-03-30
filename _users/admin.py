from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = User
    list_display = (
        'email',
        'first_name',
        'last_name',
        'is_staff', 'is_active',  'confirmed',
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(User, UserAdmin)
