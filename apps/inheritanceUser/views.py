# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from pytils.numeral import choose_plural
from apps.products.models import Product
import  settings
from django.http import   HttpResponseRedirect, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.views.generic import FormView, TemplateView, View
from apps.inheritanceUser.forms import ProfileForm, RegistrationForm
from apps.inheritanceUser.models import CustomUser, Favorites
from apps.orders.models import Order
from django.core.urlresolvers import reverse
from django.contrib.auth import  authenticate as auth_check, login as auth_login

def send_email_registration(username, password, to_email):
    from django.core.mail import send_mail

    subject = u'Регистрация на сайте – %s' % settings.SITE_NAME
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())

    message = render_to_string('users/registration_email.txt',
            {
            'username': username,
            'password': password,
            'SITE_NAME': settings.SITE_NAME
        })

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [to_email])


class RegistrationFormView(FormView):
    form_class = RegistrationForm
    template_name = 'users/registration.html'

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        data['username'] = data['email']
        reg_form = RegistrationForm(data)
        if reg_form.is_valid():
            new_user = CustomUser.objects.create_user(data['username'], data['email'], data['password1'])
            new_user.is_active = True
            new_user.save()

            send_email_registration(username=new_user.username, password=data['password1'], to_email=new_user.email)

            user = auth_check(username=request.POST['email'], password=request.POST['password1'])
            try:
                if data['order_id']:
                    try:
                        order = Order.objects.get(id=int(data['order_id']))
                    except:
                        order = False

                    if order:
                        order.profile = new_user
                        new_user.first_name = order.first_name
                        new_user.last_name = order.last_name
                        new_user.phone = order.phone
                        new_user.save()
                        order.save()
            except:
                pass

            if user is not None:
                auth_login(request, user)
                return HttpResponseRedirect('/cabinet/')
            return HttpResponseRedirect('/category/')
        else:
            return render_to_response('users/registration.html',
                    {'reg_form': reg_form, 'request': request, 'user': request.user})

    def get(self, request, **kwargs):
        if self.request.user.is_authenticated and self.request.user.id:
            return HttpResponseRedirect(reverse('index'))
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(RegistrationFormView, self).get_context_data()
        context['reg_form'] = self.form_class()
        return context

registration_form = RegistrationFormView.as_view()

class ShowProfileForm(FormView):
    form_class = ProfileForm
    template_name = 'users/profile_form.html'

    def get(self, request, **kwargs):
        if self.request.user.is_authenticated and self.request.user.id:
            pass
        else:
            return HttpResponseRedirect(reverse('index'))
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(ShowProfileForm, self).get_context_data()
        if self.request.user.is_authenticated and self.request.user.id:
            context['profile_form'] = self.form_class(initial={'id': self.request.user.id,
                                                               'name': self.request.user.name,
                                                               'last_name': self.request.user.last_name,
                                                               'user__email': self.request.user.email,
                                                               'phone': self.request.user.phone})
        return context

show_profile_form = ShowProfileForm.as_view()

class ShowCabinetView(TemplateView):
    template_name = 'users/cabinet.html'

    def get(self, request, **kwargs):
        if self.request.user.is_authenticated and self.request.user.id:
            pass
        else:
            return HttpResponseRedirect(reverse('index'))
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(ShowCabinetView, self).get_context_data()
        #context['???????'] = ???
        return context

show_cabinet = ShowCabinetView.as_view()


# AJAX

class AddProductToFavorite(View):
    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseRedirect('/')
        else:
            if 'product_id' not in request.POST:
                return HttpResponseBadRequest()
            count = 0
            try:
                product = Product.objects.get(id=int(request.POST['product_id']))
            except:
                return HttpResponseBadRequest()

            if request.user.is_authenticated and request.user.id:
                profile_id = request.user.id
                profile = CustomUser.objects.get(id=profile_id)
            else:
                profile = False

            response = HttpResponse()
            sessionid = request.session.session_key
            cookies = request.COOKIES
            artmechta_fav_id = False
            if 'artmechta_fav_id' in cookies:
                artmechta_fav_id = cookies['artmechta_fav_id']

            if profile:
                try:
                    fav = Favorites.objects.get(profile=profile)
                except Favorites.DoesNotExist:
                    if artmechta_fav_id:
                        try:
                            fav = Favorites.objects.get(id=artmechta_fav_id)
                            if fav.profile:
                                if profile:
                                    fav = Favorites.objects.create(profile=profile)
                                else:
                                    return HttpResponseBadRequest()
                            else:
                                if profile:
                                    fav.profile = profile
                                    fav.save()
                                else:
                                    return HttpResponseBadRequest()
                        except:
                            if profile:
                                fav = Favorites.objects.create(profile=profile)
                            else:
                                return HttpResponseBadRequest()
                    else:
                        fav = Favorites.objects.create(profile=profile)
            elif artmechta_fav_id:
                try:
                    fav = Favorites.objects.get(id=artmechta_fav_id)
                except Favorites.DoesNotExist:
                    fav = Favorites.objects.create(sessionid=sessionid)
            else:
                try:
                    fav = Favorites.objects.get(sessionid=sessionid)
                except Favorites.DoesNotExist:
                    fav = Favorites.objects.create(sessionid=sessionid)


            if fav:
                response.set_cookie('artmechta_fav_id', fav.id, 1209600)
                try:
                    fav_products = fav.fav_products.all()

                    if product in fav_products:
                        fav.fav_products.remove(product)
                    else:
                        fav.fav_products.add(product)
                    fav.save()
                    count = fav.fav_products.count()
                except:
                    return HttpResponseBadRequest()
            response.content = u'%s предмет%s|%s товар%s' % (count, choose_plural(count, (u'', u'а', u'ов')),count, choose_plural(count, (u'', u'а', u'ов')))
            return response

add_product_to_favorite = csrf_exempt(AddProductToFavorite.as_view())