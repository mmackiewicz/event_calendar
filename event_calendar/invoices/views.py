__author__ = 'Marek Mackiewicz'

from django.http import Http404, HttpResponse
from django.views.decorators.http import require_GET, require_POST

from tools.http import JsonResponse
from models import Invoice
from products.models import Product


@require_POST
def create_invoice_view(request):
    number = request.POST['number']
    company = request.POST['company']
    return JsonResponse(create_invoice(number=number, company=company))

def create_invoice(number, company, is_paid=False):
    invoice = Invoice(number=number, company=company, is_paid=is_paid)
    invoice.save()
    return invoice.id


@require_GET
def get_invoice_view(request, invoice_id):
    try:
        invoice = Invoice.objects.get(pk=invoice_id)
        return JsonResponse(data=invoice)
    except Product.DoesNotExist:
        return Http404

@require_GET
def get_invoices_list(request, year, month):
    try:
        invoice = Invoice.objects.get()
        return JsonResponse(data=invoice)
    except Product.DoesNotExist:
        return Http404