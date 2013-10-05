__author__ = 'Marek Mackiewicz'

from django import forms
import models

class WorkerCreateForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=50)
    password = forms.CharField(min_length=5, widget=forms.PasswordInput())
    role = forms.ChoiceField(choices=models.ROLES)

class WorkerUpdateForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=50)
    new_password1 = forms.CharField(min_length=5, widget=forms.PasswordInput(), label='new password')
    new_password2 = forms.CharField(min_length=5, widget=forms.PasswordInput(), label='repeat new password')
    role = forms.ChoiceField(choices=models.ROLES)

    