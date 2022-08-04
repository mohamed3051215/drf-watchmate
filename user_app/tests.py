from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse


class RegisterTestCase(APITestCase):

    def test_register(self):
        data = {
            "username": "mohamedayman",
            "email": "mohamed@gmail.com",
            "password": "MohamedAyman@123",
            "password2": "MohamedAyman@123"
        }

        response = self.client.post(reverse("register"), data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         f"Got wrong status code {response.status_code}")


class LoginLogoutTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example",
                                             password="NewPassword@123")
        self.token = Token.objects.create(user=self.user)

    def test_login(self):
        data = {
            "username": "example",
            "password": "NewPassword@123"
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self): 
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
