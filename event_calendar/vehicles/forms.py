__author__ = 'Marek Mackiewicz'

from django import forms
import models

class VehicleForm(forms.Form):
    registration = forms.CharField(min_length=3, max_length=50)