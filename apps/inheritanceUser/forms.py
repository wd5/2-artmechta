# -*- coding: utf-8 -*-
from django import forms
from apps.inheritanceUser.models import CustomUser
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

try:
    from PIL import Image
except ImportError:
    import Image

attrs_dict = { 'class': 'required', 'required': True }


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs=attrs_dict), label=_(u'username'))
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                maxlength=75)), label=_(u'email address'))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                label=_(u'password'))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                label=_(u'password (again)'))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

    def clean_email(self):
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_(u'Этот e-mail уже зарегистрирован на сайте. Пожалуйста введите другой e-mail или авторизуйтесь на сайте.'))
        return self.cleaned_data['email']

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.

        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(u'Пароли не совпадают')
        return self.cleaned_data

class ProfileForm(forms.ModelForm):
    id = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'required':'required',
            }
        ),
        required=True
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'required':'required',
            }
        ),
        required=True
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'required':'required',
            }
        ),
        required=True
    )
    third_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'required':'required',
            }
        ),
        required=True
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'required':'required',
            }
        ),
        required=True
    )
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                #'required':'required',
            }
        ),
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'third_name', 'email', 'phone',)

    def save(self, commit=True):
        user = super(ProfileForm, self).save()
        if user:
            user.username = user.email
            user.save()
