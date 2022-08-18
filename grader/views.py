import json
import shutil

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import jwt, datetime
from .models import File
from .autograde import autograde
from django.utils.decorators import method_decorator
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from .serializers import QuestionSerializer, FileSerializer, TestCaseSerializer
from home.models import User
from grader.models import TestCase, Question, File
import random
import string
import os


# Create your views here.

def slug_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def handle_uploaded_file(f):
    with open(f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

# validating user authentication
def validate_user(request):
    token = request.COOKIES.get('token')
    if token is None:
        raise AuthenticationFailed('Invalid credentials')

    payload = jwt.decode(token, 'SECRET_KEY', algorithms='HS256')

    user = User.objects.filter(id=payload['id']).first()
    if not user:
        return False, user

    return True, user

@method_decorator(csrf_exempt, name='dispatch')
class QuestionView(APIView):

    def get(self, request):
        stat, user = validate_user(request)
        if not stat:
            return Response({
                "status": "error",
                "message": "no user found"
            }, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_lecturer:
            return Response({
                "status": "error",
                "message": "only lecturers can upload a question"
            }, status=status.HTTP_401_UNAUTHORIZED)

        quest = Question.objects.filter(lecturer=user)
        question = QuestionSerializer(quest, many=True)
        return Response({
            "status": "success",
            "data": question.data,
            "message": "Question added"
        }, status=status.HTTP_200_OK)


    def post(self, request):

        # if not request.user.is_authenticated:
        #     return Response({
        #         "status": "error",
        #         "message": "no user found"
        #     }, status=status.HTTP_401_UNAUTHORIZED)

        # user = request.user

        stat, user = validate_user(request)
        if not stat:
            return Response({
                    "status": "error",
                    "message": "no user found"
            }, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_lecturer:
            return Response({
                "status": "error",
                "message": "only lecturers can upload a question"
            }, status=status.HTTP_401_UNAUTHORIZED)

        question = QuestionSerializer(data=request.data)
        question.is_valid(raise_exception=True)

        slug = slug_generator()
        question.validated_data['lecturer'] = user
        question.validated_data['slug'] = slug
        question.save()
        quest = Question.objects.get(slug=slug)
        # upload = TestCaseSerializer(data=request.FILES)
        # if upload.is_valid():
        for f in request.FILES.getlist('file'):
            TestCase.objects.create(file=f, question=quest)
        # else:
        #     print("not valid")
        #     print(request.FILES)

        from autograderstable.autograder.autograder import AutograderPaths, Grader
        from autograderstable.autograder import guide

        current_dir = f'media/upload/{quest.slug}'
        os.mkdir(f"{current_dir}/results")
        guide.main(AutograderPaths(current_dir))

        return Response({
            "status": "success",
            "data": question.data,
            "message": "Question added"
        }, status=status.HTTP_200_OK)

    def delete(self, request, id):
        stat, user = validate_user(request)
        if not stat:
            return Response({
                "status": "error",
                "message": "no user found"
            }, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_lecturer:
            return Response({
                "status": "error",
                "message": "You are not a lecturer"
            }, status=status.HTTP_401_UNAUTHORIZED)

        question = get_object_or_404(Question, id=id)

        if os.path.exists(f"media/upload/{question.slug}"):
            shutil.rmtree(f"media/upload/{question.slug}")
        question.delete()

        return Response({
            "status": "success",
            "message": "Question deleted"
        }, status=status.HTTP_200_OK)

class TestCaseView(APIView):

    def post(self, request):
        id = request.data['question']
        quest = Question.objects.get(id=id)
        testcases = {}
        num = 1
        for f in request.FILES.getlist('file'):
            test = TestCase.objects.create(file=f, question=quest)
            testcases[num] = TestCaseSerializer(test).data
            num +=1

        return Response({
            "status": "success",
            "data": testcases,
            "message": "Question added"
        }, status=status.HTTP_200_OK)

    def get(self, request, id):
        stat, user = validate_user(request)
        if not stat:
            return Response({
                "status": "error",
                "message": "no user found"
            }, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_lecturer:
            return Response({
                "status": "error",
                "message": "You are not a lecturer"
            }, status=status.HTTP_401_UNAUTHORIZED)

        question = Question.objects.get(id=id, lecturer=user)
        if not question:
            return Response({
                "status": "success",
                "message": "No question with id"
            }, status=status.HTTP_404_NOT_FOUND)

        testcase = TestCase.objects.filter(question=question)
        testcaseserializer = TestCaseSerializer(testcase, many=True)

        return Response({
            "status": "success",
            "data": testcaseserializer.data,
            "message": "List of test cases"
        }, status=status.HTTP_200_OK)

    def patch(self, request):
        pass

    def delete(self, request, id):
        stat, user = validate_user(request)
        if not stat:
            return Response({
                "status": "error",
                "message": "no user found"
            }, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_lecturer:
            return Response({
                "status": "error",
                "message": "You are not a lecturer"
            }, status=status.HTTP_401_UNAUTHORIZED)

        testcase = get_object_or_404(TestCase, id=id)
        if os.path.exists(f"media/{testcase.file}"):
            os.remove(f"media/{testcase.file}")
        testcase.delete()

        return Response({
            "status": "success",
            "message": "Test case deleted"
        }, status=status.HTTP_200_OK)

class FileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):

        file_serializer = FileSerializer(data=request.data)

        if not file_serializer.is_valid():
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        file_serializer.save()
        id = file_serializer.data['id']

        file = File.objects.get(id=id)

        # run the autograder
        os.system(f"python ./tester.py 'media/upload/{file.question.slug}' '{file.id}'")

        file = File.objects.get(id=id)
        file_serializer = FileSerializer(file)
        # obj = serializers.serialize('json', [file,])

        if os.path.exists(f"media/{file.file}"):
            os.remove(f"media/{file.file}")

        return Response({
            "status": "success",
            "data": file_serializer.data,
        }, status=status.HTTP_201_CREATED)

    def get(self, request, id):

        stat, user = validate_user(request)
        if not stat:
            return Response({
                "status": "error",
                "message": "no user found"
            }, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_lecturer:
            return Response({
                "status": "error",
                "message": "Unauthorized"
            }, status=status.HTTP_401_UNAUTHORIZED)

        question = Question.objects.get(id=id, lecturer=user)
        if not question:
            return Response({
                "status": "success",
                "message": "No question with id"
            }, status=status.HTTP_404_NOT_FOUND)


        files = File.objects.filter(question=question)
        file_serializer = FileSerializer(files, many=True)

        return Response({
            "status": "success",
            "data": file_serializer.data,
            "message": "Question added"
        }, status=status.HTTP_200_OK)


