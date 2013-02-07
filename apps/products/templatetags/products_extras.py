# -*- coding: utf-8 -*-
from django import template
from django.db.models import Q
from string import split
from apps.inheritanceUser.models import Favorites, CustomUser
from apps.products.models import *
from apps.products.views import GetFavorites

register = template.Library()


@register.inclusion_tag("products/block_footer_categories.html")
def block_footer_categories():
    footer_pic = ['/media/img/pic_zs.png','/media/img/glass_zs.png']
    categories = Category.objects.filter(is_published=True, parent=None, is_footer_menu=True)
    return {'categories': categories, 'footer_pic':footer_pic}

@register.inclusion_tag("products/block_categories_menu.html")
def block_categories_menu(id_cat):
    menu = Category.objects.filter(is_published=True, parent=None)
    try:
        current = Category.objects.get(is_published=True, id=id_cat)
    except:
        current = False
    if current:
        if current.parent:
            parent_id = current.parent.id
            child_id = current.id
        else:
            parent_id = current.id
            child_id = False
    else:
        parent_id = False
        child_id = False

    return {'menu': menu, 'parent_id': parent_id, 'child_id':child_id }

@register.inclusion_tag("products/block_fav_products.html", takes_context=True)
def block_fav_products(context):
    if 'request' in context:
        request = context['request']
        path = request.path
        fav = GetFavorites(request)
    else:
        fav = False
        path = ''
    if fav:
        count = fav.fav_products.count()
    else:
        count = False
    return {'count': count, 'path':path}