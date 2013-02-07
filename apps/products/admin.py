# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django import forms
from apps.utils.widgets import Redactor
from sorl.thumbnail.admin import AdminImageMixin
from mptt.admin import MPTTModelAdmin


from models import *

class CategoryAdminForm(forms.ModelForm):
    parent = forms.ModelChoiceField(queryset=Category.objects.filter(parent=None), label='Родительская Категория', required=False)

    class Meta:
        model = Category

    class Media:
        js = (
            '/media/js/jquery.js',
            '/media/js/clientadmin.js',
            '/media/js/jquery.synctranslit.js',
            )

class CategoryAdmin(AdminImageMixin, MPTTModelAdmin):
    list_display = ('id','title','slug','order','is_published',)
    list_display_links = ('id','title',)
    list_editable = ('order','is_published',)
    list_filter = ('parent',)
    form = CategoryAdminForm

admin.site.register(Category, CategoryAdmin)


class PhotoInline(admin.TabularInline):
    model = Photo

class FeatureValueInline(admin.TabularInline):
    model = FeatureValue
    extra = 0

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class ProductAdminForm(forms.ModelForm):
    short_description = forms.CharField(widget=Redactor(attrs={'cols': 110, 'rows': 20}), required=False)
    short_description.label=u'Краткое описание'
    description = forms.CharField(widget=Redactor(attrs={'cols': 110, 'rows': 20}), required=False)
    description.label=u'Описание'
    category = forms.ModelChoiceField(queryset=Category.objects.filter(is_published=True).exclude(parent=None),
        label=u'Категория', required=True)
    price = forms.DecimalField(label=u'Цена',  required=True)

    class Meta:
        model = Product

class ProductAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('id','admin_photo_preview','title', 'category','price', 'order','is_published',)
    list_display_links = ('id','title',)
    list_editable = ('order','is_published',)
    list_filter = ('is_published','category')
    search_fields = ('title', 'description', 'short_description',)
    inlines = [PhotoInline, FeatureValueInline, CommentInline]
    form = ProductAdminForm

admin.site.register(Product, ProductAdmin)

class FeatureNameAdmin(admin.ModelAdmin):
    list_display = ('id','title',)
    list_display_links = ('id','title',)

admin.site.register(FeatureName, FeatureNameAdmin)
