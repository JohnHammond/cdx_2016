from django.conf.urls import *
from django.shortcuts import render

from nano.user import views

signup_done_data = {'template_name': 'nano/user/signup_done.html'}

# 'project_name' should be a setting
password_reset_data = {'project_name': 'CALS'}

urlpatterns = patterns('',
    url(r'^signup/$',           views.signup, name='signup'),
    url(r'^password/reset/$',   views.password_reset, password_reset_data, name='nano_user_password_reset'),
    url(r'^password/change/$',  views.password_change, name='nano_user_password_change'),
    url(r'^signup/done/$',      render, signup_done_data, name='nano_user_signup_done'),
)

