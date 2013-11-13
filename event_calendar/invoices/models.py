from django.conf import settings
from django.db import models

from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from time import strftime

INVOICE_ISSUED = 'ISSUED'
INVOICE_OUTDATED = 'OUTDATED'
INVOICE_PAID = 'PAID'

INVOICE_TIMEOUT = 30

class Invoice(models.Model):
    number = models.CharField(max_length=5)
    is_paid = models.BooleanField(default=False)
    company = models.CharField(choices=settings.OWN_COMPANIES, max_length=50)
    issue_date = models.DateField(null=False)

    def serialize_to_json(self):
        result_dict = {
            'id': self.id,
            'number': self.number,
            'is_paid': self.is_paid,
            'company': self.company,
            'issue_date': self.issue_date.strftime('%Y-%m-%d'),
            'status_str': self.status_str,
            'is_outdated': self.is_outdated()
        }

        return result_dict

    def is_outdated(self):
        now = datetime.now()
        today = date(now.year, now.month, now.day)
        return not self.is_paid and (today > self.issue_date + relativedelta(days=INVOICE_TIMEOUT))

    @property
    def status_str(self):
        if(self.is_paid):
            return INVOICE_PAID
        elif self.is_outdated():
            return INVOICE_OUTDATED
        else:
            return INVOICE_ISSUED
