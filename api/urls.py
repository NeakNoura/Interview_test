from django.urls import path
from .views import CategoryView, ImageSearchAPIView, ProductView

urlpatterns = [

    path('category/', CategoryView.as_view(), name='create-category'),
    path('category/<int:id>/', CategoryView.as_view(), name='category-detail'),
    path('category/name/<str:name>/', CategoryView.as_view(), name='category-by-name'),

    path('image-search/', ImageSearchAPIView.as_view(), name='image-search'),
    path('products/', ProductView.as_view(), name='create-product'),
    path('products/<int:id>/', ProductView.as_view(), name='product-detail'),
]
