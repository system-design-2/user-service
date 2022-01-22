from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        exclude = ['password']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        # At this point, user is a User object that has already been
        # saved to the database. You can continue to change its
        # attributes if you want to change other fields.

        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)
    old_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')
