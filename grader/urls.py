from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.CourseList.as_view()),
    path('<str:id>/', views.CourseView.as_view()),
    path("assignment/", views.AssignmentList.as_view()),
    path('assignment/<str:id>/', views.AssignmentView.as_view()),
    path('assignment/course/<str:id>', views.getCourseAssignment),
    path('submission', views.SubmissionView.as_view()),
    path('submission/<str:id>', views.SubmissionView.as_view()),
    path('submission/<str:id>/last', views.getLastSubmission),
    path('submission/<str:id>/<str:user_id>>', views.getUserSubmission),
    path('testcase', views.TestCaseView.as_view()),
    path('testcase/<str:id>', views.TestCaseView.as_view()),
]
