import urllib
from urlparse import urlparse

import logging
_LOG = logging.getLogger(__name__)

from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.template import loader, RequestContext
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.urlresolvers import resolve
from django.views.generic import ListView
from django.utils.html import escape

from nano.comments.models import Comment
from nano.comments.forms import *

def _get_contenttype(model):
    if model:
        return ContentType.objects.get_for_model(model)
    return None

def _get_queryset(object_id=None, model=None):
    queryset = Comment.objects

    if object_id and model:
        object = model.objects.get(pk=object_id)
        contenttype = _get_contenttype(model)
        queryset = queryset.filter(object_pk=str(object.id), content_type=contenttype)
    else:
        queryset = queryset.all()
    return queryset        

def _get_object(model, object_id, object_field=None, **kwargs):
    if model and object_id:
        if object_field: # and hasattr(model, object_field):
            return model.objects.get(**{object_field: object_id})
        else:
            return model.objects.get(pk=object_id)
    return None

@login_required
def post_comment(request, object_arg='object_id', object_field=None, model=None, part_of=None, template_name='nano/comments/comment_form.html', *args, **kwargs):
    """Post a comment to the object of type ``model``, with primary key
    fetched from the field named in ``object_field``"""

    object_id = kwargs.get(object_arg, None)
    kwargs.pop(object_arg)
    assert object_id
    assert model

    contenttype = _get_contenttype(model)
    object = _get_object(model, object_id, object_field=object_field, **kwargs)
    part_of = request.REQUEST.get('part_of', None) or part_of

    cpart_of = None
    if part_of:
        try:
            cpart_of = Comment.objects.get(id=int(part_of))
        except Comment.DoesNotExist:
            pass

    good_data = {}
    good_data['content_type'] = contenttype
    good_data['object_pk'] = str(object.id)
    good_data['user'] = request.user
    good_data['part_of'] = part_of

    data = {}
    if request.method == 'POST' and contenttype and object:
        form = CommentForm(data=request.POST, initial={'part_of': part_of})
        data['commentform'] = form

        if form.is_valid():
            part_of = form.cleaned_data['part_of'] or part_of
            if part_of and not (contenttype and object):
                cpart_of = Comment.objects.get(id=int(part_of))
                good_data['content_type'] = cpart_of.content_type
                good_data['object_pk'] = str(cpart_of.content_object.pk)
            good_data['part_of'] = part_of
            good_data['comment'] = form.cleaned_data['comment']
            good_data['comment_xhtml'] = escape(good_data['comment'])

            if cpart_of or (contenttype and object):
                if request.POST.get('submit'):
                    if good_data['part_of']:
                        good_data['part_of'] = Comment.objects.get(id=int(part_of))
                    else:
                        del good_data['part_of']
                    try:
                        c = Comment(**good_data)
                    except TypeError:
                        assert False, repr(Comment)
                        raise
                    c.save()
                    return HttpResponseRedirect('../')
                else:
                    data['commentform'] = CommentForm(data=request.POST, initial=good_data)
                    data['preview'] = good_data
    else:
        form = CommentForm(initial=good_data)
        data['commentform'] = form

    return render(request, template_name, data)


class ListCommentView(ListView):
    template_name = 'nano/comments/comment_list.html'

    def get_queryset(self):
        object_arg = self.kwargs.get('object_arg', 'object_id')
        object_id = self.kwargs.get(object_arg)
        model = self.kwargs.get('model')
        object_field = self.kwargs.get('object_field', None)
        object = _get_object(model, object_id, object_field)
        queryset = _get_queryset(object_id=object.id, model=model)
        if not object_arg in ('object_id',):
            self.kwargs.pop(object_arg, None)
        return queryset
list_comments = ListCommentView.as_view()
