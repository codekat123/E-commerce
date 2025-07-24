from django.db import models
import random
import string
from django.utils import timezone
from store.models import product
def generate_order_id(length=8):
     characters = string.ascii_letters + string.digits
     return ''.join(random.choices(characters,k =length))

class Order(models.Model):
     order_id = models.CharField(max_length = 8 , default = generate_order_id,unique=True)
     first_name = models.CharField(max_length = 30)
     last_name = models.CharField(max_length = 30)
     city = models.CharField(max_length = 30)
     address = models.CharField(max_length = 200)
     email = models.EmailField()
     created_at = models.DateTimeField(default=timezone.now)
     update_at = models.DateTimeField(auto_now_add = True)
     paid = models.BooleanField(default=False)
     postal_code = models.PositiveIntegerField()


     class Meta:
          ordering = ['-created_at']
          indexes = [
               models.Index(fields=['created_at'])
          ]
     def __str__(self):
          return f'order_id:{self.order_id}'
     def save(self,*args,**kwargs):
          if not self.order_id:
               unique_id = generate_order_id
               while Order.objects.filter(order_id = unique_id):
                    unique_id = generate_order_id
               self.order_id = unique_id
          super().save(*args,**kwargs)
     def get_total_cost(self):
          return sum(item.get_cost() for item in self.items.all())
     def get_full_name(self):
          return self.first_name + self.last_name


class OrderItem(models.Model):
     order = models.ForeignKey(Order,related_name='items',on_delete = models.CASCADE)
     product = models.ForeignKey(product,related_name='order_item',on_delete= models.CASCADE)
     price = models.DecimalField(max_digits=6,decimal_places=2)
     quantity = models.PositiveIntegerField(default=1)

     def __str__(self):
          return str(self.id)

     def get_cost(self):
          return self.price * self.quantity
     
class OrderPay(models.Model):
     order = models.ForeignKey(Order,on_delete = models.CASCADE)
     pay_phone_number = models.CharField(max_length = 11)
     pay_image = models.ImageField(upload_to = 'vodafone_cash')
     created_at = models.DateTimeField(auto_now_add = True)

     class Meta:
          ordering = ['-created_at']
     def __str__(self) -> str:
          return f"your order id is : {self.order.order_id}"
     