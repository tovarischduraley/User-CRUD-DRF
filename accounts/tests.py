import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .api.serializers import *


class TestSetUp(APITestCase):
    def setUp(self):
        self.users_url = reverse('users')
        self.login_url = reverse('login')

        self.user_data = {
            'username': 'test_username',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'password': 'test_password',
            'is_active': True,
        }
        return super().setUp()

    def tearDown(self):
        return super().tearDown()


class TestViews(TestSetUp):
    def test_registration(self):
        response = self.client.post(self.users_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_authentication(self):
        self.client.post(self.users_url, self.user_data)
        response = self.client.post(self.login_url,
                                    {'username': self.user_data['username'], 'password': self.user_data['password']},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
