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
    loads = models.ManyToManyField(l_models.ReturnLoad)
    invoice = models.ManyToManyField(i_models.Invoice, null=True)

    def serialize_to_json(self):
        result_dict = {'start_location': self.start_location,
                'end_location': self.end_location,
                'loads': [return_load.serialize_to_json() for return_load in self.loads.all()],}
        if self.invoice:
            result_dict['invoice'] = self.invoice.serialize_to_json()
        else:
            result_dict['invoice'] = ''

        return result_dict
