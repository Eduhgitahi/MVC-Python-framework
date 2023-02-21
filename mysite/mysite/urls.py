"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views
from django.contrib.auth.views import logout
from django.contrib.auth import views as auth_views
from accounts.views import (login_view, register_view,success,logout_page,reset_view,refer_view)
from payments.views import task,task2
from freelance.views import index2,orders,requests,search,search1,usearch,stats,notify,earning,circles,join,clientcircle,circles2,csearch,wjoin,writercircle
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from mysite import admin_auth
from django_private_chat import urls as django_private_chat_urls


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^', include('django.contrib.auth.urls')),  
    url(r'^', include('visitors.urls')),
    url(r'^contact/', include('contactform.urls')),
    url(r'^contact_success/', include('contactform.url')),
    url(r'^site/w/accept/(?P<pk>\d+)/edit/',include('freelance.ur')),
    url(r'^site/w/approve/(?P<pk>\d+)/edit/',include('freelance.acceptw')),
    url(r'^site/w/new_requests/$',requests,name='requests'),
    url(r'^site/', include('freelance.urls')),
    url(r'^site/w/earnings/$',earning,name='earning'),
    url(r'^site/w/search/$',search1,name='search1'),
    url(r'^site/w/submit_task/', task2,name="task2"),
    url(r'^site/w/circles/', circles2,name="circles2"),
    url(r'^site/w/csearch/$',csearch,name='csearch'),
    url(r'^site/w/join/(?P<pk>\d+)$',wjoin,name='wjoin'),
    url(r'^site/w/yourcircles/$',writercircle,name='writercircle'),
    url(r'^site/w/',index2,name="index2"),
    url(r'^site/payments/', include('payments.urls')),
    url(r'^site/create-task/', task,name="task"),
    url(r'^accounts/login/',login_view,name='login'),
    url(r'^logout/',logout_page,name='logout'),
    url(r'^register/',register_view,name='register'),
    url(r'^success/',success,name='success'),
    url(r'^reset/',reset_view,name='reset'),
    url(r'^refer/',refer_view,name='refer'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',include('accounts.urls')),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^site/completed_orders/$',orders,name='orders'),
    url(r'^site/notify/$',notify,name='notify'),
    url(r'^site/search/$',search,name='search'),
    url(r'^site/usearch/$',usearch,name='usearch'),
    url(r'^site/stats/$',stats,name='stats'),
    url(r'^site/circles/$',circles,name='circles'),
    url(r'^site/yourcircles/$',clientcircle,name='clientcircle'),
    url(r'^site/approve/(?P<pk>\d+)/edit/',include('freelance.url')),
    url(r'^site/accept/(?P<pk>\d+)/edit/',include('freelance.accept')),  
    url(r'^site/join/(?P<pk>\d+)$',join,name='join'),
    url(r'^notifications/', include('notify.urls', 'notifications')),
    url(r'^ken/', include('django_private_chat.urls')),
    ]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += staticfiles_urlpatterns()