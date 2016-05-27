from datetime import timedelta

from django.utils.timezone import now as tznow
from django.template.loader import render_to_string

from nano.blog.models import Entry as _Entry
from nano.blog.settings import NANO_BLOG_TAGS, NANO_BLOG_SPECIAL_TAGS

_five_minutes = timedelta(seconds=5*60)

def add_entry_to_blog(obj, headline, template, date_field='last_modified'):
    """Auto-blog about <obj>

    obj: object to blog about

    headline: string w/o html
    
    template: template, given the context 'obj' mapping to the object
    
    date_field: date_field on object to be used for publishing date
    """
    data = {'obj': obj}
    current_time = tznow()
    template = render_to_string(template, dictionary=data)
    pub_date = obj.__dict__.get(date_field, current_time)
    latest = _Entry.objects.latest()
    # Prevent duplicates
    if not (latest.headline == headline and latest.pub_date > current_time - _five_minutes):
        blog_entry = _Entry.objects.create(content=template,headline=headline,pub_date=pub_date)
        return blog_entry

def get_nano_blog_entries(special_tags=NANO_BLOG_SPECIAL_TAGS, cutoff=2):
    """Fetch <cutoff> number of most recent blog entries and split out
    entries tagged with <special_tags>.

    cutoff: integer, default 2
    
    special_tags: iterable collection of strings, default NANO_BLOG_SPECIAL_TAGS
    """
    special_news = ()
    news = _Entry.objects
    if NANO_BLOG_TAGS:
        if NANO_BLOG_TAGS.__name__ == 'taggit':
            special_news = news.filter(tags__slug__in=special_tags)
        elif NANO_BLOG_TAGS.__name__ == 'tagging':
            special_news = news.tagged.with_any(special_tags)
        special_news = special_news.order_by('-pub_date')[:cutoff]
        if special_news:
            news = news.exclude(id__in=[e.id for e in special_news])
        else:
            news = news.all()
    news = news.order_by('-pub_date')[:cutoff]
    return news, special_news
