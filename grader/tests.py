
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from home.models import User
from grader.models import TestCase, Assignment, Submission, Course


class AssignmentTestCase(APITestCase):
    url = reverse('assignment')

    def setUp(self):
        self.user = User.objects.create(name="test_user",
                                        password="password123",
                                        login_id="test@mail.com",
                                        role=2)

    def test_create_assignment(self):
        data = {
            "name": "test_assignment",
            "course_id": '1',
            "description": 'test'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class CourseTestCase(APITestCase):
    url = reverse('course')

    def setUp(self):
        self.user = User.objects.create(name="test_user",
                                        password="password123",
                                        login_id="test@mail.com",
                                        role=2)

    def test_create_assignment(self):
        data = {
            "name": "test_course",
            "course_code": '1'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
