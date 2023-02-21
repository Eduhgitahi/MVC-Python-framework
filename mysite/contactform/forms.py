from django import forms

class ContactForm(forms.Form):
	contact_name = forms.CharField(required = True,label="Your Name", max_length=30,widget=forms.TextInput(attrs={'class':'form-control','name':'Name'}))
	contact_email = forms.EmailField(required  = True,label="Your Email", max_length=50,widget=forms.TextInput(attrs={'class':'form-control','name':'Email'}))
	content = forms.CharField(required = True,label="Type Your Message",widget = forms.Textarea(attrs={'class':'form-control','name':'Message'}))
	
	def __init__(self,*args,**kwargs):
		super(ContactForm,self).__init__(*args,**kwargs)
		self.fields['contact_name']
		self.fields['contact_email']
		self.fields['content']