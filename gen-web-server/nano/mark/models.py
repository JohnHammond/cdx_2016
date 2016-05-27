from django.utils.timezone import now as tznow
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
#from django.conf import settings

from nano.tools.models import GenericForeignKeyAbstractModel

from nano.mark.managers import MarksManager

class MarkedMixin(models.Model):
    "Used by marked models"

    class Meta:
        abstract = True

    def marks(self):
        ct = ContentType.objects.get_for_model(self)
        return Mark.objects.filter(content_type = ct, object_pk = unicode(self.pk))
    
    def flagged(self):
        return self.marks.filter(marktype__slug='flag')

    def faved(self):
        return self.marks.filter(marktype__slug='fave')

    def scrambled(self):
        return self.marks.filter(marktype__slug='scrambled')

    def removed(self):
        return self.marks.filter(marktype__slug='removed')

    @property
    def hidden(self):
        marks = self.marks.filter(marktype__slug='flag')
        return True if marks.filter(marktype__hide=True) else False

class MarkType(models.Model):
    name = models.CharField(max_length=32)
    slug = models.SlugField(unique=True)
    hide = models.BooleanField(default=False)
    verify = models.BooleanField(default=False)
    permanent = models.BooleanField(default=False)

    class Meta:
        db_table='nano_mark_marktype'

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(MarkType, self).save(*args, **kwargs)

class Mark(GenericForeignKeyAbstractModel):
    marked_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'), related_name="marks")
    marked_at = models.DateTimeField(_('date/time marked'), default=tznow)
    marktype = models.ForeignKey(MarkType)
    comment = models.CharField(max_length=256, blank=True, null=True)

    objects = MarksManager()

    class Meta:
        db_table='nano_mark_mark'

    class Meta:
        db_table = "nano_mark"
        ordering = ('marked_at',)
        get_latest_by = 'marked_at'

    def __unicode__(self):
        return "%s have marked %s" % (self.marked_by, self.content_object)    

    def save(self, parent=None, *args, **kwargs):
        if self.marked_at is None:
            self.marked_at = tznow()
        super(Mark, self).save(*args, **kwargs)

