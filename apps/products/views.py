# -*- coding: utf-8 -*-
import os,md5
from datetime import datetime, date, timedelta
from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponseForbidden
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.views.generic.simple import direct_to_template

from django.views.generic import ListView, DetailView, DetailView


from models import Category, Product


class ProductDetail(DetailView):
    model = Product
    context_object_name = Product
    template_name = 'products/product_detail.html'
    queryset = Product.objects.published()

    def get_context_data(self, **kwargs):
        context = super(ProductDetail,self).get_context_data()
        context['photos'] = self.object.get_photos()
        return context

product_view = ProductDetail.as_view()