__author__ = 'Marek Mackiewicz'

from django import forms
import models

class ProductForm(forms.Form):
    product_code = forms.CharField(min_length=3, max_length=50)
    name = forms.CharField(min_length=3, max_length=75)