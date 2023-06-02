from django.contrib import admin

from .models import (
    Table,
    Campain,
    CampainTemplate,
    )


admin.site.register(Table)
admin.site.register(Campain)
admin.site.register(CampainTemplate)
