from django.shortcuts import render
from contactform.forms import ContactForm
from django.core.mail import EmailMessage
from django.template import Context
from django.shortcuts import redirect
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect
# Create your views here.
@csrf_protect
def contact(request):
	form_class = ContactForm

	if request.method == 'POST':
		form = form_class(data = request.POST)
		if form.is_valid():
			contact_name = request.POST.get('contact_name','')
			contact_email = request.POST.get('contact_email','')
			form_content = request.POST.get('content','')

			template = get_template('contact_template.txt')
			context = {
				'contact_name':contact_name,
				'contact_email':contact_email,
				'form_content':form_content,
				}

			content = template.render(context)

			email = EmailMessage(
					"New contact form submission",
					content,
					"Your website" +'',
					['muriithiken0@gmail.com'],
					headers = {'Reply-to':contact_email})
			email.send()
			return redirect('/contact_success/')
		else:
			return render(request,'contactform/formpage.html',{'form':form_class,})

	return render(request,'contactform/formpage.html',{'form':form_class,})

def success(request):
	return render_to_response('contactform/success.html')