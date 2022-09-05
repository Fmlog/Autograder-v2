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
from rest_framework.decorators import api_view
import jwt
import datetime
from .models import Course, Submission, Assignment
from django.utils.decorators import method_decorator
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from .serializers import AssignmentSerializer, CourseSerializer, SubmissionSerializer, TestCaseSerializer
from home.models import User
from grader.models import TestCase, Assignment, Submission
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


@api_view(['GET'])
def getCourseAssignment(request, id):
    user = request.user
    user = User.objects.filter(id=user.id).first()
    if not user:
        return Response({"status": "error", "data": [], "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    course = Course.objects.filter(id=id).first()
    quest = Assignment.objects.filter(course=course)
    question = AssignmentSerializer(quest, many=True)

    return Response({
        "status": "success",
        "data": question.data,
        "message": f"Assignments for {course.name}"
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def getAllSubmissions(request, id):
    user = request.user
    user = User.objects.filter(id=user.id).first()
    if not user:
        return Response({"status": "error", "data": [], "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    course = Course.objects.filter(id=id).first()
    quest = Assignment.objects.filter(course=course)
    question = AssignmentSerializer(quest, many=True)

    return Response({
        "status": "success",
        "data": question.data,
        "message": "Assignment query succesful"
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def getLastSubmission(request, id):
    user = request.user
    user = User.objects.filter(id=user.id).first()
    if not user:
        return Response({"status": "error", "data": [], "message": "User not found"},
                        status=status.HTTP_404_NOT_FOUND)

    if not user.is_lecturer:
        return Response({
            "status": "error",
            "message": "only lecturers can create a course"
        }, status=status.HTTP_401_UNAUTHORIZED)

    course = Course.objects.filter(id=id).first()
    quest = Assignment.objects.filter(course=course).order_by('-id').first()
    question = AssignmentSerializer(quest, many=True)

    return Response({
        "status": "success",
        "data": question.data,
        "message": "last submission"
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def getUserSubmission(request, id, user_id):
    user = request.user
    user = User.objects.filter(id=user.id).first()
    if not user:
        return Response({"status": "error", "data": [], "message": "User not found"},
                        status=status.HTTP_404_NOT_FOUND)

    if not user.is_lecturer:
        return Response({
            "status": "error",
            "message": "only lecturers can create a course"
        }, status=status.HTTP_401_UNAUTHORIZED)

    submitted_user = User.objects.filter(id=user_id).first()

    course = Course.objects.filter(id=id).first()
    quest = Assignment.objects.filter(course=course, user=submitted_user)
    question = AssignmentSerializer(quest, many=True)

    return Response({
        "status": "success",
        "data": question.data,
        "message": "last submission"
    }, status=status.HTTP_200_OK)

# @method_decorator(csrf_exempt, name='dispatch')


class CourseList(APIView):

    def get(self, request):
        print(request.user)
        user = request.user
        user = User.objects.filter(id=user.id).first()
        if not user:
            return Response({"status": "error", "data": [], "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        cours = Course.objects.all()
        course = CourseSerializer(cours, many=True)
        return Response(
            course.data,
            status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        user = User.objects.filter(id=user.id).first()
        if not user:
            return Response({"status": "error", "data": [], "message": "User not found"},
                            status=status.HTTP_404_NOT_FOUND)

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
            "message": "Course added"
        }, status=status.HTTP_200_OK)


class CourseView(APIView):

    def get(self, request, id):
        print(request.user)
        user = request.user
        user = User.objects.filter(id=user.id).first()
        if not user:
            return Response({"status": "error", "data": [], "message": "User not found"},
                            status=status.HTTP_404_NOT_FOUND)

        ass = Assignment.objects.filter(course_id=id)
        course = AssignmentSerializer(ass, many=True)
        print(course)
        return Response(
            course.data,
            status=status.HTTP_200_OK)

    def delete(self, request, id):
        user = request.user
        user = User.objects.filter(id=user.id).first()
        if not user:
            return Response({"status": "error", "data": [], "message": "User not found"},
                            status=status.HTTP_404_NOT_FOUND)

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


# @method_decorator(csrf_exempt, name='dispatch')
class AssignmentList(APIView):

    def post(self, request):
        user = request.user
        print(request.user)
        user = User.objects.filter(id=user.id).first()
        if not user:
            return Response({
                "status": "error",
                "data": [],
                "message": "User not found"
            }, status=status.HTTP_404_NOT_FOUND)

        if not user.is_lecturer:
            return Response({
                "status": "error",
                "message": "only lecturers can create a course"
            }, status=status.HTTP_401_UNAUTHORIZED)

        course = request.data['course_id']
        assignment = AssignmentSerializer(data=request.data)
        assignment.is_valid(raise_exception=True)

        slug = slug_generator()
        assignment.validated_data['course_id'] = course
        assignment.validated_data['slug'] = slug
        assignment.save()
        quest = Assignment.objects.get(slug=slug)

        from autograderstable.autograder.autograder import AutograderPaths, Grader
        from autograderstable.autograder import guide

        current_dir = f'media/upload/{quest.slug}'
        os.mkdir(f"{current_dir}/")
        os.mkdir(f"{current_dir}/results")
        guide.main(AutograderPaths(current_dir))

        return Response({
            "status": "success",
            "data": assignment.data,
            "message": "Assignment added"
        }, status=status.HTTP_200_OK)

    def get(self, request):
        user = request.user
        user = User.objects.filter(id=user.id).first()
        if not user:
            return Response({"status": "error", "data": [], "message": "User not found"},
                            status=status.HTTP_404_NOT_FOUND)

        #course = request.data['course_id']
        quest = Assignment.objects.all()
        question = AssignmentSerializer(quest, many=True)
        return Response(
            question.data,
            status=status.HTTP_200_OK)


class AssignmentView(APIView):
    def get(self, request, id):
        user = request.user
        user = User.objects.filter(id=user.id).first()
        if not user:
            return Response({"status": "error", "data": [], "message": "User not found"},
                            status=status.HTTP_404_NOT_FOUND)

        quest = Assignment.objects.filter(id=id).first()
        question = AssignmentSerializer(quest)

        return Response(
            question.data,
            status=status.HTTP_200_OK)

    def put(self, request, id):
        user = request.user
        user = User.objects.filter(id=user.id).first()
        if not user:
            return Response({"status": "error", "data": [], "message": "User not found"},
                            status=status.HTTP_404_NOT_FOUND)

        if not user.is_lecturer:
            return Response({
                "status": "error",
                "message": "only lecturers can create an assignment"
            }, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        quest = Assignment.objects.filter(id=id).first()
        question = AssignmentSerializer(quest, data=data, partial=True)
        question.is_valid(raise_exception=True)
        question.save()

        return Response({
            "status": "success",
            "data": question.data,
            "message": "Assignment query succesful"
        }, status=status.HTTP_200_OK)

    def delete(self, request, id):
        user = request.user
        user = User.objects.filter(id=user.id).first()
        if not user:
            return Response({"status": "error", "data": [], "message": "User not found"},
                            status=status.HTTP_404_NOT_FOUND)

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
            num += 1

        return Response({
            "status": "success",
            "data": testcases,
            "message": "Testcase added"
        }, status=status.HTTP_200_OK)

    def get(self, request, id):
        user = request.user
        user = User.objects.filter(id=user.id).first()
        if not user:
            return Response({"status": "error", "data": [], "message": "User not found"},
                            status=status.HTTP_404_NOT_FOUND)

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
        user = request.user
        user = User.objects.filter(id=user.id).first()
        if not user:
            return Response({"status": "error", "data": [], "message": "User not found"},
                            status=status.HTTP_404_NOT_FOUND)

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
        user = request.user
        user = User.objects.filter(id=user.id).first()
        if not user:
            return Response({
                "status": "error",
                "data": [],
                "message": "User not found"
            }, status=status.HTTP_404_NOT_FOUND)

        f = request.data['file']
        assignment_id = request.data['assignment_id']
        sub = Submission.objects.create(
            file=f, user_id=user.id, assignment_id=assignment_id)
        file_sub = SubmissionSerializer(sub).data
        id = file_sub['id']

        file = Submission.objects.get(id=id)
        # run the autograder
        os.system(
            f"python ./runner.py 'media/upload/{file.assignment.slug}' '{file.id}'")

        file = Submission.objects.get(id=id)
        file_serializer = SubmissionSerializer(file)

        if os.path.exists(f"media/{file.file}"):
            os.remove(f"media/{file.file}")

        return Response(
            file_serializer.data,
            status=status.HTTP_201_CREATED)

    def get(self, request):

        user = request.user
        user = User.objects.filter(id=user.id).first()
        if not user:
            return Response({"status": "error", "data": [], "message": "User not found"},
                            status=status.HTTP_404_NOT_FOUND)

        sub = Submission.objects.get(user_id=user)
        if not sub:
            return Response({
                "status": "success",
                "message": "No question with id"
            }, status=status.HTTP_404_NOT_FOUND)

        files = Submission.objects.filter(assignment_id=sub)
        file_serializer = SubmissionSerializer(files, many=True)

        return Response({
            "status": "success",
            "data": file_serializer.data,
            "message": "Assignment added"
        }, status=status.HTTP_200_OK)

    def get(self, request, id):

        user = request.user
        user = User.objects.filter(id=user.id).first()
        if not user:
            return Response({"status": "error", "data": [], "message": "User not found"},
                            status=status.HTTP_404_NOT_FOUND)

        if not user.is_lecturer:
            return Response({
                "status": "error",
                "message": "Unauthorized"
            }, status=status.HTTP_401_UNAUTHORIZED)

        sub = Submission.objects.get(id=id)
        if not sub:
            return Response({
                "status": "success",
                "message": "No submission with id"
            }, status=status.HTTP_404_NOT_FOUND)

        files = Submission.objects.filter(assignment_id=sub)
        file_serializer = SubmissionSerializer(files, many=True)

        return Response({
            "status": "success",
            "data": file_serializer.data,
            "message": "Submission query completed"
        }, status=status.HTTP_200_OK)
