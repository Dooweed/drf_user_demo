import factory
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from factory.django import DjangoModelFactory

from users.models import User


class UserFactory(DjangoModelFactory):
    # Excluded
    profile = factory.Faker('simple_profile')
    PASSWORD = '123'

    username = factory.LazyAttribute(lambda p: p.profile['username'])
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.LazyAttribute(lambda p: p.profile['mail'])
    is_active = True
    is_staff = factory.Faker('boolean', chance_of_getting_true=50)
    is_superuser = factory.Faker('boolean', chance_of_getting_true=20)
    date_joined = factory.Faker('date_time', tzinfo=timezone.get_current_timezone(), end_datetime=timezone.now())
    password = factory.LazyAttribute(lambda p: make_password(p.PASSWORD))

    class Meta:
        model = User
        django_get_or_create = ['username']
        exclude = ['PASSWORD', 'profile']
