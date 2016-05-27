from django.db import models

class Link(models.Model):
    uri = models.URLField(unique=True)   
    last_checked = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'nano_link_link'

    def __unicode__(self):
        return self.uri

    def check(self):
        pass
