from django.conf.urls import *

from nano.badge import views

urlpatterns = patterns('',
    url(r'^$',                 views.list_badges, name='badge-list'),
    url(r'^(?P<pk>[0-9]+)/$',  views.show_badge, name='badge-detail'),
)
