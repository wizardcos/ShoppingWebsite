from django.contrib import admin
from .models import Product,CustomerAddress,Cart,Purchase

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display= ['id' , 'title' ,'category','product_image']



@admin.register(CustomerAddress)
class CustomerAddressModelAdmin(admin.ModelAdmin):
    list_display= ['id' , 'user' ,'address','city','zipcode']

@admin.register(Cart)
class CartModelAdmin (admin.ModelAdmin):
  list_display = ['id', 'user', 'product', 'quantity']

@admin.register(Purchase)
class PurchaseModelAdmin(admin.ModelAdmin):
   list_display = ['id', 'user', 'product', 'quantity']

