from django.conf import settings
from django.contrib.auth.models import Group, User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from base.models import BaseModel


# Table for Device Registration
class Device(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_device'
    )
    device_name = models.CharField(max_length=50, blank=True)
    device_model = models.CharField(max_length=50, blank=True)
    device_make = models.CharField(max_length=50, blank=True)
    device_token = models.CharField(max_length=250, blank=True, unique=True)
    fcm_token = models.CharField(max_length=500, blank=True, null=True, default="")
    status = models.BooleanField(default=True, blank=True)
    is_fingerprint_enabled = models.BooleanField(default=False, blank=True)
    is_passcode_enabled = models.BooleanField(default=False, blank=True)

    class Meta:
        db_table = 'device'
        verbose_name_plural = 'Devices'
        verbose_name = 'Device'
        ordering = ['-id']

    def __str__(self):
        return "{} {}".format(self.user, self.device_name)


class Employee(BaseModel):
    employee_id = models.CharField(max_length=255, unique=True)
    user = models.OneToOneField(User, on_delete=models.RESTRICT, related_name='employee')

    class Meta:
        db_table = 'employee'
        verbose_name_plural = 'Employees'
        verbose_name = 'Employee'
        # ordering = ['-id']

    def __str__(self):
        return "{} {}".format(self.employee_id, self.user)


@receiver(post_save, sender=Employee)
def assign_default_group_employee(sender, instance: Employee, created, **kwargs):
    if created:
        instance.user.groups.add(Group.objects.get(name=settings.EMPLOYEE))
