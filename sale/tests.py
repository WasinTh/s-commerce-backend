from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from sale.models import CartItem, Order
from catalog.factories import ProductFactory
from shop.factories import MemberFactory

class CartFunctionalTestCase(TestCase):
    def setUp(self):
        self.member = MemberFactory()
        self.cart = self.member.cart
        self.product = ProductFactory()

    def test_cart_creation(self):
        self.assertEqual(self.cart.member, self.member)
        self.assertEqual(self.cart.items.count(), 0)

    def test_checkout(self):
        email = "test@example.com"
        address = "123 Main St, Anytown, USA"
        slip_image = "test.jpg"
        self.cart.items.create(product=self.product, quantity=10)
        self.assertEqual(self.cart.items.count(), 1)
        self.assertEqual(self.cart.total_price, self.product.price * 10)
        self.cart.checkout(email, address, slip_image)
        self.cart.refresh_from_db()
        self.assertEqual(self.cart.items.count(), 0)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.first().email, email)
        self.assertEqual(Order.objects.first().shipping_address, address)
        self.assertEqual(Order.objects.first().slip_image, slip_image)
        self.assertEqual(Order.objects.first().status, Order.Status.PENDING)


class CartAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.member = MemberFactory()
        self.client.force_authenticate(user=self.member.user)
        self.cart = self.member.cart
        self.product = ProductFactory()
        
    def test_add_item_to_cart(self):
        response = self.client.post("/api/sale/add-cart-item/", {
            'product': self.product.id,
            'quantity': 10
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(CartItem.objects.first().product, self.product)
        self.assertEqual(CartItem.objects.first().quantity, 10)
