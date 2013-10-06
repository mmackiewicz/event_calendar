from django.db import models
from transports import models as t_models
from vehicles import models as v_models

from time import strftime


class ReturnEvent(models.Model):
    vehicle = models.ForeignKey(v_models.Vehicle)
    return_date = models.DateField()
    transports = models.ManyToManyField(t_models.ReturnTransport)


class Event(models.Model):
    producer = models.CharField(max_length=250)
    recipient = models.CharField(max_length=250)
    production_date = models.DateField()
    recipients_date = models.DateField()
    transport = models.OneToOneField(t_models.Transport)
    return_event = models.ForeignKey(ReturnEvent, null=True)

    def serialize_to_json(self):
        return {'producer': self.producer,
                'recipient': self.recipient,
                'production_date': self.production_date.strftime('%Y-%m-%d'),
                'recipients_date': self.recipients_date.strftime('%Y-%m-%d'),
                'transport': self.transport.serialize_to_json()}
