from django import forms
from django.contrib.auth.models import User


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    website = forms.URLField(required=False)
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)