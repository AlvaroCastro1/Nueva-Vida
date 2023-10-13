from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)

	def __str__(self):
		return self.name

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