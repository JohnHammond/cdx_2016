from django.contrib import admin

from nano.blog.models import *
from nano.activation.models import Key

class KeyAdmin(admin.ModelAdmin):
    model = Key
    list_display = ('key', 'group', 'pub_date', 'activated_by', 'expires')
    list_filter = ('group', 'activated_by')
    date_hierarchy = 'pub_date'

admin.site.register(Key, KeyAdmin)
