"""
Wrapper for loading templates from the filesystem.
"""

from django.conf import settings
from django.db.models import get_model
from django.template.base import TemplateDoesNotExist
from django.utils._os import safe_join

# Avoid warning/exception in 1.8+
try:
    # >= Django 2.0
    from django.template.loaders.base import Loader as BaseLoader
except:
    # < Django 2.0
    from django.template.loader import BaseLoader

class Loader(BaseLoader):
    is_usable = True
    chunk_model = get_model('chunk', 'Chunk')
    chunk_model_name = chunk_model.__name__

    def load_template_source(self, template_name, template_dirs=None):
        template_id = (self.chunk_model_name, template_name)
        try:
            chunk = self.chunk_model.objects.get(slug=template_name)
            return (chunk.content, "chunk:%s:%s" % template_id)
        except self.chunk_model.DoesNotExist:
            error_msg = "Couldn't find a %s-chunk named %s" % template_id
            raise TemplateDoesNotExist(error_msg)
