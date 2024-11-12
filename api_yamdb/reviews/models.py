from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    role = models.CharField("роль", max_length=20, blank=True)
