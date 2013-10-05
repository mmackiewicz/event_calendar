from django.db import models
from vehicles import models as v_models
from workers import models as w_models
from loads import models as l_models

class Transport(models.Model):
    vehicle = models.ForeignKey(v_models.Vehicle)
    driver = models.ForeignKey(w_models.Worker)
    loads = models.ManyToManyField(l_models.Load)

    def serialize_to_json(self):
        return {'id': self.id,
                'vehicle': self.vehicle.serialize_to_json(),
                'driver': self.driver.serialize_to_json(),
                'loads': [load.serialize_to_json() for load in self.loads.all()]}