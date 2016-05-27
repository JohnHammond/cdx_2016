"""
Mixin-models, with minimal example implementations.

"""

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core import urlresolvers
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Avoid warning/exception in 1.7+
try:
    # >= Django 1.7
    from django.contrib.contenttypes import fields as generic
except ImportError:
    # < Django 1.7
    from django.contrib.contenttypes import generic


class UnorderedTreeManager(models.Manager):
    def roots(self):
        "Return a list of tree roots, nodes having no parents"
        return self.get_queryset().filter(part_of__isnull=True)

class UnorderedTreeMixin(models.Model):
    part_of = models.ForeignKey('self', blank=True, null=True, default=None, related_name='has_%(class)s_children')
    path = models.CharField(max_length=255, blank=True, default='')

    tree = UnorderedTreeManager()

    _sep = u'/'

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            super(UnorderedTreeMixin, self).save(*args, **kwargs)

        self._set_path()
        super(UnorderedTreeMixin, self).save(*args, **kwargs)


    def _set_path(self):

        if self.part_of:
            self.path = "%s%i/" % (self.part_of.path, self.id)
        else:
            self.path = "%i/" % self.id

    @property
    def level(self):
        "Count how far down in the tree self is"
        return unicode(self.path).count(self._sep)

    def roots(self):
        "Get all roots, nodes without parents"
        return self._default_manager.filter(part_of__isnull=True)

    def get_path(self):
        "Get all ancestors, ordered from root to self"
        return [self._default_manager.get(id=p) for p in unicode(self.path).split(self._sep) if p]

    def descendants(self):
        "Get all descendants in no particular order"
        return self._default_manager.filter(path__startswith=self.path).exclude(id=self.id)

    def parent(self):
        "Get parent of self"
        return self.part_of

    def siblings(self):
        "Get all nodes with the same parent"
        if not self.part_of: return []
        return [p for p in self.part_of.descendants() if p.level == self.level]

    def children(self):
        "Get nodes that have self as parent"
        return [p for p in self.descendants() if p.level == self.level + 1]

    def is_sibling_of(self, node):
        "Check if <node> has the same parent as self"
        return self.part_of == node.part_of

    def is_child_of(self, node):
        "Check if <node> is the parent of self"
        return self.part_of == node

    def is_root(self):
        """Check if self is a root. Roots have no parents"""
        return not bool(self.part_of)

    def is_leaf(self):
        """Check if self is a leaf. Leaves have no descendants"""
        return self.descendants().count() == 0

class AbstractText(models.Model):
    "Denormalized storage of text"
    DEFAULT_TYPE = 'plaintext'
    text = models.TextField()
    text_formatted = models.TextField(editable=False)
    text_type = models.CharField(max_length=64, default=DEFAULT_TYPE)

    class Meta:
        abstract = True

    def save(self, formatters=None, *args, **kwargs):
        if self.text_type == self.DEFAULT_TYPE:
            self.text_formatted = self.text
        else:
            if formatters:
                self.text_formatted = formatters(self.text_type)
        super(AbstractText, self).save(*args, **kwargs)

class GenericForeignKeyAbstractModel(models.Model):
    """
    An abstract base class for models with one GenericForeignKey
    """

    # Content-object field
    content_type = models.ForeignKey(ContentType, verbose_name=_('content type'), related_name="content_type_set_for_%(class)s")
    object_pk = models.TextField(_('object ID'))
    content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")

    class Meta:
        abstract = True
