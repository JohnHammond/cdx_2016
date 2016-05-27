from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse

import logging
_LOG = logging.getLogger(__name__)

from nano.tools import pop_error
from nano.privmsg.models import PM
from nano.privmsg.forms import *

def get_user(request, **kwargs):
    username = kwargs.get(u'username', None) or request.REQUEST.get(u'username', None)
    User = get_user_model()
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        pass
    user = kwargs.get(u'user', None) or request.REQUEST.get(u'user', None)
    object_id = kwargs.get(u'object_id', None) or request.REQUEST.get(u'object_id', None)
    uid = filter(None, (user, object_id))[0]
    try:
        return User.objects.get(id=int(uid))
    except User.DoesNotExist:
        return None

def _archive(user, recipient, msgids):
    if recipient != user:
        raise Http404
    if not msgids:
        raise Http404
    pms = PM.objects.filter(recipient=user, id__in=msgids)
    pms.update(recipient_archived=True)

@login_required
def move_to_archive(request, *args, **kwargs):
    next = request.GET.get('next', None)
    recipient = get_user(request, **kwargs)
    msgid = int(kwargs.get(u'msgid', None))
    _archive(request.user, recipient, (msgid,))
    if next:
        return HttpResponseRedirect(next)
    return HttpResponseRedirect(reverse('nano.privmsg.views.show_pm_archived',
            kwargs={'object_id': request.user.id}))

def _delete(user, msgid):
    if not msgid:
        raise Http404
    pm = PM.objects.get(id=msgid)
    if pm.recipient == user:
        pm.recipient_deleted=True
    if pm.sender == user:
        pm.sender_deleted=True
    pm.save()
    pm.delete()

@login_required
def delete(request, *args, **kwargs):
    next = request.GET.get('next', None)
    msgid = int(kwargs.get(u'msgid', None))
    _delete(request.user, msgid)
    if next:
        return HttpResponseRedirect(next)
    return HttpResponseRedirect(reverse('nano.privmsg.views.show_pm_received',
            kwargs={'object_id': request.user.id}))

@login_required
def show_pm_archived(request, *args, **kwargs):
    recipient = get_user(request, **kwargs)
    if recipient != request.user:
        raise Http404
    messages = PM.objects.archived(request.user)
    template = 'privmsg/list_archived.html'
    data = {'pms': messages,
            }
    return render(request, template, data)

@login_required
def show_pm_sent(request, *args, **kwargs):
    recipient = get_user(request, **kwargs)
    if recipient != request.user:
        raise Http404
    messages = PM.objects.sent(request.user)
    template = 'privmsg/list_sent.html'
    data = {'pms': messages,
            }
    return render(request, template, data)

@login_required
def show_pm_received(request, *args, **kwargs):
    recipient = get_user(request, **kwargs)
    if recipient != request.user:
        raise Http404
    messages = PM.objects.received(request.user)
    template = 'privmsg/list_received.html'
    data = {'pms': messages,
            }
    return render(request, template, data)

@login_required
def show_pms(request, *args, **kwargs):
    recipient = get_user(request, **kwargs)
    if recipient != request.user:
        raise Http404
    ACTIONS = {
        u'archive': PM.objects.archived,
        u'sent': PM.objects.sent,
        u'received': PM.objects.received,
    }
    actionstr = kwargs.get(u'action', None) or u'received'
    action = ACTIONS[actionstr]
    messages = action(request.user)
    if request.method == 'POST':
        msgids = request.POST.getlist(u'msgid')
        action = request.POST.get(u'submit')
        #assert False, '%s %s' % (action, msgids)
        if action == u'delete':
            _delete(request.user, msgids[0])
        elif action == u'archive':
            _archive(request.user, recipient, msgids)
    template = 'privmsg/archive.html'
    data = {'pms': messages,
            'action': actionstr,
            }
    return render(request, template, data)

@login_required
def add_pm(request, template='privmsg/add.html', *args, **kwargs):
    form = PMForm()
    recipient = get_user(request, **kwargs)
    next = request.GET.get('next', None)
    if request.method == 'POST':
        form = PMForm(data=request.POST)
        if form.is_valid():
            pm = form.save(commit=False)
            pm.sender = request.user
            pm.recipient = recipient
            pm.save()
            if next:
                return HttpResponseRedirect(next)
            else:
                return HttpResponseRedirect(reverse('nano.privmsg.views.show_pm_sent',
                        kwargs={'object_id': request.user.id}))
    data = {
            'pms': PM.objects.all(),
            'form': PMForm(),
            'recipient': recipient,
            }

    return render(request, template, data)
