from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from random import randint
from .softDelete import SoftDeleteModel
# Create your models here.


class User(SoftDeleteModel, AbstractUser):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    login_id = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_lecturer = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    username = None

    USERNAME_FIELD = 'login_id'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name