# Generated by Django 4.2.6 on 2023-10-14 14:28

from django.db import migrations
from django.contrib.auth.models import User

def cargar_registros_iniciales(apps, schema_editor):
    Customer = apps.get_model('store', 'Customer')

    User = apps.get_model('auth', 'User')  # Modelo User de Django

    # Recuperar el usuario 'admin'
    admin_user = User.objects.get(username='admin')
    Product = apps.get_model('store', 'Product')


    # Crear el objeto Customer asociado al usuario
    customer = Customer.objects.create(
                                        user=admin_user,
                                        Nombre='Administrador',
                                        Apellidos='Admin',
                                        Telefono='1234567890',
                                        Email='correo@admin.com',
                                        Monedero=0.00
                                    )
    
    product = Product.objects.create(name='Producto de Prueba', 
                                     Disponible=False,
                                     Talla='No aplica',
                                     Color='No aplica',
                                     Genero='No aplica',
                                     Material='Delicado',
                                     Tipo='No aplica',
                                     Descripcion='Lindo espejo con luces',
                                     Precio=120,
                                     PuntosC=5.1,
                                     Destino='No aplica',
                                     ImagenPrincipal='LED_Mirror.jpg'
                                     )


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_rename_name_customer_nombre_remove_customer_email_and_more'),
    ]

    operations = [
        migrations.RunPython(cargar_registros_iniciales),
    ]
