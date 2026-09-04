from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    def __generate_cart(self):
        from sale.models import Cart    
        cart, created = Cart.objects.get_or_create(member=self)
        return cart

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not hasattr(self, 'cart'):
            self.cart = self.__generate_cart()


class Banner(models.Model):
    image = models.ImageField(upload_to='shop/banner/')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.image.url
