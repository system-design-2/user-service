from datetime import datetime

from django.conf import settings
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import (NotAcceptable, PermissionDenied,
                                       ValidationError)

from restaurant.serializers import MenuListSerializer
from users.models import Employee
from vote.models import Vote


class VoteSerializer(serializers.ModelSerializer):
    voting_date = serializers.DateField(required=False, read_only=True)
    employee = serializers.PrimaryKeyRelatedField(required=False, read_only=True)

    class Meta:
        model = Vote
        fields = '__all__'

    def validate(self, attrs):
        today_datetime = datetime.now()
        voting_deadline = today_datetime.replace(hour=settings.VOTING_LAST_HOUR, minute=0, second=0, microsecond=0)
        if attrs['menu'].menu_date != today_datetime.date():
            raise NotAcceptable("You can't vote future or past date")
        elif voting_deadline < today_datetime:
            raise NotAcceptable(f"Voting deadline time is over. Please vote before at {voting_deadline}")
        return attrs

    def create(self, validated_data):
        try:
            validated_data['voting_date'] = validated_data['menu'].menu_date
            validated_data['employee'] = self.context['request'].user.employee
            vote = Vote.objects.create(**validated_data)
            return vote
        except IntegrityError:
            raise serializers.ValidationError("Duplicate Vote!!! You can vote only one restaurant in a day")


class VoteDetailsSerializer(serializers.ModelSerializer):
    menu = MenuListSerializer()

    class Meta:
        model = Vote
        fields = '__all__'
