from django.db import models


RENTAL_ID = 0
RENTAL_REGISTRATION = 'RENTAL'
RENTAL_COLOUR = '000000'

class Vehicle(models.Model):
    registration = models.CharField(max_length=20)
    colour = models.CharField(max_length=6)


    def serialize_to_json(self):
        return {'id': self.id,
                'colour': self.colour,
                'registration': self.registration}

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('vehicles.views.update_vehicle_view', args=[str(self.id)])