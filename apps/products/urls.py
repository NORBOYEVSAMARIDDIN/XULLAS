from django.urls import path
from . import views
app_name='products'
urlpatterns = [
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('food_details', views.food_details, name='food_details'),
    path('food_shop', views.food_shop, name='food_shop'),
    path('help', views.help, name='help'),
    path('payment_failed', views.payment_failed, name='payment_failed'),
    path('payment_success', views.payment_success, name='payment_success'),
    path('payment_details', views.payment_details, name='payment_details'),
    path('shop/', views.shop, name='shop'),
    path('shop/<int:id>/', views.shop, name='shop'),


    path('create_product/', views.create_product, name='create_product'),
    path('list_products/', views.list_products, name='list_products'),
    path('get_product/<int:id>/', views.get_product, name='get_product'),
    path('update_product/<int:id>/', views.update_product, name='update_product'),
    path('delete_product/<int:id>/', views.delete_product, name='delete_product'),


    path('create_catalog/', views.create_catalog, name='create_catalog'),
    path('list_catalogs/', views.list_catalogs, name='list_catalogs'),
    path('get_catalog/<int:id>/', views.get_catalog, name='get_catalog'),
    path('update_catalog/<int:id>/', views.update_catalog, name='update_catalog'),
    path('delete_catalog/<int:id>/', views.delete_catalog, name='delete_catalog'),
]