from django.contrib import admin
from .models import account


@admin.register(account)
class AcountAdmin(admin.ModelAdmin):
     display = ['first_name','email','username']
     search_fields  = ['username']
