__author__ = 'Marek Mackiewicz'

from django.http import Http404, HttpResponse
from django.views.decorators.http import require_GET, require_POST

from tools.http import JsonResponse
from models import Load
from products.models import Product


@require_POST
def create_load_view(request):
    product_id = request.POST['product']
    amount = request.POST['amount']
    product = Product.objects.get(pk=product_id)
    return JsonResponse(create_load(product=product, amount=amount))

def create_load(product, amount):
    load = Load(product=product, amount=amount)
    load.save()
    return load.id


@require_GET
def get_load_view(request, load_id):
    try:
        load = Load.objects.get(pk=load_id)
        return JsonResponse(data=load)
    except Product.DoesNotExist:
        return Http404
