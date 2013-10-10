from django.db import models
from loads import models as l_models
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
    vehicle = models.OneToOneField(v_models.Vehicle, null=True)
    loads = models.ManyToManyField(l_models.Load)
    return_event = models.ForeignKey(ReturnEvent, null=True)

    def serialize_to_json(self):

        event_dict = {'id': self.id,
                    'producer': self.producer,
                    'recipient': self.recipient,
                    'production_date': self.production_date.strftime('%Y-%m-%d'),
                    'recipients_date': self.recipients_date.strftime('%Y-%m-%d'),
                    'loads': [load.serialize_to_json() for load in self.loads.all()]}
        if self.vehicle:
            event_dict['vehicle'] = self.vehicle.serialize_to_json()

        return event_dict
