from django.contrib import admin

from nano.comments.models import Comment

class CommentAdmin(admin.ModelAdmin):
    model = Comment
    ordering = ('added',)
    list_display = ('content_type', 'object_pk', 'comment', 'user', 'path') 
    list_filter = ('content_type',)
    date_hierarchy = 'added'
admin.site.register(Comment, CommentAdmin)

