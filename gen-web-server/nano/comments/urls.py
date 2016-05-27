from django.conf.urls import *
try:
    # Django >= 1.8
    from django.contrib.contenttypes.views import shortcut
except ImportError:
    # Django < 1.8
    from django.views.defaults import shortcut

from nano.comments import views


urlpatterns = patterns('',
    url(r'^$',         views.list_comments, name='comments-list-comments'),
    url(r'^post$',     views.post_comment, name='comments-post-comment'),
)

urlpatterns += patterns('',
    url(r'^cr/(\d+)/(.+)/$', shortcut, name='comments-url-redirect'),
)

