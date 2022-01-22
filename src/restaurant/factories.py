from datetime import date

import factory

from restaurant.models import Menu, Restaurant
from users.factories import UserFactory


class RestaurantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Restaurant
    name = factory.Sequence(lambda n: 'Restaurant Test %s' % n)
    latitude = 23.7470304
    longitude = 90.3671072
    manager = factory.SubFactory(UserFactory)


class MenuFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Menu

    menu_date = date.today()
    restaurant = factory.SubFactory(RestaurantFactory)
