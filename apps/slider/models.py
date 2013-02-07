# -*- coding: utf-8 -*-
import os, datetime
from django.utils.translation import ugettext_lazy as _
from django.db import models

from pytils.translit import translify
from sorl.thumbnail import ImageField  as sorl_ImageField, get_thumbnail

from apps.utils.managers import PublishedManager
from apps.utils.models import ImageCropMixin
import settings

class ImageField(sorl_ImageField, models.ImageField):
    pass



def file_path_Photo(instance, filename):
    return os.path.join('images','slider',  translify(filename).replace(' ', '_') )

def file_path_InteriorPhoto(instance, filename):
    return os.path.join('images','InteriorPhoto',  translify(filename).replace(' ', '_') )

#class Photo(ImageCropMixin, models.Model):
#    image = ImageField(verbose_name=u'Картинка', upload_to=file_path_Photo)
#    order = models.IntegerField(verbose_name=u'Порядок сортировки',default=10)
#    is_published = models.BooleanField(verbose_name = u'Опубликовано', default=True)
#
#    crop_size = [300, 200]
#
#    objects = PublishedManager()
#
#    class Meta:
#        verbose_name =_(u'slider_photo')
#        verbose_name_plural =_(u'slider_photos')
#        ordering = ['-order',]
#
#    def __unicode__(self):
#        return u'ID фото %s' %self.id
#
#    def admin_photo_preview(self):
#        image = self.image
#        if image:
#            im = get_thumbnail(self.image, '96x96', crop='center', quality=99)
#            return u'<span><img src="%s" width="96" height="96"></span>' %im.url
#        else:
#            return u'<span></span>'
#    admin_photo_preview.allow_tags = True
#    admin_photo_preview.short_description = u'Превью'

class InteriorPhoto(ImageCropMixin, models.Model):
    image = ImageField(verbose_name=u'Картинка', upload_to=file_path_InteriorPhoto)
    order = models.IntegerField(verbose_name=u'Порядок сортировки',default=10)
    is_published = models.BooleanField(verbose_name = u'Опубликовано', default=True)

    crop_size = []

    objects = PublishedManager()

    class Meta:
        verbose_name =_(u'interior_photo')
        verbose_name_plural =_(u'interior_photos')
        ordering = ['-order']

    def __unicode__(self):
        return u'ID фото %s' %self.id

    def get_image(self):
        file, ext = os.path.splitext(self.image.url)
        file = u'%s_crop.jpg' % file
        if os.path.isfile(settings.ROOT_PATH +file):
            return file
        else:
            return get_thumbnail(self.image, '641x168', crop='center', quality=99).url

    def admin_photo_preview(self):
        image = self.image
        if image:
            im = get_thumbnail(self.image, '96x96', crop='center', quality=99)
            return u'<span><img src="%s" width="96" height="96"></span>' %im.url
        else:
            return u'<span></span>'
    admin_photo_preview.allow_tags = True
    admin_photo_preview.short_description = u'Превью'