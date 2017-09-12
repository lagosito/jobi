from __future__ import unicode_literals

from django.conf import settings
from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models
from templated_email import send_templated_mail


class NewsletterSubscription(models.Model):
    """
    Keywords contains subject and links to recommended jobs
    """
    email = models.EmailField(unique=True)
    keywords = JSONField()
    create_time = models.DateTimeField(auto_now_add=True)

    def parse_email(self):
        ctx = {}  # TODO
        send_templated_mail(
            template_name='newsletter',
            from_email=settings.FROM_EMAIL,
            recipient_list=[self.email],
            context=ctx
        )

