from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from restaurant.models import Menu

from .restaurant import RestaurantDetailsSerializer


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

    def validate(self, attrs):
        user = self.context['request'].user
        if attrs['restaurant'].manager != user:
            raise PermissionDenied()
        return attrs


class MenuDetailsSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(required=False)
    restaurant = RestaurantDetailsSerializer()

    class Meta:
        model = Menu
        fields = ['id', 'name', 'image', 'description', 'menu_date', 'price', 'restaurant',
                  'created_by', 'updated_by', 'created_at', 'updated_at']

    def get_image(self, instance):
        image_url = None
        request = self.context.get('request', None)
        if instance.image:
            image_url = request.build_absolute_uri(instance.image.url)
        return image_url


class MenuListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Menu
        fields = ['id', 'name', 'image', 'description', 'menu_date', 'price']

    def get_image(self, instance):
        image_url = None
        request = self.context.get('request', None)
        if instance.image:
            image_url = request.build_absolute_uri(instance.image.url)
        return image_url
