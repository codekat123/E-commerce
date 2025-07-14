from django.conf import settings


class Cart:
     
     def __init__(self,request):
          self.session = request.session
          cart = self.session.get(settings.cart_session_id)
          
          if not cart:
               cart = self.session[settings.cart_session_id] ={}
          
          self.cart = cart

     def add(self,product,quantity=1,override_quantity=False):
          product_id = str(product.id)
          if product_id not in self.cart:
               self.cart[product_id] = {'quantity':0,'price':str(product.price)}
          if override_quantity:
               self.cart[product_id]['quantity'] = quantity
          else:
               self.cart[product]['quantity'] += quantity
          self.save()
     def save(self):
          self.session.modified = True