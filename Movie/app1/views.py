from django.contrib import messages
from django.shortcuts import render, redirect,reverse
from django.contrib.auth.hashers import make_password, check_password
from .models import User_reg
from django.contrib.auth import authenticate, login as auth_login, logout


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstName')
        lastname = request.POST.get('lastName')
        email = request.POST.get('email')
        password = make_password(request.POST.get('password'))

        user = User_reg.objects.filter(username=username)
        collections={'username':username,'firstname':firstname,'lastname':lastname,'email':email}
        if user.exists():
            error_message = "Username already taken."
            return render(request, 'registration.html', {'error_message': error_message,**collections})

        if User_reg.objects.filter(email=email).exists():
            error_message1 = "Email already taken."
            return render(request, 'registration.html', {'error_message1': error_message1,**collections})
        else:
            User_reg.objects.create(username=username, first_name=firstname, last_name=lastname, email=email,
                                password=password)
            messages.success(request, 'Welcome, ' + firstname + '! Your account has been created successfully.')
            return redirect('app1:login')

    return render(request, 'registration.html')


# def login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         try:
#             user = User_reg.objects.get(username=username)
#
#         except User_reg.DoesNotExist:
#             return render(request, 'login.html', {'error_message': 'Username does not exist'})
#
#         if check_password(password, user.password):
#             request.session['user_id'] = user.id
#             return redirect('user:home')
#
#         else:
#             return render(request, 'login.html', {'error': 'Invalid password'})
#
#     return render(request, 'login.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('user:home')

        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('app1:login')
    return render(request,'logout.html')
