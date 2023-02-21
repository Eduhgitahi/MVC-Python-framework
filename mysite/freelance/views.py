from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import user_passes_test  
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_protect
from freelance.models import Document,Writer,client_cost
from freelance.tables import DocumentTable,WriterTable,CostTable,DocumentTable1,WriterTable1,CostTable1,CircleTable,CircleTable1
from freelance.models import Document,Writer,circle
from freelance.forms import JoinForm
from payments.models import payment
from django.contrib.auth.models import User
from django_tables2 import RequestConfig
from django.template import Context
from django.contrib import messages
import datetime
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth import (
authenticate,
get_user_model,
login,
logout,
	)

class ReporterDetailView(DetailView):
    model = Writer

    def get_context_data(self, **kwargs):
        context = super(ReporterDetailView, self).get_context_data(**kwargs)
        return context


class ReporterDetailView1(DetailView):
    model = Document

    def get_context_data(self, **kwargs):
        context = super(ReporterDetailView1, self).get_context_data(**kwargs)
        return context

class ReporterDetailView2(DetailView):
    model = circle

    def get_context_data(self, **kwargs):
        context = super(ReporterDetailView2, self).get_context_data(**kwargs)
        return context

class ReporterDetailView3(DetailView):
    model = circle

    def get_context_data(self, **kwargs):
        context = super(ReporterDetailView3, self).get_context_data(**kwargs)
        return context

class ReporterDetailView4(DetailView):
    model = circle

    def get_context_data(self, **kwargs):
        context = super(ReporterDetailView4, self).get_context_data(**kwargs)
        return context

@csrf_protect
@ensure_csrf_cookie
@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Client').exists())
def index(request):
	now = datetime.datetime.now()
	take = DocumentTable1(Document.objects.all().filter(user_id = request.user).order_by('-created_at'))
	RequestConfig(request, paginate={"per_page": 10}).configure(take)
	no = len(Document.objects.filter(user_id=request.user,status=False))
	bal = payment.objects.values_list('Amount',flat=True).get(user_id=request.user)

	numb = len(Writer.objects.filter(client_email=request.user.email,status=False))
	return render(request, 'freelance/index.html',{
        'take': take,'no':no,'bal':bal,'numb':numb,'now':now
    },locals())

@csrf_protect
@ensure_csrf_cookie
@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Client').exists())    
def c_accept(request, pk):
	many = circle.objects.filter(id=pk).update(status=True,wstatus=True,cstatus=True,created_at=timezone.now())
	messages.success(request, 'Successfull! The writer exists in your circle now.')
	return HttpResponseRedirect('/site/yourcircles/')

@csrf_protect
@ensure_csrf_cookie
@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Writer').exists())    
def w_accept(request, pk):
	many = circle.objects.filter(id=pk).update(status=True,wstatus=True,cstatus=True,created_at=timezone.now())
	messages.success(request, 'Successfull! The client exists in your circle now.')
	return HttpResponseRedirect('/site/w/yourcircles/')


@csrf_protect
@ensure_csrf_cookie
@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Client').exists())    
def approve(request, pk):
	#selecteditem = get_object_or_404(Writer, pk=pk)
	B = Writer.objects.get(order_number=pk)
	B.status = True
	B.save()
	w = Writer.objects.values_list('user_id',flat=True).get(order_number=pk)
	u = User.objects.values_list('email',flat=True).get(id=w)
	v = User.objects.values_list('username',flat=True).get(id=w)
	e = Writer.objects.values_list('urlhash',flat=True).get(order_number=pk)
	c = Document.objects.values_list('cost',flat=True).filter(urlhash=e,user_id=request.user,writer_email=u).latest('created_at')
	many = Writer.objects.filter(urlhash=e).update(status=True) 
	if not client_cost.objects.filter(writer_email=u,client_id=request.user).exists():
		client_cost.objects.create(writer_email=u,client_id=request.user,Username=v,created_at=timezone.now(),total=0.0)
		cost = client_cost.objects.get(writer_email=u,client_id=request.user)
		cost.total = c
		cost.save()
	else:
		Bal = client_cost.objects.get(writer_email=u,client_id=request.user)
		x = client_cost.objects.values_list('total',flat=True).get(writer_email=u,client_id=request.user)
		A = c + x
		Bal.total = A
		Bal.created_at = timezone.now()
		Bal.save()

	return HttpResponseRedirect('/site/completed_orders/')


@csrf_protect
@ensure_csrf_cookie
@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Client').exists())    
def join(request,pk):
	k = User.objects.values_list('username',flat=True).get(pk=pk)
	if not circle.objects.filter(Username=k,client_id=request.user).exists():
		circle.objects.create(Username=k,client_id=request.user,status=False,created_at=timezone.now(),cstatus=True,wstatus=False)
		messages.success(request, 'Request sent')
	messages.success(request, 'Request already sent ,awaiting approval.')
	return HttpResponseRedirect('/site/circles/')
	
	
@csrf_protect
@ensure_csrf_cookie
@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Writer').exists())    
def accept(request, pk):
	B = Document.objects.get(order_number=pk)
	B.status = True
	B.save()
	r = Document.objects.values_list('urlhash',flat=True).get(order_number=pk)
	many = Document.objects.filter(urlhash=r).update(status=True)
	return HttpResponseRedirect('/site/w/new_requests/')


@csrf_protect
@ensure_csrf_cookie
@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Writer').exists())
def index2(request):
	now = datetime.datetime.now()
	table1 =WriterTable1(Writer.objects.all().filter(user_id = request.user).order_by('-created_at'))
	RequestConfig(request, paginate={"per_page": 5}).configure(table1)
	number = len(Writer.objects.filter(user_id=request.user,status=False))
	orders = len(Document.objects.filter(writer_email=request.user.email,status=False))
	balance = payment.objects.values_list('Amount',flat=True).get(user_id=request.user)
	return render(request, 'freelance/writers.html',{'table1': table1,'number':number,'orders':orders,'balance':balance,'now':now},locals())
	
@csrf_protect
@ensure_csrf_cookie
@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Client').exists())
def orders(request):
	now = datetime.datetime.now()
	table2 = WriterTable(Writer.objects.all().filter(client_email=request.user.email).order_by('-created_at'))
	RequestConfig(request, paginate={"per_page": 5}).configure(table2)
	return render(request,'freelance/new_orders.html',{'table2':table2,'now':now},locals())

@csrf_protect
@ensure_csrf_cookie
@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Writer').exists())
def requests(request):
	now = datetime.datetime.now()
	table3 = DocumentTable(Document.objects.all().filter(writer_email=request.user.email).order_by('-created_at'))
	RequestConfig(request, paginate={"per_page": 5}).configure(table3)
	bal = payment.objects.values_list('Amount',flat=True).get(user_id=request.user)
	return render(request,'freelance/new_orders2.html',{'table3':table3,'bal':bal,'now':now},locals())
@csrf_protect
@ensure_csrf_cookie
@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Client').exists())	
def search(request):
	if request.method=="POST":
		search_text = request.POST['search_text']
	else:
		search_text = ''

	articles =  Document.objects.all().filter(user_id = request.user,Title__icontains=search_text)
	return render(request,'freelance/ajax_search.html',{'articles':articles})

@csrf_protect
@ensure_csrf_cookie
@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Client').exists())	
def circles(request):
	now = datetime.datetime.now()
	bal = payment.objects.values_list('Amount',flat=True).get(user_id=request.user)
	return render(request, 'freelance/Indexuser.html',{'bal':bal,'now':now},locals())

@csrf_protect
@ensure_csrf_cookie
@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Writer').exists())	
def circles2(request):
	now = datetime.datetime.now()
	bal = payment.objects.values_list('Amount',flat=True).get(user_id=request.user)
	return render(request, 'freelance/Indexuserw.html',{'bal':bal,'now':now},locals())

@csrf_protect
@ensure_csrf_cookie
@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Writer').exists())	
def csearch(request):
	if request.method=="POST":
		search_text = request.POST['search_text']
	else:
		search_text = ''

	u = User.objects.all()
	arts =  u.filter(is_staff=False,groups__name='Client',username__icontains=search_text)
	return render(request,'freelance/ajax_search3.html',{'arts':arts})

@csrf_protect
@ensure_csrf_cookie
@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Writer').exists())    
def wjoin(request,pk):
	user = User.objects.get(id=pk)
	if not circle.objects.filter(Username=request.user.username,client_id=user).exists():
		circle.objects.create(Username=request.user.username,client_id=user,status=False,created_at=timezone.now(),cstatus=False,wstatus=True)
		messages.success(request, 'Request sent')
	messages.success(request, 'Request already sent ,awaiting approval.')
	return HttpResponseRedirect('/site/w/circles/')

@csrf_protect
@ensure_csrf_cookie
@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Writer').exists())    
def writercircle(request):
	now = datetime.datetime.now()
	bal1 = circle.objects.all().filter(Username=request.user.username)
	table1 =CircleTable1(bal1.order_by('-created_at'))
	RequestConfig(request, paginate={"per_page": 10}).configure(table1)
	bal = payment.objects.values_list('Amount',flat=True).get(user_id=request.user)
	return render(request, 'freelance/circle1.html',{'table1':table1,'bal':bal,'now':now},locals())



@csrf_protect
@ensure_csrf_cookie
@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Client').exists())	
def clientcircle(request):
	now = datetime.datetime.now()
	bal1 = circle.objects.all().filter(client_id=request.user)
	table1 =CircleTable(bal1.order_by('-created_at'))
	RequestConfig(request, paginate={"per_page": 10}).configure(table1)
	bal = payment.objects.values_list('Amount',flat=True).get(user_id=request.user)
	return render(request, 'freelance/circle.html',{'table1':table1,'bal':bal,'now':now},locals())



@csrf_protect
@ensure_csrf_cookie
@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Client').exists())	
def usearch(request):
	if request.method=="POST":
		search_text = request.POST['search_text']
	else:
		search_text = ''

	v = User.objects.all()
	articles =  v.filter(is_staff=False,groups__name='Writer',username__icontains=search_text)
	return render(request,'freelance/ajax_search2.html',{'articles':articles})



@csrf_protect
@ensure_csrf_cookie
@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Writer').exists())	
def search1(request):
	if request.method=="POST":
		search_text1 = request.POST['search_text1']
	else:
		search_text1 = ''

	h=Writer.objects.all()
	art =  h.filter(user_id = request.user,Title__icontains=search_text1)

	return render(request,'freelance/ajax_search1.html',{'art':art})

@csrf_protect
@ensure_csrf_cookie
@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Client').exists())	
def stats(request):
	now = datetime.datetime.now()
	tablestats = CostTable(client_cost.objects.all().filter(client_id=request.user))
	RequestConfig(request, paginate={"per_page": 10}).configure(tablestats)
	bal = payment.objects.values_list('Amount',flat=True).get(user_id=request.user)
	return render(request,'freelance/costing.html',{'tablestats':tablestats,'bal':bal,'now':now},locals())

@csrf_protect
@ensure_csrf_cookie
@user_passes_test(lambda u: u.groups.filter(name='Client').exists())
def notify(request):
	stat = request.POST['status']
	s = Document.objects.get(user_id=request.user)
	s.status = stat
	s.save(['status'])
	return HttpResponse('Yess you did it!!')
@csrf_protect
@ensure_csrf_cookie
@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Writer').exists())	
def earning(request):
	now = datetime.datetime.now()
	tablestats = CostTable1(client_cost.objects.all().filter(writer_email=request.user.email))
	bal = payment.objects.values_list('Amount',flat=True).get(user_id=request.user)
	RequestConfig(request, paginate={"per_page": 10}).configure(tablestats)
	return render(request,'freelance/costing1.html',{'tablestats':tablestats,'now':now,'bal':bal},locals())