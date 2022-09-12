from django.db import models
from home.softDelete import SoftDeleteModel
from django.contrib.auth.models import AbstractUser
import uuid
from home.models import User
import os

def get_upload_to(instance, filename):
    return 'upload/%s/%s' % (f"{instance.assignment.slug}/tests/testcases", filename)

def get_file_upload_to(instance, filename):
    return 'upload/%s/%s' % (f"{instance.assignment.slug}", filename)


class Course(SoftDeleteModel):
    id = models.AutoField(primary_key=True)
    course_code = models.CharField(max_length=255, null=False)
    name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.name

class Assignment(SoftDeleteModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    slug = models.CharField(max_length=255)    

    def __str__(self):
        return self.name

class TestCase(SoftDeleteModel):
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, max_length=100)
    file = models.FileField(upload_to=get_upload_to)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)

class Submission(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, max_length=100)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(blank=False, null=False, upload_to=get_file_upload_to)
    result = models.JSONField(blank=False, null=False, default='{}')
    grade = models.CharField(max_length=20, default="0")
    timestamp = models.DateTimeField(auto_now_add=True)

    def filename(self):
        return os.path.basename(self.file.name)
