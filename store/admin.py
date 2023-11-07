from django.contrib import admin
from .models import *

class ImagenProductoInline(admin.TabularInline):  # admin.StackedInline
    model = ImagenProducto
    extra = 1 

class IProductoAdmin(admin.ModelAdmin):
    inlines = [ImagenProductoInline]
    
class OrderItemInline(admin.TabularInline):  # admin.StackedInline
    model = OrderItem
    extra = 1 

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'date_ordered', 'get_cart_total']
    inlines = [OrderItemInline]

    list_filter = ['complete']
    search_fields = ['id', 'customer__name', 'transaction_id']


admin.site.register(Customer)
admin.site.register(Product, IProductoAdmin)

# admin.site.register(Order)
# admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(DonacionRopa)

