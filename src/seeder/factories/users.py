from django.contrib.auth.models import User
from factory import django
from faker import Faker, factory

faker = Faker()


class UserFactory(django.DjangoModelFactory):
    is_active = True

    class Meta:
        model = User
