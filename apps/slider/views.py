# -*- coding: utf-8 -*-
import datetime
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from apps.faq.forms import QuestionForm
from apps.faq.models import Question
from apps.utils.context_processors import custom_proc



def questions_list(request):
    questions = Question.objects.filter(published=True)

    faq_form = QuestionForm()

    return render_to_response(
            'faq/faq.html',
            {'questions':questions,
             'faq_form':faq_form,
             'menu_url': u'/faq/'
            },
            context_instance=RequestContext(request, processors=[custom_proc])
        )



@csrf_exempt
def send_question(request):
    if request.is_ajax:
        faq_form = QuestionForm(request.POST)
        if faq_form.is_valid():
            faq_form.save()
            return HttpResponse('success')
        else:
            faq_form_html = render_to_string(
                    'faq/faq_form.html',
                    {'faq_form':faq_form}
                )
            return HttpResponse(faq_form_html)
    else:
        return HttpResponseRedirect('/')
