from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=40, null=True, blank=True)
    updated_by = models.CharField(max_length=40, null=True, blank=True)

    class Meta:
        abstract = True
        app_label = 'base'
