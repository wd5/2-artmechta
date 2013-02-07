# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from apps.slider.models import InteriorPhoto


class IndexView(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super(IndexView,self).get_context_data(**kwargs)
        context['interiorPhotos'] = InteriorPhoto.objects.published()[:9]
        return context

index = IndexView.as_view()