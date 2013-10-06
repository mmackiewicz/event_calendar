from django.db import models
from invoices import models as i_models
from loads import models as l_models
from vehicles import models as v_models

class Transport(models.Model):
    vehicle = models.ForeignKey(v_models.Vehicle)
    loads = models.ManyToManyField(l_models.Load)

    def serialize_to_json(self):
        return {'id': self.id,
                'vehicle': self.vehicle.serialize_to_json(),
                'loads': [load.serialize_to_json() for load in self.loads.all()]}

class ReturnTransport(models.Model):
    start_location = models.CharField(max_length=50)
    end_location = models.CharField(max_length=50)
    load = models.OneToOneField(l_models.ReturnLoad)
    invoice = models.ManyToManyField(i_models.Invoice)
