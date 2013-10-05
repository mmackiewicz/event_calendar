__author__ = 'Marek Mackiewicz'

from django import forms
import models

class VehicleForm(forms.Form):
    vehicle_code = forms.CharField(min_length=3, max_length=50)
    model = forms.CharField(min_length=3, max_length=50)
    registration = forms.CharField(min_length=3, max_length=50)