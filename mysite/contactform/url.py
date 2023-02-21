from contactform import views
from django.conf.urls import url,include

urlpatterns = [
url(r'^',views.success,name = 'success'),
]