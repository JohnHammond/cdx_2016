from django.contrib import admin

from nano.mark.models import MarkType, Mark

class MarkAdmin(admin.ModelAdmin):
    model = Mark
    ordering = ('marked_at',)
    list_display = ('marktype', 'marked_by')
    list_filter = ('marktype',)
admin.site.register(Mark, MarkAdmin)

class MarkTypeAdmin(admin.ModelAdmin):
    model = MarkType
    ordering = ('name',)
    list_display = ('name',)
    list_filter = ('verify','permanent','hide')
admin.site.register(MarkType, MarkTypeAdmin)

