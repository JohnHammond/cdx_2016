from django.views.generic import ListView

from nano.faq.models import QA


class ListFAQView(ListView):
    queryset = QA.objects.all().order_by('question')

    def get_context_data(self, **kwargs):
        context = super(ListFAQView, self).get_context_data(**kwargs)
        context['me'] = 'faq'
        return context
list_faqs = ListFAQView.as_view()
