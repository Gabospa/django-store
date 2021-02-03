from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.models import User
from users.models import User
from django.http import HttpResponseRedirect


from .forms import RegisterForm
from products.models import Product


def index(request):

    products = Product.objects.all().order_by('-id')

    return render( request, 'index.html', {
        'message': 'Listado de productos',
        'title': 'Productos',
        'products': products,
    })

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username') #diccionario
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Bienvenido {}'.format(user.username))

            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET['next'])

            return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseña invalidos')
        

    return render(request, 'users/login.html', {
    
    })

def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('login')


def register(request):
    if request.user.is_authenticated:
        return redirect('index')

    form = RegisterForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        
        user = form.save()
        if user:
            login(request, user)
            messages.success(request, 'Usuario creado exitosamente')
            return redirect('index')

    return render( request, 'users/register.html', {
        'form':form 
    })