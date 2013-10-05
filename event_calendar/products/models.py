from django.db import models


class Product(models.Model):
    product_code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)

    def serialize_to_json(self):
        return {'id': self.id,
                'product_code': self.product_code,
                'name': self.name,}

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('products.views.update_product_view', args=[str(self.id)])
