from rest_framework import serializers

from home.models import User
from.models import Assignment, Course, Submission

class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ('id', 'course_code', 'name')


class AssignmentSerializer(serializers.ModelSerializer):
    course_id = serializers.PrimaryKeyRelatedField(source='course', queryset=Course.objects.all())

    class Meta:
        model = Assignment
        fields = ('id', 'name','course_id', 'language')
        extra_kwargs = {
            'grader': {'read_only':True},
        }

class TestCaseSerializer(serializers.ModelSerializer):
    assignment_id = serializers.PrimaryKeyRelatedField(source='assignment', queryset=Assignment.objects.all())

    class Meta:
        model = Submission
        fields = ('id', 'assignment_id', 'file')

class SubmissionSerializer(serializers.ModelSerializer):

    assignment_id = serializers.PrimaryKeyRelatedField(source='assignment', queryset=Assignment.objects.all())
    user_id = serializers.PrimaryKeyRelatedField(source='user', queryset=User.objects.all())

    class Meta:
        model = Submission
        fields = ('id', 'assignment_id', 'user_id', 'file', 'result')
        extra_kwargs = {
            'result': {'read_only': True},
        }