from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.CourseView.as_view()),
    path('assignment', views.AssignmentView.as_view()),
    path('file-upload', views.SubmissionView.as_view()),
    path('file-upload/<str:id>', views.SubmissionView.as_view()),
    path('testcase', views.TestCaseView.as_view()),
    path('testcase/<str:id>', views.TestCaseView.as_view()),
    path('<str:id>', views.AssignmentView.as_view()),
]
