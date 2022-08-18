from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.QuestionView.as_view()),
    path('file-upload', views.FileView.as_view()),
    path('file-upload/<str:id>', views.FileView.as_view()),
    path('testcase', views.TestCaseView.as_view()),
    path('testcase/<str:id>', views.TestCaseView.as_view()),
    path('<str:id>', views.QuestionView.as_view()),
]
