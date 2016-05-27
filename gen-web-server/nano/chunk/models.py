from django.db import models

class Chunk(models.Model):
    slug = models.SlugField()
    content = models.TextField()

    class Meta:
        db_table = 'nano_chunk_chunk'

    def __unicode__(self):
        return self.slug
    
