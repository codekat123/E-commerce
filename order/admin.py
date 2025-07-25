from django.contrib import admin
from .models import Order,OrderItem
import csv
import datetime
from django.http import HttpResponse
from django.db import models
from django.utils.safestring import mark_safe
from django.urls import reverse


def order_pdf(obj):
     url = reverse('order:admin_order_pdf',args=[obj.order_id])
     return mark_safe(f'<a href="{url}" target="_blank" >PDF</a>')

order_pdf.short_description = 'invoice'




def export_to_csv(modeladmin,request,queryset):
     #  HTTP Response
     opts = modeladmin.model._meta
     content_disposition = f"attachment; filename={opts.verbose_name}.csv"
     response = HttpResponse(content_type='text/csv')
     response['Content-Disposition'] = content_disposition
     # write into CSV file

     writer = csv.writer(response)
     fields = [field for field in opts.get_fields() if isinstance(field, models.Field)]
     writer.writerow(field.verbose_name for field in fields)

     for obj in queryset:
          date_row = []
          for field in fields:
               value = getattr(obj,field.name)
               if isinstance(value,datetime.datetime):
                    value = value.strftime('%d%m%U')
               date_row.append(value)
          writer.writerow(date_row)
     return response


export_to_csv.short_description = 'export to CSV'

class OrderItemInline(admin.TabularInline):
     model = OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
     list_display = ["first_name","email","paid","created_at",order_pdf]
     inlines = [OrderItemInline]
     actions = [export_to_csv]
