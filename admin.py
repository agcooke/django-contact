from django import forms
from django.contrib import admin
from django.db import models
from django_contact.models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ('user',)

admin.site.register(Contact, ContactAdmin)
