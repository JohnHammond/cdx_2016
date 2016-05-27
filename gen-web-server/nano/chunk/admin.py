from django.contrib import admin
from nano.chunk.models import Chunk
 
class ChunkAdmin(admin.ModelAdmin):
    ordering = ['slug',]
    list_display = ('slug',)
    search_fields = ('slug', 'content')

admin.site.register(Chunk, ChunkAdmin)
