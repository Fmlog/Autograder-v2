import json

from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from home.models import User
from home.serializers import UserSerializers

class RegistrationTestCase(APITestCase):
    url = reverse('register')

    def test_registration(self):
        data = {
            "name": "test_user",
            "login_id": "test@mail.com",
            "password": "password123"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class LoginTestCase(APITestCase):
    url = reverse('login')

    def setUp(self):
        self.user = User.objects.create(name="test_user",
                                        password="password123",
                                        login_id="test@mail.com",
                                        role="2")

    def test_login(self):
        data = {
            "login_id": "test@mail.com",
            "password": "password123"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class UserTestCase(APITestCase):
    user_url = reverse('user')

    def setUp(self):
        self.user = User.objects.create(name="test_user",
                                        password="password123",
                                        login_id="test@mail.com",
                                        role="2")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_user_detail_retrieved(self):
        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "test")
