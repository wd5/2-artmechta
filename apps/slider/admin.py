# -*- coding: utf-8 -*-
from django.contrib import admin

from apps.slider.models import InteriorPhoto
from sorl.thumbnail.admin import AdminImageMixin
from apps.utils.widgets import AdminImageCrop
from django import forms

#class PhotoAdminForm(forms.ModelForm):
#    image = forms.ImageField(
#    	widget=AdminImageCrop(attrs={'path': 'slider/photo'}),
#    	label=u'Изображение'
#    )
#    model = Photo
#
#class PhotoAdmin(AdminImageMixin, admin.ModelAdmin):
#    list_display = ('id','admin_photo_preview','order','is_published',)
#    list_display_links = ('id','admin_photo_preview',)
#    list_editable = ('order','is_published',)
#    list_filter = ('is_published',)
#    form = PhotoAdminForm
#
#admin.site.register(Photo, PhotoAdmin)


class InteriorPhotoAdminForm(forms.ModelForm):
    image = forms.ImageField(
    	widget=AdminImageCrop(attrs={'path': 'slider/photo'}),
    	label=u'Изображение'
    )
    model = InteriorPhoto

class InteriorPhotoAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('id','admin_photo_preview','order','is_published',)
    list_display_links = ('id','admin_photo_preview',)
    list_editable = ('order','is_published',)
    list_filter = ('is_published',)
    form = InteriorPhotoAdminForm

admin.site.register(InteriorPhoto, InteriorPhotoAdmin)