from django.contrib import admin

from nano.badge.models import Badge

class BadgeAdmin(admin.ModelAdmin):
    list_display = ('level', 'name', 'description')
    list_filter = ('level',)
    ordering = ('level', 'name',)
admin.site.register(Badge, BadgeAdmin)

