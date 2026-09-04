from django.urls import path
from sale.views import AddCartItemView, CartDetailView, SubmitPaymentView

urlpatterns = [
    path('add-cart-item/', AddCartItemView.as_view()),
    path('cart-detail/', CartDetailView.as_view()),
    path('submit-payment/', SubmitPaymentView.as_view())
]
