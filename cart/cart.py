from django.conf import settings
from decimal import Decimal
from store.models import product
from coupons.models import Coupon

class Cart:
     
     def __init__(self,request):
          self.session = request.session
          cart = self.session.get(settings.CART_SESSION_ID)
          if not cart:
               cart = self.session[settings.CART_SESSION_ID] ={}
          self.coupon_id = request.session.get('coupon_id')
          self.cart = cart


     def add(self,product,quantity=1,override_quantity=False):
          product_id = str(product.id)
          if product_id not in self.cart:
               self.cart[product_id] = {'quantity':0,'price':str(product.price)}
          if override_quantity:
               self.cart[product_id]['quantity'] = quantity
          else:
               self.cart[product_id]['quantity'] += quantity
          self.save()



     def save(self):
          self.session.modified = True


     def remove(self,product)->str:
          product_id = str(product.id)
          if product_id in self.cart:
               del self.cart[product_id]
               self.save()

     def __iter__(self):
          product_id = self.cart.keys()
          
          products = product.objects.filter(id__in=product_id)

          cart = self.cart.copy()
          for Product in products:
               cart[str(Product.id)]['product'] = Product
          for item in cart.values():
               item['price'] = Decimal(item['price'])
               item['price_total'] = item['price'] * item['quantity']
               yield item

     def __len__(self):
          return sum(item['quantity'] for item in self.cart.values())
     
     def get_total_price(self):
          return sum(Decimal(item['price']) * item['quantity'] for  item in self.cart.values())
     
     def clear(self):
          del self.session[settings.CART_SESSION_ID]
          self.save()
     

     @property
     def coupon(self):
          if self.coupon_id:
               try:
                    return Coupon.objects.get(id = self.coupon_id)
               except Coupon.DoesNotExist:
                    pass
          return None
     
     @property
     def get_discount(self):
          if self.coupon:
               return (self.coupon.discount / Decimal(100)) * self.get_total_price()
          return Decimal(0)
     
     def get_discounted_total(self):
          return  self.get_total_price() - self.get_discount
     
