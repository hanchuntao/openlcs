import json

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class TaskManager(models.Manager):

    def create(self, *args, **kwargs):
        params = kwargs.get('params', None)
        if params and isinstance(params, dict):
            kwargs['params'] = json.dumps(params)
        return super(TaskManager, self).create(*args, **kwargs)


class Task(models.Model):
    owner = models.ForeignKey(
        get_user_model(),
        related_name='tasks',
        on_delete=models.CASCADE
    )
    meta_id = models.TextField(unique=True)
    params = models.TextField()
    task_flow = models.TextField()
    retries = models.IntegerField(default=0)
    content_type = models.ForeignKey(
        ContentType,
        blank=True, null=True,
        on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    objects = TaskManager()

    def __str__(self):
        return str(self.pk)

    class Meta:
        app_label = 'tasks'

    def save(self, *args, **kwargs):
        params = kwargs.get('params')
        if params and isinstance(params, dict):
            kwargs['params'] = json.dumps(params)
        super(Task, self).save(*args, **kwargs)

    def get_params(self):
        try:
            return json.loads(self.params)
        except Exception:
            return self.params
