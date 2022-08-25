from django.http import HttpResponse
from urllib import response
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from .serializers import UserSerializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from .models import User
import jwt, datetime

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

# Create your views here.
@api_view(('GET',))
def test(request):
    if request.method == "GET":
        return Response({"status": "success", "data": "its alive", "message" : "user created"}, status=status.HTTP_200_OK)


class RegisterLecturerViews(APIView):
    ''' Create new lecturer user '''
    def post(self, request):
        serializer = UserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['is_lecturer'] = True
        serializer.save()
        return Response({"status": "success", "data": serializer.data, "message" : "user created"}, status=status.HTTP_200_OK)


class RegisterStudentViews(APIView):
    ''' Create new student user '''
    def post(self, request):
        serializer = UserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['is_student'] = True
        serializer.save()

        return Response({"status": "success", "data": serializer.data, "message" : "user created"}, status=status.HTTP_200_OK)


class RegisterAdminViews(APIView):
    ''' Create new admin user '''
    def post(self, request):
        serializer = UserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['is_superuser'] = True
        serializer.validated_data['is_staff'] = True
        serializer.save()
        return Response({"status": "success", "data": serializer.data, "message" : "user created"}, status=status.HTTP_200_OK)


class LoginViews(APIView):
    ''' Authentication '''
    def post(self, request):
        email = request.data.get('login_id')
        password = request.data.get('password')

        user = User.objects.filter(login_id=email).first()

        if user is None:
            raise AuthenticationFailed('Invalid credentials')

        if not user.check_password(password):
            raise AuthenticationFailed('Password is incorrect')

        # 'iat' means the date it was created
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            'iat': datetime.datetime.utcnow()
        }

        serializer = UserSerializers(user)
        token = jwt.encode(payload, 'SECRET_KEY', algorithm='HS256')
        response = Response()

        response.set_cookie('token', token, httponly=True)
        response.data = {
            "status" : "success",
            "data" : serializer.data,
            "message" : "Login Successful",
            "token" : token
        }

        return response

# @login_required()
class UserViews(APIView):

    def get(self, request):
        ''' Get the token from the cookie
            and return current user's details '''
        token = request.COOKIES.get('token')
        if token is None:
            raise AuthenticationFailed('Invalid credentials')

        payload = jwt.decode(token, 'SECRET_KEY', algorithms='HS256')

        user = User.objects.filter(id=payload['id']).first()
        if not user:
            return Response({"status": "error", "data": [], "message" : "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializers(user)

        return Response({
            "status": "success",
            "data": serializer.data,
            "message": "user details"
        }, status=status.HTTP_200_OK)

    def delete(self, request):
        ''' Get the token from the cookie
            and return current user's details '''
        token = request.COOKIES.get('token')
        if token is None:
            raise AuthenticationFailed('Invalid credentials')

        payload = jwt.decode(token, 'SECRET_KEY', algorithms='HS256')

        item = get_object_or_404(User, id=payload['id'])
        item.soft_delete()
        return Response({"status": "success", "data": [], "message": "user deleted"})

class LogoutViews(APIView):
    ''' logout by deleting token from the cookie '''

    def get(self, request):
        # logout(request)

        response = Response()
        response.delete_cookie('token')
        response.data = {
            "status": "success",
            "message" : "Logout Successful"
        }
        return response