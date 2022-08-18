from rest_framework import serializers
from.models import Question, File


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('id', 'title', 'description', 'language')
        extra_kwargs = {
            'grader': {'read_only':True},
        }

class TestCaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = ('id', 'question', 'file')

class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = ('id', 'question', 'file', 'result')
        extra_kwargs = {
            'result': {'read_only': True},
        }