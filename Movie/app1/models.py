from django.db import models
from django.contrib.auth.models import AbstractUser


class User_reg(AbstractUser):

    def __str__(self):
        return self.username