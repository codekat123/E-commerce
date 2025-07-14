from django.contrib import admin
from .models import category,product

@admin.register(product)
class ProductAdmin(admin.ModelAdmin):
     readonly_fields = ['slug']

@admin.register(category)
class CategoryAdmin(admin.ModelAdmin):
     readonly_fields = ['slug']