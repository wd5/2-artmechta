# -*- coding: utf-8 -*-
from django.conf.urls.defaults import url, patterns, include
from views import *
from django.views.generic.simple import redirect_to

urlpatterns = patterns('',
    url(r'^$', redirect_to,  {'url': '/'}),
    (r'^favorites/$', favorites_list),
    url(r'^product/(?P<pk>\d+)/$', product_detail, name='product_detail'),
    url(r'^product/(?P<pk>\d+)/add_comment/$', comment_form, name='add_comment'),

    #AJAX
    (r'^(?P<slug>[^/]+)/load_items/$', load_items),
    (r'^(?P<slug>[^/]+)/(?P<sub_slug>[^/]+)/load_items/$', load_items),


    url(r'^(?P<slug>[^/]+)/$', category_detail, name='category_detail'),
    url(r'^(?P<slug>[^/]+)/(?P<sub_slug>[^/]+)/$', category_detail, name='sub_category_detail'),

)
