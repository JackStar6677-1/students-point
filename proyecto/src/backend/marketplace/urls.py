from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'marketplace'

urlpatterns = [
    # Categorías
    path('categories/', views.CategoryListAPIView.as_view(), name='category-list'),
    
    # Productos
    path('products/', views.ProductListAPIView.as_view(), name='product-list'),
    path('products/search/', views.search_products, name='product-search'),
    path('products/<int:pk>/', views.ProductDetailAPIView.as_view(), name='product-detail'),
    path('products/<int:product_id>/views/', views.increment_product_views, name='product-views'),
    path('my-products/', views.UserProductsAPIView.as_view(), name='user-products'),
    
    # Transacciones
    path('transactions/', views.TransactionListAPIView.as_view(), name='transaction-list'),
    path('transactions/<int:pk>/', views.TransactionDetailAPIView.as_view(), name='transaction-detail'),
    
    # Reseñas
    path('reviews/', views.ReviewListAPIView.as_view(), name='review-list'),
    path('reviews/user/<int:user_id>/', views.ReviewListAPIView.as_view(), name='user-reviews'),
]
