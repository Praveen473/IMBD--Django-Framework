from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class TestRegisterCase(APITestCase):
    def test_register(self):
        data = {
            "username": "testcased",
            "email": "testexample@123.com",
            "password": "dddd@123",
            "password2": "dddd@123"
        }
        response = self.client.post(reverse('register'), data)
        # self.assertRedirects(response, reverse('expected_redirect_view'))
        print(response.status_code)
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class LoginLogoutTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example",
                                             password="NewPassword@123")

    def test_login(self):
        data = {
            "username": "example",
            "password": "NewPassword@123"
        }
        response = self.client.post(reverse('login'), data)
        print(response.status_code)
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_logout(self):
    #     self.token = Token.objects.get(user__username="example")
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    #     response = self.client.post(reverse('logout'))
    #     print(response.status_code)
    #     print(response.content)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
