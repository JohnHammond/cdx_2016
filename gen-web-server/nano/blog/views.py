import datetime

from django.views.generic import ListView
from django.views.generic import (ArchiveIndexView,
                                  YearArchiveView,
                                  MonthArchiveView,
                                  DayArchiveView,
                                  TodayArchiveView,
)

from nano.blog.models import Entry

class BlogMixin(object):
    queryset = Entry.objects.all().order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super(BlogMixin, self).get_context_data(**kwargs)
        context['me'] = 'news'
        context['now_today'] = datetime.date.today()
        context['latest'] = self.get_queryset()[:30]
        return context

class BlogDateMixin(BlogMixin):
    date_field = 'pub_date'

class MonthBlogMixin(BlogDateMixin):
    allow_empty = True
    month_format = '%m'

class ListBlogView(BlogMixin, ListView):
    pass
list_entries = ListBlogView.as_view()

class YearBlogView(BlogDateMixin, YearArchiveView):
    allow_empty = True
    make_object_list = True
list_entries_by_year = YearBlogView.as_view()

class MonthBlogView(MonthBlogMixin, MonthArchiveView):
    pass
list_entries_by_year_and_month = MonthBlogView.as_view()

class DayBlogView(MonthBlogMixin, MonthArchiveView):
    pass
list_entries_by_date = DayBlogView.as_view()

class TodayBlogView(MonthBlogMixin, MonthArchiveView):
    pass
list_entries_for_today = TodayBlogView.as_view()

class LatestBlogView(BlogDateMixin, ArchiveIndexView):
    pass
list_latest_entries = LatestBlogView.as_view()
