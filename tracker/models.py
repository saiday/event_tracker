from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Event(models.Model):
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    confirmed_user = models.ManyToManyField(User)

    def __str__(self):  # dunder str
        return self.key + ": " + self.value

    def get_absolute_url(self):
        """
        form_valid() would use this method as return value
        """
        return reverse('event-detail', kwargs={'pk': self.pk})
