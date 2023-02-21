from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from freelance.models import Document,Writer,client_cost
from django.forms.fields import TimeField
from django.contrib.auth import (
authenticate,
get_user_model,
logout,
	)

class DateInput(forms.DateTimeInput):
	input_type = 'date'

class TimeInput(forms.DateTimeInput):
	input_type = 'time'
	

class TaskForm(forms.ModelForm):
	Title = forms.CharField(label='Assignment Title:',max_length=200,required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
	due_date = forms.DateTimeField(label='Date due:',required=True,widget=DateInput())
	timer = forms.TimeField(required=True,widget=TimeInput())
	Number_of_pages=forms.IntegerField(label="Number of pages",widget=forms.TextInput(attrs={'class':'form-control'}))
	writer_email = forms.CharField(label="Writer's email:", required = True,max_length=30,widget=forms.TextInput(attrs={'multiple':True,'class':'form-control','name':'writer_email'}))
	attachment = forms.FileField(label="Attachment:",widget=forms.ClearableFileInput(attrs={'class':'form-control','multiple':"true",'name':'attachment'}))
	cost = forms.CharField(label="cost:", required =True,max_length=30,widget=forms.TextInput(attrs={'class':'form-control','name':'cost'}))
	Message = forms.CharField(label="Any Message?:", max_length=200,widget=forms.Textarea(attrs={'class':'form-control','name':'Message','rows':'4'}))
	class Meta:
		model = Document
		fields = ('Title','due_date','timer','writer_email','Number_of_pages','attachment','cost','Message')

	def clean_writer_email(self):
		writer_email = self.cleaned_data.get("writer_email")
		if writer_email=="":
			raise forms.ValidationError("Please enter the writer's email!")
		return writer_email

	def clean_cost(self):
		cost = self.cleaned_data.get("cost")
		if cost=="":
			raise forms.ValidationError("Please enter a number!")
		return cost

	def save(self, commit=True):
		Document = super(TaskForm,self).save(commit=False)
		if commit:
			Document.save()
		return Document

class SubmitForm(forms.ModelForm):
	Title = forms.CharField(label='Assignment Title:',max_length=200,required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
	client_email = forms.CharField(label="Client's email:", required = True,max_length=200,widget=forms.TextInput(attrs={'class':'form-control','name':'client_email'}))
	attachment = forms.FileField(label="Attachment:",widget=forms.ClearableFileInput(attrs={'class':'form-control','multiple':True,'name':'attachment'}))
	description = forms.CharField(label="Any Message?:", max_length=200,widget=forms.Textarea(attrs={'class':'form-control','name':'Message','rows':'4'}))
	urlhash = forms.CharField(label='Reference Number:',max_length=7,required=True,widget=forms.TextInput(attrs={'class':'form-control'}))

	class Meta:
		model = Writer
		fields = ('Title','urlhash','client_email','attachment','description')

	def clean(self,*args,**kwargs):
		email = self.cleaned_data.get("client_email")
		code = self.cleaned_data.get("urlhash")
		
		qs = Document.objects.filter(urlhash=code)
		use = User.objects.filter(email=email)		
		
		if not qs.exists():
			raise forms.ValidationError("This reference number does not exist.")
		if not use.exists():
			raise forms.ValidationError("This email does not exist.")
		else:
			if not Document.objects.filter(user_id=User.objects.get(email=email).pk).exists():
				raise forms.ValidationError("Please enter the correct email of the client.")		
		if not Document.objects.filter(urlhash=code,user_id=User.objects.get(email=email).pk).exists():
			raise forms.ValidationError("Please enter a reference number and email that matches the client's order you received.")

		return super(SubmitForm,self).clean(*args,**kwargs)
	
	def save(self, commit=True):
		Writer = super(SubmitForm,self).save(commit=False)
		if commit:
			Writer.save()
		return Writer

class JoinForm(forms.ModelForm):
	pass