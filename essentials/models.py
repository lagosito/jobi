from __future__ import unicode_literals
from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models
# Create your models here.


class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    keywords = JSONField()
    create_time = models.DateTimeField(auto_now_add=True)