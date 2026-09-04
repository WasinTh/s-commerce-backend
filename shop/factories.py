import factory
from django.utils import timezone
from django.contrib.auth import get_user_model
from shop.models import Member


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Faker('email')


class MemberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Member

    user = factory.SubFactory(UserFactory)
    address = factory.Faker('address')
