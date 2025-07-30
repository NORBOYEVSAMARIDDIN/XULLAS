from django.db import models
from apps.products.models import Product
from apps.users.models import User
# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(User, related_name='cart', on_delete=models.CASCADE)

    def __str__(self):
        return f'Cart belongs to \'{self.user.username}\''

    @property
    def items_count(self):
        return self.cartitems.count()

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cartitems')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems')

    def __str__(self):
        return f'{self.product} in {self.cart}'