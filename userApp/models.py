from django.db import models
from django.contrib.auth.models import AbstractUser

USER_TYPE = (
    ("manager", "Manager"),
    ("user", "User")
)

class User(AbstractUser):
    user_type = models.CharField(max_length=10, choices=USER_TYPE, default="user")
    address = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.username
