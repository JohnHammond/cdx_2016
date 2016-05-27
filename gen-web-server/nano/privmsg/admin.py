from django.contrib import admin

from nano.privmsg.models import PM

class PMAdmin(admin.ModelAdmin): 
    model = PM
    ordering = ('subject', '-sent')
    list_display = ('subject', 'sender', 'recipient', 'sent', 'recipient_archived', 'recipient_deleted', 'sender_deleted')
    list_filter = ('sender', 'recipient',)
    search_fields = ('sender', 'recipient', 'subject', 'sent')
admin.site.register(PM, PMAdmin)

