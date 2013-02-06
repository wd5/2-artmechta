# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url

#from apps.app.urls import urlpatterns as app_url

from views import index

urlpatterns = patterns('',
    url(r'^$',index, name='index'),
    url(r'^faq/', include('apps.faq.urls')),
    url(r'^cart/', include('apps.orders.urls')),
    url(r'^cabinet/', include('apps.inheritanceUser.urls')),


)
#url(r'^captcha/', include('captcha.urls')),

#urlpatterns += #app_url


