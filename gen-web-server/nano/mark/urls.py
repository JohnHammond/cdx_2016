from django.conf.urls import *

from nano.mark import views

urlpatterns = patterns('',
    url(r'^toggle$',    views.toggle_mark, name='toggle_mark'),
)
