from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def item_count(self):
        return self.products.all().count()
    

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(null=True, blank=True, upload_to='products/')
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return f"{self.name} - {self.price}"

