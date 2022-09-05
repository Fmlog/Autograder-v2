from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from .serializers import UserSerializers
from rest_framework.response import Response
from rest_framework import status
from .models import User

from home.tokens import create_jwt_pair_for_user


class RegisterLecturerViews(APIView):
    ''' Create new teacher user '''

    def post(self, request):
        serializer = UserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['role'] = User.TEACHER
        serializer.save()
        return Response({
            "status": "success",
            "data": serializer.data,
            "message": "user created"
        }, status=status.HTTP_200_OK)


class RegisterStudentViews(APIView):
    ''' Create new student user '''

    def post(self, request):
        serializer = UserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['role'] = User.STUDENT
        serializer.save()

        return Response({"status": "success", "data": serializer.data, "message": "user created"}, status=status.HTTP_200_OK)


class RegisterAdminViews(APIView):
    ''' Create new admin user '''

    def post(self, request):
        serializer = UserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['is_superuser'] = True
        serializer.validated_data['is_staff'] = True
        serializer.save()
        return Response({"status": "success", "data": serializer.data, "message": "user created"}, status=status.HTTP_200_OK)


class LoginViews(APIView):
    ''' Authentication '''

    def post(self, request):
        email = request.data.get('login_id')
        password = request.data.get('password')

        user = authenticate(login_id=email, password=password)
        if not user:
            return Response({
                "status": "error",
                "message": "incorrect credentials"
            }, status=status.HTTP_404_NOT_FOUND)

        token = create_jwt_pair_for_user(user)

        serializer = UserSerializers(user)

        return Response({
            "status": "success",
            "data": serializer.data,
            "token": token,
            "message": "Login Successful"
        }, status=status.HTTP_200_OK)


class UserViews(APIView):

    def get(self, request):
        user = request.user
        user = User.objects.filter(id=user.id).first()
        if not user:
            return Response({"status": "error", "data": [], "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializers(user)

        return Response({
            "status": "success",
            "data": serializer.data,
            "message": "user details"
        }, status=status.HTTP_200_OK)

    def delete(self, request):
        user = request.user
        user = User.objects.filter(id=user.id).first()
        if not user:
            return Response({"status": "error", "data": [], "message": "User not found"},
                            status=status.HTTP_404_NOT_FOUND)

        user.soft_delete()
        return Response({"status": "success", "data": [], "message": "user deleted"})
