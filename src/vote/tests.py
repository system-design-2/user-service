from datetime import datetime

from django.conf import settings
from rest_framework import status

from restaurant.factories import MenuFactory
from users.tests import UserBaseTestCase
from vote.factories import VoteFactory

from .models import Vote


# Create your tests here.
class VoteTestCase(UserBaseTestCase):
    def test_vote_today_menu(self):
        """
        Voting for restaurant menu.
        """
        menu_obj = MenuFactory()

        data = {
            "menu": menu_obj.id
        }
        today_datetime = datetime.now()
        voting_deadline = today_datetime.replace(hour=settings.VOTING_LAST_HOUR, minute=0, second=0, microsecond=0)
        deadline_over = False
        if voting_deadline < today_datetime:
            deadline_over = True

        # Voting for employee1
        self.client.credentials(HTTP_AUTHORIZATION='Bearer  ' + self.employee1_access_token)
        response = self.client.post(self.vote_url, data, format='json')
        if deadline_over:
            self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        else:
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Vote.objects.count(), 1)
            self.assertEqual(Vote.objects.all().last().employee, self.employee_one)
            self.assertEqual(Vote.objects.all().last().menu, menu_obj)

    def test_vote_result_today_menu(self):
        """
        Getting results for the current day. The winner restaurant should not be the winner for 3 consecutive working days
        """
        # Create n Vote
        n = 5
        for i in range(n):
            VoteFactory()

        today_datetime = datetime.now()
        voting_deadline = today_datetime.replace(hour=settings.VOTING_LAST_HOUR, minute=0, second=0, microsecond=0)
        deadline_over = False
        if voting_deadline < today_datetime:
            deadline_over = True

        # getting result for today votes
        self.client.credentials(HTTP_AUTHORIZATION='Bearer  ' + self.admin_access_token)
        response = self.client.get(self.vote_result_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Vote.objects.count(), n)

        # publish result for today vote
        self.client.credentials(HTTP_AUTHORIZATION='Bearer  ' + self.admin_access_token)
        response = self.client.post(self.vote_result_publish_url)
        if deadline_over:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        else:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
