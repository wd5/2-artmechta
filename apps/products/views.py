# -*- coding: utf-8 -*-
import os, md5
from datetime import datetime, date, timedelta
from django.core.mail.message import EmailMessage
from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponseForbidden
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.db.models import Q
from django.views.generic.simple import direct_to_template
from django.db.models.loading import get_model

from django.views.generic import ListView, DetailView, View, TemplateView, FormView
from apps.inheritanceUser.models import CustomUser, Favorites
from apps.products.forms import CommentForm
from apps.siteblocks.models import Settings

from models import Category, Product
import settings

class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'products/product_detail.html'
    queryset = Product.objects.published()

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data()
        product = self.object
        fav = GetFavorites(self.request)
        fav_products = fav.fav_products.published()
        if product in fav_products:
            setattr(product, 'is_fav', True)
        context['product'] = product
        context['comments'] = product.get_comments()
        return context

product_detail = ProductDetail.as_view()

class CategoryDetail(DetailView):
    model = Category
    context_object_name = 'category'
    template_name = 'products/category_detail.html'
    queryset = Category.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super(CategoryDetail, self).get_context_data()

        slug = self.kwargs.get('slug', None)
        sub_slug = self.kwargs.get('sub_slug', None)

        all_categories = Category.objects.filter(is_published=True)
        category = False
        if slug or sub_slug:
            if slug == 'all':
                category = False
                context['catalog'] = Product.objects.published()
            else:
                if sub_slug and not category:
                    try:
                        category = all_categories.filter(slug=sub_slug)
                    except:
                        pass
                if slug and not category:
                    try:
                        category = all_categories.filter(slug=slug)
                    except:
                        pass
        else:
            category = False

        if category and category.count() == 1:
            category = category[0]
        elif category and category.count() > 1: # если по slug'у будет найдено несколько категорий
            try:
                category = category.get(parent__slug__in=[slug, sub_slug])
            except:
                category = False

        if category:
            context['parent_category'] = category.get_root()
            context['category'] = category
            products = category.get_products()[:9]

            # пометка избранных
            fav = GetFavorites(self.request)
            if fav:
                fav_products = fav.fav_products.published()
                for product in products:
                    if product in fav_products:
                        setattr(product, 'is_fav', True)
            try:
                loaded_count = int(Settings.objects.get(name='loaded_count').value)
            except:
                loaded_count = 2
            context['loaded_count'] = loaded_count
            context['category_products'] = products
        else:
            context['category'] = False
        return context

category_detail = CategoryDetail.as_view()

class FavoritesList(TemplateView):
    template_name = 'products/favorites_list.html'

    def get_context_data(self, **kwargs):
        context = super(FavoritesList, self).get_context_data()
        fav = GetFavorites(self.request)
        context['fav_products'] = fav.fav_products.published()
        return context

favorites_list = FavoritesList.as_view()

class CommentFromView(FormView):
    form_class = CommentForm
    template_name = 'products/comment_form.html'

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = request.POST.copy()
            form = CommentForm(data)
            if form.is_valid():
                saved_object = form.save()
                subject = u'%s - Новый отзыв' % settings.SITE_NAME
                subject = u''.join(subject.splitlines())
                message = render_to_string(
                    'products/admin_message_template.html',
                        {
                        'saved_object': saved_object,
                        'site_name': settings.SITE_NAME,
                    }
                )
                try:
                    emailto = Settings.objects.get(name='workemail').value
                except Settings.DoesNotExist:
                    emailto = False

                if emailto:
                    msg = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [emailto])
                    msg.content_subtype = "html"
                    msg.send()

                return HttpResponse('success')
            else:
                faq_form_html = render_to_string(
                    'products/comment_form.html',
                    {'form': form}
                )
                return HttpResponse(faq_form_html)
        else:
            return HttpResponseBadRequest()

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(**kwargs)
        pk = self.kwargs.get('pk', None)
        try:
            product_set = Product.objects.filter(id=pk)
            product = Product.objects.get(id=pk)
            form.fields['product'].queryset = product_set
            form.fields['product'].initial = product

            if self.request.user.is_authenticated and self.request.user.id:
                form.fields['name'].initial = self.request.user.get_name()
                form.fields['email'].initial = self.request.user.email

            context['form'] = form
            return self.render_to_response(context)
        except:
            return HttpResponseBadRequest()

comment_form = csrf_exempt(CommentFromView.as_view())


def GetFavorites(request):
    try:
        cookies = request.COOKIES
        artmechta_fav_id = False
        if 'artmechta_fav_id' in cookies:
            artmechta_fav_id = cookies['artmechta_fav_id']
        if request.user.is_authenticated and request.user.id:
            profile = CustomUser.objects.get(id=request.user.id)
        else:
            profile = False

        sessionid = request.session.session_key

        if profile:
            try:
                fav = Favorites.objects.get(profile=profile)
            except Favorites.DoesNotExist:
                if artmechta_fav_id:
                    try:
                        fav = Favorites.objects.get(id=artmechta_fav_id)
                        if fav.profile:
                            fav = False
                        else:
                            if profile:
                                fav.profile = profile
                                fav.save()
                    except:
                        fav = False
                else:
                    fav = False
        elif artmechta_fav_id:
            try:
                fav = Favorites.objects.get(id=artmechta_fav_id)
            except Favorites.DoesNotExist:
                fav = False
        else:
            try:
                fav = Favorites.objects.get(sessionid=sessionid)
            except Favorites.DoesNotExist:
                fav = False
        return fav
    except:
        return False