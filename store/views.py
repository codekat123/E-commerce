from django.shortcuts import render , get_object_or_404
from .models import product,category
from django.contrib.postgres.search import SearchVector,SearchQuery,SearchRank
from cart.forms import CartAddProductForm
from django.core.cache import cache
from django.core.paginator import Paginator

def home(request,category_slug=None):
     Category = None
     categories = category.objects.all()
     cache_key = f"products_{category_slug if category_slug else 'all'}"
     products = cache.get(cache_key)
     if products is None:
          if category_slug:
               Category = get_object_or_404(category,slug = category_slug)
               products = product.objects.filter(category = Category.id,status = product.Status.available)
          else:
               products = product.objects.filter(status=product.Status.available)     
          cache.set(cache_key,products,timeout=60 *20)

     paginator = Paginator(products,1)
     page_number = request.GET.get('page')
     page_obj = paginator.get_page(page_number)





     context = {
          'products':products,
          'categories':categories,
          'category':Category,
          'page_obj':page_obj,
                }
     return render(request,'store/home.html',context)



def product_detail(request,product_slug):
     cache_key = f"product_{product_slug}"
     products = cache.get(cache_key)
     if products is None :
          products = get_object_or_404(product,slug = product_slug ,status = product.Status.available )
          cache.set(cache_key,products,timeout=60*30)
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





def about(request):
     return render(request,'pages/about.html')
def why(request):
     return render(request,'pages/why.html')