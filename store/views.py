from django.shortcuts import render , get_object_or_404
from .models import product,category
from django.contrib.postgres.search import SearchVector,SearchQuery,SearchRank
from cart.forms import CartAddProductForm


def home(request,category_slug=None):
     Category = None
     categories = category.objects.all()
     products = product.objects.filter(status = product.Status.available)
     if category_slug:
         Category = get_object_or_404(category,slug=category_slug)
         products = product.objects.filter(category = Category)

     context = {
          'products':products,
          'categories':categories,
          'category':Category,
                }
     return render(request,'store/home.html',context)



def product_detail(request,product_slug):
     products = get_object_or_404(product,slug = product_slug ,status = product.Status.available )
     context = {
          'detail':products,
          'form':CartAddProductForm()
     }
     return render(request,'store/product_detail.html',context)


def product_search(request):
     query = None
     results = []
     if 'query' in request.GET:
          query = request.GET.get('query')
          search_query = SearchQuery(query)
          search_vector = SearchVector('name','description')
          results = product.objects.annotate(search = search_vector,rank=SearchRank(search_vector,search_query)).filter(search=search_query,status = product.Status.available)
     context ={
          'query':query,
          'results':results,
     }
     return render(request,'store/search.html',context)