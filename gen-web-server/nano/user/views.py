from random import choice, sample
import string

from django.utils.timezone import now as tznow
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template.defaultfilters import slugify

from nano.tools import pop_error, get_profile_model, asciify
from nano.user.forms import SignupForm, PasswordChangeForm, PasswordResetForm
from nano.user import new_user_created


import logging
_LOG = logging.getLogger(__name__)

class NanoUserError(Exception):
    pass

class NanoUserExistsError(NanoUserError):
    pass

# def pop_error(request):
#     error = request.session.get('error', None)
#     if 'error' in request.session:
#         del request.session['error']
#     return error
def store_picture(pic):
    with open('/var/www/pics/' + pic.name ,'wb') as dest:
        print 'trying to write file'
        for chunk in pic.chunks():
            dest.write(chunk)


def random_password():
    sample_space = string.letters + string.digits + r'!#$%&()*+,-.:;=?_'
    outlist = []
    for i in xrange(1,8):
        chars = sample(sample_space, 2)
        outlist.extend(chars)
    return ''.join(outlist)

def make_user(firstName, lastName, username, password, email=None, request=None):
    User = get_user_model()
    try:
        User.objects.get(username=username)
    except User.DoesNotExist:
        # make user
        user = User(username=username[:30])
        user.set_password(password)
        user.first_name = firstName
        user.last_name = lastName
        user.is_staff = False
        user.is_superuser = False
        user.is_active = True
        if email:
            user.email = email
        user.save()
        ''' 
        # Create profile
        Profile = get_profile_model(raise_on_error=False)
        if Profile:
            profile = Profile(user=user, username=username)
            profile.save()
        '''
        # Don't signal creation of test users
        test_users = getattr(settings, 'NANO_USER_TEST_USERS', ())
        for test_user in test_users:
            if user.username.startswith(test_user):
                break
        else:
            new_user_created.send(sender=User, user=user) 
        if request is not None:
            infomsg = u"You're now registered, as '%s'" % username
            messages.info(request, infomsg)
            _LOG.debug('Created user: %s/%s' % (user, user.check_password(password)))
        return user
    else:
        raise NanoUserExistsError("The username '%s' is already in use by somebody else" % username)

def signup(request, template_name='signup.html', *args, **kwargs):
    me = 'people'
    error = pop_error(request)
    data = {
            'me': me,
            'error': '',
            'form': SignupForm()
    }
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        print 'testing'
        print request.FILES
        print form.errors
        if form.is_valid():
            print 'testing'
            username = asciify(form.cleaned_data['username'])
            password = form.cleaned_data['password2']
            email = form.cleaned_data['email'].strip() or ''
            firstName = asciify(form.cleaned_data['first'])
            lastName = asciify(form.cleaned_data['last'])
            store_picture(request.FILES['picture'])


            # check that username not taken
            userslug = slugify(username)
            Profile = get_profile_model(raise_on_error=False)
            if Profile.objects.filter(username=userslug).count():
                data['error'] = u'Username "{}" is taken'.format(userslug)
                # error!
                #return HttpResponseRedirect('user:signup')
                '''
                safe_username = slugify('%s-%s' % (username, str(tznow())))
                changed_warningmsg = errormsg + ", changed it to '%s'."
                messages.warning(request, changed_warningmsg % (username, safe_username))
                username = safe_username
                '''
            # make user
            else:
                try:
                    user = make_user(firstName, lastName,username, password, email=email, request=request)
                except NanoUserExistsError:
                    next_profile = Profile.objects.get(user=user).get_absolute_url()
                    return HttpResponseRedirect(next_profile)
                else:
                    # fake authentication, avoid a db-lookup/thread-trouble/
                    # race conditions
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    _LOG.debug('Attempting login of: %s' % user)
                    login(request, user)
                    nexthop = getattr(settings, 'NANO_USER_SIGNUP_NEXT', reverse('user:nano_user_signup_done'))
                    '''
                    try:
                        nexthop_profile = Profile.objects.get(user=user).get_absolute_url()
                        return HttpResponseRedirect(nexthop_profile)
                    except Profile.DoesNotExist:
                        pass
                    '''
                    return HttpResponseRedirect(nexthop)
                _LOG.debug('Should never end up here')
    return render(request, template_name, data)

@login_required
def password_change(request, *args, **kwargs):
    error = pop_error(request)
    template_name = 'password_change_form.html'
    if request.method == "POST":
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data[u'password2']
            user = request.user
            user.set_password(password)
            user.save()
            request.session['error'] = None
            return HttpResponseRedirect('/password/change/done/')
    else:
        form = PasswordChangeForm()
    data = { 'form': form,
            'error': error,}
    return render(request, template_name, data)

def password_reset(request, project_name='Nano', *args, **kwargs):
    User = get_user_model()
    error = pop_error(request)
    template = 'password_reset_form.html'
    e_template = 'password_reset.txt'
    help_message = None
    e_subject = '%s password assistance' % project_name
    e_message = """Your new password is: 

%%s

It is long deliberately, so change it to 
something you'll be able to remember.


%s' little password-bot
""" % project_name
    e_from = getattr(settings, 'NANO_USER_EMAIL_SENDER', '')
    form = PasswordResetForm()
    if e_from and request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user = get_object_or_404(User, username=form.cleaned_data['username'])
            if user.email:
                tmp_pwd = random_password()
                user.set_password(tmp_pwd)
                result = send_mail(subject=e_subject, from_email=e_from, message=e_message % tmp_pwd, recipient_list=(user.email,))
                user.save()
                request.session['error'] = None
                return HttpResponseRedirect('/password/reset/sent/')
            else:
                error = """There's no email-address registered for '%s', 
                        the password can't be reset.""" % user.username
                request.session['error'] = error
                
    data = {'form': form,
            'help_message': help_message,
            'error':error}
    return render(request, template, data)

