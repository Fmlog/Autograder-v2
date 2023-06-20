
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from home.models import User
from grader.models import TestCase, Assignment, Submission, Course
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

class CourseAPITest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(name='Math', description='Mathematics Course')
        self.assignment = Assignment.objects.create(title='Algebra', description='Algebra Assignment', course=self.course)

    def test_get_courses(self):
        # Test retrieving all courses
        url = reverse('course')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Assuming only one course is created

    def test_create_course(self):
        # Test creating a new course
        url = reverse('course')
        data = {'name': 'Physics', 'description': 'Physics Course'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)  # Assuming one course is already created

    def test_get_course_by_id(self):
        # Test retrieving a specific course by ID
        url = reverse('course-detail', args=[self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.course.id))

    def test_delete_course(self):
        # Test deleting a course
        url = reverse('course-detail', args=[self.course.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Course.objects.count(), 0)  # The course should be deleted

    def test_get_assignments(self):
        # Test retrieving all assignments
        url = reverse('assignment')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Assuming only one assignment is created

    def test_create_assignment(self):
        # Test creating a new assignment
        url = reverse('assignment')
        data = {'title': 'Calculus', 'description': 'Calculus Assignment', 'course': str(self.course.id)}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Assignment.objects.count(), 2)  # Assuming one assignment is already created

    def test_get_assignment_by_id(self):
        # Test retrieving a specific assignment by ID
        url = reverse('assignment-detail', args=[self.assignment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.assignment.id))

    def test_get_submissions(self):
        # Test retrieving all submissions
        url = reverse('submission')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add assertions based on the expected response data for submissions

    def test_create_submission(self):
        # Test creating a new submission
        url = reverse('submission')
        data = {'assignment': str(self.assignment.id), 'student_name': 'John Doe', 'code': 'print("Hello, World!")'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Add assertions based on the expected response data for the created submission

    def test_get_test_cases(self):
        # Test retrieving all test cases
        url = reverse('testcase')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add assertions based on the expected response data for test cases

    def test_delete_test_case(self):
        # Test deleting a test case
        url = reverse('testcase-delete', args=[self.test_case.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add assertions based on the expected behavior after deleting the test case

    # Add more test cases for other views and models based on the URL patterns

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
