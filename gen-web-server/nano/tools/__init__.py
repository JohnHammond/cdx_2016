import logging
import unicodedata
from itertools import izip_longest

_LOG = logging.getLogger(__name__)

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render
from django.template import RequestContext, loader, Context
from django.db.models import get_model
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

class SiteProfileNotAvailable(Exception):
    pass

def nullfunction(return_this=None, *args, **kwargs):
    return return_this

def pop_error(request):
    error = request.session.get('error', None)
    if 'error' in request.session:
        del request.session['error']
    return error

def asciify(string):
    """Convert unicode string to ascii, normalizing with NFKD"""

    string = unicodedata.normalize('NFKD', string)
    return string.encode('ascii', 'ignore')

def render_page(request, *args, **kwargs):
    return render(request, *args, **kwargs)

def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

def get_profile_model(raise_on_error=True):
    '''
    if not getattr(settings, 'AUTH_PROFILE_MODULE', False):
        error = "AUTH_PROFILE_MODULE isn't set in the settings, couldn't fetch profile"
        _LOG.error(error)
        if raise_on_error:
            raise SiteProfileNotAvailable(error)
        return None
    try:
        app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
        model = get_model(app_label, model_name)
    except ImportError:
        error = "Could not import the profile '%s' given in AUTH_PROFILE_MODULE" % settings.AUTH_PROFILE_MODULE
        _LOG.error(error)
        if raise_on_error:
            raise SiteProfileNotAvailable(error)
        return None
    except ImproperlyConfigured:
        error = "An unknown error happened while fetching the profile model"
        if raise_on_error:
            raise SiteProfileNotAvailable(error)
        return None
    return model
    '''
    return User

if 'nano.blog' in settings.INSTALLED_APPS:
    try:
        from nano.blog import add_entry_to_blog
    except ImportError:
        add_entry_to_blog = nullfunction
else:
    add_entry_to_blog = None
