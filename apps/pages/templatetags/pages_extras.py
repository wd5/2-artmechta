# -*- coding: utf-8 -*-
from apps.pages.models import Page
from django import template
from apps.utils.utils import url_spliter

register = template.Library()

@register.inclusion_tag("pages/block_footer_pages_menu.html")
def block_footer_pages_menu():
    menu = Page.objects.filter(is_published = True, is_at_footer_menu = True)
    return {'menu': menu}

@register.inclusion_tag("pages/block_pages_menu.html")
def block_pages_menu(url):
    current = url_spliter(url,1)
    menu = Page.objects.filter(is_published = True, is_at_menu = True)
    return {'menu': menu, 'current': current}
