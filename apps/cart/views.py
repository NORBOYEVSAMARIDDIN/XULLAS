from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from apps.products.models import Product
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from django.db.models import Count
from django.db.models import Count, F, FloatField, ExpressionWrapper
from django.conf import settings
from apps.users.models import UserAddress


@login_required
def add_product_to_cart(request, id=None):
    user = request.user
    try:
        cart = Cart.objects.get(user = user)
    except Cart.DoesNotExist:
        cart = ''

    if cart:
        print(cart)
    else:
        cart = Cart.objects.create(user = user)
    
    try:
        product = get_object_or_404(Product, id=id)
    except Http404:
        messages.error(request, "The product does not exist.")
        return redirect('products:list_products')

    cartItem = CartItem.objects.create(cart = cart, product = product)

    return redirect('products:shop', )

@login_required
def cart(request):
    user = request.user
    try:
        cart = Cart.objects.get(user = user)
    except Cart.DoesNotExist:
        cart = ''

    if not cart:
        cart = Cart.objects.create(user = user)
    product_cartitems = defaultdict(list)
    products = Product.objects.annotate(
    cartitem_count=Count('cartitems'),
    ).filter(
        cartitem_count__gt=0
    ).annotate(
        total_price=ExpressionWrapper(
            F('price') * F('cartitem_count'),
            output_field=FloatField()
        )
    )
    total = 0
    total_products = 0
    for product in products:
        total += product.total_price
        total_products += product.cartitem_count

    if request.method == 'POST':
        order_dict = {}
        for product in products:
            order_dict[product.id] = product.cartitem_count
            CartItem.objects.filter(cart = cart, product = product).delete()
        request.session['order_dict'] = order_dict
        request.session['address'] = request.POST.get('address')
        request.session['latitude'] = request.POST.get('latitude')
        request.session['longitude'] = request.POST.get('longitude')
        return redirect('orders:create_order')
    
    try:
        address = UserAddress.objects.get(user=user)
    except UserAddress.DoesNotExist:
        address = None

    return render(request, 'cart.html', {'products': products,
                                         'total': total, 
                                         'total_products': total_products, 
                                         'address': address,
                                         "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY})

@login_required
def add(request, id=None):
    user = request.user
    try:
        cart = Cart.objects.get(user = user)
    except Cart.DoesNotExist:
        cart = ''

    if not cart:
        cart = Cart.objects.create(user = user)
    
    try:
        product = get_object_or_404(Product, id=id)
    except Http404:
        messages.error(request, "The product does not exist.")
        return redirect('products:list_products')

    cartItem = CartItem.objects.create(cart = cart, product = product)

    return redirect('cart:cart')

@login_required
def substract(request, id=None):
    user = request.user
    try:
        cart = Cart.objects.get(user = user)
    except Cart.DoesNotExist:
        cart = ''

    if not cart:
        cart = Cart.objects.create(user = user)

    try:
        product = get_object_or_404(Product, id=id)
    except Http404:
        messages.error(request, "The product does not exist.")
        return redirect('products:list_products')
    
    cartItem = CartItem.objects.filter(cart = cart, product = product).first()
    cartItem.delete()

    return redirect('cart:cart')