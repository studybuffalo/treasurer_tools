from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    name = models.CharField(
        blank=True,
        help_text=_('Full name of user'),
        max_length=255,
    )

    def __str__(self):
        return self.name if self.name else self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})
