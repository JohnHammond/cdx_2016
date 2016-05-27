from django.contrib import admin

from nano.link.models import Link

class LinkAdmin(admin.ModelAdmin):
    model = Link
    ordering = ('uri',)
admin.site.register(Link, LinkAdmin)

