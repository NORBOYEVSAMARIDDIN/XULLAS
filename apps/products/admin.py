from django.contrib import admin
from .models import Catalog, Product


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'catalog']
    list_filter = ['catalog']
    search_fields = ['name', 'description']
