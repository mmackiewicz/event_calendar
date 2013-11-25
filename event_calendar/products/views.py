__author__ = 'Marek Mackiewicz'

from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
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
        errors = []
        name = request.POST['name'].strip()
        create_product(name=name)
        products = Product.objects.all()
        return render(request, 'products_list.html', {'products': products,
                                                      'errors': errors,})
    return render(request, 'product_create_form.html')

@csrf_exempt
@require_POST
@is_in_roles([ROLE_DISPATCHER, ROLE_ADMIN])
def validate_product_create(request):
    name = request.POST['name'].strip()
    if Product.objects.filter(name=name):
        return JsonResponse(data={'status': 'ERROR',
                                  'errors': ['Product with name %s already exists'%(name,)],
                                  })
    return JsonResponse(data={'status': 'OK'})

def create_product(name):
    product = Product(name=name)
    product.save()
    return product

@require_http_methods(['GET', 'POST'])
@is_in_roles([ROLE_DISPATCHER, ROLE_ADMIN])
def update_product_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        errors = []
        name = request.POST['name'].strip()
        update_product(product, name=name)
        products = Product.objects.all()
        return render(request, 'products_list.html', {'products': products,
                                                      'errors': errors})
    return render(request, 'product_create_form.html', {'product': product})

@csrf_exempt
@require_POST
@is_in_roles([ROLE_DISPATCHER, ROLE_ADMIN])
def validate_product_update(request, product_id):
    name = request.POST['name'].strip()
    product = Product.objects.filter(name=name)
    if product and not product[0].id == int(product_id):
        return JsonResponse(data={'status': 'ERROR',
                                  'errors': ['Product with name %s already exists'%(name,)],
                                  })
    return JsonResponse(data={'status': 'OK'})

def update_product(product, name):
    product.name = name
    product.save()
    return product

@require_GET
def get_product_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return JsonResponse(data=product)


@require_GET
@is_in_roles([ROLE_DISPATCHER, ROLE_ADMIN])
def get_all_products_view(request):
    products = Product.objects.all()
    return render(request, 'products_list.html', {'products': products})