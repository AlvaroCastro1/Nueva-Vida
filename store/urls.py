from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from django.contrib import admin

urlpatterns = [
    path('', views.home, name="home"),
    path('Nuestra_Historia/', views.Nuestra_Historia, name='Nuestra_Historia'),
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
    path('',views.dashboard, name = 'dashboard'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name= 'password_change'),
    path('password_change/done', auth_views.PasswordChangeDoneView.as_view(), name = 'password_change_done'),
    path('donacion/', views.donacion, name='RegistroDonador'),
    path('productos/<int:product_id>/', views.product_detail, name='product_detail')
]