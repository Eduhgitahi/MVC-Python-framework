from contactform import views
from django.conf.urls import url,include

urlpatterns = [
url(r'^',views.contact,name = 'contact'),
]