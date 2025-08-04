from django.shortcuts import render , get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from store.models import category,product
from accounts.models import account
from .serializers import CategorySerializer , ProductSerializer , RegisterSerializer
from .tasks import verification
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes


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

@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([AllowAny])
def register_api(request, id=None):
    print("REGISTER VIEW CALLED")
    if request.method == 'GET':
        if id:
            user = get_object_or_404(account, id=id)
            serializer = RegisterSerializer(user)
        else:
            user = account.objects.all()
            serializer = RegisterSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            verification.delay(user.id)
            return Response({'message': 'account created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method in ['PUT', 'PATCH']:
        user = get_object_or_404(account, id=id)
        partial = request.method == 'PATCH'
        serializer = RegisterSerializer(user, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'account updated'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        user = get_object_or_404(account, id=id)
        user.delete()
        return Response({'message': 'account deleted'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def activation(request, uid, token):
    try:
        id = urlsafe_base64_decode(uid).decode()
        user = account.objects.get(id=id)
    except (TypeError, ValueError, OverflowError, account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return Response({'message': 'Your account is activated successfully'}, status=status.HTTP_200_OK)

    return Response({'message': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def logout(request):
     try :
          refresh_token = request.data.get('refresh')
          if not refresh_token:
               return Response({'message':'refresh token is required'},status = status.HTTP_400_BAD_REQUEST)
          token = RefreshToken(refresh_token)
          token.blacklist()
          return Response({'message':'successfully logout'},status = status.HTTP_200_OK)
     except Exception as e:
          return Response({'error':'Invalid token'},status = status.HTTP_400_BAD_REQUEST)
