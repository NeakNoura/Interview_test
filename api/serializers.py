from rest_framework import serializers
from .models import CategoryTB, ProductTB

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryTB
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTB
        fields = ['id', 'name', 'image', 'price', 'category']
