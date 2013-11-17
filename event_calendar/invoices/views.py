__author__ = 'Marek Mackiewicz'

from django.conf import settings
from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.shortcuts import get_object_or_404, render, redirect

from tools.auth import is_in_roles
from tools.http import JsonResponse
from models import Invoice, INVOICE_TIMEOUT, INVOICE_OUTDATED
from products.models import Product
from workers.models import ROLE_ADMIN, ROLE_SECRETARY

from datetime import datetime
from dateutil.relativedelta import relativedelta

@require_GET
@is_in_roles([ROLE_ADMIN, ROLE_SECRETARY])
def create_invoice_view(request, transport_id):
    return render(request, 'invoice_create_form.html', {'companies': settings.OWN_COMPANIES,
                                                        'transport_id': transport_id})

def create_invoice(number, company, issue_date, is_paid=False):
    invoice = Invoice.objects.create(number=number, company=company, issue_date=issue_date, is_paid=is_paid)
    return invoice

@require_http_methods(['GET', 'POST'])
@is_in_roles([ROLE_ADMIN, ROLE_SECRETARY])
def edit_invoice_view(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    if request.method == 'GET':
        return render(request, 'invoice_edit_form.html', {'companies': settings.OWN_COMPANIES,
                                                          'invoice': invoice})
    else:
        company = request.POST['company']
        invoice_number = request.POST['invoice_number']
        issue_date = datetime.strptime(request.POST['issue_date'], '%Y-%m-%d')
        invoice.company = company
        invoice.number = invoice_number
        invoice.issue_date = issue_date
        invoice.save()
        return JsonResponse(data={'status': 'OK'})


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
                                                  'companies': settings.OWN_COMPANIES,
                                                  'outdated': INVOICE_OUTDATED,})

@csrf_exempt
@require_POST
@is_in_roles([ROLE_ADMIN, ROLE_SECRETARY])
def mark_as_paid(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    invoice.is_paid = True
    invoice.save()
    return JsonResponse(data={'status': 'OK'})

@require_GET
@is_in_roles([ROLE_ADMIN, ROLE_SECRETARY])
def outdated_invoices_view(request):
    return render(request, 'invoices_outdated_list.html', {'invoices': outdated_invoices(),
                                                           'outdated': INVOICE_OUTDATED})

def outdated_invoices():
    border_date = datetime.now() - relativedelta(days=INVOICE_TIMEOUT)
    invoices = Invoice.objects.filter(is_paid=False, issue_date__lt=border_date)
    return invoices