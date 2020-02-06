# Django
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect

# Messages
from django.contrib import messages

# Auth
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout

# from django.contrib.auth.models import User
from users.models import User

# Forms
from .forms import RegisterForm

# Models
from products.models import Product


def index(request):

    template_name = 'index.html'
    products = Product.objects.all().order_by('-id')

    context = {
        'message': 'Listado de Productos',
        'title': 'Productos',
        'products': products,
    }

    return render(request, template_name, context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('forms:index')

    if request.method == 'POST':
        # POST es un diccionario
        username = request.POST.get('username') # diccionario
        password = request.POST.get('password')

        # Si encuentra el usuario, devolverá un objeto tipo user, si falla, retornará un 'None'
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Bienvenido, eres uno de los nuestros.')
            
            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET['next'])

            return redirect('forms:index')
        else:
            messages.error(request, 'Algo ha fallado...')

    return render(request, 'users/login.html', {
        
    })

def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('forms:login')


def register(request):
    if request.user.is_authenticated:
        return redirect('forms:index')

    # instancia de form
    # Haciendo lo siguiente, establecemos valores en formulario
    # form = RegisterForm({
    #     'username': 'Eduardo',
    #     'email': 'eduardo@codigo.com'
    # })

    form = RegisterForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        # username = form.cleaned_data.get('username') # Diccionario
        # email = form.cleaned_data.get('email')
        # password = form.cleaned_data.get('password')

        # user = User.objects.create_user(username, email, password)

        user = form.save()

        if user:
            login(request, user)
            messages.success(request, 'Usuario creado exitosamente')
            return redirect('forms:index')
        

    return render(request, 'users/register.html', {
        'form': form
    })