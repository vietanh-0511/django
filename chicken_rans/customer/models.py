from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.


class Category(models.Model):
    name_category = models.CharField(max_length=100, unique=True)


class Product(models.Model):
    name_product = models.CharField(max_length=255, unique=True)
    price = models.FloatField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)


class Order(models.Model):
    created_time = models.DateTimeField(auto_now_add=True, blank=True)
    name_customer = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)
    is_ordered = models.BooleanField(default=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Order_detail(models.Model):
    # property
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=CASCADE)
    price = models.FloatField()
    quantity = models.IntegerField()
    # method

    def get_price(self):
        return self.price*self.quantity

    class Meta:
        unique_together = (('order'), ('product'))
