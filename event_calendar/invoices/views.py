__author__ = 'Marek Mackiewicz'

from django.conf import settings
from django.http import Http404, HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import get_object_or_404, render

from tools.auth import is_in_roles
from tools.http import JsonResponse
from models import Invoice
from products.models import Product
from workers.models import ROLE_ADMIN, ROLE_SECRETARY

from datetime import datetime
from dateutil.relativedelta import relativedelta

@require_POST
@is_in_roles([ROLE_ADMIN, ROLE_SECRETARY])
def create_invoice_view(request):
    number = request.POST['number']
    company = request.POST['company']
    return JsonResponse(create_invoice(number=number, company=company).id)

def create_invoice(number, company, is_paid=False):
    invoice = Invoice.objects.create(number=number, company=company, is_paid=is_paid)
    return invoice


@require_GET
@is_in_roles([ROLE_ADMIN, ROLE_SECRETARY])
def get_invoice_view(request, invoice_id):
    try:
        invoice = Invoice.objects.get(pk=invoice_id)
        return JsonResponse(data=invoice)
    except Product.DoesNotExist:
        return Http404

@require_GET
@is_in_roles([ROLE_ADMIN, ROLE_SECRETARY])
def get_invoices_list(request, year, month):
    start_date = datetime.strptime('-'.join((year,month,'01')), '%Y-%m-%d')
    end_date = (start_date + relativedelta(months=1)) + relativedelta(days=-1)

    invoices = Invoice.objects.filter(returntransport__returnevent__return_date__gte=start_date, returntransport__returnevent__return_date__lte=end_date)

    return render(request, "invoices_list.html", {'invoices': invoices,
                                                  'year': year,
                                                  'month': month,
                                                  'companies': settings.OWN_COMPANIES})