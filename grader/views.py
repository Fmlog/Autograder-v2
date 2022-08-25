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
from .models import Course, File, Assignment
from django.utils.decorators import method_decorator
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from .serializers import AssignmentSerializer, CourseSerializer, FileSerializer, TestCaseSerializer
from home.models import User
from grader.models import TestCase, Assignment, File
import random
import string
import os


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
class CourseView(APIView):

    def get(self, request):
        stat, user = validate_user(request)
        if not stat:
            return Response({
                "status": "error",
                "message": "no user found"
            }, status=status.HTTP_401_UNAUTHORIZED)

        cours = Course.objects.all()
        course = CourseSerializer(cours, many=True)
        return Response({
            "status": "success",
            "data": course.data,
            "message": "Assignment query succesful"
        }, status=status.HTTP_200_OK)


    def post(self, request):
        stat, user = validate_user(request)
        if not stat:
            return Response({
                    "status": "error",
                    "message": "no user found"
            }, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_lecturer:
            return Response({
                "status": "error",
                "message": "only lecturers can create a course"
            }, status=status.HTTP_401_UNAUTHORIZED)

        course = CourseSerializer(data=request.data)
        course.is_valid(raise_exception=True)
        course.save()

        return Response({
            "status": "success",
            "data": course.data,
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

        course = get_object_or_404(Course, id=id)
        course.delete()

        return Response({
            "status": "success",
            "message": "Course deleted"
        }, status=status.HTTP_200_OK)



@method_decorator(csrf_exempt, name='dispatch')
class AssignmentView(APIView):

    def get(self, request):
        stat, user = validate_user(request)
        course = request.data['course_id']
        if not stat:
            return Response({
                "status": "error",
                "message": "no user found"
            }, status=status.HTTP_401_UNAUTHORIZED)

        quest = Assignment.objects.filter(course_id=course)
        question = AssignmentSerializer(quest, many=True)
        return Response({
            "status": "success",
            "data": question.data,
            "message": "Assignment query succesful"
        }, status=status.HTTP_200_OK)


    def post(self, request):
        stat, user = validate_user(request)
        course = request.data['course_id']
        if not stat:
            return Response({
                    "status": "error",
                    "message": "no user found"
            }, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_lecturer:
            return Response({
                "status": "error",
                "message": "only lecturers can create an assignment"
            }, status=status.HTTP_401_UNAUTHORIZED)

        question = AssignmentSerializer(data=request.data)
        question.is_valid(raise_exception=True)

        slug = slug_generator()
        question.validated_data['course_id'] = course
        question.validated_data['slug'] = slug
        question.save()
        quest = Assignment.objects.get(slug=slug)

        for f in request.FILES.getlist('file'):
            TestCase.objects.create(file=f, question=quest)

        from autograderstable.autograder.autograder import AutograderPaths, Grader
        from autograderstable.autograder import guide

        current_dir = f'media/upload/{quest.slug}'
        os.mkdir(f"{current_dir}/")
        os.mkdir(f"{current_dir}/results")
        guide.main(AutograderPaths(current_dir))

        return Response({
            "status": "success",
            "data": question.data,
            "message": "Assignment added"
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

        question = get_object_or_404(Assignment, id=id)

        if os.path.exists(f"media/upload/{question.slug}"):
            shutil.rmtree(f"media/upload/{question.slug}")
        question.delete()

        return Response({
            "status": "success",
            "message": "Assignment deleted"
        }, status=status.HTTP_200_OK)

class TestCaseView(APIView):

    def post(self, request):
        assignment_id = request.data['assignment_id']
        testcases = {}
        num = 1
        for f in request.FILES.getlist('file'):
            test = TestCase.objects.create(file=f, assignment_id=assignment_id)
            testcases[num] = TestCaseSerializer(test).data
            num +=1

        return Response({
            "status": "success",
            "data": testcases,
            "message": "Testcase added"
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

        question = Assignment.objects.get(id=id, lecturer=user)
        if not question:
            return Response({
                "status": "success",
                "message": "No question with id"
            }, status=status.HTTP_404_NOT_FOUND)

        testcase = TestCase.objects.filter(assignment_id=question)
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

class SubmissionView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        stat, user = validate_user(request)
        if not stat:
            return Response({
                "status": "error",
                "message": "no user found"
            }, status=status.HTTP_401_UNAUTHORIZED)

        f = request.data['file']
        assignment_id = request.data['assignment_id']
        sub = File.objects.create(file=f, user_id=user.id, assignment_id=assignment_id)
        file_sub = FileSerializer(sub).data
        id = file_sub['id']
       
        file = File.objects.get(id=id)
        # run the autograder
        os.system(f"python ./tester.py 'media/upload/{file.assignment.slug}' '{file.id}'")

        file = File.objects.get(id=id)
        file_serializer = FileSerializer(file)

        if os.path.exists(f"media/{file.file}"):
            os.remove(f"media/{file.file}")

        return Response({
            "status": "success",
            "data": file_serializer.data,
        }, status=status.HTTP_201_CREATED)

    def get(self, request):

        stat, user = validate_user(request)
        if not stat:
            return Response({
                "status": "error",
                "message": "no user found"
            }, status=status.HTTP_401_UNAUTHORIZED)

        question = File.objects.get(user_id=user)
        if not question:
            return Response({
                "status": "success",
                "message": "No question with id"
            }, status=status.HTTP_404_NOT_FOUND)


        files = File.objects.filter(assignment_id=question)
        file_serializer = FileSerializer(files, many=True)

        return Response({
            "status": "success",
            "data": file_serializer.data,
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
                "message": "Unauthorized"
            }, status=status.HTTP_401_UNAUTHORIZED)

        question = File.objects.get(id=id)
        if not question:
            return Response({
                "status": "success",
                "message": "No submission with id"
            }, status=status.HTTP_404_NOT_FOUND)


        files = File.objects.filter(assignment_id=question)
        file_serializer = FileSerializer(files, many=True)

        return Response({
            "status": "success",
            "data": file_serializer.data,
            "message": "Submission query completed"
        }, status=status.HTTP_200_OK)

