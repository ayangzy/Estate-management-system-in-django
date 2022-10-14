from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from contacts.models import Contact
from django.contrib.auth.decorators import login_required
from accounts.decorators import unauthenticated_user
from django.contrib.auth.models import Group


# Create your views here.

@unauthenticated_user
def register(request):
    if request.method == 'POST':

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        #role = request.POST['role']
        #user_id = request.POST['user_id']

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
                    # group = Group.objects.get_or_create(name='agent')
                    # user.groups.add(group)
                    # Login after register
                    # auth.login(request, user)
                    # return redirect('index')
                    user.save()
                    return render(request, 'accounts/login.html', {'success': 'You have successfully registered'})
        else:
            return render(request, 'accounts/register.html', {'error': 'password does not match'})

    else:

        return render(request, 'accounts/register.html')

@unauthenticated_user
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'accounts/login.html', {'error': 'username or password is incorrect'})

    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('index')
    else:
        return render(request, 'accounts/logout.html')

@login_required(login_url='login')
def dashboard(request):
    user_contacts = Contact.objects.order_by(
        '-contact_date').filter(user_id=request.user.id)

    context = {
        'contacts': user_contacts
    }

    return render(request, 'accounts/dashboard.html', context)
