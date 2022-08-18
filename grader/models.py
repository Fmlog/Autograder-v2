from django.db import models
from home.softDelete import SoftDeleteModel
from django.contrib.auth.models import AbstractUser
import uuid
from home.models import User
import os

# Create your models here.

def get_upload_to(instance, filename):
    return 'upload/%s/%s' % (f"{instance.question.slug}/tests/testcases", filename)

def get_file_upload_to(instance, filename):
    return 'upload/%s/%s' % (f"{instance.question.slug}", filename)

class Question(SoftDeleteModel):

    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, max_length=100)
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_lecturer': True}, null=True, blank=True)
    title = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=255, null=False)
    slug = models.CharField(max_length=255)
    language = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title

class TestCase(SoftDeleteModel):
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, max_length=100)
    file = models.FileField(upload_to=get_upload_to)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

class File(models.Model):

    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, max_length=100)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    file = models.FileField(blank=False, null=False, upload_to=get_file_upload_to)
    result = models.JSONField(blank=False, null=False, default='{}')
    timestamp = models.DateTimeField(auto_now_add=True)

    def filename(self):
        return os.path.basename(self.file.name)
