import factory
from factory.django import DjangoModelFactory
from catalog.models import Product, Category


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker('name')
    description = factory.Faker('sentence')


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker('name')
    description = factory.Faker('sentence')
    price = factory.Faker('pyint', min_value=1000, max_value=50000)
    category = factory.SubFactory(CategoryFactory)
