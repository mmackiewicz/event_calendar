from django.conf import settings
from django.db import models


INVOICE_CREATED = 'CREATED'
INVOICE_OUTDATED = 'OUTDATED'
INVOICE_PAID = 'PAID'

class Invoice(models.Model):
    number = models.CharField(max_length=5)
    is_paid = models.BooleanField(default=False)
    company = models.CharField(choices=settings.OWN_COMPANIES, max_length=50)