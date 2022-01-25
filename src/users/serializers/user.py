from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from users.models import Employee, Device
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


class EmployeeSerializer(serializers.ModelSerializer):
    user = RegisterSerializer()

    class Meta:
        model = Employee
        fields = ['employee_id', 'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data.pop('password2')
        user = User.objects.create_user(**user_data)
        employee = Employee.objects.create(user=user, **validated_data)
        return employee


class EmployeeDetailsSerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer()

    class Meta:
        model = Employee
        fields = ['id', 'employee_id', 'user']
