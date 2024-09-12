from django.shortcuts import render, redirect
from employees.forms import EmployeeRegistrationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from employees.forms import EmployeeForm
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
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EmployeeForm()
    return render(request, 'add_employee.html', {'form': form})
