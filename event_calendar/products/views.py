__author__ = 'Marek Mackiewicz'

from django.http import Http404, HttpResponse
from django.shortcuts import render, render_to_response, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from tools.http import JsonResponse
from tools.auth import is_in_roles
from workers.models import ROLE_DISPATCHER, ROLE_ADMIN
from forms import ProductForm
from models import Product


@require_http_methods(['GET', 'POST'])
@is_in_roles([ROLE_DISPATCHER, ROLE_ADMIN])
def create_product_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product_code = form.cleaned_data['product_code']
            name = form.cleaned_data['name']
            units = form.cleaned_data['units']
            product = create_product(product_code=product_code, name=name, units=units)
            return JsonResponse(product.id)
    else:
        form = ProductForm()
    return render(request, 'product_create_form.html', {'form': form})


def create_product(product_code, name, units):
    product = Product(product_code=product_code, name=name, units=units)
    product.save()
    return product

@require_http_methods(['GET', 'POST'])
@is_in_roles([ROLE_DISPATCHER, ROLE_ADMIN])
def update_product_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product_code = form.cleaned_data['product_code']
            name = form.cleaned_data['name']
            units = form.cleaned_data['units']
            product = update_product(product, product_code=product_code, name=name, units=units)
            return JsonResponse(product.id)
    else:
        form = ProductForm(initial={'product_code': product.product_code,
                                    'name': product.name,
                                    'units': product.units})
    return render(request, 'product_create_form.html', {'form': form})

def update_product(product, product_code, name, units):
    product.product_code = product_code
    product.name = name
    product.units = units
    product.save()
    return product

@require_GET
def get_product_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return JsonResponse(data=product)


@require_GET
def get_all_products_view(request):
    products = Product.objects.all()
    return render(request, 'products_list.html', {'products': products})