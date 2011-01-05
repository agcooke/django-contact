from django.conf.urls.defaults import *
from django.contrib.sitemaps import FlatPageSitemap
from django.contrib.sitemaps import GenericSitemap
from django_contact.models import Contact
urlpatterns = patterns('',
                       (r'^contact', 'django_contact.views.contact'),
                       )