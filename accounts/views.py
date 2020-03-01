from django.shortcuts import render, redirect
from django.contrib.auth.models import User


# Create your views here.


def register(request):
    if request.method == 'POST':

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # check if password mactch.

        if password == password2:
            # check if username already exist
            if User.objects.filter(username=username).exists():
                return render(request, 'accounts/register.html', {'error': 'this username is already taken'})
            else:
                if User.objects.filter(email=email).exists():
                    return render(request, 'accounts/register.html', {'error': 'this email has already been used'})
                else:
                    user = User.objects.create_user(
                        username=username, email=email, password=password, first_name=first_name, last_name=last_name
                    )
                    # Login after register
                    # auth.login(request, user)
                    # return redirect('index')
                    user.save()
                    return render(request, 'accounts/login.html', {'success': 'You have successfully registered'})
        else:
            return render(request, 'accounts/register.html', {'error': 'password does not match'})

    else:

        return render(request, 'accounts/register.html')


def login(request):
    return render(request, 'accounts/login.html')


def logout(request):
    return render(request, 'accounts/logout.html')


def dashboard(request):
    return render(request, 'accounts/dashboard.html')
