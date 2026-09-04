from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import permissions
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from catalog.models import Category, Product
from catalog.serializers import CategorySerializer, ProductSerializer
from .filters import ProductFilter


class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductPagination(PageNumberPagination):
    page_size = 3  # Set default page to 1 for testing only
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data['total'] = self.page.paginator.count
        response.data['pages'] = self.page.paginator.num_pages
        response.data['current_page'] = self.page.number
        return response



class ProductView(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    filterset_class = ProductFilter


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = "id"
    lookup_url_kwarg = "product_id"

    def get_object(self):
        show_error = self.request.query_params.get('show_error', 'false').lower() == 'true'
        product_id = self.kwargs.get(self.lookup_url_kwarg)
        product = Product.objects.filter(id=product_id).first()
        if product is not None:
            return product
        elif show_error:
            raise NotFound(detail=f"Product id {product_id} not found")
        else:
            raise NotFound(detail={})

