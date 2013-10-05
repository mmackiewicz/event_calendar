from django.db import models
from transports import models as t_models

from time import strftime

EVENT_STATUS_WAITING = 'WAITING'
EVENT_STATUS_STARTED = 'STARTED'
EVENT_STATUS_DONE = 'DONE'
EVENT_STATUS_CANCELED = 'CANCELED'


EVENT_STATUSES = (
    (EVENT_STATUS_WAITING, 'waiting'),
    (EVENT_STATUS_STARTED, 'started'),
    (EVENT_STATUS_DONE, 'done'),
    (EVENT_STATUS_CANCELED, 'canceled'),
)

class Event(models.Model):
    status = models.CharField(max_length=10, choices=EVENT_STATUSES)
    start_location = models.CharField(max_length=250)
    end_location = models.CharField(max_length=250)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    transports = models.ManyToManyField(t_models.Transport)

    def serialize_to_json(self):
        return {'status': self.status,
                'start_location': self.start_location,
                'end_location': self.end_location,
                'start_time': self.start_time.strftime('%Y-%m-%d %H:%M'),
                'end_time': self.end_time.strftime('%Y-%m-%d %H:%M'),
                #'start_time': str(self.start_time),
                #'end_time': str(self.end_time),
                'transports': [transport.serialize_to_json() for transport in self.transports.all()]}
