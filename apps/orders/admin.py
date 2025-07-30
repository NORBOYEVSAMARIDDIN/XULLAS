from django.contrib import admin
from .models import Order, OrderAddress, OrderItem
# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status']
    list_filter = ['user']
    search_fields = ['user', 'status']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity']
    list_filter = ['order']
    search_fields = ['order', 'product', 'quantity']

@admin.register(OrderAddress)
class OrderAddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'address', 'latitude', 'longitude']
    list_filter = ['order']
    search_fields = ['order', 'order', 'latitude', 'longitude']