from django.db import models

from base.models import BaseModel
from restaurant.models import Menu
from users.models import Employee


# Create your models here.
class Vote(BaseModel):
    voting_date = models.DateField(null=False, blank=False)
    menu = models.ForeignKey(
        Menu,
        on_delete=models.RESTRICT,
        related_name='votes_manu'
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.RESTRICT,
        related_name='votes_employee'
    )

    class Meta:
        ordering = [
            '-voting_date',
        ]
        db_table = 'vote'
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'
        unique_together = ['voting_date', 'employee']
        indexes = [
            models.Index(fields=['voting_date']),
        ]


class Result(BaseModel):
    publish_date = models.DateField(null=False, blank=False, unique=True)
    menu = models.OneToOneField(
        Menu,
        on_delete=models.RESTRICT,
        related_name='result'
    )
    number_of_votes = models.IntegerField(null=False, blank=False)

    class Meta:
        ordering = [
            '-publish_date',
        ]
        db_table = 'result'
        verbose_name = 'result'
        verbose_name_plural = 'result'
