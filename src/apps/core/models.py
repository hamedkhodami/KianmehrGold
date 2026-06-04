import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .utils import get_timesince_persian


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(_("Creation Time"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Update Time"), auto_now=True)
    is_deleted = models.BooleanField(_("Is Deleted"), default=False)
    deleted_at = models.DateTimeField(_("Deleted Time"), blank=True, null=True)

    class Meta:
        abstract = True

    def get_created_at(self):
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")

    def get_created_date(self):
        return self.created_at.strftime("%Y-%m-%d")

    def get_updated_at(self):
        return self.updated_at.strftime("%Y-%m-%d %H:%M:%S")

    def get_updated_date(self):
        return self.updated_at.strftime("%Y-%m-%d")

    def get_created_at_time_past(self):
        return get_timesince_persian(self.created_at)

    # TODO:
    # Implement SoftDeleteManager in Phase 3
    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at"])

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=["is_deleted", "deleted_at"])
