from django.db import models

METER = 'METER'
UNIT = 'UNIT'
KILOGRAM = 'KILOGRAM'

UNIT_TYPES = (
    (METER, 'm'),
    (UNIT, 'szt'),
    (KILOGRAM, 'kg'),
)


class Product(models.Model):
    product_code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    units = models.CharField(max_length=8, choices=UNIT_TYPES)

    def serialize_to_json(self):
        return {'id': self.id,
                'product_code': self.product_code,
                'name': self.name,
                'units': self.units,}

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('products.views.update_product_view', args=[str(self.id)])
