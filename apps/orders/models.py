from django.db import models
from apps.users.models import User
from apps.products.models import Product

class OrderStatus(models.TextChoices):
    ORDERED = 'ordered', 'Ordered'
    COLLECTING = 'collecting', 'Collecting'
    DELIVERING = 'delivering', 'Delivering'
    SHIPPED = 'shipped', 'Shipped'
    ACCEPTED = 'accepted', 'Accepted'
    CANCELED = 'canceled', 'Canceled'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # created_at = models.DateTimeField(auto_now_add=True, default='11-11-2011')
    # updated_at = models.DateTimeField(auto_now=True, default='11-11-2011')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.ORDERED,
    )

    @property
    def items_count(self):
        return self.orderitems.count()

    def __str__(self):
        return self.user.username
    
class OrderAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='orderaddress')
    address = models.CharField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f'{self.address}'

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orderitem')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitem')
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product} in {self.order}'
    

    @property
    def total_price(self):
        return self.product.price * self.quantity