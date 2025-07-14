from django.urls import path
from . import views


app_name = 'store'

urlpatterns = [
     path('',views.home,name="home"),
     path('product/<slug:product_slug>/',views.product_detail,name="product_detail"),
     path('category/<slug:category_slug>',views.home,name="category"),
     path('search/',views.product_search,name='search')
]