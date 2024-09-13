from django.shortcuts import render
from django.http import HttpResponse
from employees.models import EmployeeModel
# Create your views here.


def home(request):
    employee = EmployeeModel.objects.all()
    return render(request, 'home.html', {'employees': employee})
