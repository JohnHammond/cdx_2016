from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.decorators import login_required
from django.template import loader, RequestContext
from django.contrib.contenttypes.models import ContentType

try:
    import json as simplejson
except:
    from django.utils import simplejson

from nano.mark.models import Mark, MarkType

@login_required
def toggle_mark(request, allow_xmlhttprequest=False):
    """
    Generic object vote function.

    The given template will be used to confirm the vote if this view is
    fetched using GET; vote registration will only be performed if this
    view is POSTed.

    If ``allow_xmlhttprequest`` is ``True`` and an XMLHttpRequest is
    detected by examining the ``HTTP_X_REQUESTED_WITH`` header, the
    ``xmlhttp_vote_on_object`` view will be used to process the
    request - this makes it trivial to implement voting via
    XMLHttpRequest with a fallback for users who don't have JavaScript
    enabled.

    Templates:``<app_label>/<model_name>_confirm_vote.html``
    Context:
        object
            The object being voted on.
        direction
            The type of vote which will be registered for the object.
    """
#     if allow_xmlhttprequest and request.is_ajax():
#         return xmlhttprequest_vote_on_object(request, model, direction,
#                                              object_id=object_id, slug=slug,
#                                              slug_field=slug_field)

    next = '/'
    if request.method == 'POST':
        model_pk = request.POST.get('model_pk', None)
        model_type = request.POST.get('model_type', None)
        
        if not (model_pk and model_type):
            return HttpResponseRedirect('/')

        ct = ContentType.objects.get(id=int(model_type))
        object = ct.get_object_for_this_type(pk=model_pk)
        #assert False, ct

        marktype = MarkType.objects.get(slug=request.POST.get('type', 'flag'))
        if not marktype:
            marktype = MarkType.objects.create(slug='flag', name='Flag', hide=True, permanent=True, verify=True)
        mark, created = Mark.objects.get_or_create(
                marked_by=request.user, 
                marktype=marktype, 
                object_pk=unicode(object.pk), 
                content_type=ct,
                )
        if not (created or mark.marktype.permanent):
            mark.delete()

        next = request.POST.get('next', None) or next

        # Django-notify-support
        if hasattr(request, 'notifications'):
            flip = {'flag': 'flagged', 'fave': 'faved'}
            request.notifications.add("You've now %s %s as %s" %
            (u'marked' if created else u'unmarked', object, flip.get(mark.marktype.slug, mark.marktype.slug)))

        if mark.marktype.verify:
            callable = 'nano_mark_verify_%s' % marktype.type
            return HttpResponseRedirect(reverse(callable))
    return HttpResponseRedirect(next)

def nano_mark_verify_flag(request, *args, **kwargs):
    template = ''
    raise Http404
