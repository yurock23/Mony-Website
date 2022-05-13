"""
Celeste Ha, Linh Luu, Yurock Heo
COM214 Final Project
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

# Create your models here.
CATEGORY_CHOICES = (
    ('M', 'Men'),
    ('F', 'Women'),
    ('D','Decorations'),
    ('A','Accessories'),
)


class Product(models.Model):
    item_name = models.CharField(max_length=100)
    item_image = models.ImageField(upload_to='static/images')
    item_description = models.TextField(max_length=500, blank = True)
    item_category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    item_price = models.FloatField()

    def get_absolute_url(self):
        return reverse('products:product_details', args=[str(self.id)])

    def get_add_to_cart_url(self):
        return reverse("products:add_cart", args=[str(self.id)])

    def get_remove_one_from_cart_url(self):
        return reverse("products:remove_cart_one", args=[str(self.id)])

    def get_remove_from_cart_url(self):
        return reverse("products:remove_cart", args=[str(self.id)])

    def __str__(self):
        return self.item_name
        

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    customer = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    complete = models.BooleanField(default=False)


    def get_total(self):
        return self.product.item_price * self.quantity


class Order(models.Model):
    customer = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, blank=False)
    items = models.ManyToManyField(OrderItem)

    def __str__(self):
        return str(self.id)

    def get_cart_total(self):
        total = sum([item.get_total() for item in self.items.all()])
        return str(total)

    def checkout(self):
        return reverse("products:checkout")

class Review(models.Model):
    #fields
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    created_on = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(
        get_user_model(),
        on_delete = models.CASCADE,
    )

    def __str__(self):
        return self.body
