import logging.handlers
import datetime
import os
import sys
import random
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Contact(models.Model):
    user = models.ForeignKey(User, help_text='This is the person who will be receiving emails from the website contact.')

    def __unicode__(self):
        return self.user.username

    # for now set up as a singleton
    def save(self):
        self.id = 1
        super(Contact, self).save()

    def delete(self):
        pass

