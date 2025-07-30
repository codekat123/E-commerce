from rest_framework import serializers
from store.models import product , category
from accounts.models import account

class CategorySerializer(serializers.ModelSerializer):
     class Meta:
          model = category 
          fields = ['name','slug']

class ProductSerializer(serializers.ModelSerializer):
     class Meta:
          model = product
          exclude = ['image']
          depth = 1

class RegisterSerializer(serializers.ModelSerializer):
     class Meta:
          model = account 
          extra_kwargs = {'password':{'write_only':True}}
          fields  = ['first_name','last_name','email','username','country','password']
     def create(self,validated_data):
          user = account.objects.create_user(
               first_name = validated_data['first_name'],
               last_name = validated_data['last_name'],
               email =  validated_data['email'],
               username = validated_data['username'],
               country = validated_data['country'],
          )
          return user