from __future__ import unicode_literals
from django.contrib.postgres.fields.jsonb import JSONField

from django.db import models


# Create your models here.


class Source(models.Model):
    name = models.CharField(max_length=20)
    verbose_name = models.CharField(max_length=120)
    DS_TYPE = (('A', 'API with Structured Data'),
               ('S', 'API without Structured Data'),
               ('C', 'No API')
               )
    ds_type = models.CharField(max_length=1, ds_type=DS_TYPE)
    call_method = models.TextField()
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


class DataManager(models.Manager):
    pass


class Data(models.Model):
    """
    Stores all the data, where info is a JSON type storage which primarily holds
    fields like 'posted-on' and 'title' of job post.
    """
    source = models.ForeignKey(Source)
    link = models.TextField()
    msg = models.TextField()
    info = JSONField()
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.link
