from django.db import models
from shop.models import Product
from functools import reduce
from django.conf import settings

# Create your models here.
class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    online_order_id = models.CharField(max_length=50, blank=True, null=True, unique=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return f'order {self.id}'
    
    def get_total(self):
        product_cost = sum(items.get_cost() for items in self.items.all() ) 
        delivery_charge = self.get_delivery_charge()
        total = product_cost + delivery_charge
        return total 
    
    def get_delivery_charge(self):
        charge = 0 
        total_quantity = reduce(lambda x,y: x + y.quantity,self.items.all(),0)
        charge = total_quantity * settings.DELIVERY_CHARGE_PER_ITEM
        return int(charge)

    def get_order_url(self):
        return f'https://dashboard.razorpay.com/app/payments/{self.online_order_id}'
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name='items',on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name='order_items',on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        return self.price* self.quantity

class OrderDetails(models.Model):
    order = models.OneToOneField(Order, related_name="order_details", on_delete=models.CASCADE)
    requested_delivery_date = models.DateTimeField()