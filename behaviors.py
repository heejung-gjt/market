from django.db import models
import time

class Nameable(models.Model):
  name = models.CharField(max_length=64)

  class Meta:
    abstract = True


class TimeStampable(models.Model):
  created_at = models.TextField(default=time.time())
  updated_at = models.TextField(null=True, blank=True)

  class Meta:
    abstract = True


class Deleteable(models.Model):
  is_deleted = models.BooleanField(default=True)

  class Meta:
    abstract = True