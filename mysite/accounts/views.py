# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.shortcuts import render,redirect
from django.contrib.sessions.backends.base import SessionBase
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie
from payments.models import payment
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import (
authenticate,
get_user_model,
login,
logout,
	)
from .forms import UserLoginForm,MyRegistrationForm,PasswordResetForm
# Create your views here.
@csrf_protect
@ensure_csrf_cookie
def login_view(request):
	if request.method =='POST':
		form = UserLoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get("username")
			password = form.cleaned_data.get("password")
			user = authenticate(username=username,password=password)
			login(request, user)
			if not payment.objects.filter(user_id=request.user).exists():	
				payment.objects.create(user_id=request.user,Amount=0.0,email=request.user.email,updated_at=timezone.now())
			else:
				pass

			if user.groups.filter(name='Writer').exists():
				return HttpResponseRedirect('/site/w/')
			if user.groups.filter(name='Client').exists():
				return HttpResponseRedirect('/site/')
		else:
			messages.success(request, 'Sorry we have a problem !')
			return render(request,'accounts/login1.html',{"form":form})

	else:
		form = UserLoginForm()
		args = {'form':form}
		args.update(csrf(request))
		args['form'] = UserLoginForm()
		return render(request,'accounts/login1.html',args)

@csrf_protect
@ensure_csrf_cookie
def register_view(request):
	if request.method =='POST':
		form = MyRegistrationForm(request.POST)  
		if form.is_valid():
			user = (form.save(commit=False))
			user.is_active = False
			user.save()
			group = form.cleaned_data.get('group')
			user.groups.add(group)
			current_site = get_current_site(request)
			message = render_to_string('accounts/activate-email.html',{
			'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': account_activation_token.make_token(user),
            })
			mail_subject = 'Activate your freelance account.'
			to_email = form.cleaned_data.get('email')
			email = EmailMessage(mail_subject,message, to=[to_email])
			email.send()
			return redirect('/success/')
			return HttpResponse('Please confirm your email address to complete the registration')
		else:
			messages.success(request, 'Sorry we have a problem!')
			return render(request,'accounts/sign.html',{"form":form})

	else:
		form = MyRegistrationForm()
		args = {'form':form}
		args.update(csrf(request))
		args['form'] = MyRegistrationForm()
		return render(request,'accounts/sign.html',args)
def success(request):
	return render_to_response('accounts/success.html')
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        return render(request,'accounts/valid.html')
    else:
    	return render(request,'accounts/invalid.html')
@csrf_protect
def logout_page(request):
	user = User.objects.get(username='username')
	[s.delete() for s in Session.objects.all() if s.get_decoded().get('_auth_user_id') == user.id]
	logout(request,user)
	return HttpResponseRedirect('/accounts/login/')
@csrf_protect
def forgot_view(request):
	return render(request,'accounts/forgot-password.html')
@csrf_protect
def reset_view(request):
	form = PasswordResetForm(request.POST or None)
	if form.is_valid():
		return render(request,"accounts/referal.html")
	else:
		return render(request,'accounts/forgot-password.html',{"form":form})
def refer_view(request):
	return render(request, 'accounts/referal.html')
