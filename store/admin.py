from django.contrib import admin
from .models import *

class ImagenProductoInline(admin.TabularInline):  # admin.StackedInline
    model = ImagenProducto
    extra = 1 

class IProductoAdmin(admin.ModelAdmin):
    inlines = [ImagenProductoInline]
    
admin.site.register(Customer)
admin.site.register(Product, IProductoAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)