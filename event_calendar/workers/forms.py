__author__ = 'Marek Mackiewicz'

from django import forms
import models

class WorkerCreateForm(forms.Form):
    first_name = forms.CharField(min_length=3, max_length=50)
    last_name = forms.CharField(min_length=3, max_length=50)
    username = forms.CharField(min_length=3, max_length=50)
    password = forms.CharField(min_length=5, widget=forms.PasswordInput())
    role = forms.ChoiceField(choices=models.ROLES)
    pesel = forms.CharField(min_length=11, max_length=11)
    email = forms.EmailField()

class WorkerUpdateForm(forms.Form):
    first_name = forms.CharField(min_length=3, max_length=50)
    last_name = forms.CharField(min_length=3, max_length=50)
    username = forms.CharField(min_length=3, max_length=50)
    old_password = forms.CharField(min_length=5, widget=forms.PasswordInput(), label='current password')
    new_password1 = forms.CharField(min_length=5, widget=forms.PasswordInput(), label='new password')
    new_password2 = forms.CharField(min_length=5, widget=forms.PasswordInput(), label='repeat new password')
    role = forms.ChoiceField(choices=models.ROLES)
    pesel = forms.CharField(min_length=11, max_length=11)
    email = forms.EmailField()

    