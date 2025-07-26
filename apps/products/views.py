from django.shortcuts import render, redirect, get_object_or_404
from . models import Product, Catalog
from django.http import Http404
from django.contrib import messages
from .permissions import superuser_required




# Create your views here.
def cart(request):
    return render(request, 'cart.html')

def checkout(request):
    return render(request, 'checkout.html')

def food_details(request):
    return render(request, 'food-details.html')

def food_shop(request):
    return render(request, 'food-shop.html')

def help(request):
    return render(request, 'help.html')

def payment_failed(request):
    return render(request, 'payment-failed.html')

def payment_success(request):
    return render(request, 'payment-success.html')

def payment_details(request):
    return render(request, 'payment-details.html')

def shop(request):
    return render(request, 'shop.html')






#PRODUCTS VIEWS
@superuser_required
def create_product(request):
    if request.method == 'POST' and request.FILES.get("image"):
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        photo = request.FILES["image"]
        catalog_id = request.POST.get('catalog_id')

        if Product.objects.filter(name=name).exists():
            messages.error(request, "This name field should be unique!")
            return redirect('products:create_product')

        try:
            catalog = get_object_or_404(Catalog, id=catalog_id)
        except Http404:
            messages.error(request, "The catalog does not exist.")
            return redirect('products:create_product')

        Product.objects.create(
            name=name,
            price=price,
            description=description,
            photo=photo,
            catalog=catalog
        )
        messages.success(request, "Product successfully created!")
        return redirect('products:list_products')

    catalogs = Catalog.objects.all()
    return render(request, 'products/create.html', {'catalogs': catalogs})


@superuser_required
def list_products(request):
    print('hello')
    products = Product.objects.all()
    return render(request, 'products/list.html', {'products': products})


@superuser_required
def get_product(request, id):
    try:
        product = get_object_or_404(Product, id=id)
    except Http404:
        messages.error(request, "The product does not exist.")
        return redirect('products:list_products')
    return render(request, 'products/get.html', {'product': product})


@superuser_required
def update_product(request, id):
    try:
        product = get_object_or_404(Product, id=id)
    except Http404:
        messages.error(request, "The product does not exist.")
        return redirect('products:list_products')

    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        new_photo = request.FILES.get("photo")
        catalog_id = request.POST.get('catalog_id')

        if Product.objects.filter(name=name).exclude(id=product.id).exists():
            messages.error(request, "This name field should be unique!")
            return redirect('products:update_product', id=id)

        try:
            catalog = get_object_or_404(Catalog, id=catalog_id)
        except Http404:
            messages.error(request, "The catalog does not exist.")
            return redirect('products:update_product', id=id)

        changed = (
            product.name != name or
            str(product.price) != price or
            product.description != description or
            (new_photo is not None) or
            product.catalog.id != catalog.id
        )

        if not changed:
            return redirect('products:list_products')

        product.name = name
        product.price = price
        product.description = description
        if new_photo:
            product.photo = new_photo
        product.catalog = catalog
        product.save()

        messages.success(request, "Product successfully updated!")
        return redirect('products:list_products')

    catalogs = Catalog.objects.all()
    return render(request, 'products/update.html', {'product': product, 'catalogs': catalogs})


@superuser_required
def delete_product(request, id):
    try:
        product = get_object_or_404(Product, id=id)
    except Http404:
        messages.error(request, "The product does not exist.")
        return redirect('products:list_products')
    product.delete()
    messages.success(request, "Product successfully deleted!")
    return redirect('products:list_products')






#CATALOG VIEWS
@superuser_required
def create_catalog(request):
    if request.method == 'POST':
        name = request.POST.get('name')

        if Catalog.objects.filter(name=name).exists():
            messages.error(request, "This name field should be unique!")
            return redirect('products:create_catalog')

        Catalog.objects.create(
            name=name,
        )
        messages.success(request, "Catalog successfully created!")
        return redirect('products:list_catalogs')

    return render(request, 'catalogs/create.html')


@superuser_required
def list_catalogs(request):
    catalogs = Catalog.objects.all()
    print('hello')
    return render(request, 'catalogs/list.html', {'catalogs': catalogs})


@superuser_required
def get_catalog(request, id):
    try:
        catalog = get_object_or_404(Catalog, id=id)
    except Http404:
        messages.error(request, "The catalog does not exist.")
        return redirect('catalog:list_catalogs')
    return render(request, 'catalogs/get.html', {'catalog': catalog})


@superuser_required
def update_catalog(request, id):
    try:
        catalog = get_object_or_404(Catalog, id=id)
    except Http404:
        messages.error(request, "The catalog does not exist.")
        return redirect('products:list_catalogs')

    if request.method == 'POST':
        name = request.POST.get('name')

        if Catalog.objects.filter(name=name).exclude(id=catalog.id).exists():
            messages.error(request, "This name field should be unique!")
            return redirect('products:update_catalog')

        changed = (
            catalog.name != name
        )

        if not changed:
            return redirect('products:list_catalogs')

        catalog.name = name
        catalog.save()

        messages.success(request, "Catalog successfully updated!")
        return redirect('products:list_catalogs')

    return render(request, 'catalogs/update.html', {'catalog': catalog})


@superuser_required
def delete_catalog(request, id):
    try:
        catalog = get_object_or_404(Catalog, id=id)
    except Http404:
        messages.error(request, "The catalog does not exist.")
        return redirect('products:list_catalogs')
    catalog.delete()
    messages.success(request, "Catalog successfully deleted!")
    return redirect('products:list_catalogs')