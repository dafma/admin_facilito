from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.views import View

from .forms import LoginForm, CreateUSerForm
from django.contrib.auth import authenticate, login as login_django
from django.contrib.auth import logout as logout_django
from django.contrib.auth.decorators import login_required
# Create your views here.


def show(request):
    return HttpResponse("Hola desde el cliente")

class LoginView(View):
    form = LoginForm()
    message = None
    template = 'login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('client:dashboard')
        return render(request, self.template, self.get_context())

    def post(self, request, *args, **kwargs):
        username_post = request.POST['username']
        password_post = request.POST['password']
        user = authenticate(username=username_post, password=password_post)
        if user is not None:
            login_django(request, user)
            return redirect('client:dashboard')
        else:
            self.message = "Usernam o password incorrecto"
        return render(request, self.template, self.get_context())

    def get_context(self):
        return {'form': self.form, 'message':self.message}

def login(request):

    #if request.user.is_authentificated():
        #return redirect('client:dashboard')
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

@login_required( login_url= 'client:login' )
def dashboard(request):
    context = {

    }
    return render(request, 'dashboard.html', context)

@login_required( login_url= 'client:login' )
def logout(request):
    logout_django(request)
    return redirect('client:login')

def create(request):
    form = CreateUSerForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit = False)
            user.set_password(user.password)
            user.save()
            return redirect('client:login')
    context = {
        'form':form
    }
    return render(request, 'create.html', context)


