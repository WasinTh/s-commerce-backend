import django_filters as filters
from .models import Product


class ProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = []

    name = filters.CharFilter(lookup_expr='icontains')
    cheap = filters.BooleanFilter(method='filter_cheap', label='Get Product price less than 20,000')

    def filter_cheap(self, queryset, name, value):
        if value:
            return queryset.filter(price__lte=10000)
        else:
            return queryset.filter(price__gt=10000)
