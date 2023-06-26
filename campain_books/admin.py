from django.contrib import admin

from .models import (
    Table,
    Campain,
    Collection,
    )


admin.site.register(Table)
admin.site.register(Campain)


class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'game', 'is_official', 'date_updated')
    list_filter = ('is_official', 'date_created', 'date_updated')
    search_fields = ('name', 'author__username')


admin.site.register(Collection, CollectionAdmin)
