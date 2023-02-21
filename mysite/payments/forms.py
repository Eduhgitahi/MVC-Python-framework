from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from payments.models import payment,transaction
from django.contrib.auth import (
authenticate,
get_user_model,
logout,
	)
User = get_user_model()
class TransactionForm(forms.ModelForm):
	receiver = forms.CharField(label='Enter username of recipient:',required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
	balance = forms.FloatField(label='Enter the amount',required=True,widget=forms.TextInput(attrs={'class':'form-control'}))

	class Meta:
		model = transaction
		fields = ('receiver','balance')


	def clean(self,*args,**kwargs):
		receiver = self.cleaned_data.get("receiver")
		bal = self.cleaned_data.get("balance")

		if not User.objects.filter(username=receiver):
			raise forms.ValidationError("Sorry, this user does not exist.")

		if not isinstance(bal, float):
			raise forms.ValidationError("Please enter a valid number.")

		#if payment.objects.values_list('Amount',flat=True).get(user_id=User.objects.get(username=request.user.username)) < bal:
			#raise forms.ValidationError("Please, enter an amount greater than your balance.")
		return super(TransactionForm,self).clean(*args,**kwargs)

	def clean_receiver(self):
		receiver = self.cleaned_data.get("receiver")
		if receiver=="":
			raise forms.ValidationError("Please enter a valid username!")
		return receiver

	def save(self, commit=True):
		transaction = super(TransactionForm,self).save(commit=False)
		if commit:
			transaction.save()
		return transaction