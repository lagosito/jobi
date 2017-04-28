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
    ds_type = models.CharField(max_length=1, choices=DS_TYPE)
    call_method = models.TextField()
    call_kwargs = models.TextField(blank=True, null=True)
    ex_details = JSONField(null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


class DataManager(models.Manager):
    def filter_choices(self, meta):
        # TODO: use meta info
        return self.get_queryset().all()


# FIXME: migrate to ES
class Data(models.Model):
    """
    Stores all the data, where info is a JSON type storage which primarily holds
    fields like 'posted-on' and 'title' of job post.
    """
    source = models.ForeignKey(Source)
    link = models.TextField()
    msg = models.TextField()
    info = JSONField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)

    objects = DataManager()

    def __unicode__(self):
        return self.link
