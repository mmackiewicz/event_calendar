from django.db import models
from django.contrib.auth.models import User

ROLE_SECRETARY = 'SECRETARY'
ROLE_DISPATCHER = 'DISPATCHER'
ROLE_ADMIN = 'ADMIN'

ROLES = (
    (ROLE_DISPATCHER, 'dispatcher'),
    (ROLE_ADMIN, 'administrator'),
    (ROLE_SECRETARY, 'secretary')
)

class Worker(models.Model):
    user = models.OneToOneField(User)
    role = models.CharField(max_length=10, choices=ROLES)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('workers.views.update_worker_view', args=[str(self.id)])

    def serialize_to_json(self):
        return {'id': self.id,
                'username': self.user.username,
                'role': self.role,}

