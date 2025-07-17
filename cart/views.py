from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.http import require_POST
from store.models import product
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request,product_id):
     cart = Cart(request)
     Product = get_object_or_404(product,id = product_id,status=product.Status.available)
     form = CartAddProductForm(request.POST)
     if form.is_valid():
          cd = form.cleaned_data
          cart.add(Product,cd['quantity'],cd['override'])
     return redirect('cart:cart_detail')
          
@require_POST
def cart_remove(request,product_id):
     cart = Cart(request)
     Product = get_object_or_404( product , id=product_id , status = product.Status.available) 
     cart.remove(Product)
     return redirect("cart:cart_detail")

def cart_detail(request):
     cart = Cart(request)
     for item in cart:
          item['update'] = CartAddProductForm(initial={'quantity':item['quantity'],'override':True})
     context = {
          'cart':cart,
     }
     return render(request,'cart/cart_details.html',context)