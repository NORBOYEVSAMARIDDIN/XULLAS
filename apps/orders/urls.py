from django.urls import path,include
from . import views
app_name='orders'

urlpatterns = [
    path('', views.list_orders, name='list'),
    path('create_order/', views.create_order, name='create_order'),
    path('orders/<int:order_id>/update-status/', views.update_order_status, name='update_order_status'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('cancel/<int:order_id>/', views.cancel_order, name='cancel')
]