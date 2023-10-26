from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	Nombre = models.CharField(max_length=200, null=True)
	Apellidos = models.CharField(max_length=60)
	Telefono = models.CharField(max_length=10)
	Email = models.EmailField(unique=True)
	Monedero = models.DecimalField(max_digits=4, decimal_places=2)

	def __str__(self):
		return self.Nombre

class Product(models.Model):
	name = models.CharField(max_length=200)
	Disponible = models.BooleanField(default=False)
	Talla = models.CharField(max_length=20, default='Talla Única')
	Color = models.CharField(max_length=15, default='Blanco')
	Genero = models.CharField(max_length=20, default='Unisex')
	Material = models.CharField(max_length=30, default='No especificado')
	Tipo = models.CharField(max_length=30, default='No especificado')
	Descripcion = models.CharField(max_length=300, default='Sin descripción disponible')
	Precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
	PuntosC = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
	Destino = models.CharField(max_length=30, default='No especificado')
	ImagenPrincipal = models.ImageField(null=True, blank=True)
 
	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.ImagenPrincipal.url
		except:
			url = ''
		return url
class ImagenProducto(models.Model):
	IDIProducto = models.ForeignKey(Product, on_delete=models.CASCADE)
	Imagen = models.ImageField(upload_to="productos",null=True)


class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total

	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.Disponible == False:
				shipping = True
		return shipping
		
class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.Precio * self.quantity
		return total

# futuras verificaciones
class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address
#Registro de una donacion	
class DonacionRopa(models.Model):
    Donante = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    fecha_donacion = models.DateField(help_text="Fecha de la donación")
    descripcion = models.TextField(help_text="Descripción de la donación")
    cantidad = models.PositiveIntegerField(help_text="Cantidad de ropa donada")
    tipo_ropa = models.CharField(max_length=50, help_text="Tipo de ropa donada")
    talla = models.CharField(max_length=10, help_text="Talla de la ropa")
    estado = models.CharField(max_length=20, help_text="Estado de la ropa")
    puntuacion = models.DecimalField(max_digits=3, decimal_places=2, help_text="Puntuación de la donación")

    def __str__(self):
        return f"Donación de {self.Donante} el {self.fecha_donacion}"

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=DonacionRopa)
def actualizar_monedero(sender, instance, **kwargs):
    # Obtenemos el valor de 'puntuación' de la instancia de DonacionRopa
    puntuacion_donacion = instance.puntuacion

    # Supongamos que hay una relación ForeignKey o OneToOneField en DonacionRopa
    # que enlaza a un usuario Customer, llamémosla 'usuario'
    usuario = instance.Donante

    # Actualizamos el 'Monedero' del usuario en Customer
    usuario.Monedero += puntuacion_donacion
    usuario.save()