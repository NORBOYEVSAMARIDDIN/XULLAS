from django.contrib import admin
from .models import Cart, CartItem
# Register your models here.
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']
    search_fields = ['user']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'cart']
    list_filter = ['cart']
    search_fields = ['product', 'cart']