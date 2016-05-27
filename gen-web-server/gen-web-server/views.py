from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from schedule.models import Calendar, Event
from forums.models import Category, Post
from nano.blog.models import Entry
from forms import EmailForm, ContactUsForm, UserSearchForm
from django.core.mail import send_mail
from commands import getoutput
from datetime import datetime
from pytz import timezone

def _get_future_events():
    future_events = []
    now = datetime.now(timezone('UTC'))
    all_events = Event.objects.all().order_by('start')
    for x in all_events:
        if x.start > now:
            future_events.append(x)
        if len(future_events)>2:
            return future_events
    return future_events

def index(request):
    calendars = Calendar.objects.all()
    blogs = Entry.objects.all()
    posts = Post.objects.order_by('updated')[::-1][:8]
    return render(request, 'index/index.html',
                {'calendar':Calendar.objects.first(),
                'events':_get_future_events(),
                             'posts':posts,
                             'blog_list':blogs})

def connect(request):
    if request.method == 'POST':
        email_form = EmailForm(request.POST)
        search_form = UserSearchForm(request.POST)
        email_form.is_valid()
        search_form.is_valid()
        address = email_form.cleaned_data['email']
        searched_user = search_form.cleaned_data['lastName']
        if address:
            data = getoutput('echo "{}" >> emails && echo "Complete!"'.format(address)).split('\n')
            return render(request, 'connect.html', {'email_form':email_form, 'email':True , 'data':data, 'search_form':search_form})
            pass
        elif searched_user:
            regUsers = User.objects.raw('SELECT * from auth_user where last_name like "%%{}%%";'.format(searched_user))
            return render(request, 'connect.html', {'email_form':email_form, 'regUsers':regUsers, 'search_form':search_form})
        else:
            return render(request, 'connect.html', {'email_form':email_form, 'search_form':search_form})
    else:
        email_form = EmailForm()
        search_form = UserSearchForm()
    return render(request, 'connect.html', {'email_form':email_form, 'search_form':search_form})

def profile(request):
    return render(request, 'profile.html') 

def contact(request):
    subject = 'JBC - Admin AUTO REPLY'
    body = 'Thank you for contacting the administrator, you will be contacted shortly concerning:\n\n'
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            msg = form.cleaned_data['message']
            #sending the email is in development
            #send_mail(subject,body+msg,'admin@jbc.org',[email]) 
            return render(request, 'thankyou.html', {'name':name, 'email':email })
    else:
        form = ContactUsForm()

    return render(request, 'contact.html', {'form':form})

