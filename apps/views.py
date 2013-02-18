# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from apps.slider.models import InteriorPhoto


class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            self.template_name = 'siteblocks/interiorPhotos_template.html'
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(IndexView,self).get_context_data(**kwargs)
        interiorPhotos = InteriorPhoto.objects.published()
        context['interiorPhotos'] = interiorPhotos
        context['interiorPhotos_count'] = interiorPhotos.count()
        return context

index = IndexView.as_view()