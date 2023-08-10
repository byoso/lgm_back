from django.contrib import admin

# Register your models here.
from .models import HomeArticle


class HomeArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'subtitle', 'show', 'date_created']
    list_filter = ['show', 'date_created', 'date_updated', 'show']
    search_fields = ['title', 'subtitle']


admin.site.register(HomeArticle, HomeArticleAdmin)
