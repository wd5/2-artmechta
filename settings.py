# -*- coding: utf-8 -*-
DATABASE_NAME = u'artmechta'
PROJECT_NAME = u'artmechta'
SITE_NAME = u'ArtМечта'
DEFAULT_FROM_EMAIL = u'support@artmechta.octweb.ru'

from config.base import *

try:
    from config.development import *
except ImportError:
    from config.production import *

TEMPLATE_DEBUG = DEBUG

INSTALLED_APPS += (
    'apps.siteblocks',
    'apps.pages',
    #'apps.faq',
    'apps.slider',
    'apps.products',
    #'apps.newsboard'
    'apps.orders',
    'apps.inheritanceUser',



    'sorl.thumbnail',
    #'south',
    #'captcha',
)

MIDDLEWARE_CLASSES += (
    'apps.pages.middleware.PageFallbackMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'apps.auth_backends.CustomUserModelBackend',
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'apps.pages.context_processors.meta',
    'apps.siteblocks.context_processors.settings',
    'apps.utils.context_processors.authorization_form',
)