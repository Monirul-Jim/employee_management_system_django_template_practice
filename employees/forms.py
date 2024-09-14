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


# class EmployeeForm(forms.ModelForm):
#     class Meta:
#         model = EmployeeModel
#         fields = ['name', 'address', 'phone_number',
#                   'salary', 'designation', 'description']

#     def save(self, commit=True, user=None):
#         employee = super().save(commit=False)
#         if user:
#             employee.user = user
#         if commit:
#             employee.save()
#         return employee
# class EmployeeForm(forms.ModelForm):
#     class Meta:
#         model = EmployeeModel
#         fields = ['name', 'address', 'phone_number',
#                   'designation', 'salary', 'description']

#     def __init__(self, *args, **kwargs):
#         super(EmployeeForm, self).__init__(*args, **kwargs)
#         if self.instance and self.instance.pk:
#             self.fields['designation'].widget.attrs['readonly'] = True
#             self.fields['salary'].widget.attrs['readonly'] = True

#     def save(self, commit=True, user=None):
#         employee = super(EmployeeForm, self).save(commit=False)

#         if self.instance and self.instance.pk:
#             employee.designation = self.instance.designation
#             employee.salary = self.instance.salary

#         if user:
#             employee.user = user

#         if commit:
#             employee.save()

#         return employee
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = EmployeeModel
        fields = ['name', 'address', 'phone_number',
                  'designation', 'salary', 'description']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Extract user from kwargs
        super(EmployeeForm, self).__init__(*args, **kwargs)

        # If the form is being used to update (i.e., there's an instance)
        if self.instance and self.instance.pk:
            # If the user is not a superuser, make designation and salary fields read-only
            if self.user and not self.user.is_superuser:
                self.fields['designation'].widget.attrs['readonly'] = True
                self.fields['salary'].widget.attrs['readonly'] = True

    def save(self, commit=True):
        employee = super(EmployeeForm, self).save(commit=False)

        # If the user is not a superuser, do not update the designation or salary
        if not self.user.is_superuser and self.instance and self.instance.pk:
            employee.designation = self.instance.designation
            employee.salary = self.instance.salary

        if commit:
            employee.save()

        return employee
