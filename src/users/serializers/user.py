from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from users.models import Device
from users.serializers import RegisterSerializer, UserDetailsSerializer


class DeviceSerializer(serializers.ModelSerializer):
    # user = RegisterSerializer()

    class Meta:
        model = Device
        # exclude = ['created_at', 'updated_at', 'created_by', 'updated_by']
        fields = '__all__'
        # fields = ['employee_id', 'user']

    def validate(self, attrs):
        user = self.context['request'].user
        if attrs['user'] != user:
            raise PermissionDenied()
        return attrs



class DeviceListSerializer(serializers.ModelSerializer):
    # user_id = serializers.IntegerField(user.id)

    class Meta:
        model = Device
        exclude = ['created_at', 'updated_at', 'created_by', 'updated_by']
        # fields = '__all__'
        # fields = ['employee_id', 'user']