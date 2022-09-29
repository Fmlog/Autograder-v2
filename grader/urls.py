from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.CourseView.as_view(), name="course"),
    path('<str:id>/', views.CourseViewByID.as_view(), name="course-detail"),
    path('assignment', views.AssignmentView.as_view(), name="assignment"),
    path('assignment/<str:id>/', views.AssignmentViewByID.as_view(), name="assignment-detail"),
    path('assignment/submission', views.SubmissionView.as_view(), name="submission"),
    path('assignment/submission/<str:id>', views.SubmissionView.as_view(), name="submission-list"),
    path('assignment/testcase', views.TestCaseView.as_view(), name="testcase"),
    path('assignment/testcase/<str:id>', views.TestCaseView.as_view(), name="testcase-delete"),
]
