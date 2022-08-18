from django.db import models
from django.utils import timezone
from django.contrib.auth.models import UserManager

class SoftDeleteManager(UserManager):

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class SoftDeleteModel(models.Model):

    deleted_at = models.DateTimeField(null=True, default=None, blank=True)
    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    class Meta:
        abstract = True
