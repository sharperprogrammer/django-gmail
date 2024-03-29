# sendemail/views.py
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ContactForm
from django.conf import settings

def emailView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                # I am only specifying auth_user and auth_password here because I wanted
                # to make sure there wasn't some issue passing in the defaults from settings.py
                mailresult = send_mail(subject, "Sent from: " + from_email + "\n\n" + message, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            print(mailresult)
            return redirect('success')
    return render(request, "email.html", {'form': form})

def successView(request):
    return HttpResponse('Success! Thank you for your message.')
