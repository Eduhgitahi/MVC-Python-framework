# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.html import format_html
from polymorphic.models import PolymorphicModel
import string
import random

class payment(models.Model):
	email = models.EmailField(default="user.email.ac.ke")
	user_id = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
	Amount = models.FloatField(max_length=30,default = 0.0)
	updated_at = models.DateTimeField(default="2018-04-04 12:00:00")

class transaction(models.Model):
	sender = models.EmailField(max_length=255,default="user@freelance.com")
	balance = models.FloatField(max_length=30,default=0.0)
	last_updated = models.DateTimeField(default="2018-04-04 12:00:00")
	receiver = models.CharField(max_length=30,default="receiver")
	user_id = models.ForeignKey(User,on_delete=models.CASCADE,default=2)
