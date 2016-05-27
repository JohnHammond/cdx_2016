
from django.contrib import admin

from nano.faq.models import *

class QAAdmin(admin.ModelAdmin):
    model = QA
    list_display = ('question', 'answer', 'last_modified')

admin.site.register(QA, QAAdmin)
