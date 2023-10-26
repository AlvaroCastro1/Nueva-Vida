from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from django.contrib import admin

urlpatterns = [
    path('', views.home, name="home"),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('favicon.ico', RedirectView.as_view(url='static/src/logo.jpg')),
    path('cart/', views.cart, name="cart"),
    path('store/', views.store, name="store"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('donacion/', views.donacion, name='RegistroDonador'),
]