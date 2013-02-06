# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views

urlpatterns = patterns('apps.inheritanceUser.views',

    url(r'^$','show_cabinet', name='show_cabinet'),
    (r'^edit_info_form/$','show_profile_form'),
    (r'^registration_form/$','registration_form'),
    url(r'^password/reset/$',
        auth_views.password_reset,
            {'template_name': 'users/password_reset_form.html',},
        name='auth_password_reset'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
            {'template_name': 'users/password_reset_confirm.html'},
        name='auth_password_reset_confirm'),
    url(r'^password/reset/complete/$',
        auth_views.password_reset_complete,
            {'template_name': 'users/password_reset_complete.html'},
        name='auth_password_reset_complete'),
    url(r'^password/reset/done/$',
        auth_views.password_reset_done,
            {'template_name': 'users/password_reset_done.html'},
        name='auth_password_reset_done'),
    url(r'^password/change/$',
        auth_views.password_change,
            {'template_name': 'users/password_change_form.html'},
        name='auth_password_change'),
    url(r'^password/change/done/$',
        auth_views.password_change_done,
            {'template_name': 'users/password_change_done.html'},
        name='auth_password_change_done'),

)