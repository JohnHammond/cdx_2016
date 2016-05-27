from django.template import Library, Context
from django.template.loader import get_template
from django.contrib.contenttypes.models import ContentType

from nano.mark.models import MarkType, Mark

register = Library()

@register.inclusion_tag('nano/mark/mark.html', takes_context=True)
def mark(context, model, type="flag"):
    ok_type = MarkType.objects.filter(slug=type)
    model_pk = model.pk
    ct = ContentType.objects.get_for_model(model)
    model_type = ct.id

    status = Mark.objects.filter(object_pk=str(model_pk), content_type=ct).count()

    request = context['request']
    user = request.user
    next = request.path
    return {
        'model_pk': model_pk,
        'model_type': model_type,
        'type': type if ok_type else "flag",
        'unique_id': '%s_%s' % (type, model_pk),
        'user': user,
        'next': next,
        'status': status,
    }

@register.inclusion_tag('nano/mark/mark_faved.html', takes_context=True)
def mark_faved(context, model):
    return mark(context, model, 'fave')
