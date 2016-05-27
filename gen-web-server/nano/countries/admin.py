from django.contrib import admin

from nano.countries.models import Country


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'iso')

admin.site.register(Country, CountryAdmin)
