import json

from django.conf import settings
from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.factories import UserFactory, DeviceFactory
from users.models import Device


# Create your tests here.
class UserBaseTestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse("users:auth-register")
        self.login_url = reverse("users:auth-login")
        self.logout_url = reverse("users:auth-logout")

        self.device_url = reverse("users:device")

        # Create Employee and Manager Group
        self.employee_group = Group.objects.create(name=settings.EMPLOYEE)
        self.manager_group = Group.objects.create(name=settings.MANAGER)
        self.password = "bs23"

        # create a super user
        self.admin = UserFactory(username="admin", is_superuser=True, is_staff=True)
        self.user1 = UserFactory(username="user1")
        self.user2 = UserFactory(username="user2")

        self.admin_access_token = self.get_jwt_token({"username": self.admin.username, "password": self.password})
        self.user1_access_token = self.get_jwt_token(
            {"username": self.user.user1.username, "password": self.password})
        self.employee2_access_token = self.get_jwt_token(
            {"username": self.user.user2.username, "password": self.password})

        self.user = UserFactory(username="mahfuz11")

    def get_jwt_token(self, user_data):
        data = {"username": user_data['username'], "password": user_data['password']}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token_data = json.loads(response.content)['data']
        self.assertTrue("access" in token_data.keys())
        access_token = token_data.get('access', "")
        return access_token


class UserAuthenticationTestCase(UserBaseTestCase):
    def test_user_registration(self):
        """
        Ensure we can register a new user
        """
        data = {
            'username': "user1",
            'first_name': "User",
            'last_name': "One",
            'email': "user1@gmail.com",
            'password': self.password,
            "password2": self.password,
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().last().username, "user1")

    def test_user_registration_login(self):
        """
        Ensure an user can login and get access and refresh token
        """
        user_obj = UserFactory()
        data = {"username": user_obj.username, "password": self.password}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token_data = json.loads(response.content)['data']
        self.assertTrue("refresh" in token_data.keys())
        self.assertTrue("access" in token_data.keys())

    def test_user_registration_logout(self):
        """
        Ensure an user can login and get access and refresh token and logout with the token
        """
        user_obj = UserFactory()
        data = {"username": user_obj.username, "password": self.password}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token_data = json.loads(response.content)['data']
        self.assertTrue("refresh" in token_data.keys())
        self.assertTrue("access" in token_data.keys())
        access_token = token_data.get('access', "")
        refresh_token = token_data.get('refresh', "")

        data = {"refresh_token": refresh_token}
        self.client.credentials(HTTP_AUTHORIZATION='Bearer  ' + access_token)
        response = self.client.post(self.logout_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)


class DeviceTestCase(UserBaseTestCase):
    def test_device_creation(self):
        """
        Ensure we can create a employee with user.
        """
        data = {
            "device_name": "One Plus 9 Pro",
            "device_model": "One Plus 9 Pro",
            "device_make": "One Plus",
            "device_token": "asjasfhadhjfvafvjasvg4585",
            "fcm_token": "asjasfhadhjfvafvjasvg4585HJGJHFF",
            "status": True,
            "is_fingerprint_enabled": True,
            "is_passcode_enabled": True,
            "user": self.user1
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer  ' + self.user1_access_token)
        response = self.client.post(self.device_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Device.objects.get(device_token=data["asjasfhadhjfvafvjasvg4585"]).device_token, data["asjasfhadhjfvafvjasvg4585"])
