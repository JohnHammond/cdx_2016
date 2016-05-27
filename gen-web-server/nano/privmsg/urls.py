from django.conf.urls import *

from nano.privmsg import views

urlpatterns = patterns('',
    url(r'^add$',          views.add_pm, name='add_pm'),
    url(r'^(?P<msgid>[1-9][0-9]*)/archive$', views.move_to_archive, name='archive_pm'),
    url(r'^(?P<msgid>[1-9][0-9]*)/delete$', views.delete, name='delete_pm'),
    #url(r'^(?:(?P<action>(archive|sent))/?)?$', views.show_pms, name='show_pms'),
    url(r'^archive/$', views.show_pm_archived, name='show_archived_pms'),
    url(r'^sent/$', views.show_pm_sent, name='show_sent_pms'),
    url(r'^$', views.show_pm_received, name='show_pms'),
    #url(r'^$', views.show_pms, {u'action': u'received'}, name='show_pms'),
)

