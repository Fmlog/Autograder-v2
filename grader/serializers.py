from rest_framework import serializers

from home.models import User
from grader.models import Assignment, Config, Course, Submission, TestCase


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ('id', 'course_code', 'name')


class AssignmentSerializer(serializers.ModelSerializer):
    # Overwrites Django's default key from course to course_id.
    course_id = serializers.PrimaryKeyRelatedField(
        source='course', queryset=Course.objects.all())

    class Meta:
        model = Assignment
        fields = ('id', 'name', 'course_id', 'description')
        extra_kwargs = {
            'grader': {
                'read_only': True
            },
        }


class TestCaseSerializer(serializers.ModelSerializer):
    # Overwrites Django's default key from assignment to assignment_id.
    assignment_id = serializers.PrimaryKeyRelatedField(
        source='assignment', queryset=Assignment.objects.all())

    class Meta:
        model = TestCase
        fields = ('id', 'assignment_id', 'file')


class ConfigSerializer(serializers.ModelSerializer):
    assignment_id = serializers.PrimaryKeyRelatedField(
        source='assignment', queryset=Assignment.objects.all())

    class Meta:
        model = Config
        fields = ('id', 'assignment_id', 'file')


class SubmissionSerializer(serializers.ModelSerializer):
    # Overwrites Django's default key from assignment to assignment_id.
    assignment_id = serializers.PrimaryKeyRelatedField(
        source='assignment', queryset=Assignment.objects.all())
    # Overwrites Django's default key from user to user_id.
    user_id = serializers.PrimaryKeyRelatedField(source='user',
                                                 queryset=User.objects.all())

    class Meta:
        model = Submission
        fields = ('id', 'assignment_id', 'user_id', 'file', 'result', 'grade')
        extra_kwargs = {
            'result': {
                'read_only': True
            },
        }
