from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import LoginUserForm, CreateUSerForm, EditUserForm, EditPasswordForm
from django.contrib.auth import authenticate, login as login_django, update_session_auth_hash
from django.contrib.auth import logout as logout_django
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.contrib.auth.models import User
from django.contrib import messages

class ShowView(DetailView):
    model = User
    template_name = 'show.html'
    slug_field = 'username' # que campo de la base de datos
    slug_url_kwarg = 'username_url' # que de la url


class EditView(UpdateView, LoginRequiredMixin, SuccessMessageMixin):
    model = User
    template_name = 'edit.html'
    success_url = reverse_lazy('client:dashboard')
    form_class = EditUserForm
    success_message = 'Tu usuario ha sido actualizado'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(EditView, self).form_invalid(request, *args, **kwargs)


class LoginView(View):
    form = LoginUserForm()
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
            self.message = "Username o password incorrecto"
        return render(request, self.template, self.get_context())

    def get_context(self):
        return {'form': self.form, 'message':self.message}

class DashboardView(LoginRequiredMixin, View):
    login_url = 'client:login'

    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard.html', {})

class CreateUserr(CreateView):
    success_url = reverse_lazy('client:login')
    template_name = 'create.html'
    model = User
    form_class = CreateUSerForm

    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.set_password(self.object.password)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

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

def edit_password(request):

    form = EditPasswordForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            current_password = form.cleaned_data['password']
            new_password = form.cleaned_data['new_password']
            if authenticate(username = request.user.username, password = current_password):
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, "El password actualizado, messages")
            else:
                messages.error(request, 'No es posible actualizarlo')

    context = {'form': form}
    return render(request, 'edit_password.html', context)

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


