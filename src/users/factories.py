import factory
from django.contrib.auth.models import User

from users.models import Employee


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'john%s' % n)
    password = factory.PostGenerationMethodCall('set_password', 'bs23')
    email = factory.LazyAttribute(lambda o: '%s@example.org' % o.username)


class EmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Employee

    employee_id = factory.Sequence(lambda n: 'Employee Test%s' % n)
    user = factory.SubFactory(UserFactory)
