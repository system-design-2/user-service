from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from restaurant.models import Restaurant
from users.serializers import RegisterSerializer, UserDetailsSerializer


class RestaurantSerializer(serializers.ModelSerializer):
    manager = RegisterSerializer()

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'latitude', 'longitude', 'phone', 'manager']

    def create(self, validated_data):
        user_data = validated_data.pop('manager')
        user_data.pop('password2')
        user = User.objects.create_user(**user_data)
        restaurant = Restaurant.objects.create(manager=user, **validated_data)
        return restaurant


class RestaurantDetailsSerializer(serializers.ModelSerializer):
    manager = UserDetailsSerializer()

    class Meta:
        model = Restaurant
        fields = '__all__'
