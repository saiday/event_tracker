from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Event(models.Model):
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    confirmed_user = models.ManyToManyField(User)
