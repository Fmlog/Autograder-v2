from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('register/student', views.RegisterStudentViews.as_view(), name='register'),
    path('register/lecturer', views.RegisterLecturerViews.as_view(), name='register'),
    path('login', views.LoginViews.as_view(), name='login'),
    path('user', views.UserViews.as_view(), name='user'),
]