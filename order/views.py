from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.core.mail import send_mail
from django.conf import settings


def order_create(request):
     cart = Cart(request)
     success = False
     if request.method == 'POST':
          form = OrderCreateForm(request.POST)
          if form.is_valid():
               order = form.save()
               for item in cart:
                    OrderItem.objects.create(
                         order = order, product = item['product'],
                         price=item['price'],quantity=item['quantity']
                         )
               cart.clear()
               subject = "Order confirmation"
               message = f"your order-id=> {order.order_id} has been created successfully \n\n order details: \n "
               for item in cart:
                    message += f"product: {item['product'].name}, Price : {item['price']}, Quantity:{item['quantity']}"
               send_mail(subject,message,settings.DEFAULT_FROM_EMAIL,[form.cleaned_data['email']])
               success = True
          return render(request,'order/checkout.html',{'order':order,'success':success})
     else:
          form = OrderCreateForm()
     return render(request,'order/checkout.html',{'form':form,'cart':cart})
          