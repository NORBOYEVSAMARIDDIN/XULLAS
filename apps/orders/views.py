from django.shortcuts import render, redirect
from .models import Order, OrderItem, OrderAddress, OrderStatus
from django.contrib import messages
from apps.products.models import Product
from django.shortcuts import redirect, get_object_or_404
from .models import Order
from django.contrib.auth.decorators import login_required

# Create your views here.
def list_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    order_items = OrderItem.objects.all()

    choices = OrderStatus.choices

    return render(request, 'orders.html', {'orders': orders, 'choices': choices})

def create_order(request):
    user = request.user
    order_dict = request.session.get('order_dict', {})
    address = request.session.get('address', '')
    latitude = request.session.get('latitude')
    longitude = request.session.get('longitude')

    #ORDER CREATING LOGIC HERE

    if not order_dict:
        messages.error(request, "Cart is empty")
        return redirect('cart:cart')
    
    order = Order.objects.create(user = user)

    order_address = OrderAddress.objects.create(
        order = order,
        address = address,
        latitude = latitude,
        longitude = longitude
    )
    
    for key, value in order_dict.items():
        product = Product.objects.get(id = key)
        OrderItem.objects.create(product = product, order = order, quantity = value)

    request.session.pop('order_dict', None)
    request.session.pop('address', None)
    request.session.pop('latitude', None)
    request.session.pop('longitude', None)

    return redirect('users:my-orders')

@login_required
def update_order_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id, user=request.user)
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()
    return redirect('orders:list')

@login_required
def delete_order(request, order_id):
    Order.objects.get(id = order_id).delete()
    return redirect('orders:list')

@login_required
def cancel_order(request, order_id):
    order = Order.objects.get(id = order_id)
    order.status = OrderStatus.CANCELED
    order.save()
    return redirect('users:my-orders')