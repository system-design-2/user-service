from datetime import datetime

from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import NotAcceptable, ValidationError

from restaurant.serializers import MenuListSerializer
from vote.models import Result


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'

    def validate(self, attrs):
        today_datetime = datetime.now()
        voting_deadline = today_datetime.replace(hour=settings.VOTING_LAST_HOUR, minute=0, second=0, microsecond=0)
        if voting_deadline > today_datetime:
            raise NotAcceptable(
                f"Voting result publish failed, it can be published after voting deadline at {voting_deadline}")
        return attrs


class ResultDetailsSerializer(serializers.ModelSerializer):
    menu = MenuListSerializer()

    class Meta:
        model = Result
        fields = ['menu', 'publish_date', 'number_of_votes',
                  'created_by', 'updated_by', 'created_at', 'updated_at']
