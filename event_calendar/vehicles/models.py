from django.db import models


class Vehicle(models.Model):
    vehicle_code = models.CharField(max_length=200)
    registration = models.CharField(max_length=20)

    def serialize_to_json(self):
        return {'id': self.id,
                'vehicle_code': self.vehicle_code,
                'registration': self.registration}

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('vehicles.views.update_vehicle_view', args=[str(self.id)])