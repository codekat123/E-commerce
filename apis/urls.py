from django.urls import path
from . import views
app_name = 'api'

urlpatterns = [
     path('category/',views.category_api,name='category_api'),
     path('category/<str:slug>/',views.category_api,name='category_api'),
     path('product/',views.product_api,name='product'),
     path('product/<str:slug>/',views.product_api,name='product'),
     path('register/',views.register_api,name='register_api'),
     path('register/<id>',views.register_api,name='register_api'),
     path('activation/<uid>/<token>/',views.activation,name='activation'),
]