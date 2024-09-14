from django.shortcuts import render, redirect, get_object_or_404
from employees.forms import EmployeeRegistrationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from employees.forms import EmployeeForm
from employees.models import EmployeeModel
from django.http import HttpResponseForbidden
# Create your views here.


def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = EmployeeRegistrationForm(request.POST)
            if form.is_valid():
                messages.success(request, "User Created Successfully")
                form.save()
            else:
                print(form.errors)
        else:
            form = EmployeeRegistrationForm()
        return render(request, 'sign_up.html', {'forms': form})
    else:
        return redirect('login')


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                name = form.cleaned_data['username']
                user_pass = form.cleaned_data['password']
                # is user is available in database
                user = authenticate(username=name, password=user_pass)
                if user is not None:
                    login(request, user)
                    print(user)
                    return redirect('home')
        else:
            form = AuthenticationForm()
            return render(request, 'login.html', {'forms': form})
    else:
        return redirect('home')
    return render(request, 'login.html', {'forms': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def add_employee(request):
    if request.method == 'POST':
        existing_employee = EmployeeModel.objects.filter(
            user=request.user).first()

        if existing_employee:
            form = EmployeeForm(
                request.POST, instance=existing_employee, user=request.user)
        else:
            form = EmployeeForm(request.POST, user=request.user)

        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EmployeeForm()

    return render(request, 'add_employee.html', {'form': form})


def employee_list(request):
    employees = EmployeeModel.objects.filter(user=request.user)
    context = {'employees': employees}
    return render(request, 'update_delete.html', context)


def employee_list(request):
    if request.user.is_superuser:
        employee = EmployeeModel.objects.all()
    else:
        employee = EmployeeModel.objects.filter(user=request.user)
    return render(request, 'update_delete.html', {'employees': employee})


# def update_employee(request, id):
#     employee = get_object_or_404(EmployeeModel, id=id, user=request.user)

#     if request.method == 'POST':
#         form = EmployeeForm(request.POST, instance=employee)
#         if form.is_valid():
#             form.save()
#             return redirect('delete_update_employee')
#     else:
#         form = EmployeeForm(instance=employee)
#     return render(request, 'update_employee.html', {'form': form})
def update_employee(request, id):
    employee = get_object_or_404(EmployeeModel, id=id)

    if not request.user.is_superuser and employee.user != request.user:
        return HttpResponseForbidden("You are not allowed to update this employee.")

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('delete_update_employee')
    else:
        form = EmployeeForm(instance=employee, user=request.user)
    return render(request, 'update_employee.html', {'form': form})


# def delete_employee(request, id):
#     employee = get_object_or_404(EmployeeModel, id=id, user=request.user)
#     if request.method == 'POST':
#         employee.delete()
#         return redirect('delete_update_employee')
#     return render(request, 'confirm_delete.html', {'employee': employee})
def delete_employee(request, id):
    employee = get_object_or_404(EmployeeModel, id=id)
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to delete this employee.")

    if request.method == 'POST':
        employee.delete()
        return redirect('delete_update_employee')

    return render(request, 'confirm_delete.html', {'employee': employee})
