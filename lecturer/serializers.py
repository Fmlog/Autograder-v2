from rest_framework import serializers
from.models import Question, File


class QuestionSerializer(serializers.ModelSerializer):
    '''A class that is used to serialize the data from the database.'''
    class Meta:
        model = Question
        fields = ('id', 'title', 'description', 'function', 'test_case', 'test_result', 'lecturer')
        extra_kwargs = {
            'test_case': {'write_only': True},
            'test_result': {'write_only': True},
            'lecturer': {'read_only':True},
        }



class FileSerializer(serializers.ModelSerializer):
    '''Used to serialize the data from the database.'''
    class Meta():
        model = File
        fields = ('id', 'question', 'file', 'remark', 'timestamp')