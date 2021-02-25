from django.db.models.signals import post_save
from django.dispatch import receiver

from creator.models import DataSet
from creator.tasks import create_scv


@receiver(post_save, sender=DataSet)
def data_set_post_save(sender, instance, **kwargs):
    if instance.status == DataSet.Status.PROCESSING:
        create_scv.delay(instance.id)
