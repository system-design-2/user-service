import json

from django.conf import settings
from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.factories import EmployeeFactory, UserFactory
from users.models import Employee


# Create your tests here.
class UserBaseTestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse("users:auth-register")
        self.login_url = reverse("users:auth-login")
        self.logout_url = reverse("users:auth-logout")
        self.employee_url = reverse("users:employee-list")
        self.restaurant_url = reverse("restaurant:restaurant-list")
        self.menu_url = reverse("restaurant:restaurant-menu-list")

        self.vote_url = reverse("vote:vote-list")
        self.vote_result_url = reverse("vote:voting-result-today")
        self.vote_result_publish_url = reverse("vote:voting-result-publish")

        # Create Employee and Manager Group
        self.employee_group = Group.objects.create(name=settings.EMPLOYEE)
        self.manager_group = Group.objects.create(name=settings.MANAGER)
        self.password = "bs23"

        # create a super user
        self.admin = UserFactory(username="admin", is_superuser=True, is_staff=True)
        self.employee_one = EmployeeFactory(employee_id="employee_1")
        self.employee_two = EmployeeFactory(employee_id="employee_2")

        self.admin_access_token = self.get_jwt_token({"username": self.admin.username, "password": self.password})
        self.employee1_access_token = self.get_jwt_token(
            {"username": self.employee_one.user.username, "password": self.password})
        self.employee2_access_token = self.get_jwt_token(
            {"username": self.employee_two.user.username, "password": self.password})

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


class EmployeeTestCase(UserBaseTestCase):
    def test_employee_creation(self):
        """
        Ensure we can create a employee with user.
        """
        data = {
            "employee_id": "employee10",
            "user": {
                "username": "employee10",
                "password": self.password,
                "password2": self.password,
                "email": "employee10@gmail.com",
                "first_name": "Employee",
                "last_name": "10"
            }
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer  ' + self.admin_access_token)
        response = self.client.post(self.employee_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.get(employee_id="employee10").employee_id, "employee10")
