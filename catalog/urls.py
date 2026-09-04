from django.urls import path, include
from rest_framework.routers import DefaultRouter
from catalog import views

router = DefaultRouter()
router.register('product', views.ProductView, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('category/', views.CategoryView.as_view()),
    path('product-detail/<int:product_id>/', views.ProductDetailView.as_view())
]
