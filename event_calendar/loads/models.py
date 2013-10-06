from django.db import models
from products import models as p_models

class Load(models.Model):
    amount = models.IntegerField()
    product = models.ForeignKey(p_models.Product)

    def serialize_to_json(self):
        return {'id':self.id,
                'amount': self.amount,
                'product': self.product.serialize_to_json()}


class ReturnLoad(models.Model):
    product = models.CharField(max_length=50)
    amount = models.IntegerField()