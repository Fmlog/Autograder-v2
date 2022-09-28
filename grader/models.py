from django.db import models
from home.softDelete import SoftDeleteModel
from django.contrib.auth.models import AbstractUser
import uuid
from home.models import User
import os

def get_testcase_upload_to(instance, filename):
    """
    Gets the exact path to upload the testcases for a
    new testcase instance.
    """
    return 'upload/%s/%s' % (f"{instance.assignment.slug}/tests/testcases", filename)

def get_config_upload_to(instance, filename):
    """
    Gets the exact path to upload the config file for a
    new config instance.
    """
    return 'upload/%s/%s' % (f"{instance.assignment.slug}/tests", filename)

def get_sub_upload_to(instance, filename):
    """
    Gets the exact path to upload the submission file for a
    new submission instance.
    """
    return 'upload/%s/%s' % (f"{instance.assignment.slug}", filename)


# Represents a course
# The course model owns assignment model(s).
class Course(SoftDeleteModel):
    '''
    Represents a course
    The course model owns assignment model(s).
    '''
    id = models.AutoField(primary_key=True)
    course_code = models.CharField(max_length=255, null=False)
    name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.name


class Assignment(SoftDeleteModel):
    '''
    Represents an assignment
    It is used to create the grading directory structure 
    '''
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    slug = models.CharField(max_length=255)    

    def __str__(self):
        return self.name

class TestCase(SoftDeleteModel):
    '''
    Represents a Testcase of an assignment.
    It is linked to uploaded testcase file in the grading directory. 
    '''
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False,
                                                    unique=True, max_length=100)
    file = models.FileField(upload_to=get_testcase_upload_to)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    
    def filename(self):
        return os.path.basename(self.file.name)


class Config(SoftDeleteModel):
    '''
    Represents the configuration settings for the assignment.
    It is linked to uploaded testcase file in the grading directory. 
    '''
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, 
                                                    unique=True, max_length=100)
    file = models.FileField(upload_to=get_config_upload_to)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    
    def filename(self):
        return os.path.basename(self.file.name)


class Submission(models.Model):
    '''
    Represents a submission
    Runs a hold details of a grading instance
    '''
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, 
                                                    unique=True, max_length=100)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(blank=False, null=False, upload_to=get_sub_upload_to)
    result = models.JSONField(blank=False, null=False, default='{}')
    grade = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def filename(self):
        return os.path.basename(self.file.name)
