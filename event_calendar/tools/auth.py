__author__ = 'Marek Mackiewicz'

from django.contrib.auth.decorators import user_passes_test
from workers import models

def is_admin():
    def has_admin_role(u):
        return u is not None and u.is_authenticated and u.get_profile().role == models.ROLE_ADMIN
    return user_passes_test(has_admin_role)

def is_dispatcher():
    def has_dispatcher_role(u):
        return u is not None and u.is_authenticated and u.get_profile().role == models.ROLE_DISPATCHER
    return user_passes_test(has_dispatcher_role)

def is_driver():
    def has_driver_role(u):
        return u is not None and u.is_authenticated and u.get_profile().role == models.ROLE_DRIVER
    return user_passes_test(has_driver_role)

def is_in_roles(roles):
    def has_roles(u):
        return (u is not None and u.is_authenticated and u.get_profile().role in roles)
    return user_passes_test(has_roles)

def is_authenticated():
    return user_passes_test(lambda u: u is not None and u.is_authenticated)