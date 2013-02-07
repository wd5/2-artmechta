# -*- coding: utf-8 -*-
from decimal import Decimal
import os, datetime
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from pytils.numeral import choose_plural

from pytils.translit import translify
from django.core.urlresolvers import reverse

from sorl.thumbnail import ImageField
from mptt.models import MPTTModel, TreeForeignKey, TreeManager
from sorl.thumbnail.shortcuts import get_thumbnail

from apps.utils.managers import PublishedManager
from apps.utils.utils import moneyfmt

def file_path_Category(instance, filename):
    return os.path.join('images', 'category', translify(filename).replace(' ', '_'))


def file_path_Product(instance, filename):
    return os.path.join('images', 'products', translify(filename).replace(' ', '_'))

category_view_choices = (
    (u'list', u'Списком'),
    (u'block', u'Блоком'),
    )

class Category(MPTTModel):
    parent = TreeForeignKey('self', verbose_name=u'Категория', related_name='children', blank=True, null=True,
        on_delete=models.SET_NULL)
    title = models.CharField(verbose_name=u'Название', max_length=100)
    slug = models.CharField(verbose_name=u'Алиас', max_length=100, unique=True)
    icon = ImageField(verbose_name=u'Иконка', upload_to=file_path_Category, blank=True, editable=False)
    image = ImageField(verbose_name=u'Изображение', upload_to=file_path_Category, blank=True)
    category_view = models.CharField(max_length=30, verbose_name=u'Стиль отображения товаров в категории',
        choices=category_view_choices, default=u'list')
    order = models.IntegerField(verbose_name=u'Порядок сортировки', default=10)
    is_footer_menu = models.BooleanField(verbose_name=u'Отображать в меню', help_text=u'внизу страницы', default=False)
    is_published = models.BooleanField(verbose_name=u'Опубликовано', default=True)

    objects = TreeManager()

    def __unicode__(self):
        if self.parent:
            return u'%s - %s' % (self.parent, self.title)
        else:
            return u'%s' % self.title

    class Meta:
        verbose_name = _(u'category')
        verbose_name_plural = _(u'categories')
        ordering = ['-order']

    class MPTTMeta:
        order_insertion_by = ['order']

    def get_absolute_url(self):
        if self.parent:
            parent_slug = self.parent.slug
            return reverse('sub_category_detail', kwargs={'slug': '%s' % parent_slug, 'sub_slug': '%s' % self.slug})
        else:
            return reverse('category_detail', kwargs={'slug': '%s' % self.slug})

    def get_children(self):
        return self.children.filter(is_published=True).select_related()

    def get_children_footer_menu(self):
        return self.children.filter(is_published=True, is_footer_menu=True).select_related()

    def get_descend(self):
        return self.get_descendants(include_self=False)

    def get_bread_product(self):
        if self.is_child_node():
            abs_bread = u'<a href="%s" class="bread_lnk">%s</a> / <a href="%s" class="bread_lnk">%s</a>' % (
                self.parent.get_absolute_url(), self.parent.title, self.get_absolute_url(), self.title)
            return u'%s' % abs_bread
        else:
            return u' <a href="%s">%s</a>' % (self.get_absolute_url(), self.title)

    def get_products(self):
        if self.get_children():
            # развернем для данной все дочерние категории
            descend_ids = self.get_descend().values('id')
            if descend_ids:
                products = Product.objects.filter(is_published=True, category__id__in=descend_ids)
            else:
                products = Product.objects.filter(title="1").filter(title="2")
            return products
        else:
            return self.product_set.published()

    def get_products_count(self):
        return self.get_products().count()

    def get_products_count_text_1(self):
        count = self.get_products_count()
        return u'%s картин%s' % (count, choose_plural(count, (u'а', u'ы', u'')))

    def get_products_count_text_2(self):
        count = self.get_products_count()
        return u'%s товар%s' % (count, choose_plural(count, (u'', u'а', u'ов')))


class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name=u'Категория', blank=True, null=True)
    title = models.CharField(verbose_name=u'Название', max_length=400)
    price = models.DecimalField(verbose_name=u'Цена', decimal_places=2, max_digits=10, blank=True, null=True)
    height = models.CharField(verbose_name=u'Высота', help_text=u'см', max_length=50)
    width = models.CharField(verbose_name=u'Ширина', help_text=u'см', max_length=50)
    short_description = models.TextField(verbose_name=u'Краткое описание', blank=True)
    description = models.TextField(verbose_name=u'Описание', blank=True)
    image = ImageField(verbose_name=u'Изображение', upload_to=file_path_Product, blank=False)
    is_avaliable = models.BooleanField(verbose_name=u'Есть в наличии', default=True)

    order = models.IntegerField(verbose_name=u'Порядок сортировки', default=10)
    is_published = models.BooleanField(verbose_name=u'Опубликовано', default=True)

    # Managers
    objects = PublishedManager()

    class Meta:
        verbose_name = _(u'product_item')
        verbose_name_plural = _(u'product_items')
        ordering = ['-order', ]

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': '%s' % self.id})

    def get_str_price(self):
        try:
            return moneyfmt(self.price)
        except:
            return u''

    def get_size(self):
        return u'%sx%s см' % (self.width, self.height)

    def get_published_features(self):
        featurevalues = self.get_feature_values().filter(is_show=True)
        return featurevalues

    def get_photos(self):
        return self.photo_set.all()

    def get_related_products(self):
        return self.related_products.published()

    def get_feature_values(self):
        return self.featurevalue_set.all()

    def get_comments(self):
        return self.comment_set.published()

    def get_raiting_stars(self):
        all_rating = Decimal(0)
        comments = self.get_comments()
        for comment in comments:
            all_rating += Decimal(comment.rating)
        all_rating = all_rating/comments.count()
        stars_set = []
        d2 = (all_rating % 1)
        d1 = int(all_rating - d2)

        for i in range(0,d1):
            stars_set.append(u'<span class="rating_all"></span>')
        if d2>=0.5:
            stars_set.append(u'<span class="rating_pol"></span>')
        leng = 5-len(stars_set)
        for i in range(0,leng):
            stars_set.append(u'<span class="rating_non"></span>')
        return ''.join(stars_set)

    def get_short_url(self):
        return u'%s/' % (self.id)

    def admin_photo_preview(self):
        image = self.image
        if image:
            im = get_thumbnail(self.image, '96x96', crop='center', quality=99)
            return u'<span><img src="%s" width="96" height="96"></span>' % im.url
        else:
            return u'<span></span>'

    admin_photo_preview.allow_tags = True
    admin_photo_preview.short_description = u'Превью'


class Photo(models.Model):
    product = models.ForeignKey(Product, verbose_name=u'Товар')
    image = ImageField(verbose_name=u'Картинка', upload_to=file_path_Product)
    order = models.IntegerField(verbose_name=u'Порядок сортировки', default=10)

    class Meta:
        verbose_name = _(u'product_photo')
        verbose_name_plural = _(u'product_photos')
        ordering = ['-order', ]

    def __unicode__(self):
        return u'Фото товара %s' % self.product.title


class FeatureName(models.Model):
    title = models.CharField(verbose_name=u'название', max_length=400)

    # Managers
    objects = PublishedManager()

    class Meta:
        verbose_name = _(u'featurename_item')
        verbose_name_plural = _(u'featurename_items')

    def __unicode__(self):
        return self.title


class FeatureValue(models.Model):
    product = models.ForeignKey(Product, verbose_name=u'Товар')
    feature_name = models.ForeignKey(FeatureName, verbose_name=u'название характеристики', )
    value = models.CharField(verbose_name=u'значение', max_length=500)
    order = models.IntegerField(verbose_name=u'Порядок сортировки', default=10)
    is_show = models.BooleanField(verbose_name=u'отображать значение харакеристики в списке товаров', default=False)

    class Meta:
        verbose_name = _(u'featurevalue_item')
        verbose_name_plural = _(u'featurevalue_items')
        ordering = ['-order', ]

    def __unicode__(self):
        return self.value


class Comment(models.Model):
    product = models.ForeignKey(Product, verbose_name=u'Товар')
    name = models.CharField(max_length=150, verbose_name=u'Имя')
    text = models.TextField(verbose_name=u'комментарий')
    email = models.CharField(verbose_name=u'E-mail', max_length=75, blank=True)
    rating = models.IntegerField(verbose_name=u'Рейтинг', default=5)
    pub_date = models.DateTimeField(verbose_name=u'Дата', default=datetime.datetime.now)
    is_published = models.BooleanField(verbose_name=u'Опубликовано', default=False)

    # Managers
    objects = PublishedManager()

    class Meta:
        verbose_name = _(u'comment')
        verbose_name_plural = _(u'comments')
        ordering = ['-pub_date']

    def __unicode__(self):
        return u'комментарий от %s' % self.pub_date

    def get_raiting_stars(self):
        stars_set = []
        for i in range(0,5):
            if i>=int(self.rating):
                stars_set.append(u'<span class="rating_non"></span>')
            else:
                stars_set.append(u'<span class="rating_all"></span>')
        return ''.join(stars_set)