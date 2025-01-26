import json
import numpy as np
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from torch import cosine_similarity

from .utils import extract_features

from .models import CategoryTB, ProductTB
from .serializers import CategorySerializer, ProductSerializer
from django.shortcuts import get_object_or_404


class CategoryView(APIView):

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, id=None, name=None):
        if id:
            category = get_object_or_404(CategoryTB, id=id)
        elif name:
            category = get_object_or_404(CategoryTB, name=name)
        else:
            return Response({"error": "Provide id or name to retrieve a category"}, status=status.HTTP_400_BAD_REQUEST)

        category_data = CategorySerializer(category).data
        products = ProductTB.objects.filter(category=category)
        category_data['products'] = ProductSerializer(products, many=True).data
        return Response(category_data)


    def put(self, request, id):
        category = get_object_or_404(CategoryTB, id=id)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        category = get_object_or_404(CategoryTB, id=id)
        category.delete()
        return Response({"message": "Category deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    

class ProductView(APIView):

    def post(self, request, id=None):
        if id:
    
            product = get_object_or_404(ProductTB, id=id)
            serializer = ProductSerializer(product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
    
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, id):
        product = get_object_or_404(ProductTB, id=id)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        product = get_object_or_404(ProductTB, id=id)
        product.delete()
        return Response({"message": f"Product with ID {id} deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


    def get(self, request, id=None):
        if id:
           
            product = get_object_or_404(ProductTB, id=id)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
         
            products = ProductTB.objects.all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Provide 'id' or 'name' to search for a product"}, status=status.HTTP_400_BAD_REQUEST)
    
class ImageSearchAPIView(APIView):
    def post(self, request):
        uploaded_image = request.FILES.get('image')
        if not uploaded_image:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Save the uploaded image temporarily
        temp_path = f'tmp/{uploaded_image.name}'
        with open(temp_path, 'wb') as f:
            for chunk in uploaded_image.chunks():
                f.write(chunk)

        # Extract features from the uploaded image
        query_features = extract_features(temp_path)
        if query_features is None:
            return Response({'error': 'Invalid image'}, status=status.HTTP_400_BAD_REQUEST)

        # Compute similarity with all products
        products = ProductTB.objects.exclude(features__isnull=True)
        similarities = []
        for product in products:
            product_features = np.array(json.loads(product.features))
            similarity_score = cosine_similarity([query_features], [product_features])[0][0]
            similarities.append((product, similarity_score))

        # Sort products by similarity score
        similarities = sorted(similarities, key=lambda x: x[1], reverse=True)[:10]

        # Prepare the response
        result = []
        for product, score in similarities:
            result.append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'image_url': product.image.url,
                'similarity_score': score
            })

        return Response({'results': result}, status=status.HTTP_200_OK)