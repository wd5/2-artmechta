# -*- coding: utf-8 -*-
from django import forms
from apps.orders.models import Order

class RegistrationOrderForm(forms.ModelForm):
    full_name = forms.CharField(error_messages={'required': 'Введите ФИО'}, widget=forms.TextInput(attrs={'class':'input1'}))
    email = forms.EmailField(error_messages={'required': 'Введите ваш e-mail'}, widget=forms.TextInput(attrs={'class':'input1'}))
    phone = forms.CharField(error_messages={'required': 'Введите ваш номер телефона'}, widget=forms.TextInput(attrs={'class':'input1'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class':'input2'}))
    note = forms.CharField(
        widget=forms.Textarea(
            #attrs={'class':'textarea1'}
        ),
        required=False
    )

    class Meta:
        model = Order
        exclude = ('create_date',)