from rest_framework import serializers
from store.models import product , category




class CategorySerializer(serializers.ModelSerializer):
     class Meta:
          model = category 
          fields = ['name','slug']

class ProductSerializer(serializers.ModelSerializer):
     class Meta:
          model = product
          exclude = ['image']
          depth = 1