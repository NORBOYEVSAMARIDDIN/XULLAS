from django.db import models

# Create your models here.
class Catalog(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    price = models.IntegerField()
    description = models.TextField()
    photo = models.ImageField(upload_to='product_photos/')
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name