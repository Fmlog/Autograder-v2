from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from .softDelete import SoftDeleteModel

class User(SoftDeleteModel, AbstractUser):
    '''Represent all types of users of the autograder
    '''
    ADMIN = 1
    TEACHER = 2
    STUDENT = 3

    ROLE_CHOICES = (
        (ADMIN, 'admin'),
        (TEACHER, 'teacher'),
        (STUDENT, 'student'),
    )

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    login_id = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
    username = None

    USERNAME_FIELD = 'login_id'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name