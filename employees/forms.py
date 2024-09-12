from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from employees.models import EmployeeModel


class EmployeeRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'id': 'required'}))
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'id': 'required'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'id': 'required'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = EmployeeModel
        fields = ['name', 'address', 'phone_number',
                  'salary', 'designation', 'description']
