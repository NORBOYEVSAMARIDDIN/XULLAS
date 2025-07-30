from django.urls import path
from . import views
app_name = 'cart'
urlpatterns = [
    path('add_product_to_cart/<int:id>/', views.add_product_to_cart, name='add_product_to_cart'),
    path('add/<int:id>/', views.add, name='add'),
    path('substract/<int:id>/', views.substract, name='substract'),
    path('', views.cart, name='cart'),
]