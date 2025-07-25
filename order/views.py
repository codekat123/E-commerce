from django.shortcuts import render , redirect , get_object_or_404
from .models import OrderItem
from .forms import OrderCreateForm , OrderPayForm
from cart.cart import Cart
from .tasks import send_mails , send_invoice
from .tasks import send_invoice
from .models import Order
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
import weasyprint
import os


@staff_member_required
def admin_order_pdf(request,order_id):
     order = get_object_or_404(Order,order_id=order_id)
     url = render_to_string('order/pdf.html',{'order':order})
     response = HttpResponse(content_type = 'application/pdf')
     response['Content-disposition'] = f'filename=order_{order.order_id}.pdf'
     weasyprint.HTML(string=url).write_pdf(response)
     return response


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
               order_id = order.order_id
               send_mails.delay(order_id)
               success = True
               return redirect('order:pay_form',order_id = order_id)
          else:
               return render(request,'order/checkout.html',{'form':form,'cart':cart})
     else:
          form = OrderCreateForm()
     return render(request,'order/checkout.html',{'form':form,'cart':cart})
          

def order_pay_by_vodafone(request,order_id):
     order = get_object_or_404(Order,order_id= order_id)
     if request.method == 'POST':
          form = OrderPayForm(request.POST,request.FILES)
          if form.is_valid():
               order_pay = form.save(commit=False)
               order_pay.order = order
               order_pay.paid = True
               order_pay.save()
               order.paid = True
               order.save()
               return redirect('order:payment_success',order_id = order_id)
          else:
               context = {
               'form': OrderPayForm(),
               'order':order,}
               return render(request,"order/pay_form.html",context)
     else:
          context = {
               'form': OrderPayForm(),
               'order':order,
          }
          return render(request,'order/pay_form.html',context)
               
def pay_successful(request,order_id):
     order = get_object_or_404(Order,order_id=order_id)
     send_invoice.delay(order.order_id)
     return render(request,'order/payment_success.html',{'order':order})
