from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields.jsonb import JSONField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
from ipware.ip import get_real_ip


class ActivityLogManager(models.Manager):
    """
    Manager for Activity Log. 'actor' is none in the case of Anonymous user.
    """

    def create_log(self, request, user=None, entity=None, level='I', **kwargs):
        try:
            info = {
                'ip': self.get_ip(request),
                'view_name': str(kwargs.pop('view', "")),
                'arguments': kwargs.pop('arguments', {}),
                'message': str(kwargs.pop('message', "")),
                'act_type': kwargs.pop('act_type', ""),
                'extra': kwargs
            }
            self.create(user=user, entity=entity, level=level, meta_info=info)
        except Exception as e:
            self.create_log(
                request=None, level='C', message=str(e.message), act_type="Error in creating activity Log",
                kw_details=str(kwargs), actor_details=str(user), entity_details=str(entity)
            )
            return False
        else:
            return True

    @staticmethod
    def get_ip(request):
        if request:
            return get_real_ip(request)
        return "No request data"


class ActivityLog(models.Model):
    """
    Logs all activities within the domain of the application
    meta_info data -> view method, arguments of view, message, extra, ip, act_type

    Required arguments for creating a log entry ->
        request(send 'None' for system level logging), level, category
    Can send extra any key based arguments, they'll be stored in the JSON field.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)

    content_type2 = models.ForeignKey(ContentType, null=True, blank=True, related_name='entity')
    object_id2 = models.PositiveIntegerField(null=True, blank=True)
    entity = GenericForeignKey('content_type2', 'object_id2')

    CHOICES = (('I', 'INFO'),
               ('E', 'ERROR'),
               ('C', 'CRITICAL'),
               ('D', 'DEBUG'),
               ('W', 'WARNING'),
               )
    level = models.CharField(max_length=1, choices=CHOICES)
    category = models.CharField(max_length=20)

    meta_info = JSONField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)

    objects = ActivityLogManager()

    def __unicode__(self):
        return self.actor or "No unicode - Activity Log"
