# -*- coding: utf-8 -*-
from django import template
from django.db.models import Q
from string import split

register = template.Library()
from models import *
