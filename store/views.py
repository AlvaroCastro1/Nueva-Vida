from store.models import Product
from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, cartData, guestOrder
import os


# Create your views here.
from django.urls import reverse
from django.shortcuts import redirect

def admin_login(request):
    admin_login_url = reverse('admin:login')  # URL por defecto del login del administrador
    return redirect(admin_login_url)

def home(request):
    return render(request, 'store/index.html')

def store(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)

def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    data = cartData(request)
    
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    nombre_host = os.environ.get('DATABASE_HOST')

    context = {'items':items, 'order':order, 'cartItems':cartItems, 'nombre_host':nombre_host}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)

from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm

from django.views.decorators.csrf import csrf_protect

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            nombre = form.cleaned_data.get('first_name')
            apellidos = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            telefono = form.cleaned_data.get('telefono')  # Obtenemos el campo Telefono del formulario

            customer = Customer.objects.create(user=user, Nombre=nombre, Apellidos=apellidos, Email=email, Telefono=telefono, Monedero=0.00)

            login(request, user)
            return redirect('store')  # Reemplaza 'tu_pagina_principal' con la URL de la página principal
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

from django.contrib.auth import login, authenticate

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirige a la página de perfil del usuario
            return redirect("store")
        else:
            # Maneja el caso de credenciales inválidas
            return render(request, "registration/login.html", {"error": "Credenciales inválidas."})

    return render(request, "registration/login.html")

from django.contrib.auth import logout


def user_logout(request):
    logout(request)
    return render(request, 'registration/logout_confirmation.html')

from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.utils import timezone

@receiver(user_logged_out)
def update_last_login(sender, request, **kwargs):
    if request.user.is_authenticated:
        # El usuario ha iniciado sesión
        request.user.last_login = timezone.now()
        request.user.save()

from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            # Modificar Customer
            customer_id = request.user.id
            customer = Customer.objects.get(pk=customer_id)

            user_data = user_form.cleaned_data
            first_name = user_data['first_name']
            last_name = user_data['last_name']
            email = user_data['email']

            # Paso 2: Actualiza los campos del objeto Customer
            customer.Nombre = first_name
            customer.Apellidos = last_name
            # customer.Telefono = "NuevoT"
            customer.Email = email

            # Paso 3: Guarda el objeto Customer
            customer.save()
            
            
            # Redirige al usuario
            return redirect("store")
    else:
        user_form = UserProfileForm(instance=request.user)
    return render(request, 'registration/edit_profile.html', {'user_form': user_form})


@login_required
def dashboard(request):
    return render(request, 'store/base.htm',{'section': 'dashboard'})
    

def donacion(request):
      return render(request, 'registration/RegistroDonador.html')

def Nuestra_Historia(request):
      return render(request, 'store/NuevaVida.html')

from django.shortcuts import get_object_or_404

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'store/productos.html', {'product': product})

