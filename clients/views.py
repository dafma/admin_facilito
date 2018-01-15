from django.http import HttpResponse

from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import authenticate, login as login_django

# Create your views here.


def show(request):
    return HttpResponse("Hola desde el cliente")


def login(request):
    message = None

    if request.method == 'POST':
        username_post = request.POST['username']
        password_post = request.POST['password']
        user = authenticate( username = username_post, password = password_post)
        if user is not None:
            login_django(request, user)
            return redirect('client:dashboard')
        else:
            message = "Usernam o password incorrecto"
    form = LoginForm()
    context = {
        'form': form,
        'message': message
    }
    return render(request, 'login.html', context)

def dashboard(request):
    context = {

    }
    return render(request, 'dashboard.html', context)


