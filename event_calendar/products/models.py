from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)

    def serialize_to_json(self):
        return {'id': self.id,
                'name': self.name,}

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('products.views.update_product_view', args=[str(self.id)])
