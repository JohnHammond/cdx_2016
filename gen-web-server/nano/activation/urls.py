from django.conf.urls import *

urlpatterns = patterns('nano.activation.views',
    url(r'^activate$',         'activate_key', name='nano-activate-key'),
)

urlpatterns += patterns('',
    url(r'^activation_ok/$', 'django.shortcuts.render', 
                             {'template_name': 'nano/activation/activated.html'},
                             name='nano-activation-ok'),
)

