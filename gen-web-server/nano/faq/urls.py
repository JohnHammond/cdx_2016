from django.conf.urls import *

from nano.faq import views

urlpatterns = patterns('',
    url(r'^$',     views.list_faqs),
)
