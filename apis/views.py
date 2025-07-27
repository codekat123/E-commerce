from django.shortcuts import render , get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from store.models import category,product
from .serializers import CategorySerializer ,ProductSerializer

@api_view(['GET','POST','PATCH','PUT','DELETE'])
def category_api(request, slug=None): 
     if request.method == 'GET':
          if slug:
               qs = get_object_or_404(category,slug=slug)
               serializer = CategorySerializer(qs)
          else:
               qs = category.objects.all()
               serializer = CategorySerializer(qs,many=True)
          print(serializer.data)
          return Response(serializer.data,status=status.HTTP_200_OK)
     elif request.method == 'POST':
         Category = CategorySerializer(data = request.data)
         if Category.is_valid():
              Category.save()
              return Response({'message':"The data that you've entered has been saved"},status = status.HTTP_200_OK)
         return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
     elif request.method in ['PUT','PATCH']:
          Category = get_object_or_404(category,slug = slug)
          partial = request.method == "PATCH"
          serializer = CategorySerializer(Category, data=request.data,partial = partial)
          if serializer.is_valid():
               print("Validated Data:", serializer.validated_data)
               serializer.save()
               return Response({'message':"the data have been updated"},status=status.HTTP_200_OK)
          return Response({'message':"there's something went wrong"}, status = status.HTTP_400_DAB_REQUEST)
     elif request.method == "DELETE":
          Category = get_object_or_404(category,slug=slug)
          Category.delete()
          return Response('the object has been delete',status=status.HTTP_NO_CONTENT)

@api_view(['GET','POST','PUT','PATCH','DELETE'])
def product_api(request,slug=None):
     if request.method == 'GET':
          if slug:
               qs = get_object_or_404(product,slug =slug ,status = product.Status.available)
               serializer = ProductSerializer(qs)
          else:
               qs = product.objects.filter(status = product.Status.available)
               serializer = ProductSerializer(qs,many=True)
          return Response(serializer.data, status = status.HTTP_200_OK)
     elif request.method == 'POST':
         Product = ProductSerializer(data = request.data)
         if Product.is_valid():
              Product.save()
              return Response({'message':"The data that you've entered has been saved"},status = status.HTTP_200_OK)
         return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
     elif request.method in ['PUT','PATCH']:
          Product = get_object_or_404(product , slug = slug)
          partial = request.method == 'PATCH'
          serializer = ProductSerializer(Product,data=request.data,partial=partial)
          if serializer.is_valid():
               serializer.save()
               return Response('the data has been updated',status = status.HTTP_200_OK)
          return Response('the data hasn\'t updated', status= status.HTTP._400_BAD_REQUEST)
     elif request.method == 'DELETE':
          Product = get_object_or_404(product,slug=slug)
          Product.delete()
          return Response('the data you seleted has been delete ',status = status.HTTP_NO_CONTENT)
     