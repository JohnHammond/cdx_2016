from django.views.generic import DetailView, ListView

from nano.badge.models import Badge


class BadgeMixin(object):
    queryset = Badge.objects.all()

    def get_context_data(self, **kwargs):
        context = super(BadgeMixin, self).get_context_data(**kwargs)
        context['me'] = 'badge'
        return context


class ListBadgeView(BadgeMixin, ListView):
    pass
list_badges = ListBadgeView.as_view()


class DetailBadgeView(BadgeMixin, DetailView):
    pass
show_badge = DetailBadgeView.as_view()
