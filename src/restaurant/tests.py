import tempfile
from datetime import date

from django.contrib.auth.models import User
from PIL import Image
from rest_framework import status

from users.factories import User
from users.tests import UserBaseTestCase

from .factories import MenuFactory, RestaurantFactory
from .models import Menu, Restaurant


# Create your tests here.
class RestaurantTestCase(UserBaseTestCase):
    def test_restaurant_creation(self):
        """
        Ensure we can create a restaurant with manager user.
        """
        data = {
            "name": "Restaurant Test 1",
            "address": "Dhaka, Dhanmondi",
            "latitude": 23.7470304,
            "longitude": 90.3671072,
            "phone": "+8801520103197",
            "manager": {
                "username": "manager1",
                "password": self.password,
                "password2": self.password,
                "email": "manager1@gmail.com",
                "first_name": "Manager",
                "last_name": "1"
            }
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer  ' + self.admin_access_token)
        response = self.client.post(self.restaurant_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        manager_obj = User.objects.get(username="manager1")
        self.assertEqual(manager_obj.username, "manager1")

        restaurant_obj = Restaurant.objects.filter(name="Restaurant Test 1")
        self.assertEqual(restaurant_obj[0].name, "Restaurant Test 1")

    def test_menu_creation(self):
        """
        Ensure we can create a menu for a restaurant.
        """
        restaurant_obj = RestaurantFactory()

        # Get JWT token for this manager
        manager_access_token = self.get_jwt_token(
            {"username": restaurant_obj.manager.username, "password": self.password})

        # Test Menu Upload for this Restaurant with image
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)
        data = {
            "name": "Super Lunch 19",
            "description": "Vegetable, Rice, Chicken Curry, Fruits",
            "menu_date": date.today(),
            "restaurant": restaurant_obj.id,
            "price": 250,
            "image": tmp_file
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer  ' + manager_access_token)
        response = self.client.post(self.menu_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_getting_today_menu(self):
        """
        Ensure we can get current day menu from two restaurant.
        """
        # Create n Today Menu
        n = 5
        for i in range(n):
            MenuFactory()

        # Get today menu for a employee
        self.client.credentials(HTTP_AUTHORIZATION='Bearer  ' + self.employee1_access_token)
        response = self.client.get(self.menu_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Menu.objects.count(), n)
