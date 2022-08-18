from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from .models import File
from .autograde import autograde

from .serializers import QuestionSerializer, FileSerializer
from home.models import User

# Create your views here.
# @login_required()
class QuestionView(APIView):

    #validating user authentication
    def validate_user(self, request):
        token = request.COOKIES.get('token')
        if token is None:
            raise AuthenticationFailed('Invalid credentials')

        payload = jwt.decode(token, 'SECRET_KEY', algorithms='HS256')

        user = User.objects.filter(id=payload['id']).first()
        if not user:
            return False, user

        return True, user

    def get(self, request):
        pass


    def post(self, request):
        # user = request.user

        stat, user = self.validate_user(request)
        if not stat:
            return Response({"status": "error", "data": [], "message": "User not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = QuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['lecturer'] = user
        serializer.save()
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class FileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):

        # file = File.objects.filter(id='32010825-936d-4590-b914-5b88023024f2').first()
        # print(file.file.url)

        file_serializer = FileSerializer(data=request.data)

        if not file_serializer.is_valid():
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        file_serializer.save()
        id = file_serializer.data.id
        response = autograde(id)

        return Response({
            "status": "success",
            "data": file_serializer.data,
            # "result": response
        }, status=status.HTTP_201_CREATED)