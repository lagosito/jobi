from django.dispatch import receiver
from django.db.models.signals import post_save

from data.models import Source
from data.tasks import update_es_index


@receiver(post_save, sender=Source)
def update_es(sender, **kwargs):
    source = kwargs.get('instance')
    update_es_index.delay(source.id)
