from datetime import date

import factory

from restaurant.factories import MenuFactory
from users.factories import EmployeeFactory

from .models import Result, Vote


class VoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vote

    voting_date = date.today()
    menu = factory.SubFactory(MenuFactory)
    employee = factory.SubFactory(EmployeeFactory)


class ResultFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Result

    menu = factory.SubFactory(MenuFactory)
