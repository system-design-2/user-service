from django.conf import settings
from django.contrib.auth.models import Group, User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from base.models import BaseModel


# Create your models here.
class Restaurant(BaseModel):
    class Status(models.TextChoices):
        ACTIVE = 'active', _('active')
        INACTIVE = 'inactive', _('inactive')
        CLOSED = 'closed', _('closed')
        SUSPENDED = 'suspended', _('suspended')
        ARCHIVED = 'archived', _('archived')

    name = models.CharField(max_length=255, unique=True)
    address = models.TextField(null=False, blank=False)
    latitude = models.FloatField(
        validators=[MaxValueValidator(90), MinValueValidator(-90)]
    )
    longitude = models.FloatField(
        validators=[MaxValueValidator(180), MinValueValidator(-180)]
    )
    phone = models.CharField(max_length=15, null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.ACTIVE
    )
    manager = models.OneToOneField(
        User,
        on_delete=models.RESTRICT,
        null=True,
        related_name='restaurant_manager',
    )

    class Meta:
        ordering = [
            'name',
        ]
        db_table = 'restaurant'
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['status']),
        ]


class Menu(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=False, blank=False)
    menu_date = models.DateField(null=False, blank=False)
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='menus_restaurant'
    )
    price = models.FloatField(default=0, blank=True)
    image = models.ImageField(upload_to='menu', blank=True, null=True)

    class Meta:
        ordering = [
            '-menu_date',
        ]
        db_table = 'menu'
        verbose_name = 'menu'
        verbose_name_plural = 'menu'
        unique_together = ['menu_date', 'restaurant']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['menu_date']),
        ]


@receiver(post_save, sender=Restaurant)
def assign_default_group_manager(sender, instance: Restaurant, created, **kwargs):
    if created:
        instance.manager.groups.add(Group.objects.get(name=settings.MANAGER))
