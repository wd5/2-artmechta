# -*- coding: utf-8 -*-
from django import forms
from models import Comment

class CommentForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'placeholder':'E-mail'
            }
        ),
        required=False
    )
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'required':'required',
                'placeholder':'Имя'
            }
        ),
        required=True
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'required':'required',
                'placeholder':'Текст отзыва'
            }
        ),
        required=True
    )

    class Meta:
        model = Comment
        exclude = ('pub_date','is_published','email')