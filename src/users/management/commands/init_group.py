import logging

from django.conf import settings
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


def command():
    logger.info("Initiating Groups")
    initial_groups = [
        {
            'name': settings.EMPLOYEE,
        },
        {
            'name': settings.MANAGER,
        }
    ]
    for item in initial_groups:
        group = Group.objects.filter(name=item['name']).first()
        if not group:
            group = Group(
                **item
            )
            group.save()
    logger.info('-------------- SUCCESS --------------')


class Command(BaseCommand):
    def handle(self, **options):
        command()
