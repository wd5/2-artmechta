# -*- coding: utf-8 -*-
from apps.siteblocks.models import Settings
from settings import SITE_NAME

def settings(request):
    try:
        contacts = Settings.objects.get(name='contacts_block').value
    except Settings.DoesNotExist:
        contacts = False
    try:
        loaded_count = int(Settings.objects.get(name='loaded_count').value)
    except:
        loaded_count = 3

    return {
        'contacts': contacts,
        'site_name': SITE_NAME,
        'loaded_count': loaded_count,
    }