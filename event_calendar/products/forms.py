__author__ = 'Marek Mackiewicz'

from django import forms
import models

class ProductForm(forms.Form):
    name = forms.CharField(min_length=3, max_length=75)