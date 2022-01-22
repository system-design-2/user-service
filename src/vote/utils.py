import logging

from django.conf import settings

from .models import Result

logger = logging.getLogger('user_app')


def all_same(items):
    return len(set(items)) < 2


def check_winner(restaurant_ids, restaurant_id):
    consecutive_working_days = settings.CONSECUTIVE_WORKING_DAYS - 1
    winner = True
    if restaurant_ids:
        if all_same(restaurant_ids) and restaurant_id == restaurant_ids[0]:
            winner = False
    logger.info(
        f"previous {consecutive_working_days} days winner Restaurant list Ids{restaurant_ids}; "
        f"Given Restaurant Id {restaurant_id}; "
        f"Winner {winner}")
    return winner


def get_previous_winner_restaurant_ids():
    consecutive_working_days = settings.CONSECUTIVE_WORKING_DAYS - 1
    restaurant_ids = list(Result.objects.all().values_list('menu__restaurant_id', flat=True)
                          [:consecutive_working_days:-1])
    return restaurant_ids
