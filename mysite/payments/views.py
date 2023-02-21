from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from freelance.forms import TaskForm,SubmitForm
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_protect
from freelance.models import Document,Writer,client_cost
from payments.models import payment,transaction
from payments.forms import TransactionForm
from django.contrib.auth.models import User
from datetime import datetime 
from django.contrib import messages
from django.core.exceptions import ValidationError
import string
import random
from django.db.models import Avg
from django.utils import timezone
from django.contrib.auth import (
authenticate,
get_user_model,
login,
logout,
	)

@login_required(login_url='/accounts/login/')
@csrf_protect
@ensure_csrf_cookie
def pay(request):
	bal = payment.objects.values_list('Amount',flat=True).get(user_id=request.user)
	if request.method=="POST":
		form = TransactionForm(request.POST)
		if form.is_valid():
			receiver = form.cleaned_data['receiver']
			balance = form.cleaned_data['balance']
			amount = payment.objects.values_list('Amount',flat=True).get(user_id=request.user)	
			if amount > 0 and balance < amount:
				am = amount - balance
				A = payment.objects.get(user_id=request.user)
				A.Amount=am
				A.save()
				if not payment.objects.filter(user_id=User.objects.get(username=receiver).pk).exists():	
					payment.objects.create(user_id=User.objects.get(username=receiver),Amount=0.0,email=User.objects.get(username=receiver).email,updated_at=timezone.now())
					bal = payment.objects.values_list('Amount',flat=True).get(user_id=User.objects.get(username=receiver).pk)
					b = balance + bal
					B = payment.objects.get(user_id=User.objects.get(username=receiver).pk)
					B.Amount=b
					B.save()				
				else:
					bal = payment.objects.values_list('Amount',flat=True).get(user_id=User.objects.get(username=receiver).pk)
					b = balance + bal
					B = payment.objects.get(user_id=User.objects.get(username=receiver).pk)
					B.Amount=b
					B.save()
			else:
				messages.info(request, 'The amount you entered is greater than your balance.')
				return render(request, 'freelance/payments.html',{"form":form,'bal':bal})

			transaction.objects.create(receiver=receiver,balance=balance,sender=request.user.email,last_updated =timezone.now())
			return HttpResponseRedirect('/site/')
			messages.info(request, 'The funds were sent successfully.')
		else:
			return render(request, 'freelance/payments.html',{"form":form,'bal':bal})
	else:
		form = TransactionForm()
		args = {'form':form,'bal':bal}
		args.update(csrf(request))
		args['form'] = TransactionForm()
		return render(request, 'freelance/payments.html',args)

def id_generator(size=6,chars=string.ascii_uppercase + string.digits):
		return ''.join(random.choice(chars) for _ in range(size))


@login_required(login_url='/accounts/login/')
@csrf_protect
@ensure_csrf_cookie
def task(request):
	bal = payment.objects.values_list('Amount',flat=True).get(user_id=request.user)
	if request.method=="POST":
		form = TaskForm(request.POST , request.FILES)
		
		if form.is_valid():
			c = form.cleaned_data['cost']
			m = form.cleaned_data['Message']
			t = form.cleaned_data['Title']
			d = form.cleaned_data['due_date']
			w = form.cleaned_data['writer_email']
			r = form.cleaned_data['timer']
			e = datetime.combine(d,r)
			v = id_generator()

			if Document.objects.filter(urlhash=v).exists():
				v = id_generator()
				for f in request.FILES.getlist("attachment"):
					Document.objects.create(attachment=f,user_id = request.user,created_at=timezone.now(),writer_email=w,due_date=e,timer=r,cost=c,Message=m,Title=t,urlhash=v)
					#client_cost.objects.create(writer_email=w,client_id=request.user,cost=c)
			else:
				for f in request.FILES.getlist("attachment"):
					Document.objects.create(attachment=f,user_id = request.user,created_at=timezone.now(),writer_email=w,due_date=e,timer=r,cost=c,Message=m,Title=t,urlhash=v)
					

			return HttpResponseRedirect('/site/')
			messages.success(request, 'The assignment was sent successfully.')
		else:
			return render(request, 'freelance/tasks.html',{"form":form,'bal':bal})
	else:			
		form = TaskForm()
		args = {'form':form,'bal':bal}
		args.update(csrf(request))
		args['form'] = TaskForm()
		return render(request,'freelance/tasks.html',args)

@login_required(login_url='/accounts/login/')
@csrf_protect
@ensure_csrf_cookie
def task2(request):
	bal = payment.objects.values_list('Amount',flat=True).get(user_id=request.user)
	if request.method=="POST":
		form = SubmitForm(request.POST , request.FILES)
		if form.is_valid():
			T = form.cleaned_data['Title']
			c = form.cleaned_data['client_email']
			d = form.cleaned_data['description']
			e = form.cleaned_data['urlhash']
			for f in request.FILES.getlist("attachment"):
				Writer.objects.create(attachment=f,Title=T,client_email=c,description=d,user_id=request.user,created_at=timezone.now(),urlhash=e)
			return HttpResponseRedirect('/site/w/')
		else:
			return render(request, 'freelance/task3.html',{"form":form,'bal':bal})
	else:			
		form = SubmitForm()
		args = {'form':form,'bal':bal}
		args.update(csrf(request))
		args['form'] = SubmitForm()
		return render(request, 'freelance/task3.html',args)
