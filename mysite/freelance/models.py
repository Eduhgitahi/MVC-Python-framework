from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.html import format_html
from polymorphic.models import PolymorphicModel
import string
import random

def id_generator(size=6,chars=string.ascii_uppercase + string.digits):
		return ''.join(random.choice(chars) for _ in range(size))



class Document(models.Model):
	MAYBECHOICE = (
    (1,'Yes'),
    (2,'No'),
)
	Choice=(
		('Yes'),
    	('No'),
		)

	Title = models.CharField(max_length=255,blank=False)
	due_date = models.DateTimeField(max_length=255,blank=True)
	timer = models.TimeField(max_length=20,blank=False,default='12:00')
	writer_email = models.EmailField(blank=True)
	attachment = models.FileField(upload_to='freelance',blank=False,null=False)
	Number_of_pages = models.IntegerField(blank=True,default=3)
	cost = models.FloatField(max_length=255,blank=True)
	Message = models.CharField(max_length=255,blank=False)
	Accepted_status = models.CharField(max_length=3, choices=MAYBECHOICE,default=2)
	status = models.BooleanField(max_length=10,default=1)
	created_at = models.DateTimeField()
	order_number = models.AutoField(primary_key=True)	
	user_id = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
	urlhash = models.CharField(max_length=6,blank=True,null=True,verbose_name="Reference Number")

	def __unicode__(self):
		return self.Title
		

class Writer(models.Model):
	Title = models.CharField(max_length=255,blank=False)
	client_email = models.EmailField(blank=True)
	attachment = models.FileField(upload_to='freelance',blank=False,null=False)
	description = models.CharField(max_length=255,blank=True)
	created_at = models.DateTimeField()
	order_number =  models.AutoField(primary_key=True)
	urlhash = models.CharField(max_length=6,blank=True,null=True,verbose_name="Reference Number")
	Number_of_pages = models.IntegerField(blank=True,default=3)
	status = models.NullBooleanField(max_length=10,default=1)
	user_id = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
	

	def __unicode__(self):
		return self.Title

class client_cost(models.Model):
	Username = models.CharField(max_length=255,blank=False,verbose_name="Writer's username",default="Name")
	writer_email = models.EmailField(blank=True)
	client_id = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
	total = models.FloatField(max_length=255,default = 0,verbose_name="Current earnings")
	created_at = models.DateTimeField(default="2018-04-04 12:00:00",verbose_name="Last updated")
	paid = models.FloatField(max_length=255,default = 0,verbose_name="Amount paid")
	Balance = models.FloatField(max_length=255,default = 0)

	def __unicode__(self):
		return self.Username

class circle(models.Model):
	Username = models.CharField(max_length=255,blank=False,verbose_name="Writer's username",default="Name")
	client_id = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
	created_at = models.DateTimeField(default="2018-04-04 12:00:00",verbose_name="Last updated")
	status = models.NullBooleanField(max_length=10,default=0)
	cstatus = models.NullBooleanField(max_length=10,default=0)
	wstatus = models.NullBooleanField(max_length=10,default=0)

	def __unicode__(self):
		return self.Username


