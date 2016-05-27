
from django.contrib import admin

from nano.blog.models import *
from nano.blog.settings import TAGGING, TAGGIT, NANO_BLOG_TAGS

tag_devel = None
untag_devel = None
if NANO_BLOG_TAGS:

    if NANO_BLOG_TAGS == TAGGIT:

        def tag_devel(modeladmin, request, queryset):
            for entry in queryset:
                entry.tags.add('devel')

        def untag_devel(modeladmin, request, queryset):
            for entry in queryset:
                entry.tags.remove('devel')

    elif NANO_BLOG_TAGS == TAGGING:
        Tag = TAGGING.models.Tag

        def tag_devel(modeladmin, request, queryset):
            for entry in queryset:
                Tag.objects.add_tag(entry, 'devel')

        def untag_devel(modeladmin, request, queryset):
            for entry in queryset:
                start, _, end = entry.tags.partition('devel')
                if not end:
                    continue
                entry.tags = '%s %s' % (start.strip(), end.strip())
                entry.save()

    tag_devel.short_description = "Tag selected entries with 'devel'"
    untag_devel.short_description = "Remove 'devel'-tag from selected entries"

class EntryAdmin(admin.ModelAdmin):
    model = Entry
    list_display = ('headline', 'pub_date')
    search_fields = ('headline', 'pub_date')
    date_hierarchy = 'pub_date'
    if tag_devel and untag_devel:
        actions = [tag_devel, untag_devel]

admin.site.register(Entry, EntryAdmin)
