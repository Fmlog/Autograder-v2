from django.db import models
from home.softDelete import SoftDeleteModel
from django.contrib.auth.models import AbstractUser
import uuid
from home.models import User
import os

class Question(SoftDeleteModel):
    '''`Question` is a model that is used to store the question that is created by the lecturer.'''
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, max_length=100)
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_lecturer': True})
    title = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=255, null=False)
    function = models.CharField(max_length=255, default="Function")
    test_case = models.JSONField()
    test_result = models.JSONField()
    language = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title

class File(models.Model):
    '''`File` is a model that is used to store the file that is uploaded by the lecturer.'''
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, max_length=100)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    file = models.FileField(blank=False, null=False)
    remark = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

    def filename(self):
        return os.path.basename(self.file.name)