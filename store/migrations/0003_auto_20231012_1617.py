# Generated by Django 4.2.6 on 2023-10-12 22:17

from django.db import migrations
from django.contrib.auth.models import User

def cargar_registros_iniciales(apps, schema_editor):

    user = User.objects.create_user(username='admin', password='admin', is_superuser= True, is_staff = True)

    user.save()


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0002_alter_product_price'),
    ]

    operations = [
        migrations.RunPython(cargar_registros_iniciales),
    ]
