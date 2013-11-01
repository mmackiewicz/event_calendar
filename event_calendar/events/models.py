from django.db import models
from loads import models as l_models
from transports import models as t_models
from vehicles import models as v_models

from time import strftime


class ReturnEvent(models.Model):
    vehicle = models.ForeignKey(v_models.Vehicle, unique=False, null=True)
    return_date = models.DateField()
    transports = models.ManyToManyField(t_models.ReturnTransport)
    comment = models.TextField()

    def serialize_to_json(self):
        result_dict = {'id': self.id,
                    'return_date': self.return_date.strftime('%Y-%m-%d'),
                    'transports': [transport.serialize_to_json() for transport in self.transports.all()],}
        if self.vehicle:
            result_dict['vehicle'] = self.vehicle.serialize_to_json()
        else:
            result_dict['vehicle'] = ''

        return result_dict


class Event(models.Model):
    producer = models.CharField(max_length=250)
    recipient = models.CharField(max_length=250)
    production_date = models.DateField()
    recipients_date = models.DateField()
    vehicle = models.ForeignKey(v_models.Vehicle, null=True, unique=False)
    loads = models.ManyToManyField(l_models.Load)
    return_event = models.ForeignKey(ReturnEvent, null=True)
    comment = models.TextField()

    def serialize_to_json(self):

        event_dict = {'id': self.id,
                    'producer': self.producer,
                    'recipient': self.recipient,
                    'production_date': self.production_date.strftime('%Y-%m-%d'),
                    'recipients_date': self.recipients_date.strftime('%Y-%m-%d'),
                    'loads': [load.serialize_to_json() for load in self.loads.all()],
                    'comment': self.comment}
        if self.vehicle:
            event_dict['vehicle'] = self.vehicle.serialize_to_json()

        if self.return_event:
            event_dict['return_event'] = self.return_event.serialize_to_json()
        else:
            event_dict['return_event'] = ''

        return event_dict
