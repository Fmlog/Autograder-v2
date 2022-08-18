
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.QuestionView.as_view(), name='question'),
    path('file-upload', views.FileView.as_view(), name='file'),
]