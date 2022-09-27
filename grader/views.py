from cgitb import reset
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import api_view

import shutil
import random
import string
import os
import jwt

from grader.models import TestCase, Assignment, Submission, Course
from home.models import User
from grader.serializers import (AssignmentSerializer, ConfigSerializer,
                                CourseSerializer, SubmissionSerializer,
                                TestCaseSerializer, Config)


def slug_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """
    It generates a slug for naming an assignment directory.
    """
    return ''.join(random.choice(chars) for _ in range(size))


def handle_uploaded_file(f):
    """
    It takes a file object, and saves it to a file on the server.
    
    :param f: The file object that was uploaded
    """
    with open(f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def validate_user(request):
    """
    It checks if the user is logged in.
    This is used for securing the API endpoints
    
    :param request: The request object
    """
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
    if not user.is_authenticated:
        return Response(
            {
                "status": "error",
                "data": [],
                "message": "User not found"
            },
            status=status.HTTP_404_NOT_FOUND)

    course = Course.objects.filter(id=id).first()
    quest = Assignment.objects.filter(course=course)
    question = AssignmentSerializer(quest, many=True)

    return Response(
        {
            "status": "success",
            "data": question.data,
            "message": f"Assignments for {course.name}"
        },
        status=status.HTTP_200_OK)


@api_view(['GET'])
def getAllSubmissions(request, id):
    user = request.user
    if not user.is_authenticated:
        return Response(
            {
                "status": "error",
                "data": [],
                "message": "User not found"
            },
            status=status.HTTP_404_NOT_FOUND)

    course = Course.objects.filter(id=id).first()
    quest = Assignment.objects.filter(course=course)
    question = AssignmentSerializer(quest, many=True)

    return Response(
        {
            "status": "success",
            "data": question.data,
            "message": "Assignment query succesful"
        },
        status=status.HTTP_200_OK)


@api_view(['GET'])
def getLastSubmission(request, id):
    user = request.user
    if not user.is_authenticated:
        return Response(
            {
                "status": "error",
                "data": [],
                "message": "User not found"
            },
            status=status.HTTP_404_NOT_FOUND)

    if user.role != User.TEACHER:
        return Response(
            {
                "status": "error",
                "message": "only lecturers can create a course"
            },
            status=status.HTTP_401_UNAUTHORIZED)

    course = Course.objects.filter(id=id).first()
    quest = Assignment.objects.filter(course=course).order_by('-id').first()
    question = AssignmentSerializer(quest, many=True)

    return Response(
        {
            "status": "success",
            "data": question.data,
            "message": "last submission"
        },
        status=status.HTTP_200_OK)


@api_view(['GET'])
def getUserSubmission(request, id, user_id):
    user = request.user
    if not user.is_authenticated:
        return Response(
            {
                "status": "error",
                "data": [],
                "message": "User not found"
            },
            status=status.HTTP_404_NOT_FOUND)

    if user.role != User.TEACHER:
        return Response(
            {
                "status": "error",
                "message": "only lecturers can create a course"
            },
            status=status.HTTP_401_UNAUTHORIZED)

    submitted_user = User.objects.filter(id=user_id).first()

    course = Course.objects.filter(id=id).first()
    quest = Assignment.objects.filter(course=course, user=submitted_user)
    question = AssignmentSerializer(quest, many=True)

    return Response(
        {
            "status": "success",
            "data": question.data,
            "message": "last submission"
        },
        status=status.HTTP_200_OK)


class CourseView(APIView):
    '''
    View for handling request to the course models'''

    def get(self, request):
        """
        Fetches all courses.        
        """
        print(request.user)
        user = request.user
        if not user.is_authenticated:
            return Response(
                {
                    "status": "error",
                    "data": [],
                    "message": "User not found"
                },
                status=status.HTTP_404_NOT_FOUND)

        cours = Course.objects.all()
        course = CourseSerializer(cours, many=True)
        return Response(course.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Creates a new course. Only accessible to teacher user
        
        :param request: The course as a form-data
        """

        user = request.user
        if not user.is_authenticated:
            return Response(
                {
                    "status": "error",
                    "data": [],
                    "message": "User not found"
                },
                status=status.HTTP_404_NOT_FOUND)

        if user.role != User.TEACHER:
            return Response(
                {
                    "status": "error",
                    "message": "only lecturers can create a course"
                },
                status=status.HTTP_401_UNAUTHORIZED)

        course = CourseSerializer(data=request.data)
        course.is_valid(raise_exception=True)
        course.save()

        return Response(
            {
                "status": "success",
                "data": course.data,
                "message": "Course added"
            },
            status=status.HTTP_200_OK)


class CourseViewByID(APIView):
    '''
    View for handling requests on a single course i.e. by `id`
    '''

    def get(self, request, id):
        """
        Returns all data (assignments) associated with a course.
        
        :param request: The request that was sent to the view
        :param id: The id of the course to be retrieved
        """
        user = request.user
        if not user.is_authenticated:
            return Response(
                {
                    "status": "error",
                    "data": [],
                    "message": "User not found"
                },
                status=status.HTTP_404_NOT_FOUND)

        ass_obj = Assignment.objects.filter(course_id=id)
        assignments = AssignmentSerializer(ass_obj, many=True)
        return Response(assignments.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        user = request.user
        if not user.is_authenticated:
            return Response(
                {
                    "status": "error",
                    "data": [],
                    "message": "User not found"
                },
                status=status.HTTP_404_NOT_FOUND)

        if user.role != User.TEACHER:
            return Response(
                {
                    "status": "error",
                    "message": "You are not a lecturer"
                },
                status=status.HTTP_401_UNAUTHORIZED)

        course = get_object_or_404(Course, id=id)
        course.delete()

        return Response({
            "status": "success",
            "message": "Course deleted"
        },
                        status=status.HTTP_200_OK)


class AssignmentView(APIView):
    '''
    View for handling request to the assignment models'''

    def post(self, request):
        """
        A function that is called when a POST request is made to the server.
        
        :param request: The assignment as a form-data
        """
        user = request.user
        if not user.is_authenticated:
            return Response(
                {
                    "status": "error",
                    "data": [],
                    "message": "User not found"
                },
                status=status.HTTP_404_NOT_FOUND)

        if user.role != User.TEACHER:
            return Response(
                {
                    "status": "error",
                    "message": "only lecturers can create a course"
                },
                status=status.HTTP_401_UNAUTHORIZED)

        course = request.data['course_id']
        assignment_data = AssignmentSerializer(data=request.data)
        assignment_data.is_valid(raise_exception=True)

        slug = slug_generator()
        assignment_data.validated_data['course_id'] = course
        assignment_data.validated_data['slug'] = slug
        assignment_data.save()
        # Fetching actual assignment object
        assignment = Assignment.objects.get(slug=slug)

        # Run autograder on the server to create assignment directory structure
        from grader_core.autograder.autograder import AutograderPaths
        from grader_core.autograder import guide

        current_dir = f'media/upload/{assignment.slug}'
        os.mkdir(f"{current_dir}/")
        os.mkdir(f"{current_dir}/results")
        guide.main(AutograderPaths(current_dir))

        #Add testcases and config file from request
        for f in request.FILES.getlist('testcase'):
            TestCase.objects.create(file=f, assignment=assignment)
        for f in request.FILES.getlist('config'):
            Config.objects.create(file=f, assignment=assignment)

        return Response(
            {
                "status": "success",
                "data": assignment_data.data,
                "message": "Assignment added"
            },
            status=status.HTTP_200_OK)

    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response(
                {
                    "status": "error",
                    "data": [],
                    "message": "User not found"
                },
                status=status.HTTP_404_NOT_FOUND)

        quest = Assignment.objects.filter(id=user.id)
        question = AssignmentSerializer(quest, many=True)
        return Response(question.data, status=status.HTTP_200_OK)


class AssignmentViewByID(APIView):
    '''
    View for handling requests on a single course i.e. by `id`
    '''

    def get(self, request, id):
        """
        Returns all data associated with an assignment.
        
        :param request: The request that was sent to the view
        :param id: The id of the assignment to be retrieved
        """
        user = request.user
        if not user.is_authenticated:
            return Response(
                {
                    "status": "error",
                    "data": [],
                    "message": "User not found"
                },
                status=status.HTTP_404_NOT_FOUND)

        ass_obj = Assignment.objects.filter(id=id).first()
        assignment = AssignmentSerializer(ass_obj)
        testcase_obj = TestCase.objects.filter(assignment=ass_obj)
        testcases = TestCaseSerializer(testcase_obj, many=True)
        conf_obj = Config.objects.filter(assignment=ass_obj)
        config = ConfigSerializer(conf_obj)

        return Response(
            {
                id: assignment.data,
                "testcase": testcases.data,
                #"config": config.data
            },
            status=status.HTTP_200_OK)

    def put(self, request, id):
        user = request.user
        if not user.is_authenticated:
            return Response(
                {
                    "status": "error",
                    "data": [],
                    "message": "User not found"
                },
                status=status.HTTP_404_NOT_FOUND)

        if user.role != User.TEACHER:
            return Response(
                {
                    "status": "error",
                    "message": "only lecturers can edit an assignment"
                },
                status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        quest = Assignment.objects.filter(id=id).first()
        question = AssignmentSerializer(quest, data=data, partial=True)
        question.is_valid(raise_exception=True)
        question.save()

        return Response(
            {
                "status": "success",
                "data": question.data,
                "message": "Assignment query succesful"
            },
            status=status.HTTP_200_OK)

    def delete(self, request, id):
        user = request.user
        if not user.is_authenticated:
            return Response(
                {
                    "status": "error",
                    "data": [],
                    "message": "User not found"
                },
                status=status.HTTP_404_NOT_FOUND)

        if user.role != User.TEACHER:
            return Response(
                {
                    "status": "error",
                    "message": "You are not a lecturer"
                },
                status=status.HTTP_401_UNAUTHORIZED)

        question = get_object_or_404(Assignment, id=id)

        if os.path.exists(f"media/upload/{question.slug}"):
            shutil.rmtree(f"media/upload/{question.slug}")
        question.delete()

        return Response({
            "status": "success",
            "message": "Assignment deleted"
        },
                        status=status.HTTP_200_OK)


class TestCaseView(APIView):
    '''
    Handle requests on the testcase models
    '''

    def post(self, request):
        assignment_id = request.data['assignment_id']
        testcases = {}
        num = 1
        for f in request.FILES.getlist('file'):
            test = TestCase.objects.create(file=f, assignment_id=assignment_id)
            testcases[num] = TestCaseSerializer(test).data
            num += 1

        return Response(
            {
                "status": "success",
                "data": testcases,
                "message": "Testcase added"
            },
            status=status.HTTP_200_OK)

    def patch(self, request):
        pass

    def delete(self, request, id):
        user = request.user
        if not user.is_authenticated:
            return Response(
                {
                    "status": "error",
                    "data": [],
                    "message": "User not found"
                },
                status=status.HTTP_404_NOT_FOUND)

        if user.role != User.TEACHER:
            return Response(
                {
                    "status": "error",
                    "message": "You are not a lecturer"
                },
                status=status.HTTP_401_UNAUTHORIZED)

        testcase = get_object_or_404(TestCase, id=id)
        if os.path.exists(f"media/{testcase.file}"):
            os.remove(f"media/{testcase.file}")
        testcase.delete()

        return Response({
            "status": "success",
            "message": "Test case deleted"
        },
                        status=status.HTTP_200_OK)


class SubmissionView(APIView):
    '''
    Handle requests on the Submission models
    '''
    # Parses request form contents into QueryDict.
    # i.e. files would be stored in useful structure
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        """
        A function that is called when a POST request is made to the server.
        
        :param request: The request object
        """
        user = request.user
        if not user.is_authenticated:
            return Response(
                {
                    "status": "error",
                    "data": [],
                    "message": "User not found"
                },
                status=status.HTTP_404_NOT_FOUND)

        f = request.data['file']
        assignment_id = request.data['assignment_id']
        sub = Submission.objects.create(file=f,
                                        user_id=user.id,
                                        assignment_id=assignment_id)
        file_sub = SubmissionSerializer(sub).data
        id = file_sub['id']

        file = Submission.objects.get(id=id)
        # run the autograder and create a grading instance
        # the result of this grading instance was extracted directly
        # at ../grader_core/autograder/autograder.py
        os.system(
            f"python3 ./runner.py 'media/upload/{file.assignment.slug}' '{file.id}' "
        )

        file = Submission.objects.get(id=id)
        file_serializer = SubmissionSerializer(file)

        if os.path.exists(f"media/{file.file}"):
            os.remove(f"media/{file.file}")

        return Response(file_serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response(
                {
                    "status": "error",
                    "data": [],
                    "message": "User not found"
                },
                status=status.HTTP_404_NOT_FOUND)

        sub = Submission.objects.get(user_id=user)
        if not sub:
            return Response(
                {
                    "status": "success",
                    "message": "No question with id"
                },
                status=status.HTTP_404_NOT_FOUND)

        files = Submission.objects.filter(assignment_id=sub)
        file_serializer = SubmissionSerializer(files, many=True)

        return Response(
            {
                "status": "success",
                "data": file_serializer.data,
                "message": "Assignment added"
            },
            status=status.HTTP_200_OK)

    def get(self, request, id):
        user = request.user
        if not user.is_authenticated:
            return Response(
                {
                    "status": "error",
                    "data": [],
                    "message": "User not found"
                },
                status=status.HTTP_404_NOT_FOUND)

        if user.role != User.TEACHER:
            return Response({
                "status": "error",
                "message": "Unauthorized"
            },
                            status=status.HTTP_401_UNAUTHORIZED)

        assignment = Assignment.objects.get(id=id)
        if not assignment:
            return Response(
                {
                    "status": "success",
                    "message": "No submission with id"
                },
                status=status.HTTP_404_NOT_FOUND)

        submission = Submission.objects.filter(assignment_id=assignment)
        submission_data = SubmissionSerializer(submission, many=True)

        return Response(submission_data.data, status=status.HTTP_200_OK)
