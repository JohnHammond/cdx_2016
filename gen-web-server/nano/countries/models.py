__all__ = ('Country',)

from django.db import models

class Country(models.Model):
    iso = models.CharField(max_length=2, primary_key=True)
    name = models.CharField('Country name', max_length=128)

    class Meta:
        verbose_name = 'country'
        verbose_name_plural = 'countries'
        db_table = 'nano_country'

    @property
    def printable_name(self):
        return self.name

    def __unicode__(self):
        return self.name
