import factory
from django.contrib.auth.models import User

from users.models import Device


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'john%s' % n)
    password = factory.PostGenerationMethodCall('set_password', 'bs23')
    email = factory.LazyAttribute(lambda o: '%s@example.org' % o.username)


class DeviceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Device

    device_token = factory.Sequence(lambda n: 'fklfahoadsfbgwfwhifw54548%s' % n)
    # fcm_token = factory.Sequence(lambda n: 'fcmhvasgasgdashjasasgsdagvdj%s' % n)
    user = factory.SubFactory(UserFactory)
