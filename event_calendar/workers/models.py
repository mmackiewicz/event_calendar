from django.db import models
from django.contrib.auth.models import User

ROLE_DRIVER = 'DRIVER'
ROLE_DISPATCHER = 'DISPATCHER'
ROLE_ADMIN = 'ADMIN'

ROLES = (
    (ROLE_DRIVER, 'driver'),
    (ROLE_DISPATCHER, 'dispatcher'),
    (ROLE_ADMIN, 'administrator')
)

class Worker(models.Model):
    user = models.OneToOneField(User)
    pesel = models.CharField(max_length=11)
    role = models.CharField(max_length=10, choices=ROLES)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('workers.views.update_worker_view', args=[str(self.id)])

    def serialize_to_json(self):
        return {'id': self.id,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'username': self.user.username,
                'email': self.user.email,
                'pesel': self.pesel,
                'role': self.role,}

