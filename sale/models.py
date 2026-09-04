from django.db import models
from catalog.models import Product
from shop.models import Member


class Cart(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.member}"

    @property
    def total_price(self):
        price = 0
        for item in self.items.all():
            price += item.product.price * item.quantity
        return price

    @property
    def total_item(self):
        quantity = 0
        for item in self.items.all():
            quantity += item.quantity
        return quantity

    def __generate_order_items(self, order):
        for item in self.items.all():
            OrderItem.objects.create(
                order=order, 
                product=item.product, 
                quantity=item.quantity,
                price=item.product.price
            )

    def checkout(self, email, shipping_address, slip_image=None):
        order = Order.objects.create(
            cart=self, 
            email=email,
            shipping_address=shipping_address,
            slip_image=slip_image,
        )
        self.__generate_order_items(order)
        self.items.all().delete()  # clear cart items
        return order


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.cart.member} - {self.product.name} - {self.quantity}"


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending'
        CONFIRMED = 'confirmed'

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    email = models.EmailField()
    shipping_address = models.TextField()
    slip_image = models.ImageField(upload_to='slip_images/')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.cart.member} - {self.total_price} ({self.items.count()})"

    @property
    def total_price(self):
        return self.items.aggregate(
            total_price=models.Sum(models.F('price') * models.F('quantity'))
        )['total_price']

        #total_price = 0
        #for item in self.items.all():
        #    total_price += item.price * item.quantity
        #return total_price


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price per item")

    def __str__(self):
        return f"{self.order.cart.member} - {self.product.name} - {self.quantity}"

