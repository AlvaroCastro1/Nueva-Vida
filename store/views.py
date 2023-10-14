from store.models import Product
from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, cartData, guestOrder

# Create your views here.
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

    context = {'items':items, 'order':order, 'cartItems':cartItems}
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
            return render(request, "login.html", {"error": "Credenciales inválidas."})

    return render(request, "registration/login.html")

from django.contrib.auth import logout


def user_logout(request):
    logout(request)
    return render(request, 'registration/logout_confirmation.html')